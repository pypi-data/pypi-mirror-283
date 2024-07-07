"""
Functions for graph construction
"""
import numpy as np
import warnings
import scanpy as sc
import scipy.sparse as sp
import igraph as ig
import leidenalg
import pynndescent

from . import _utils as utils

def construct_graph_rna(
        adata, n_neighbors=15, n_pcs=None, metric='correlation', verbose=False
):
    """
    Compute k-nearest neighbors of data and return the UMAP graph.

    Parameters
    ----------
    adata: adata type of scanpy (n_samples, n_features)
        adata Data 
    n_neighbors: int
        Number of neighbors desired
    n_pcs: int
        Number PCs of executing graph construction
    metric: string, default='correlation'
        Metric used when constructing the initial knn graph
    verbose: bool, default=True
        Whether to print progress

    Returns
    -------
    rows, cols, vals: list
        Each edge is rows[i], cols[i], and its weight is vals[i]
    """

    if verbose:
        print("Constructing the graph...", flush=True)
    
    if sp.issparse(adata.X):
        adata.X = adata.X.toarray()
        
    # use scanpy functions to do the graph construction
    sc.pp.neighbors(adata, n_neighbors=n_neighbors, n_pcs=n_pcs, metric=metric)
    rows, cols = adata.obsp['connectivities'].nonzero()
    vals = adata.obsp['connectivities'][(rows, cols)].A1
    if verbose:
        print("Done!", flush=True)
    return rows, cols, vals

def leiden_clustering(n, edges, resolution=1, n_runs=1, seed=None, verbose=False):
    """
    Apply Leiden modularity maximization algorithm on the graph defined by edges and weights

    Parameters
    ----------
    n: int
        Number of edges in total
    edges: list of length two or three
        If length is two, then the graph is unweighted and each edge is (edges[0][i], edges[1][i]),
        if the length is three, then the graph is weighted and the weight of (edges[0][i], edges[1][i]) is edges[2][i].
    resolution: float, default=1
        Resolution parameter in Leiden algorithm
    n_runs: int, default=1
        Number of runs of Leiden algorithm, the run with the best modularity is taken as the output
    seed: None or int, default=None
        Random seed used. If None, use a random integer. If n_runs > 1, then seed will be reset to None.
    verbose: bool, default=True
        Whether to print progress

    Returns
    -------
    labels: np.array of shape (n,)
        Cluster labels
    """
    g = ig.Graph(directed=True)
    g.add_vertices(n)
    g.add_edges(list(zip(edges[0], edges[1])))
    if len(edges) > 2:
        g.es['weight'] = tuple(edges[2])

    if n_runs > 1 and seed is not None:
        seed = None
        warnings.warn('n_runs > 1, seed is reset to None.')

    partition_kwargs = {'n_iterations': -1, 'seed': seed,
                        'resolution_parameter': resolution}
    if len(edges) > 2:
        partition_kwargs['weights'] = np.array(g.es['weight']).astype(np.float64)

    partition_type = leidenalg.RBConfigurationVertexPartition

    best_modularity = float('-inf')
    best_labels = None
    if verbose and n_runs > 1:
        print('Running Leiden algorithm for {} times...'.format(n_runs), flush=True)
    for _ in range(n_runs):
        curr_part = leidenalg.find_partition(
            graph=g, partition_type=partition_type,
            **partition_kwargs
        )
        curr_modularity = curr_part.modularity
        if curr_modularity > best_modularity:
            best_modularity, best_labels = curr_modularity, np.array(curr_part.membership)

    assert best_labels is not None

    if verbose:
        if n_runs > 1:
            print('Best modularity among {} runs is {}.'.format(n_runs, best_modularity), flush=True)
        else:
            print('Modularity is {}.'.format(best_modularity), flush=True)
        print('The label has {} distinct clusters.'.format(len(np.unique(best_labels))), flush=True)

    return best_labels

def graph_clustering(
        n, edges, resolution=1, n_clusters=None, n_runs=1, resolution_tol=0.05, seed=None, verbose=False
):
    """
    Cluster the graph defined by edges and weights using Leiden algorithm.

    Parameters
    ----------
    n: int
        Number of edges in total
    edges: list of length two or three
        If length is two, then the graph is unweighted and each edge is (edges[0][i], edges[1][i]),
        if the length is three, then the graph is weighted and the weight of (edges[0][i], edges[1][i]) is edges[2][i].
    resolution: None or int, default=1
        If not None, then this is the resolution parameter in the clustering algorithm,
        if None, then n_clusters must be not None.
    n_clusters: None or int, default=None
        If not None, use binary search to select the resolution parameter to achieve the desired number of clusters,
        if None, then resolution must be not None.
    n_runs: int, default=1
        Number of runs of Leiden algorithm, the run with the best modularity is taken as the output.
    resolution_tol: float, default=0.05
        Any resolution within the range of plus/minus resolution_tol will not be differentiated.
    seed: None or int, default=None
        Random seed used. If None, use a random integer. If n_runs > 1, then seed will be reset to None.
    verbose: bool, default=True
        Whether to print progress

    Returns
    -------
    labels: np.array of shape (n,)
        Cluster labels
    """
    assert (resolution is not None) ^ (n_clusters is not None)

    def cluster_func(res, vb):
        return leiden_clustering(
            n=n, edges=edges, resolution=res, n_runs=n_runs, seed=seed, verbose=vb
        )

    if resolution is not None:
        return cluster_func(resolution, verbose)

    right = 1
    while True:
        curr_labels = cluster_func(right, False)
        curr_n_clusters = len(np.unique(curr_labels))
        if verbose:
            print('A resolution of {} gives {} clusters.'.format(right, curr_n_clusters), flush=True)
        if curr_n_clusters == n_clusters:
            return curr_labels
        elif curr_n_clusters < n_clusters:
            right *= 2
        else:
            break
    left = 0 if right == 1 else right / 2
    # desired resolution is in [left, right)
    while left + resolution_tol < right:
        mid = (left + right) / 2
        curr_labels = cluster_func(mid, False)
        curr_n_clusters = len(np.unique(curr_labels))
        if verbose:
            print('A resolution of {} gives {} clusters.'.format(mid, curr_n_clusters), flush=True)
        if curr_n_clusters == n_clusters:
            return curr_labels
        elif curr_n_clusters > n_clusters:
            right = mid
        else:
            left = mid
    return curr_labels


def get_nearest_neighbors(query_arr, target_arr, svd_components=None, randomized_svd=False, svd_runs=1,
                          metric='correlation'):
    """
    For each row in query_arr, compute its nearest neighbor in target_arr.

    Parameters
    ----------
    query_arr: np.array of shape (n_samples1, n_features)
        The query data matrix.
    target_arr: np.array of shape (n_samples2, n_features)
        The target data matrix.
    svd_components: None or int, default=None
        If not None, will first conduct SVD to reduce the dimension
        of the vertically stacked version of query_arr and target_arr.
    randomized_svd: bool, default=False
        Whether to use randomized SVD.
    svd_runs: int, default=1
        Run multiple instances of SVD and select the one with the lowest Frobenious reconstruction error.
    metric: string, default='correlation'
        The metric to use in nearest neighbor search.

    Returns
    -------
    neighbors: np.array of shape (n_samples1)
        The i-th element is the index in target_arr to whom the i-th row of query_arr is closest to.
    dists: np.array of shape (n_samples1)
        The i-th element is the distance corresponding to neighbors[i].
    """
    query_arr = utils.convert_to_numpy(query_arr)
    target_arr = utils.convert_to_numpy(target_arr)
    arr = np.vstack([query_arr, target_arr])
    arr = utils.svd_embedding(
        arr=arr, n_components=svd_components,
        randomized=randomized_svd,
        n_runs=svd_runs
    )
    query_arr = arr[:query_arr.shape[0], :]
    pivot_arr = arr[query_arr.shape[0]:, :]
    # approximate nearest neighbor search
    index = pynndescent.NNDescent(pivot_arr, n_neighbors=100, metric=metric)
    neighbors, dists = index.query(query_arr, k=50)
    neighbors, dists = neighbors[:, 0], dists[:, 0]
    return neighbors, dists
