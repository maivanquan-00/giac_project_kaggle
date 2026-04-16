"""
dataset.py
----------
Load 4 file đã done từ data_final/ và chia 80/20 (train+val / test).

Cấu trúc file thực tế (Patient ID là index, không phải cột riêng):
  final_labels.csv:
      <index=TCGA-ID>  Cancer_Type  Clean_Subtype  Target_Label
  final_gene.csv / final_methylation.csv / final_mirna.csv:
      <index=TCGA-ID>  feature_1  feature_2  ...
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import torch
from torch.utils.data import Dataset


def build_datasets(cfg: dict, seed: int = 42):
    """
    Returns
    -------
    datasets      : dict {'train': OmicDataset, 'val': OmicDataset, 'test': OmicDataset}
    feature_names : dict {'gene': [...], 'meth': [...], 'mirna': [...]}
    dims          : dict {'gene': int, 'meth': int, 'mirna': int}
    """
    root = cfg["data_dir"]
    print("📂 Loading data từ:", root)

    # ── Load 4 file — Patient ID là index (cột đầu tiên) của tất cả file ──
    labels = pd.read_csv(os.path.join(root, "final_labels.csv"),            index_col=0)
    gene   = pd.read_csv(os.path.join(root, "final_gene_symbol.csv"),          index_col=0)
    meth   = pd.read_csv(os.path.join(root, "final_methylation.csv"),   index_col=0)
    mirna  = pd.read_csv(os.path.join(root, "final_mirna.csv"),         index_col=0)

    print(f"  Labels : {labels.shape}")
    print(f"  Gene   : {gene.shape}")
    print(f"  Meth   : {meth.shape}")
    print(f"  miRNA  : {mirna.shape}")

    # ── Align: chỉ giữ Patient ID có mặt trong cả 4 file ────────────
    common_ids = (labels.index
                        .intersection(gene.index)
                        .intersection(meth.index)
                        .intersection(mirna.index))
    print(f"\n  Samples sau align : {len(common_ids)}")

    labels = labels.loc[common_ids]
    gene   = gene.loc[common_ids]
    meth   = meth.loc[common_ids]
    mirna  = mirna.loc[common_ids]

    X_gene  = gene.values.astype(np.float32)   # (N, F_gene)
    X_meth  = meth.values.astype(np.float32)   # (N, F_meth)
    X_mirna = mirna.values.astype(np.float32)  # (N, F_mirna)

    # THÊM 3 DÒNG NÀY ĐỂ CHUẨN HÓA DỮ LIỆU (Đưa Mean về 0, Std về 1)
    X_gene = (X_gene - X_gene.mean(axis=0)) / (X_gene.std(axis=0) + 1e-8)
    X_meth = (X_meth - X_meth.mean(axis=0)) / (X_meth.std(axis=0) + 1e-8)
    X_mirna = (X_mirna - X_mirna.mean(axis=0)) / (X_mirna.std(axis=0) + 1e-8)
    
    y       = labels["Target_Label"].values.astype(np.int64)  # (N,)

    N = len(y)
    print(f"  Phân bố subtype   : {dict(zip(*np.unique(y, return_counts=True)))}")

    # ── Split 80/20: (train+val) / test — stratify theo subtype ─────
    idx = np.arange(N)
    idx_trainval, idx_test = train_test_split(
        idx, test_size=0.2, random_state=seed, stratify=y
    )
    # Chia tiếp 90/10 trong trainval → train / val
    idx_train, idx_val = train_test_split(
        idx_trainval, test_size=0.1, random_state=seed, stratify=y[idx_trainval]
    )
    print(f"\n📊 Split: train={len(idx_train)}, val={len(idx_val)}, test={len(idx_test)}")

    feature_names = {
        "gene":  gene.columns.tolist(),
        "meth":  meth.columns.tolist(),
        "mirna": mirna.columns.tolist(),
    }

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


class OmicDataset(Dataset):
    def __init__(self, gene, meth, mirna, label, feature_names):
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
