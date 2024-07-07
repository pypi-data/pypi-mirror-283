import math
import numpy as np
import scipy.sparse as sp
from typing import Optional, Tuple

import torch
import torch.nn as nn
from torch import Tensor
import torch.nn.functional as F
from torch.nn.functional import normalize
from torch_geometric.utils import (negative_sampling, remove_self_loops, add_self_loops)
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv, GATConv, GATv2Conv
from torch_geometric.nn import GAE, InnerProductDecoder

from ._utils import scipy_sparse_mat_to_torch_sparse_tensor, extract_subgraph

# Domain-specific Batch Normalization（领域特定的批次归一化）是一种调整神经网络中批次归一化层以适应不同输入数据源或领域的技术。
class DSBatchNorm(nn.Module):
    """
    Domain-specific Batch Normalization
    """

    def __init__(self, num_features, n_domain, eps=1e-5, momentum=0.1):
        """
        Parameters
        ----------
        num_features
            dimension of the features
        n_domain
            domain number
        """
        super().__init__()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # self.device = torch.device("cpu")
        self.n_domain = n_domain
        self.num_features = num_features
        self.bns = nn.ModuleList(
            [nn.BatchNorm1d(num_features, eps=eps, momentum=momentum) for i in range(n_domain)]).to(self.device)

    def reset_running_stats(self):
        for bn in self.bns:
            bn.reset_running_stats()

    def reset_parameters(self):
        for bn in self.bns:
            bn.reset_parameters()

    def _check_input_dim(self, input):
        raise NotImplementedError

    def forward(self, x, y):
        device = x.device  # 获取输入数据的设备
        out = torch.zeros(x.size(0), self.num_features, device=device)  # , requires_grad=False)
        for i in range(self.n_domain):
            indices = np.where(y.cpu().numpy() == i)[0]
            if len(indices) > 1:
                out[indices] = self.bns[i](x[indices])
            elif len(indices) == 1:
                self.bns[i].training = False
                out[indices] = self.bns[i](x[indices])
                self.bns[i].training = True
        return out


class GATEncoder(nn.Module):
    def __init__(self, in_channels, hidden_dims, latent_dim, conv_type, svd_q, num_heads,
                 dropout, concat, num_domains='', used_edge_weight=False, used_DSBN=False):
        """
        Initializes the GATEncoder

        Parameters
        ----------
        in_channels : int
            Number of input feature dimensions (length of each node's feature vector).
        hidden_dims : list[int]
            List of output dimensions for each hidden layer in the GAT.
        latent_dim : int
            Dimension of the latent feature representation produced by the encoder.
        svd_q : int
            Rank for the low-rank SVD approximation. Default is 5.
        num_heads : int
            Number of attention heads for each GAT layer.
        dropout : float
            Dropout rate for GAT layers.
        concat : bool
            Whether to concatenate outputs of all attention heads or not.
        num_domains : int or str
            Number of domains for domain-specific batch normalization (DSBN). If `1`, regular batch normalization is used.
        used_edge_weight : bool, optional
            Whether to use edge weights in the GAT layers (default is False).
        used_DSBN : bool, optional
            Whether to use domain-specific batch normalization (DSBN) (default is False).
        """
        super(GATEncoder, self).__init__()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # self.device = torch.device("cpu")
        self.svd_q = svd_q
        self.used_DSBN = used_DSBN
        self.used_edge_weight = used_edge_weight
        self.layers = nn.ModuleList()
        self.norm = nn.ModuleList()
        if conv_type == 'GAT':
            GATLayer = GATConv
        elif conv_type == 'GATv2Conv':
            GATLayer = GATv2Conv

        num_hidden_layers = len(hidden_dims)
        num_heads_list = [num_heads] * num_hidden_layers
        concat_list = [concat] * num_hidden_layers
        for i in range(num_hidden_layers):
            if concat_list[i]:
                current_dim = hidden_dims[i] * num_heads_list[i]
            else:
                current_dim = hidden_dims[i]

            if type(num_domains) == int:
                if num_domains == 1:  # TO DO
                    norm = nn.BatchNorm1d(current_dim)
                else:
                    # num_domains >1 represent domain-specific batch normalization of n domain
                    norm = DSBatchNorm(current_dim, num_domains)
            else:
                norm = None
            self.norm.append(norm)

        current_dim = in_channels
        # num_heads_list = [num_heads] * num_hidden_layers
        dropout_list = [dropout] * num_hidden_layers
        for i in range(num_hidden_layers):
            layer = GATLayer(
                in_channels=current_dim,
                out_channels=hidden_dims[i],
                heads=num_heads_list[i],
                dropout=dropout_list[i],
                concat=concat_list[i],
                edge_dim=1 if self.used_edge_weight else None
            )
            self.layers.append(layer)
            if concat_list[i]:
                current_dim = hidden_dims[i] * num_heads_list[i]
            else:
                current_dim = hidden_dims[i]

        self.conv_mean = GATLayer(in_channels=current_dim,
                                  out_channels=latent_dim,
                                  heads=num_heads,
                                  concat=False,
                                  edge_dim=1 if self.used_edge_weight else None,
                                  dropout=dropout)
        self.conv_log_std = GATLayer(in_channels=current_dim,
                                     out_channels=latent_dim,
                                     heads=num_heads,
                                     concat=False,
                                     edge_dim=1 if self.used_edge_weight else None,
                                     dropout=dropout)

    def forward(self, data):
        """
        Basic block consist of:
            fc -> bn -> act -> dropout
        """
        x1, edge_index1, y1, edge_weight1 = data.x, data.edge_index, data.y, data.edge_attr

        # 首先，将edge_index和edge_attr转换为稀疏张量
        num_nodes = data.num_nodes  # 假设数据中节点的总数
        # 创建 SciPy 的 COO 格式稀疏矩阵
        value = torch.squeeze(data.edge_attr).cpu().numpy()
        row = data.edge_index[0].cpu().numpy()
        col = data.edge_index[1].cpu().numpy()
        sparse_adj = sp.coo_matrix((value, (row, col)),
                                   shape=(num_nodes, num_nodes))
        # perform svd reconstruction
        adj = scipy_sparse_mat_to_torch_sparse_tensor(sparse_adj).coalesce()
        #         print('Performing SVD...')
        svd_u, s, svd_v = torch.svd_lowrank(adj, q=self.svd_q)
        u_mul_s = svd_u @ (torch.diag(s))
        #         v_mul_s = svd_v @ (torch.diag(s))
        recon_adj = u_mul_s @ svd_v.T
        del svd_u, s, svd_v, u_mul_s
        #         print('SVD done.')

        # 将密集矩阵转换为稀疏矩阵
        sparse_adj = recon_adj.to_sparse()
        sparse_adj = sparse_adj.to(self.device)
        # 从稀疏矩阵中提取行和列索引，这些索引代表边的连接
        row = sparse_adj.indices()[0]
        col = sparse_adj.indices()[1]
        # 创建 PyG 的 edge_index 格式
        edge_index2 = torch.stack([row, col], dim=0)
        # 从稀疏矩阵中提取边的属性，即连接的权重
        edge_weight2 = sparse_adj.values().unsqueeze(1)
        x2, y2 = data.x, data.y
        del sparse_adj

        ### original graph
        for idx, layer in enumerate(self.layers):
            x1, _ = layer(x1, edge_index1,
                          edge_attr=edge_weight1 if self.used_edge_weight else None,
                          return_attention_weights=True)  # attn1
            if self.used_DSBN:
                if self.norm:
                    if len(x1) == 1:
                        pass
                    elif self.norm[0].__class__.__name__ == 'DSBatchNorm':
                        x1 = self.norm[idx](x1, y1)
                    else:
                        x1 = self.norm[idx](x1)
                    x1 = F.relu(x1)

        z_mean1, _ = self.conv_mean(x1, edge_index1,
                                    edge_attr=edge_weight1 if self.used_edge_weight else None,
                                    return_attention_weights=True)
        z_log_std1, _ = self.conv_log_std(x1, edge_index1,
                                          edge_attr=edge_weight1 if self.used_edge_weight else None,
                                          return_attention_weights=True)

        ### SVD_adj graph
        for idx, layer in enumerate(self.layers):
            x2, _ = layer(x2, edge_index2,
                          edge_attr=edge_weight2 if self.used_edge_weight else None,
                          return_attention_weights=True)

            if self.used_DSBN:
                if self.norm:
                    if len(x2) == 1:
                        pass
                    elif self.norm[0].__class__.__name__ == 'DSBatchNorm':
                        x2 = self.norm[idx](x2, y2)
                    else:
                        x2 = self.norm[idx](x2)
                    x2 = F.relu(x2)

        z_mean2, _ = self.conv_mean(x2, edge_index2,
                                    edge_attr=edge_weight2 if self.used_edge_weight else None,
                                    return_attention_weights=True)
        z_log_std2, _ = self.conv_log_std(x2, edge_index2,
                                          edge_attr=edge_weight2 if self.used_edge_weight else None,
                                          return_attention_weights=True)

        return z_mean1, z_log_std1, z_mean2, z_log_std2


class GATDecoder(nn.Module):
    def __init__(self, in_channels, hidden_dims, out_channels, conv_type, num_heads, dropout, concat,
                 num_domains='', used_edge_weight=False, used_DSBN=False):
        """
        Initializes the GATDecoder

        Parameters
        ----------
        in_channels : int
            Number of input feature dimensions.
        hidden_dims : list[int]
            List of output dimensions for each hidden layer in the GAT, in ascending order.
        out_channels : int
            Number of output feature dimensions.
        num_heads : int
            Number of attention heads for each GAT layer.
        dropout : float
            Dropout rate for GAT layers.
        concat : bool
            Whether to concatenate outputs of all attention heads or not.
        num_domains : int or str
            Number of domains for domain-specific batch normalization (DSBN). If `1`, regular batch normalization is used.
        used_edge_weight : bool, optional
            Whether to use edge weights in the GAT layers (default is False).
        used_DSBN : bool, optional
            Whether to use domain-specific batch normalization (DSBN) (default is False).
        """
        super(GATDecoder, self).__init__()

        # self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.used_DSBN = used_DSBN
        self.used_edge_weight = used_edge_weight
        self.layers = nn.ModuleList()
        self.norm = nn.ModuleList()
        self.dropout = dropout
        if conv_type == 'GAT':
            GATLayer = GATConv
        elif conv_type == 'GATv2Conv':
            GATLayer = GATv2Conv

        num_hidden_layers = len(hidden_dims)
        num_heads_list = [num_heads] * num_hidden_layers
        concat_list = [concat] * num_hidden_layers
        for i in range(num_hidden_layers):
            if concat_list[i]:
                current_dim = hidden_dims[::-1][i] * num_heads_list[i]
            else:
                current_dim = hidden_dims[::-1][i]  # [::-1] 代表反转

            if type(num_domains) == int:
                if num_domains == 1:  # TO DO
                    norm = nn.BatchNorm1d(current_dim)
                else:
                    # num_domains >1 represent domain-specific batch normalization of n domain
                    norm = DSBatchNorm(current_dim, num_domains)
            else:
                norm = None
            self.norm.append(norm)

        current_dim = in_channels  # in_channels
        dropout_list = [dropout] * num_hidden_layers
        for i in range(num_hidden_layers):
            layer = GATLayer(
                in_channels=current_dim,
                out_channels=hidden_dims[::-1][i],
                heads=num_heads_list[i],
                dropout=dropout_list[i],
                concat=concat_list[i],
                edge_dim=1 if self.used_edge_weight else None
            )
            self.layers.append(layer)
            if concat_list[i]:
                current_dim = hidden_dims[::-1][i] * num_heads_list[i]
            else:
                current_dim = hidden_dims[::-1][i]

        ### 数据集总重构的layers
        self.conv_recon = GATLayer(in_channels=current_dim,
                                   out_channels=out_channels,
                                   heads=num_heads,
                                   concat=False,
                                   edge_dim=1 if self.used_edge_weight else None,
                                   dropout=dropout)

    def forward(self, x, data):
        """
        Basic block consist of:
            fc -> bn -> act -> dropout
        """
        edge_index, y, edge_weight = data.edge_index, data.y, data.edge_attr

        for idx, layer in enumerate(self.layers):
            x, _ = layer(x, edge_index, edge_attr=edge_weight if self.used_edge_weight else None,
                         return_attention_weights=True)
            if self.used_DSBN:
                if self.norm:
                    if len(x) == 1:
                        pass
                    elif self.norm[0].__class__.__name__ == 'DSBatchNorm':
                        x = self.norm[idx](x, y)
                    else:
                        x = self.norm[idx](x)
                    x = F.relu(x)

        recon_x, _ = self.conv_recon(x, edge_index,
                                     edge_attr=edge_weight if self.used_edge_weight else None,
                                     return_attention_weights=True)

        return recon_x

### GCN encoder
class GCNEncoder(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, svd_q, dropout=0.2,
                 num_domains='', used_edge_weight=False, used_DSBN=False):
        """
        Initializes the GCNEncoder
        Parameters
        ----------
        in_channels : int
            Number of input feature dimensions (length of each node's feature vector).
        hidden_channels : list[int]
            List of output dimensions for each hidden layer in the GCN.
        out_channels : int
            Dimension of the output feature representation produced by the encoder.
        svd_q : int
            Rank for the low-rank SVD approximation.
        dropout : float
            Dropout rate for GCN layers.
        num_domains : int or str
            Number of domains for domain-specific batch normalization (DSBN). If `1`, regular batch normalization is used.
        used_edge_weight : bool, optional
            Whether to use edge weights in the GAT layers (default is False).
        used_DSBN : bool, optional
            Whether to use domain-specific batch normalization (DSBN) (default is False).
        """
        super(GCNEncoder, self).__init__()
        # 如果 hidden_channels 是单一数字，将其转换成单元素列表
        if isinstance(hidden_channels, int):
            hidden_channels = [hidden_channels]

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.svd_q = svd_q
        self.used_DSBN = used_DSBN
        self.used_edge_weight = used_edge_weight
        self.norm = nn.ModuleList()

        # 创建一个包含所有GCN层的列表
        gcn_layers = []
        total_layers = [in_channels] + hidden_channels
        for i in range(len(total_layers) - 1):
            gcn_layers.append(GCNConv(total_layers[i], total_layers[i + 1], dropout=dropout))

        # 使用 nn.ModuleList 以确保所有层都被正确注册
        self.gcn_layers = nn.ModuleList(gcn_layers)

        # 输出层
        self.gcn_mu = GCNConv(hidden_channels[-1], out_channels, dropout=dropout)
        self.gcn_logvar = GCNConv(hidden_channels[-1], out_channels, dropout=dropout)

        # self.norm 层
        num_hidden_layers = len(hidden_channels)
        for i in range(num_hidden_layers):
            current_dim = hidden_channels[i]

            if type(num_domains) == int:
                if num_domains == 1:  # TO DO
                    norm = nn.BatchNorm1d(current_dim)
                else:
                    norm = DSBatchNorm(current_dim,
                                       num_domains)  # num_domains >1 represent domain-specific batch normalization of n domain
            else:
                norm = None
            self.norm.append(norm)

    def forward(self, data):
        x1, edge_index1, y1, edge_weight1 = data.x, data.edge_index, data.y, data.edge_attr

        # 首先，将edge_index和edge_attr转换为稀疏张量
        num_nodes = data.num_nodes  # 假设数据中节点的总数
        # 创建 SciPy 的 COO 格式稀疏矩阵
        value = torch.squeeze(data.edge_attr).cpu().numpy()
        row = data.edge_index[0].cpu().numpy()
        col = data.edge_index[1].cpu().numpy()
        sparse_adj = sp.coo_matrix((value, (row, col)),
                                   shape=(num_nodes, num_nodes))
        # perform svd reconstruction
        adj = scipy_sparse_mat_to_torch_sparse_tensor(sparse_adj).coalesce()
        svd_u, s, svd_v = torch.svd_lowrank(adj, q=self.svd_q)
        u_mul_s = svd_u @ (torch.diag(s))
        #         v_mul_s = svd_v @ (torch.diag(s))
        recon_adj = u_mul_s @ svd_v.T
        del svd_u, s, svd_v, u_mul_s

        # 将密集矩阵转换为稀疏矩阵
        sparse_adj = recon_adj.to_sparse()
        sparse_adj = sparse_adj.to(self.device)
        # 从稀疏矩阵中提取行和列索引，这些索引代表边的连接
        row = sparse_adj.indices()[0]
        col = sparse_adj.indices()[1]
        # 创建 PyG 的 edge_index 格式
        edge_index2 = torch.stack([row, col], dim=0)
        # 从稀疏矩阵中提取边的属性，即连接的权重
        edge_weight2 = sparse_adj.values().unsqueeze(1)
        x2, y2 = data.x, data.y
        del sparse_adj

        ### original graph
        for idx, layer in enumerate(self.gcn_layers):
            x1 = layer(x1, edge_index1,
                       edge_weight=edge_weight1 if self.used_edge_weight else None)

            if self.used_DSBN:
                if self.norm:
                    if len(x1) == 1:
                        pass
                    elif self.norm[0].__class__.__name__ == 'DSBatchNorm':
                        x1 = self.norm[idx](x1, y1)
                    else:
                        x1 = self.norm[idx](x1)
                    x1 = F.relu(x1)

        z_mean1 = self.gcn_mu(x1, edge_index1,
                              edge_weight=edge_weight1 if self.used_edge_weight else None)
        z_log_std1 = self.gcn_logvar(x1, edge_index1,
                                     edge_weight=edge_weight1 if self.used_edge_weight else None)

        ### SVD_adj graph
        for idx, layer in enumerate(self.gcn_layers):
            x2 = layer(x2, edge_index2,
                       edge_weight=edge_weight2 if self.used_edge_weight else None)

            if self.used_DSBN:
                if self.norm:
                    if len(x2) == 1:
                        pass
                    elif self.norm[0].__class__.__name__ == 'DSBatchNorm':
                        x2 = self.norm[idx](x2, y2)
                    else:
                        x2 = self.norm[idx](x2)
                    x2 = F.relu(x2)

        z_mean2 = self.gcn_mu(x2, edge_index2,
                              edge_weight=edge_weight2 if self.used_edge_weight else None)
        z_log_std2 = self.gcn_logvar(x2, edge_index2,
                                     edge_weight=edge_weight2 if self.used_edge_weight else None)

        return z_mean1, z_log_std1, z_mean2, z_log_std2


### GCN decoder
class GCNDecoder(nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels, dropout=0.2,
                 num_domains='', used_edge_weight=False, used_DSBN=False):
        """
        Initializes the GCNDecoder

        Parameters
        ----------
        in_channels : int
            Number of input feature dimensions.
        hidden_channels : list[int]
            List of output dimensions for each hidden layer in the GCN, in ascending order.
        out_channels : int
            Number of output feature dimensions.
        dropout : float
            Dropout rate for GAT layers.
        num_domains : int or str
            Number of domains for domain-specific batch normalization (DSBN). If `1`, regular batch normalization is used.
        used_edge_weight : bool, optional
            Whether to use edge weights in the GAT layers (default is False).
        used_DSBN : bool, optional
            Whether to use domain-specific batch normalization (DSBN) (default is False).
        """
        super(GCNDecoder, self).__init__()
        # 如果 hidden_channels 是单一数字，将其转换成单元素列表
        if isinstance(hidden_channels, int):
            hidden_channels = [hidden_channels]

        self.used_DSBN = used_DSBN
        self.used_edge_weight = used_edge_weight
        self.layers = nn.ModuleList()
        self.norm = nn.ModuleList()

        # 创建一个包含所有GCN层的列表
        gcn_layers = []
        hidden_channels = hidden_channels[::-1]  # 反转
        total_layers = [in_channels] + hidden_channels
        for i in range(len(total_layers) - 1):
            gcn_layers.append(GCNConv(total_layers[i], total_layers[i + 1], dropout=dropout))

        # 使用 nn.ModuleList 以确保所有层都被正确注册
        self.gcn_layers = nn.ModuleList(gcn_layers)

        # 输出层
        self.gcn_recon = GCNConv(hidden_channels[-1], out_channels, dropout=dropout)

        # self.norm 层
        num_hidden_layers = len(hidden_channels)
        for i in range(num_hidden_layers):
            current_dim = hidden_channels[i]

            if type(num_domains) == int:
                if num_domains == 1:  # TO DO
                    norm = nn.BatchNorm1d(current_dim)
                else:
                    norm = DSBatchNorm(current_dim,
                                       num_domains)  # num_domains >1 represent domain-specific batch normalization of n domain
            else:
                norm = None
            self.norm.append(norm)

    def forward(self, x, data):
        edge_index, y, edge_weight = data.edge_index, data.y, data.edge_attr

        ### latent
        for idx, layer in enumerate(self.gcn_layers):
            x = layer(x, edge_index,
                      edge_weight=edge_weight if self.used_edge_weight else None)

            if self.used_DSBN:
                if self.norm:
                    if len(x) == 1:
                        pass
                    elif self.norm[0].__class__.__name__ == 'DSBatchNorm':
                        x = self.norm[idx](x, y)
                    else:
                        x = self.norm[idx](x)
                    x = F.relu(x)

        x_recon = self.gcn_recon(x, edge_index,
                                 edge_weight=edge_weight if self.used_edge_weight else None)

        return x_recon


# Based on VGAE class in PyTorch Geometric
EPS = 1e-15
MAX_LOGSTD = 10
class GNNModelVAE(GAE):
    def __init__(self, encoder, bottle_neck_neurons, hidden_dims, feature_dim,
                 num_heads, dropout, concat, n_domain, used_edge_weight, used_DSBN,
                 used_recon_exp, conv_type, cluster_num, gnn_layer=2, decoder=None):
        """
        Initializes the GCNModelVAE
        Parameters
        ----------
        encoder : nn.Module
            The encoder module used in the variational graph autoencoder. 'GAT' or 'GCN'
        enc_in_channels : int
            Number of input feature dimensions for the encoder.
        n_domain : int
            Number of domains for domain-specific batch normalization (DSBN).
        args : Namespace
            Arguments that include hyperparameters and configurations such as dropout rate, latent dimensions, etc.
        decoder : nn.Module, optional
            The decoder module used in the variational autoencoder. Defaults to `InnerProductDecoder` if not specified.
        """
        super(GNNModelVAE, self).__init__(encoder, decoder)
        self.decoder = InnerProductDecoder() if decoder is None else decoder

        self.latent = bottle_neck_neurons
        self.hidden_dims = hidden_dims
        self.feature_dim = feature_dim
        self.num_heads = num_heads
        self.dropout = dropout
        self.concat = concat
        self.n_domain = n_domain
        self.used_edge_weight = used_edge_weight
        self.used_DSBN = used_DSBN

        # model configurations
        self.used_recon_exp = used_recon_exp
        self.conv_type = conv_type
        assert self.conv_type in ['GAT', 'GATv2Conv', 'GCN'], 'Convolution must be "GCN", "GAT" or "GATv2Conv".'
        self.cluster_num = cluster_num
        self.gnn_layer = gnn_layer
        # 使用 Xavier 初始化权重
        self.eps_weight = nn.Parameter(nn.init.xavier_uniform_(torch.empty(self.latent, self.latent)))
        self.eps_bias = nn.Parameter(torch.zeros(self.latent))
        self.instance_projector = nn.Sequential(
            nn.Linear(self.latent, self.latent),
            nn.LayerNorm(self.latent, elementwise_affine=False),
            nn.ReLU(),
            nn.Linear(self.latent, self.feature_dim),
        )
        self.cluster_projector = nn.Sequential(
            nn.Linear(self.latent, self.latent),
            nn.LayerNorm(self.latent, elementwise_affine=False),
            nn.ReLU(),
            nn.Linear(self.latent, self.cluster_num),
            nn.Softmax(dim=1)
        )

        ## 重构表达谱
        if self.used_recon_exp:
            if self.conv_type in ['GAT', 'GATv2Conv']:
                self.GAT_decoder = GATDecoder(
                    in_channels=self.latent,
                    hidden_dims=self.hidden_dims,
                    out_channels=self.feature_dim,
                    conv_type=self.conv_type,
                    num_heads=self.num_heads,
                    dropout=self.dropout,
                    concat=self.concat,
                    num_domains=self.n_domain,  # DSBN
                    used_edge_weight=self.used_edge_weight,
                    used_DSBN=self.used_DSBN
                )
            elif self.conv_type == 'GCN':
                self.GCN_decoder = GCNDecoder(
                    in_channels=self.latent,
                    hidden_channels=self.hidden_dims,
                    out_channels=self.feature_dim,
                    dropout=self.dropout,
                    num_domains=self.n_domain,  # DSBN
                    used_edge_weight=self.used_edge_weight,
                    used_DSBN=self.used_DSBN
                )
            else:
                raise NotImplementedError("Unknown GNN-Operator.")

    def reparametrize(self, mu: Tensor, logstd: Tensor, eps=None) -> Tensor:
        if self.training:
            if eps is not None:
                return mu + eps * torch.randn_like(logstd) * torch.exp(logstd)
            else:
                return mu + torch.randn_like(logstd) * torch.exp(logstd)
        else:
            return mu

    def encode(self, *args, **kwargs) -> Tensor:
        """"""  # noqa: D419
        if self.conv_type in ['GAT', 'GATv2Conv']:
            self.__mu1__, self.__logstd1__, self.__mu2__, self.__logstd2__ = self.encoder(*args, **kwargs)
            return self.__mu1__, self.__logstd1__, self.__mu2__, self.__logstd2__
        else:
            self.__mu1__, self.__logstd1__, self.__mu2__, self.__logstd2__ = self.encoder(*args, **kwargs)
            return self.__mu1__, self.__logstd1__, self.__mu2__, self.__logstd2__

    def recon_loss(self, z: Tensor, pos_edge_index: Tensor,
                   neg_edge_index: Optional[Tensor] = None) -> Tensor:
        r"""Given latent variables :obj:`z`, computes the binary cross
        entropy loss for positive edges :obj:`pos_edge_index` and negative
        sampled edges.

        Args:
            z (torch.Tensor): The latent space :math:`\mathbf{Z}`.
            pos_edge_index (torch.Tensor): The positive edges to train against.
            neg_edge_index (torch.Tensor, optional): The negative edges to
                train against. If not given, uses negative sampling to
                calculate negative edges. (default: :obj:`None`)
        """
        pos_loss = -torch.log(
            self.decoder(z, pos_edge_index, sigmoid=True) + EPS).mean()

        # Do not include self-loops in negative samples
        pos_edge_index, _ = remove_self_loops(pos_edge_index)
        pos_edge_index, _ = add_self_loops(pos_edge_index)

        if neg_edge_index is None:
            neg_edge_index = negative_sampling(pos_edge_index, z.size(0))
        neg_loss = -torch.log(1 -
                              self.decoder(z, neg_edge_index.long(), sigmoid=True) +
                              EPS).mean()

        return pos_loss + neg_loss

    def kl_loss(self, mu: Optional[Tensor] = None,
                logstd: Optional[Tensor] = None) -> Tensor:
        r"""Computes the KL loss, either for the passed arguments :obj:`mu`
        and :obj:`logstd`, or based on latent variables from last encoding.

        Args:
            mu (torch.Tensor, optional): The latent space for :math:`\mu`. If
                set to :obj:`None`, uses the last computation of :math:`\mu`.
                (default: :obj:`None`)
            logstd (torch.Tensor, optional): The latent space for
                :math:`\log\sigma`.  If set to :obj:`None`, uses the last
                computation of :math:`\log\sigma^2`. (default: :obj:`None`)
        """
        mu = self.__mu1__ if mu is None else mu
        logstd = self.__logstd1__ if logstd is None else logstd.clamp(
            max=MAX_LOGSTD)
        return -0.5 * torch.mean(
            torch.sum(1 + 2 * logstd - mu ** 2 - logstd.exp() ** 2, dim=1))

    def calc_individual_metrics(self, z: Tensor, pos_edge_index: Tensor,
                                neg_edge_index: Tensor) -> Tuple[Tensor, Tensor]:
        r"""Given latent variables :obj:`z`, positive edges
        :obj:`pos_edge_index` and negative edges :obj:`neg_edge_index`,
        computes area under the ROC curve (AUC) and average precision (AP)
        scores.

        Args:
            z (torch.Tensor): The latent space :math:`\mathbf{Z}`.
            pos_edge_index (torch.Tensor): The positive edges to evaluate
                against.
            neg_edge_index (torch.Tensor): The negative edges to evaluate
                against.
        """
        from sklearn.metrics import roc_auc_score, average_precision_score, accuracy_score, f1_score, roc_curve, \
            precision_recall_curve, silhouette_score, calinski_harabasz_score, davies_bouldin_score

        pos_y = z.new_ones(pos_edge_index.size(1))
        neg_y = z.new_zeros(neg_edge_index.size(1))
        y = torch.cat([pos_y, neg_y], dim=0)

        pos_pred = self.decoder(z, pos_edge_index, sigmoid=True)
        neg_pred = self.decoder(z, neg_edge_index, sigmoid=True)
        pred = torch.cat([pos_pred, neg_pred], dim=0)

        y, pred = y.detach().cpu().numpy(), pred.detach().cpu().numpy()

        try:
            roc_score = roc_auc_score(y, pred)
        except ValueError:
            roc_score = 0.5
        ap_score = average_precision_score(y, pred)
        acc = accuracy_score(y, pred > 0.5)
        f1 = f1_score(y, pred > 0.5, average='micro')

        return roc_score, ap_score, acc, f1

    def encodeBatch(self, data):
        all_mu1 = []
        for _ in range(self.gnn_layer):
            if self.conv_type in ['GAT', 'GATv2Conv']:
                mu1, _, _, _ = self.encode(data)
                all_mu1.append(mu1)
            else:
                mu1, _, _, _ = self.encode(data)
                all_mu1.append(mu1)

        mean1 = torch.stack(all_mu1).mean(dim=0)  # sum
        logstd1 = torch.matmul(mean1, self.eps_weight) + self.eps_bias
        z1 = self.reparametrize(mean1, logstd1)

        ## 重构表达矩阵
        if self.used_recon_exp:
            if self.conv_type in ['GAT', 'GATv2Conv']:
                recon_features = self.GAT_decoder(z1, data)
            else:
                recon_features = self.GCN_decoder(z1, data)
            return mean1, recon_features
        else:
            return mean1

    def forward(self, data):
        all_mu1 = []
        all_mu2 = []
        for _ in range(self.gnn_layer):
            if self.conv_type in ['GAT', 'GATv2Conv']:
                mu1, _, mu2, _ = self.encode(data)
                all_mu1.append(mu1)
                all_mu2.append(mu2)
            else:
                mu1, _, mu2, _ = self.encode(data)
                all_mu1.append(mu1)
                all_mu2.append(mu2)

        mean1 = torch.stack(all_mu1).mean(dim=0)  # sum
        logstd1 = torch.matmul(mean1, self.eps_weight) + self.eps_bias
        z1 = self.reparametrize(mean1, logstd1)

        mean2 = torch.stack(all_mu2).mean(dim=0)
        logstd2 = torch.matmul(mean2, self.eps_weight) + self.eps_bias
        z2 = self.reparametrize(mean2, logstd2)

        z_1 = normalize(self.instance_projector(z1), dim=1)
        z_2 = normalize(self.instance_projector(z2), dim=1)

        c_1 = self.cluster_projector(z1)
        c_2 = self.cluster_projector(z2)

        # adj_pred = self.decoder.forward_all(z, sigmoid=False)

        ## 重构表达矩阵
        if self.used_recon_exp:
            if self.conv_type in ['GAT', 'GATv2Conv']:
                recon_features = self.GAT_decoder(z1, data)
            else:
                recon_features = self.GCN_decoder(z1, data)
            return z1, z_1, z_2, c_1, c_2, mean1, logstd1, recon_features
        else:
            return z1, z_1, z_2, c_1, c_2, mean1, logstd1

    def single_test(self, data):
        # Ensure test_data contains neg_edge_label_index
        if not hasattr(data, 'neg_edge_label_index'):
            data.neg_edge_label_index = negative_sampling(
                edge_index=data.pos_edge_label_index,
                num_nodes=data.num_nodes
            )

        pos_edge_label_index, neg_edge_label_index = data.pos_edge_label_index.long(), data.neg_edge_label_index.long()
        with torch.no_grad():
            all_mu = []
            for _ in range(self.gnn_layer):
                if self.conv_type in ['GAT', 'GATv2Conv']:
                    mu1, _, _, _ = self.encode(data)
                    all_mu.append(mu1)
                else:
                    mu1, _, _, _ = self.encode(data)
                    all_mu.append(mu1)

            mean = torch.stack(all_mu).mean(dim=0)
            logstd = torch.matmul(mean, self.eps_weight) + self.eps_bias
            z = self.reparametrize(mean, logstd)

        roc_score, ap_score, acc, f1 = self.calc_individual_metrics(z, pos_edge_label_index, neg_edge_label_index)
        return roc_score, ap_score, acc, f1