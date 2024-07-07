import os
import os.path as osp
import numpy as np
import pandas as pd

import torch
from torch_geometric.data import InMemoryDataset
from torch_geometric.data import Data
from sklearn.preprocessing import LabelEncoder

import scanpy as sc
import muon as mu
from mudata import MuData

# read data
from ..preprocessing.read_adata import concat_data
# preprocess utils
from ..preprocessing._utils import get_centroids, summarize_clustering
# QC
from ..preprocessing._qc import cal_qc_rna
# pca
from ..preprocessing._pca import  select_pcs
# graph
from ..preprocessing._graph import construct_graph_rna, graph_clustering
# preprocessing
from ..preprocessing.preprocess import preprocessing
# model_pre utils
from ._utils import Transfer_scData


class UserDataset(InMemoryDataset):
    def __init__(self, root, project_name, adata_list, profile, projection=False, data_type=None, sub_data_type=None,
                 weight=None, graph_const_method=None, genome=None, sample_col='batch', filter_cells_rna=False, min_features=100, min_cells=3,
                 keep_mt=False, use_top_pcs=False, use_gene_weigt=True, normalize=True, target_sum=1e4, used_hvg=True,
                 used_scale=True, single_n_top_genes=2000, rna_n_top_features=3000, atac_n_top_features=10000,
                 metacell_size=2, n_pcs=20, n_neighbors=15, metacell=True, metric='correlation',
                 method='umap', svd_solver='arpack', resolution_tol=0.1, leiden_runs=1,
                 leiden_seed=None, verbose=True):
        """
        UserDataset class for managing and processing single-cell or multi-modal datasets.

        Parameters:
        -----------
        root : str
            The directory where the graph dataset should be stored.
        project_name : str
            Name of the project for the dataset.
        adata_list : list
            List of AnnData objects representing different batches of data.
        profile : str
            Type of data profile, e.g., 'RNA', 'ATAC', 'multi-modal'.
        projection : bool
            Use for new dataset projection. Input the folder containing the pre-trained model. If False, don't do projection. Default: False.
        data_type : str, optional
            Type of multi-modal data, e.g., 'Paired', 'UnPaired'. Default is None.
        genome : str, optional
            Genome reference name, e.g., 'hg19', 'hg38', 'mm9', 'mm10'. Default is None, but if data_type is set as 'UnPaired', genome must be set.
        sample_col : str, optional
            Column name that defines different samples. Default is 'batch'.
        filter_cells_rna : bool, optional
            Whether to filter cells based on RNA expression. Default is False.
        min_features : int, optional
            Minimum number of features required for a cell. Default is 100.
        min_cells : int, optional
            Minimum number of cells required for a feature. Default is 3.
        keep_mt : bool, optional
            Whether to keep mitochondrial genes. Default is False.
        use_top_pcs : bool, optional
            Whether to use top principal components (PCs). Default is True.
        use_gene_weigt : bool, optional
            Whether to use gene weighting. Default is True.
        normalize : bool, optional
            Whether to normalize the data. Default is True.
        target_sum : float, optional
            Target sum for total count normalization. Default is 1e4.
        used_hvg : bool, optional
            Whether to use highly variable genes. Default is True.
        used_scale : bool, optional
            Whether to scale the data. Default is True.
        single_n_top_genes : int, optional
            Number of top genes to select for single-sample analysis. Default is 2000.
        rna_n_top_features : int, optional
            Number of top features to select for RNA profile. Default is 3000.
        atac_n_top_features : int, optional
            Number of top features to select for ATAC profile. Default is 10000.
        metacell_size : int, optional
            Size of metacell clusters, which will determine the number of metacell clusters. Default is 2.
        n_pcs : int, optional
            Number of principal components to use for each sample processing. Default is 20.
        n_neighbors : int, optional
            Number of neighbors for graph construction. Default is 15.
        metacell : bool, optional
            Whether to construct metacells. Default is True.
        metric : str, optional
            Distance metric for nearest neighbor search. Default is 'correlation'.
        method : str, optional
            Dimensionality reduction method. Default is 'umap'.
        svd_solver : str, optional
            SVD solver to use for PCA. Default is 'arpack'.
        resolution_tol : float, optional
            Tolerance level for resolution clustering. Default is 0.1.
        leiden_runs : int, optional
            Number of times to run Leiden clustering. Default is 1.
        leiden_seed : int or None, optional
            Seed for the Leiden algorithm. Default is None.
        verbose : bool, optional
            Whether to print progress information. Default is True.
        """

        self.name = project_name
        self.data_list = adata_list
        self.profile = profile
        self.projection = projection
        self.data_type = data_type
        self.sub_data_type = sub_data_type
        self.weight = weight
        self.graph_const_method = graph_const_method
        self.genome = genome
        self.use_gene_weigt = use_gene_weigt
        self.use_top_pcs = use_top_pcs
        self.sample_col = sample_col
        self.filter_cells_rna = filter_cells_rna
        self.min_features = min_features
        self.min_cells = min_cells
        self.keep_mt = keep_mt
        self.normalize = normalize
        self.target_sum = target_sum
        self.used_hvg = used_hvg
        self.used_scale = used_scale
        self.single_n_top_genes = single_n_top_genes
        self.rna_n_top_features = rna_n_top_features
        self.atac_n_top_features = atac_n_top_features
        self.metacell_size = metacell_size
        self.metacell = metacell
        self.n_pcs = n_pcs
        self.n_neighbors = n_neighbors
        self.metric = metric
        self.method = method
        self.svd_solver = svd_solver
        self.resolution_tol = resolution_tol
        self.leiden_runs = leiden_runs
        self.leiden_seed = leiden_seed
        self.verbose = verbose

        super(UserDataset, self).__init__(root)
        try:
            print("Data files exist, loading...")
            self.data = torch.load(self.processed_paths[0])
            ## 加载single-cell or metacell的merged_adata对象
            path = osp.join(self.processed_dir, f'{self.name}_merged_adata.pt')
            self.merged_adata = torch.load(path)
            print("Finished loading.")
        except FileNotFoundError:
            print("Data files do not exist, generating...")
            self.process()
            self.data = torch.load(self.processed_paths[0])
            ## 加载single-cell or metacell的merged_adata对象
            path = osp.join(self.processed_dir, f'{self.name}_merged_adata.pt')
            self.merged_adata = torch.load(path)
            print("Finished generating.")

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, self.name + '_processed')

    # 检查self.processed_dir目录下是否存在self.processed_file_names属性方法返回的所有文件，没有就会走process
    @property
    def processed_file_names(self):
        return ['User_single_cell.dataset']

    def process_sample(self, adata):
        # 创建一个包含子对象的列表
        sub_adata_list = []

        # 样本划分：假设每个样本的样本名称存储在adata.obs['sample_name']中
        sample_names = np.unique(adata.obs[self.sample_col])

        for sample_name in sample_names:
            # 选择属于当前样本的观测
            sub_adata = adata[adata.obs[self.sample_col] == sample_name].copy()

            # Filter genes for RNA dataset...
            sc.pp.filter_genes(sub_adata, min_cells=self.min_cells)

            # Perform QC for RNA dataset...
            cal_qc_rna(sub_adata, expr_cutoff=1)

            # Filter out cells if needed:
            if self.filter_cells_rna:
                sc.pp.filter_cells(sub_adata, min_genes=self.min_features)

            # normalization
            if self.normalize:
                # 校正测序深度
                sc.pp.normalize_total(sub_adata, target_sum=self.target_sum)
                # 表达值log转化
                sc.pp.log1p(sub_adata)
                # 备份完整矩阵
                sub_adata.raw = sub_adata

            # Optionally, variable gene selection step can be also performed.
            if self.used_hvg:
                sc.pp.highly_variable_genes(sub_adata, n_top_genes=self.single_n_top_genes)

            if self.used_scale:
                # scale data, clip values exceeding standard deviation 10.
                sc.pp.scale(sub_adata, max_value=10)

            # 将子对象添加到列表中
            sub_adata_list.append(sub_adata)

        return sub_adata_list

    def _construct_graphs(self, sub_adata_list=None, metacell_labels=None, used_hvg=True,
                          n_top_genes=2000, n_pcs=20, n_neighbors=15, metacell=False,
                          randomized_svd=False, svd_runs=1, metric='correlation',
                          svd_solver='arpack', verbose=True):
        """
        Construct neighborhood graphs for all batches of the target array.
        """
        # 创建一个包含metacell子对象的列表
        if metacell_labels is not None:
            self._metacell_labels1 = metacell_labels
        self.meta_adata_sub_list = []
        meta_adata_sub_list = self.meta_adata_sub_list
        self._edges1 = []
        edges = self._edges1

        for b, sub_adata in enumerate(sub_adata_list):
            if verbose:
                print('Constructing neighborhood graphs for cells in sample{}...'.format(b), flush=True)

            ## meta cell 构建，在单细胞的图结构的基础上
            if metacell_labels is not None and metacell:
                meta_adata_sub = get_centroids(sub_data=sub_adata,
                                               labels=self._metacell_labels1[b])

                ## 将counts矩阵赋值给adata.X,方便重新标准化
                if meta_adata_sub.layers['counts'] is not None:
                    meta_adata_sub.X = meta_adata_sub.layers['counts'].copy()

                # 将子对象添加到列表中
                meta_adata_sub_list.append(meta_adata_sub)
            else:
                ## 单细胞构图
                # 数据PCA降维，为构建图准备数据
                if used_hvg:
                    sc.tl.pca(sub_adata, svd_solver=svd_solver, use_highly_variable=used_hvg)

                # 自动确定 pc 的数目
                print('Auto-query the number of PCs for single-cell-graph construction of sample{}...'.format(b),
                      flush=True)
                if n_pcs is not None:
                    select_pcs(sub_adata, n_pcs=n_pcs)
                else:
                    select_pcs(sub_adata, n_pcs=None)
                n_pcs = sub_adata.uns['pca']['n_pcs']
                print('The best n_pcs is {}'.format(n_pcs), flush=True)

                edges.append(
                    construct_graph_rna(
                        adata=sub_adata,
                        n_pcs=n_pcs,
                        n_neighbors=n_neighbors,
                        metric=metric,
                        verbose=False
                    )
                )

        if verbose:
            print('Graph construction finished!', flush=True)
        return meta_adata_sub_list, edges

    def _cluster_graphs(self, sub_adata_list=None, metacell_labels=None, used_hvg=True,
                        n_top_genes=2000, n_pcs=20, n_neighbors=15, metacell_size=2,
                        metacell=False, randomized_svd=False, svd_runs=1, metric='correlation',
                        resolution_tol=0.1, leiden_runs=1, leiden_seed=None, svd_solver='arpack',
                        verbose=True):
        """
        Cluster the neighborhood graphs.
        """
        if not metacell:
            ## single cell clustering
            _, edges = self._construct_graphs(
                sub_adata_list=sub_adata_list, metacell_labels=metacell_labels,
                n_top_genes=n_top_genes, used_hvg=used_hvg,
                n_pcs=n_pcs, n_neighbors=n_neighbors,
                metacell=metacell, randomized_svd=randomized_svd, svd_runs=svd_runs,
                metric=metric, svd_solver=svd_solver, verbose=verbose
            )  ## 需要执行两次，第一次执行单细胞合并时，adata_sub_list是空的，

            self.metacell_size = metacell_size
            if self.metacell_size > 1:
                if verbose:
                    print(
                        'Aggregating cells into metacells of average size {}...'.format(self.metacell_size),
                        flush=True
                    )
                print('Single-Cell Merging...', flush=True)
                self._metacell_labels1 = []
                metacell_labels = self._metacell_labels1
                for b, curr_edges in enumerate(edges):
                    if verbose:
                        print('Now at sample {}...'.format(b), flush=True)
                    n = len(sub_adata_list[b])
                    metacell_labels.append(
                        graph_clustering(
                            n=n,
                            edges=curr_edges,
                            n_clusters=int(n // self.metacell_size),
                            resolution=None,
                            n_runs=leiden_runs,
                            resolution_tol=resolution_tol,
                            seed=leiden_seed,
                            verbose=False
                        )
                    )
                if verbose:
                    print('Single-cell merging finished!', flush=True)
                return metacell_labels
        else:
            if verbose:
                print(
                    'Constructing meta-cells scRNA object',
                    flush=True
                )
            meta_adata_sub_list, _ = self._construct_graphs(
                sub_adata_list=sub_adata_list, metacell_labels=metacell_labels,
                n_top_genes=n_top_genes, used_hvg=used_hvg,
                n_pcs=n_pcs, n_neighbors=n_neighbors,
                metacell=metacell, randomized_svd=randomized_svd, svd_runs=svd_runs,
                metric=metric, svd_solver=svd_solver, verbose=verbose
            )  ## 第二次执行后，里面存了合并metacell的单细胞对象

            return meta_adata_sub_list  # , labels

    def construct_metacell(self, sub_adata_list, used_hvg=True, n_top_genes=2000, n_pcs=20,
                         n_neighbors=15, metacell_size=2, metacell=True, randomized_svd=False, svd_runs=1,
                         metric='correlation', resolution_tol=0.1, leiden_runs=1,
                         leiden_seed=None, svd_solver='arpack', verbose=True):
        """
        Construct neighborhood graphs and cluster them as needed.

        Parameters
        ----------
        n_neighbors: int, default=15
            Number of neighbors for graph construction for arr.
        randomized_svd: bool, default=False
            Whether to perform randomized SVD.
        svd_runs: int, default=1
            Perform multiple runs of SVD and select the one with lowest Frobenious reconstruction error is selected.
        resolution_tol: float, default=0.1
            Any resolution within the range of plus/minus resolution_tol will not be differentiated.
        leiden_runs: int, default=1
            Perform multiple runs of Leiden algorithm and the one with highest modularity is selected.
        metric: string, default='correlation'
            The metric to use in nearest neighbor search.
        leiden_seed: None or int, default=None
            Random seed for Leiden algorithm. If leiden_runs>1, leiden_seed will be reset to None.
        verbose: bool, default=True
            Whether to print the progress.

        Returns
        -------
        None
        """
        self.metacell_size = metacell_size
        if self.metacell_size > 1:
            # single cell clustering
            # need to construct the graph + metacell merging
            metacell_labels = self._cluster_graphs(sub_adata_list=sub_adata_list, metacell_labels=None,
                                                   n_top_genes=n_top_genes, used_hvg=used_hvg,
                                                   n_pcs=n_pcs, n_neighbors=n_neighbors,
                                                   metacell_size=metacell_size,
                                                   metacell=False, randomized_svd=randomized_svd,
                                                   svd_runs=svd_runs, metric=metric,
                                                   resolution_tol=resolution_tol,
                                                   leiden_runs=leiden_runs, leiden_seed=leiden_seed,
                                                   svd_solver=svd_solver, verbose=verbose
                                                   )
            # meta cell scRNA constrution
            meta_adata_sub_list = self._cluster_graphs(
                sub_adata_list=sub_adata_list, metacell_labels=metacell_labels, used_hvg=used_hvg,
                n_top_genes=n_top_genes, n_pcs=n_pcs, n_neighbors=n_neighbors,
                metacell_size=metacell_size, metacell=metacell, randomized_svd=randomized_svd,
                svd_runs=svd_runs, metric=metric, resolution_tol=resolution_tol,
                leiden_runs=leiden_runs, leiden_seed=leiden_seed, svd_solver=svd_solver,
                verbose=verbose
            )

        return meta_adata_sub_list

    def process(self):
        # load data
        adata = concat_data(
            self.data_list,
            batch_categories=None,
            join='inner',
            batch_key=self.sample_col, # 'batch'
            index_unique=None,
            save=None
        )
        if isinstance(adata, sc.AnnData):
            if adata.X.max() < 50:
                print('Warning: adata.X may have already been normalized, adata.X must be `counts`, please check.')
            else:
                adata.layers['counts'] = adata.X.copy()
        elif isinstance(adata, mu.MuData):
            if adata.mod['rna'].X.max() < 50:
                print('Warning: adata.X may have already been normalized, adata.X must be `counts`, please check.')
            else:
                adata.mod['rna'].layers['counts'] = adata.mod['rna'].X.copy()

        # RNA ATAC ADT
        if self.profile in ['RNA', 'ATAC', 'ADT']:
            rna_adata = adata.copy()
            del adata

            if self.metacell and self.metacell_size > 1:
                # 根据样本为单位进行预处理
                sub_adata_list = self.process_sample(rna_adata)
                # 进行图构建+聚类，返回每个metacell的单细胞对象
                # 注意如果used_hvg为True，则只用高变异基因构建图
                metacell_adata_list = self.construct_metacell(
                    sub_adata_list, used_hvg=self.used_hvg, n_top_genes=self.single_n_top_genes, n_pcs=self.n_pcs,
                    n_neighbors=self.n_neighbors, metacell_size=self.metacell_size, metacell=self.metacell,
                    metric=self.metric, resolution_tol=self.resolution_tol, leiden_runs=self.leiden_runs,
                    leiden_seed=self.leiden_seed, svd_solver=self.svd_solver, verbose=self.verbose
                )
                rna_adata = metacell_adata_list[0].concatenate(metacell_adata_list[1:], join='inner')  ## X 的 数据是counts
            else:
                rna_adata = rna_adata.copy()

            ## 预处理
            _, rna_adata_hvg = preprocessing(
                rna_adata,
                profile=self.profile,
                data_type=self.data_type,
                genome=self.genome,
                use_gene_weigt=self.use_gene_weigt,
                use_top_pcs=self.use_top_pcs,
                min_features=self.min_features,
                min_cells=self.min_cells,
                target_sum=self.target_sum,
                rna_n_top_features=self.rna_n_top_features,
                atac_n_top_features=self.atac_n_top_features,
                n=self.n_neighbors,
                batch_key=self.sample_col,
                metric=self.metric,
                svd_solver=self.svd_solver,
                keep_mt=self.keep_mt
            )

            # 保存rna_adata结果，用于模型输入
            path = osp.join(self.processed_dir, f'{self.name}_merged_adata.pt')
            torch.save(rna_adata_hvg, path, pickle_protocol=4)

            # 构建 pytorch_geometric 的数据结构
            data = Transfer_scData(rna_adata_hvg, self.sample_col)

        ### Paired multi-modal
        elif self.profile == 'multi-modal':
            if len(self.sub_data_type) == 2:
                if self.sub_data_type[0] == 'rna':
                    rna_adata = adata.mod['rna'].copy()
                elif self.sub_data_type[1] == 'atac':
                    atac_adata = adata.mod['atac'].copy()
                elif self.sub_data_type[1] == 'adt':
                    adt_adata = adata.mod['adt'].copy()
            else:
                ValueError('The length of sub_data_type must be 2, such as: ["rna", "atac"] or ["rna", "adt"].')
            del adata

            if self.metacell and self.metacell_size > 1:
                ## 根据样本为单位进行预处理
                sub_adata_list = self.process_sample(rna_adata)
                ## 进行图构建+聚类，返回每个metacell的单细胞对象
                ## 注意如果used_hvg为True，则只用高变异基因构建图
                metacell_adata_list = self.construct_metacell(
                    sub_adata_list, used_hvg=self.used_hvg, n_top_genes=self.single_n_top_genes, n_pcs=self.n_pcs,
                    n_neighbors=self.n_neighbors, metacell_size=self.metacell_size, metacell=self.metacell,
                    metric=self.metric, resolution_tol=self.resolution_tol, leiden_runs=self.leiden_runs,
                    leiden_seed=self.leiden_seed, svd_solver=self.svd_solver, verbose=self.verbose
                )
                rna_adata = metacell_adata_list[0].concatenate(metacell_adata_list[1:], join='inner')  ## X 的 数据是counts
            else:
                rna_adata = rna_adata.copy()

            if atac_adata is not None:
                mdata = MuData({"rna": rna_adata, "atac": atac_adata})
            elif adt_adata is not None:
                mdata = MuData({"rna": rna_adata, "adt": adt_adata})

            ## 预处理
            merged_adata = preprocessing(
                mdata,
                profile=self.profile,
                data_type=self.data_type,
                sub_data_type=self.sub_data_type,
                genome=self.genome,
                weight=self.weight,
                use_gene_weigt=self.use_gene_weigt,
                use_top_pcs=self.use_top_pcs,
                min_features=self.min_features,
                min_cells=self.min_cells,
                target_sum=self.target_sum,
                rna_n_top_features=self.rna_n_top_features,
                atac_n_top_features=self.atac_n_top_features,
                n=self.n_neighbors,
                batch_key=self.sample_col,
                metric=self.metric,
                svd_solver=self.svd_solver,
                keep_mt=self.keep_mt
            )

            ## 保存merged_adata结果，用于模型输入
            path = osp.join(self.processed_dir, f'{self.name}_merged_adata.pt')
            torch.save(merged_adata, path, pickle_protocol=4)

            ## 构建 pytorch_geometric 的数据结构
            data = Transfer_scData(merged_adata, self.sample_col, self.data_type)

        ### spatial single- or multi-modal
        elif self.profile == 'spatial':
            ## 预处理
            merged_adata = preprocessing(
                adata,
                profile=self.profile,
                data_type=self.data_type,
                sub_data_type=self.sub_data_type,
                genome=self.genome,
                weight=self.weight,
                graph_const_method=self.graph_const_method,
                use_gene_weigt=self.use_gene_weigt,
                use_top_pcs=self.use_top_pcs,
                min_features=self.min_features,
                min_cells=self.min_cells,
                target_sum=self.target_sum,
                rna_n_top_features=self.rna_n_top_features,
                atac_n_top_features=self.atac_n_top_features,
                n=self.n_neighbors,
                batch_key=self.sample_col,
                metric=self.metric,
                svd_solver=self.svd_solver,
                keep_mt=self.keep_mt
            )
            ## 保存merged_adata结果，用于模型输入
            path = osp.join(self.processed_dir, f'{self.name}_merged_adata.pt')
            torch.save(merged_adata, path, pickle_protocol=4)

            ## 构建 pytorch_geometric 的数据结构
            data = Transfer_scData(merged_adata, self.sample_col, self.data_type)

        else:
            return "Unknown input data type."

        print('Data preprocessing and graph construction finished')
        torch.save(data, self.processed_paths[0])

    def __repr__(self) -> str:
        return f'{self.name}({len(self)})'