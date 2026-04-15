"""
dataset.py
----------
Load 4 file đã processed từ data_final/ và chia 80/20 (train+val / test).

Cấu trúc file:
  final_labels.csv          : cột [Patient_ID, Cancer_Type, Clean_Subtype, Target_Label]
  final_gene.csv            : index=Patient_ID, columns=gene_names
  final_methylation.csv     : index=Patient_ID, columns=CpG_names
  final_mirna.csv       : index=Patient_ID, columns=miRNA_names
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset


# ─────────────────────────────────────────────
#  Load + split
# ─────────────────────────────────────────────
def build_datasets(cfg: dict, seed: int = 42):
    """
    Parameters
    ----------
    cfg  : config.yaml['data']
    seed : random seed

    Returns
    -------
    datasets      : dict {'train': OmicDataset, 'val': OmicDataset, 'test': OmicDataset}
    feature_names : dict {'gene': [...], 'meth': [...], 'mirna': [...]}
    dims          : dict {'gene': int, 'meth': int, 'mirna': int}
    """
    root = cfg["data_dir"]  # đường dẫn tới data_processed/

    print("📂 Loading data từ:", root)

    # ── Load 4 file ──────────────────────────────────────────────────
    labels = pd.read_csv(os.path.join(root, "final_labels.csv"))
    gene   = pd.read_csv(os.path.join(root, "final_gene.csv"),          index_col=0)
    meth   = pd.read_csv(os.path.join(root, "final_methylation.csv"),   index_col=0)
    mirna  = pd.read_csv(os.path.join(root, "final_mirna.csv"),         index_col=0)

    print(f"  Labels : {labels.shape}")
    print(f"  Gene   : {gene.shape}")
    print(f"  Meth   : {meth.shape}")
    print(f"  miRNA  : {mirna.shape}")

    # ── Align sample order theo labels ───────────────────────────────
    patient_ids = labels["Patient_ID"].values
    gene  = gene.loc[patient_ids]
    meth  = meth.loc[patient_ids]
    mirna = mirna.loc[patient_ids]

    X_gene  = gene.values.astype(np.float32)   # (N, F_gene)
    X_meth  = meth.values.astype(np.float32)   # (N, F_meth)
    X_mirna = mirna.values.astype(np.float32)  # (N, F_mirna)
    y       = labels["Target_Label"].values.astype(np.int64)  # (N,)

    N = len(y)
    print(f"\n  Tổng số samples : {N}")
    print(f"  Phân bố subtype : {dict(zip(*np.unique(y, return_counts=True)))}")

    # ── Split 80/20: (train+val) / test ──────────────────────────────
    # stratify đảm bảo mỗi split có đủ các subtypes
    idx = np.arange(N)
    idx_trainval, idx_test = train_test_split(
        idx, test_size=0.2, random_state=seed, stratify=y
    )
    # Chia tiếp train+val → 90% train / 10% val
    # (tức 72% train, 8% val, 20% test so với tổng)
    idx_train, idx_val = train_test_split(
        idx_trainval, test_size=0.1, random_state=seed, stratify=y[idx_trainval]
    )

    print(f"\n📊 Split: train={len(idx_train)}, val={len(idx_val)}, test={len(idx_test)}")

    # ── Feature names (dùng cho interpretability) ────────────────────
    feature_names = {
        "gene":  gene.columns.tolist(),
        "meth":  meth.columns.tolist(),
        "mirna": mirna.columns.tolist(),
    }

    # ── Tạo datasets ─────────────────────────────────────────────────
    def make_dataset(idx):
        return OmicDataset(
            gene  = X_gene[idx],
            meth  = X_meth[idx],
            mirna = X_mirna[idx],
            label = y[idx],
            feature_names = feature_names,
        )

    datasets = {
        "train": make_dataset(idx_train),
        "val":   make_dataset(idx_val),
        "test":  make_dataset(idx_test),
    }

    dims = {
        "gene":  X_gene.shape[1],
        "meth":  X_meth.shape[1],
        "mirna": X_mirna.shape[1],
    }

    return datasets, feature_names, dims


# ─────────────────────────────────────────────
#  PyTorch Dataset
# ─────────────────────────────────────────────
class OmicDataset(Dataset):
    def __init__(
        self,
        gene:  np.ndarray,   # (N, F_gene)
        meth:  np.ndarray,   # (N, F_meth)
        mirna: np.ndarray,   # (N, F_mirna)
        label: np.ndarray,   # (N,)
        feature_names: dict,
    ):
        self.gene  = torch.from_numpy(gene)
        self.meth  = torch.from_numpy(meth)
        self.mirna = torch.from_numpy(mirna)
        self.label = torch.from_numpy(label)
        self.feature_names = feature_names

    def __len__(self):
        return len(self.label)

    def __getitem__(self, idx):
        return {
            "gene":  self.gene[idx],
            "meth":  self.meth[idx],
            "mirna": self.mirna[idx],
            "label": self.label[idx],
        }
