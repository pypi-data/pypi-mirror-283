"""Quality Control"""
import numpy as np
from scipy.sparse import (
    issparse,
    csr_matrix,
)
import re

def cal_qc_rna(adata, expr_cutoff=1):
    """Calculate quality control metrics.

    Parameters
    ----------
    adata: AnnData
        Annotated data matrix.
    expr_cutoff: `float`, optional (default: 1)
        Expression cutoff.
        If greater than expr_cutoff,the feature is considered 'expressed'
    assay: `str`, optional (default: 'rna')
            Choose from {'rna','atac'},case insensitive
    Returns
    -------
    updates `adata` with the following fields.
    n_counts: `pandas.Series` (`adata.var['n_counts']`,dtype `int`)
       The number of read count each gene has.
    n_cells: `pandas.Series` (`adata.var['n_cells']`,dtype `int`)
       The number of cells in which each gene is expressed.
    pct_cells: `pandas.Series` (`adata.var['pct_cells']`,dtype `float`)
       The percentage of cells in which each gene is expressed.
    n_counts: `pandas.Series` (`adata.obs['n_counts']`,dtype `int`)
       The number of read count each cell has.
    n_genes: `pandas.Series` (`adata.obs['n_genes']`,dtype `int`)
       The number of genes expressed in each cell.
    pct_genes: `pandas.Series` (`adata.obs['pct_genes']`,dtype `float`)
       The percentage of genes expressed in each cell.
    n_peaks: `pandas.Series` (`adata.obs['n_peaks']`,dtype `int`)
       The number of peaks expressed in each cell.
    pct_peaks: `pandas.Series` (`adata.obs['pct_peaks']`,dtype `int`)
       The percentage of peaks expressed in each cell.
    pct_mt: `pandas.Series` (`adata.obs['pct_mt']`,dtype `float`)
       the percentage of counts in mitochondrial genes
    """

    if(not issparse(adata.X)):
        adata.X = csr_matrix(adata.X)

    n_counts = adata.X.sum(axis=0).A1
    adata.var['n_counts'] = n_counts
    n_cells = (adata.X >= expr_cutoff).sum(axis=0).A1
    adata.var['n_cells'] = n_cells
    adata.var['pct_cells'] = n_cells/adata.shape[0]

    n_counts = adata.X.sum(axis=1).A1
    adata.obs['n_counts'] = n_counts
    n_features = (adata.X >= expr_cutoff).sum(axis=1).A1
    adata.obs['n_genes'] = n_features
    adata.obs['pct_genes'] = n_features/adata.shape[1]
    r = re.compile("^MT-", flags=re.IGNORECASE)
    mt_genes = list(filter(r.match, adata.var_names))
    if(len(mt_genes) > 0):
        n_counts_mt = adata[:, mt_genes].X.sum(axis=1).A1
        adata.obs['pct_mt'] = n_counts_mt/n_counts
    else:
        adata.obs['pct_mt'] = 0
