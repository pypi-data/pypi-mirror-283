import random
import numpy as np
import muon as mu
# from muon import MuData
import torch
from sklearn.preprocessing import LabelEncoder
from torch_geometric.data import Data
# from torch_scatter import scatter


def Transfer_scData(adata, label_name=None, data_type=None):
    """
    Converts an AnnData or MuData object into a PyTorch Geometric Data object.

    Parameters
    ----------
    adata : AnnData or MuData
        The annotated data matrix to be converted.
    label_name : str, optional
        Column name in `adata.obs` containing the labels for each node.
        If None, all nodes are assigned a default label of 1.
    data_type : str, optional
        Indicates the type of data matrix ('muData' or 'AnnData').
    Returns
    -------
    torch_geometric.data.Data
        A PyTorch Geometric Data object containing the graph data.
    """
    # Initialize an empty list for edges and their weights
    row_col = []
    # if data_type == 'Paired':
    #     # adj = adata.uns['obsp_rna']['connectivities']
    #     adj = adata.obsp['connectivities_combined']
    # else:
    adj = adata.obsp['connectivities']
    edge_weight = []
    rows, cols = adj.nonzero()
    edge_nums = adj.getnnz()
    for i in range(edge_nums):
        row_col.append([rows[i], cols[i]])
        edge_weight.append(adj.data[i])
    edge_index = torch.tensor(np.array(row_col), dtype=torch.long).T
    edge_attr = torch.tensor(np.array(edge_weight), dtype=torch.float)
    edge_attr = torch.unsqueeze(edge_attr, dim=-1)  # 在第一维度添加维度

    ## celltype label_encoder Todo 如果标签信息本身就是数值则不需要转换
    if label_name is not None:
        label_encoder = LabelEncoder()
        if data_type == 'Paired':
            meta = np.array(adata.obs['rna:' + label_name].astype('str'))
        else:
            meta = np.array(adata.obs[label_name].astype('str'))
        meta = label_encoder.fit_transform(meta)
        # meta = meta.astype(np.float32)
        inverse = label_encoder.inverse_transform(range(0, np.max(meta) + 1))
        y = torch.from_numpy(meta.astype(np.int64))
    else:
        y = torch.from_numpy(np.array([1] * adata.shape[0]))

    if type(adata.X) == np.ndarray:
        data = Data(edge_index=edge_index, edge_attr=edge_attr, x=torch.FloatTensor(adata.X),  # .todense()
                    y=torch.LongTensor(y))
    else:
        data = Data(edge_index=edge_index, edge_attr=edge_attr, x=torch.FloatTensor(adata.X.todense()),  # .todense()
                    y=torch.LongTensor(y))
    return data


def split_data(num_y, val_split, test_split):
    split_idx = list(range(num_y))
    random.shuffle(split_idx)
    train_split = (1 - test_split - val_split)
    train_idx = split_idx[: int(len(split_idx) * train_split)] # Train mask
    train_mask = torch.zeros(num_y, dtype = torch.bool)
    train_mask[train_idx] = 1
    val_idx = split_idx[ int(len(split_idx) * train_split) : int(len(split_idx) * (train_split + val_split))] # Val mask
    val_mask = torch.zeros(num_y, dtype=torch.bool)
    val_mask[val_idx] = 1
    test_idx = split_idx[int(len(split_idx) * (train_split + val_split)) :] # Test mask
    test_mask = torch.zeros(num_y, dtype=torch.bool)
    test_mask[test_idx] = 1
    return train_mask, val_mask, test_mask


from torch_geometric.data import Data
from torch_geometric.loader import NeighborLoader, GraphSAINTEdgeSampler
from torch_geometric.utils import structured_negative_sampling
def generate_batch(data, edge_attr_dict, mask, batch_size, loader_type="graphsaint",
                   num_layers=2):
    # Positive edges
    if mask == "train":
        pos_edge_index = data.edge_index[:, data.train_mask]
        edge_type = data.edge_attr[data.train_mask]
        y = data.y[data.train_mask]
    elif mask == "val":
        pos_edge_index = data.edge_index[:, data.val_mask]
        edge_type = data.edge_attr[data.val_mask]
        y = data.y[data.train_mask]
    elif mask == "test":
        pos_edge_index = data.edge_index[:, data.test_mask]
        edge_type = data.edge_attr[data.test_mask]
        y = data.y[data.train_mask]
    else:
        pos_edge_index = data.edge_index
        edge_type = data.edge_attr
        y = data.y[data.train_mask]

    # Negative edges
    neg_edge_index, neg_edge_type = negative_sampler(pos_edge_index, edge_type, edge_attr_dict)

    # All edges and labels
    total_edge_index = torch.cat([pos_edge_index, neg_edge_index], dim=-1)
    total_edge_type = torch.cat([edge_type, neg_edge_type], dim=-1)

    # Save information for the loader
    data = Data(x=data.x, edge_index=total_edge_index, edge_attr=total_edge_type, y=y)
    data.n_id = torch.arange(data.num_nodes)
    if loader_type == "neighbor":
        loader = NeighborLoader(data, num_neighbors=[-1] * num_layers, batch_size=batch_size,
                                input_nodes=torch.arange(data.num_nodes), shuffle=True)
    elif loader_type == "graphsaint":
        # loader = GraphSAINTRandomWalkSampler(data, batch_size = batch_size, walk_length = num_layers)
        loader = GraphSAINTEdgeSampler(data, batch_size=batch_size, num_steps=16)
    else:
        raise NotImplementedError

    return loader


def negative_sampler(pos_edge_index, edge_type, edge_attr_dict):
    if len(edge_type) == 0: return pos_edge_index, edge_type
    neg_edge_index = None
    neg_edge_type = []
    for attr, idx in edge_attr_dict.items():
        mask = (edge_type == idx)
        if mask.sum() == 0: continue
        pos_rel_edge_index = pos_edge_index.T[mask].T
        neg_source, neg_target, neg_rand = structured_negative_sampling(pos_rel_edge_index)
        neg_rel_edge_index = torch.stack((neg_source, neg_rand), dim=0)
        """
        neg_rel_edge_index = pos_rel_edge_index.clone()
        rand_axis = random.sample([0, 1], 1)[0]
        rand_index = torch.randperm(pos_rel_edge_index.size(1))
        neg_rel_edge_index[rand_axis, :] = pos_rel_edge_index[rand_axis, rand_index]
        """
        if neg_edge_index == None:
            neg_edge_index = neg_rel_edge_index
        else:
            neg_edge_index = torch.cat((neg_edge_index, neg_rel_edge_index), 1)

        neg_edge_type.extend([idx] * mask.sum())

    return neg_edge_index, torch.tensor(neg_edge_type)


def to_dense_adj(edge_index, edge_attr, num_nodes, device, alpha=2):
    # edge_index: [2, E] tensor of edge indices
    # edge_attr: [E, D] tensor of edge attributes
    # num_nodes: number of nodes in the graph

    # 初始化一个邻接矩阵，大小为[num_nodes, num_nodes]
    adj_matrix = alpha * torch.ones(num_nodes, num_nodes).to(device)

    # 使用scatter函数将边属性加到邻接矩阵的对应位置
    # edge_index[0] 是起始节点，edge_index[1] 是终止节点
    adj_matrix[edge_index[0], edge_index[1]] = edge_attr/alpha

    return adj_matrix


def get_prior(celltype1, celltype2, alpha=2):
    """
    Create a prior correspondence matrix according to cell labels

    Parameters
    ----------
    celltype1
        cell labels of dataset X
    celltype2
        cell labels of dataset Y
    alpha
        the confidence of label, ranges from (1, inf). Higher alpha means better confidence. Default: 2.0

    Return
    ------
    torch.tensor
        a prior correspondence matrix between cells
    """

    Couple = alpha * torch.ones(len(celltype1), len(celltype2))

    for i in set(celltype1):
        index1 = np.where(celltype1 == i)
        if i in set(celltype2):
            index2 = np.where(celltype2 == i)
            for j in index1[0]:
                Couple[j, index2[0]] = 1 / alpha

    return Couple

def scipy_sparse_mat_to_torch_sparse_tensor(sparse_mx):
    sparse_mx = sparse_mx.tocoo().astype(np.float32)
    indices = torch.from_numpy(
        np.vstack((sparse_mx.row, sparse_mx.col)).astype(np.int64))
    values = torch.from_numpy(sparse_mx.data)
    shape = torch.Size(sparse_mx.shape)
    return torch.sparse_coo_tensor(indices, values, shape) # torch.sparse.FloatTensor(indices, values, shape)


def extract_subgraph(data, label):
    # 找出所有具有特定标签的节点索引
    node_indices = (data.y == label).nonzero(as_tuple=True)[0]

    # 提取这些节点的特征
    sub_x = data.x[node_indices]
    sub_y = data.y[node_indices]

    # 提取包含这些节点的边
    edge_index = data.edge_index
    mask = torch.isin(edge_index[0], node_indices) & torch.isin(edge_index[1], node_indices)
    sub_edge_index = edge_index[:, mask]

    # 将边索引调整为新的节点索引
    _, new_indices = node_indices.unique(return_inverse=True)
    remap = {old_idx.item(): new_idx for old_idx, new_idx in zip(node_indices, new_indices)}
    for i in range(sub_edge_index.shape[1]):
        sub_edge_index[0, i] = remap[sub_edge_index[0, i].item()]
        sub_edge_index[1, i] = remap[sub_edge_index[1, i].item()]

    # 提取对应的边特征
    sub_edge_attr = data.edge_attr[mask] if data.edge_attr is not None else None

    return Data(x=sub_x, edge_index=sub_edge_index, y=sub_y, edge_attr=sub_edge_attr)


import io
import logging
import pickle

import numpy as np
import torch
from anndata import AnnData
from scipy.sparse import csr_matrix, hstack

logger = logging.getLogger(__name__)


def _validate_var_names(adata, source_var_names):
    # Warning for gene percentage
    user_var_names = adata.var_names
    try:
        percentage = (len(user_var_names.intersection(source_var_names)) / len(user_var_names)) * 100
        percentage = round(percentage, 4)
        if percentage != 100:
            logger.warning(f"WARNING: Query shares {percentage}% of its genes with the reference."
                           "This may lead to inaccuracy in the results.")
    except Exception:
        logger.warning("WARNING: Something is wrong with the reference genes.")

    user_var_names = user_var_names.astype(str)
    new_adata = adata

    # Get genes in reference that are not in query
    ref_genes_not_in_query = []
    for name in source_var_names:
        if name not in user_var_names:
            ref_genes_not_in_query.append(name)

    if len(ref_genes_not_in_query) > 0:
        print("Query data is missing expression data of ",
              len(ref_genes_not_in_query),
              " genes which were contained in the reference dataset.")
        print("The missing information will be filled with zeroes.")

        filling_X = np.zeros((len(adata), len(ref_genes_not_in_query)))
        if isinstance(adata.X, csr_matrix):
            filling_X = csr_matrix(filling_X)  # support csr sparse matrix
            new_target_X = hstack((adata.X, filling_X))
        else:
            new_target_X = np.concatenate((adata.X, filling_X), axis=1)
        new_target_vars = adata.var_names.tolist() + ref_genes_not_in_query
        new_adata = AnnData(new_target_X, dtype="float32")
        new_adata.var_names = new_target_vars
        new_adata.obs = adata.obs.copy()

    if len(user_var_names) - (len(source_var_names) - len(ref_genes_not_in_query)) > 0:
        print(
            "Query data contains expression data of ",
            len(user_var_names) - (len(source_var_names) - len(ref_genes_not_in_query)),
            " genes that were not contained in the reference dataset. This information "
            "will be removed from the query data object for further processing.")

        # remove unseen gene information and order anndata
        new_adata = new_adata[:, source_var_names].copy()

    print(new_adata)

    return new_adata


class UnpicklerCpu(pickle.Unpickler):
    """Helps to pickle.load a model trained on GPU to CPU.

    See also https://github.com/pytorch/pytorch/issues/16797#issuecomment-633423219.
    """

    def find_class(self, module, name):
        if module == 'torch.storage' and name == '_load_from_bytes':
            return lambda b: torch.load(io.BytesIO(b), map_location='cpu')
        else:
            return super().find_class(module, name)


# plot utils
## adapted from https://github.com/theislab/scarches/blob/51a0294ca987dabffb6d109178e0f69a90f9c24f/scarches/plotting/_alluvial.py#L35
import numpy as np
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.cm
import itertools
# import bidi.algorithm  # for RTL languages


def plot_alluvial(input_data, *args, **kwargs):
    at = AlluvialTool(input_data, *args, **kwargs)
    ax = at.plot(**kwargs)
    ax.axis('off')
    return ax


class AlluvialTool:
    def __init__(
            self, input_data=(), x_range=(0, 1), res=20, h_gap_frac=0.03, v_gap_frac=0.03, **kwargs):
        self.input = input_data
        self.x_range = x_range
        self.res = res  # defines the resolution of the splines for all veins
        self.combs = sorted(itertools.product((0, 1), (1, 0)), key=lambda xy: all(xy))
        self.trace_xy = self.make_vein_blueprint_xy_arrays()
        self.data_dic = self.read_input()
        self.item_widths_dic = self.get_item_widths_dic()
        self.a_members, self.b_members = self.get_item_groups(**kwargs)
        self.h_gap_frac = h_gap_frac
        self.h_gap = x_range[1] * h_gap_frac
        self.v_gap_frac = v_gap_frac
        self.v_gap = sum(
            [width for b_item_counter in self.data_dic.values() for width in b_item_counter.values()]
        ) * v_gap_frac
        self.group_widths = self.get_group_widths()
        self.item_coord_dic = self.make_item_coordinate_dic()
        self.alluvial_fan = self.generate_alluvial_fan()
        self.item_text_len, self.width_text_len = self.get_vein_label_lengths()

    def make_vein_blueprint_xy_arrays(self):
        y = np.array([0, 0.15, 0.5, 0.85, 1])
        x = np.linspace(self.x_range[0], self.x_range[-1], len(y))
        z = np.polyfit(x, y, 4)
        f = np.poly1d(z)

        blueprint_x_vals = np.linspace(x[0], x[-1], self.res)
        blueprint_y_vals = f(blueprint_x_vals)
        return blueprint_x_vals, blueprint_y_vals

    def get_vein_polygon_xy(self, y_range, width):
        x, y = self.trace_xy
        y0, yn = y_range
        scale = yn - y0
        ty = y * scale + y0
        x_new = np.concatenate([x, x[::-1], ])
        y_new = np.concatenate([ty, ty[::-1] + width, ])
        return np.array([x_new, y_new]).transpose()

    def read_input_from_list(self):
        data_table = np.array(self.input)
        data_dic = defaultdict(Counter)
        for line in data_table:
            data_dic[line[0]][line[1]] += 1
        return data_dic

    def read_input_from_dict(self):
        # data_dic = self.input
        # data_table = []
        # for x_item, y_item_counter in data_dic.items():
        #     for y_item, count in y_item_counter.items():
        #         data_table += [[x_item, y_item]] * count
        # data_table = np.array(sorted(data_table))
        # return data_table, data_dic
        return self.input

    def read_input(self):
        return {
            dict: self.read_input_from_dict(),
            list: self.read_input_from_list()
         }[type(self.input)]

    def get_item_widths_dic(self):
        iwd = Counter()
        for a_item, b_item_counter in self.data_dic.items():
            for b_item, width in b_item_counter.items():
                iwd[a_item] += width
                iwd[b_item] += width
        return iwd

    def get_item_groups(self, a_sort=None, b_sort=None, **kwargs):
        _ = kwargs
        a_members = sorted(
            {a_item for a_item in self.data_dic}, key=lambda x: self.item_widths_dic[x]
        ) if not a_sort else a_sort
        b_members = sorted(
            {b_item for b_item_counter in self.data_dic.values() for b_item in b_item_counter},
            key=lambda x: self.item_widths_dic[x]
        ) if not b_sort else b_sort
        return a_members, b_members

    def get_group_widths(self):
        return [self.get_group_width(group) for group in (self.a_members, self.b_members)]

    def make_item_coordinate_dic(self, ):
        item_coord_dic = defaultdict(ItemCoordRecord)
        groups = self.a_members, self.b_members
        group_widths = self.group_widths
        for ind, group in enumerate(groups):
            last_pos = (max(group_widths) - group_widths[ind]) / 2
            for item in group:
                width = self.item_widths_dic[item]
                xy = (self.x_range[ind], last_pos)
                item_coord_dic[item].set_start_state(width, xy, side=ind)
                last_pos += width + self.v_gap
        return item_coord_dic

    def get_group_width(self, group):
        return sum([self.item_widths_dic[item] for item in group]) + (len(group) - 1) * self.v_gap

    def generate_alluvial_vein(self, a_item, b_item):
        width = self.data_dic[a_item][b_item]
        a_item_coord = self.item_coord_dic[a_item].read_state_and_advance_y(width)
        b_item_coord = self.item_coord_dic[b_item].read_state_and_advance_y(width)
        y_range = (a_item_coord[1], b_item_coord[1],)
        return self.get_vein_polygon_xy(y_range, width)

    def get_label_rectangles_xy(self, a_item, b_item):
        width = self.data_dic[a_item][b_item]
        return (
            self.generate_item_sub_rectangle(a_item, width),
            self.generate_item_sub_rectangle(b_item, width),
        )

    def generate_item_sub_rectangle(self, item, width):
        dic_entry = self.item_coord_dic[item]
        item_coord = dic_entry.read_state()
        sign = dic_entry.get_side_sign()
        return self.get_rectangle_xy(item_coord, width, sign)

    def get_rectangle_xy(self, item_coord, width, sign):
        x, y = item_coord
        rect = [[
                    x + sign * 0.5 * (0.5 + xa) * self.h_gap,
                    y + ya * width,
                ] for xa, ya in self.combs]
        return np.array(rect)

    def generate_alluvial_fan(self, ):
        alluvial_fan = []
        for a_item in self.a_members:
            b_items4a_item = self.data_dic[a_item].keys()
            for b_item in self.b_members:
                if b_item in b_items4a_item:
                    l_a_rect, l_b_rect = self.get_label_rectangles_xy(a_item, b_item)
                    alluvial_fan += [
                        [self.generate_alluvial_vein(a_item, b_item), l_a_rect, l_b_rect, a_item, b_item, ]]
        return np.array(alluvial_fan)

    def plot(self, figsize=(10, 15), alpha=0.5, **kwargs):
        colors = self.get_color_array(**kwargs)
        fig, ax = plt.subplots(figsize=figsize)
        for num in (0, 1, 2):
            patches = [
                Polygon(item, facecolor=colors[ind], alpha=alpha,
                        ) for ind, item in enumerate(self.alluvial_fan[:, num])
                ]
            for patch in patches:
                ax.add_patch(patch)
        self.auto_label_veins(**kwargs)
        self.label_sides(**kwargs)
        ax.autoscale()
        return ax

    def get_color_array(self, colors=None, color_side=0, rand_seed=1, cmap=None, **kwargs):
        _ = kwargs
        color_items = self.b_members if color_side else self.a_members
        lci = len(color_items)
        if rand_seed is not None:
            np.random.seed(rand_seed)
        cmap = cmap if cmap is not None else matplotlib.cm.get_cmap('hsv', lci * 10 ** 3)
        color_array = colors if colors is not None else [
            cmap(item) for ind, item in enumerate(np.random.rand(lci))]
        ind_dic = {item: ind for ind, item in enumerate(color_items)}
        polygon_colors = []
        for _, _, _, a_item, b_item, in self.alluvial_fan:
            item = b_item if color_side else a_item
            polygon_colors += [color_array[ind_dic[item]]]
        return np.array(polygon_colors)

    def get_vein_label_lengths(self):
        item_text_len = max([len(it) for it in self.item_widths_dic])
        width_text_len = max([len(str(w)) for w in self.item_widths_dic.values()])
        return item_text_len, width_text_len

    def auto_label_veins(self, fontname='Arial', **kwargs):
        # shift = max([len(item) for item in self.item_coord_dic.keys()]) / 50
        for item, vein in self.item_coord_dic.items():
            y_width = vein.get_width()
            sign = vein.get_side_sign()
            side = int(sign + 1) // 2
            ha = 'left' if side else 'right'
            plt.text(
                vein.get_x() + 1.5 * sign * self.h_gap,
                vein.get_y() + y_width / 2,
                self.item_text(item, side, **kwargs),
                ha=ha, va='center', fontname=fontname)

    def label_sides(
            self, labels=None, label_shift=0, disp_width=False, wdisp_sep=7*' ', fontname='Arial', **kwargs):
        if labels is not None:
            _ = kwargs
            y = max(self.group_widths)/2
            itl, wtl = self.item_text_len, self.width_text_len
            for side, sign in enumerate((-1, 1)):
                plt.text(
                    self.x_range[side]+sign*(label_shift+itl+int(disp_width)*(len(wdisp_sep)+wtl))*self.h_gap_frac,
                    y,
                    labels[side],
                    # bidi.algorithm.get_display(labels[side]),  # RTL languages
                    ha='center', va='center', fontname=fontname, fontsize=13, rotation=90-180*side
                )

    def item_text(
            self, item, side,
            disp_width=False, wdisp_sep=7*' ', width_in=True, **kwargs):
        _ = kwargs
        f_item = item
        # f_item = bidi.algorithm.get_display(item)  # for RTL languages
        tal = '<' if f_item == item else '>'
        if not disp_width:
            ans = ('{:%s}' % tal).format(item)
        else:
            width = self.item_coord_dic[item].get_width()
            if side and width_in or (not side and not width_in):
                lc, rc, wl, wr, tl, tr = '>', tal, self.width_text_len, self.item_text_len, width, f_item,
            else:
                lc, rc, wl, wr, tl, tr = tal, '>', self.item_text_len, self.width_text_len, f_item, width,
            pat = '{:%s%d}%s{:%s%d}' % (lc, wl, wdisp_sep, rc, wr,)
            ans = pat.format(tl, tr, )
        return ans


class ItemCoordRecord:
    def __init__(self, ):
        self.width = 0
        self.xy = ()
        self.curr_xy = self.xy[:]
        self.side = -1

    def set_start_state(self, width, xy, side):
        self.width = width
        self.xy = xy
        self.curr_xy = list(self.xy[:])
        self.side = side

    def read_state_and_advance_y(self, width):
        out = self.curr_xy[:]
        self.curr_xy[1] += width
        return out

    def read_state_and_advance_x(self, width):
        out = self.curr_xy[:]
        self.curr_xy[0] += width
        return out

    def read_state(self):
        return self.curr_xy[:]

    def get_xy(self, ):
        return self.xy

    def get_x(self, ):
        return self.xy[0]

    def get_y(self, ):
        return self.xy[1]

    def get_width(self, ):
        return self.width

    def get_side_sign(self, ):
        return 1 if self.side else -1