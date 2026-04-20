"""
dataset.py
----------
Load, split, preprocess, and package multi-omics data for GIAC.

Key guarantees:
  - Split first, normalize later.
  - Feature selection is fitted only on the training subset.
  - The same preprocessing metadata can be reused for evaluation/checkpoints.
"""

import os
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_selection import f_classif
from sklearn.model_selection import StratifiedKFold, train_test_split
import torch
from torch.utils.data import Dataset


DEFAULT_PREPROCESS_CFG = {
    "gene_top_k": 3000,
    "meth_top_k": 3000,
    "mirna_top_k": 1881,
    "feature_selection_method": "variance",
    "val_size": 0.1,
    "cv_folds": 5,
}


def build_datasets(cfg: dict, seed: int = 42):
    """Build a single train/val/test split using train-fitted preprocessing."""
    raw = load_aligned_data(cfg)
    split_cfg = _get_preprocess_cfg(cfg)

    idx_train, idx_val, idx_test = _make_single_split(
        raw["labels"], seed=seed, val_size=split_cfg["val_size"]
    )
    print(f"\n📊 Split: train={len(idx_train)}, val={len(idx_val)}, test={len(idx_test)}")

    return _package_split(raw, idx_train, idx_val, idx_test, split_cfg)


def build_cv_datasets(cfg: dict, seed: int = 42, n_splits: int | None = None):
    """Build stratified CV folds. Each fold still keeps an inner validation split."""
    raw = load_aligned_data(cfg)
    split_cfg = _get_preprocess_cfg(cfg)
    n_splits = n_splits or split_cfg["cv_folds"]

    splitter = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    folds = []

    for fold_idx, (idx_trainval, idx_test) in enumerate(
        splitter.split(np.zeros(len(raw["labels"])), raw["labels"]), start=1
    ):
        idx_train, idx_val = train_test_split(
            idx_trainval,
            test_size=split_cfg["val_size"],
            random_state=seed + fold_idx,
            stratify=raw["labels"][idx_trainval],
        )
        folds.append(
            {
                "fold": fold_idx,
                "datasets": _package_split(raw, idx_train, idx_val, idx_test, split_cfg),
            }
        )

    return folds


def load_aligned_data(cfg: dict) -> dict:
    """Load aligned raw arrays once. No preprocessing is applied here."""
    root = cfg["data_dir"]
    print("📂 Loading data từ:", root)

    labels = pd.read_csv(os.path.join(root, "final_labels.csv"), index_col=0)
    gene_path = _resolve_existing_path(
        root,
        ["final_gene_symbol.csv", "final_gene.csv"],
        asset_name="gene matrix",
    )
    gene = pd.read_csv(gene_path, index_col=0)
    meth = pd.read_csv(os.path.join(root, "final_methylation.csv"), index_col=0)
    mirna = pd.read_csv(os.path.join(root, "final_mirna.csv"), index_col=0)

    print(f"  Labels : {labels.shape}")
    print(f"  Gene   : {gene.shape}")
    print(f"  Meth   : {meth.shape}")
    print(f"  miRNA  : {mirna.shape}")

    common_ids = (
        labels.index.intersection(gene.index).intersection(meth.index).intersection(mirna.index)
    )
    print(f"\n  Samples sau align : {len(common_ids)}")

    labels = labels.loc[common_ids]
    gene = gene.loc[common_ids]
    meth = meth.loc[common_ids]
    mirna = mirna.loc[common_ids]

    y = labels["Target_Label"].values.astype(np.int64)
    print(f"  Phân bố subtype   : {dict(zip(*np.unique(y, return_counts=True)))}")

    return {
        "patient_ids": common_ids.to_numpy(),
        "labels": y,
        "gene": gene.values.astype(np.float32),
        "meth": meth.values.astype(np.float32),
        "mirna": mirna.values.astype(np.float32),
        "feature_names": {
            "gene": gene.columns.tolist(),
            "meth": meth.columns.tolist(),
            "mirna": mirna.columns.tolist(),
        },
    }


def _make_single_split(labels: np.ndarray, seed: int, val_size: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    idx = np.arange(len(labels))
    idx_trainval, idx_test = train_test_split(
        idx, test_size=0.2, random_state=seed, stratify=labels
    )
    idx_train, idx_val = train_test_split(
        idx_trainval,
        test_size=val_size,
        random_state=seed,
        stratify=labels[idx_trainval],
    )
    return idx_train, idx_val, idx_test


def _package_split(
    raw: dict,
    idx_train: np.ndarray,
    idx_val: np.ndarray,
    idx_test: np.ndarray,
    split_cfg: dict,
):
    preprocess = fit_preprocessor(raw, idx_train, split_cfg)
    X_gene = apply_preprocessor(raw["gene"], preprocess["gene"])
    X_meth = apply_preprocessor(raw["meth"], preprocess["meth"])
    X_mirna = apply_preprocessor(raw["mirna"], preprocess["mirna"])
    y = raw["labels"]

    feature_names = {
        "gene": select_feature_names(raw["feature_names"]["gene"], preprocess["gene"]["indices"]),
        "meth": select_feature_names(raw["feature_names"]["meth"], preprocess["meth"]["indices"]),
        "mirna": select_feature_names(raw["feature_names"]["mirna"], preprocess["mirna"]["indices"]),
    }

    def make_dataset(indices):
        return OmicDataset(
            gene=X_gene[indices],
            meth=X_meth[indices],
            mirna=X_mirna[indices],
            label=y[indices],
            feature_names=feature_names,
            patient_ids=raw["patient_ids"][indices],
        )

    datasets = {
        "train": make_dataset(idx_train),
        "val": make_dataset(idx_val),
        "test": make_dataset(idx_test),
    }
    dims = {
        "gene": X_gene.shape[1],
        "meth": X_meth.shape[1],
        "mirna": X_mirna.shape[1],
    }
    split_info = {"train": idx_train, "val": idx_val, "test": idx_test}
    metadata = {"preprocess": preprocess, "split_info": split_info, "feature_names": feature_names}
    return datasets, feature_names, dims, metadata


def fit_preprocessor(raw: dict, idx_train: np.ndarray, split_cfg: dict) -> dict:
    """Fit feature selection and normalization on the training subset only."""
    method = split_cfg.get("feature_selection_method", "variance")
    y_train = raw["labels"][idx_train]
    return {
        "gene": _fit_modality_preprocessor(
            raw["gene"], idx_train, y_train, split_cfg["gene_top_k"], method
        ),
        "meth": _fit_modality_preprocessor(
            raw["meth"], idx_train, y_train, split_cfg["meth_top_k"], method
        ),
        "mirna": _fit_modality_preprocessor(
            raw["mirna"], idx_train, y_train, split_cfg["mirna_top_k"], method
        ),
    }


def apply_preprocessor(X: np.ndarray, proc: dict) -> np.ndarray:
    """Select features, then standardize with train-fitted statistics."""
    selected = X[:, proc["indices"]]
    standardized = (selected - proc["mean"]) / proc["std"]
    return standardized.astype(np.float32, copy=False)


def select_feature_names(names: List[str], indices: np.ndarray) -> List[str]:
    return [names[i] for i in indices.tolist()]


def _fit_modality_preprocessor(
    X: np.ndarray,
    idx_train: np.ndarray,
    y_train: np.ndarray,
    top_k: int | None,
    method: str,
) -> dict:
    train_slice = X[idx_train]
    selected_idx = _select_top_features(train_slice, y_train, top_k, method)
    train_selected = train_slice[:, selected_idx]

    mean = train_selected.mean(axis=0, dtype=np.float64)
    std = train_selected.std(axis=0, dtype=np.float64)
    std = np.where(std < 1e-8, 1.0, std)

    return {
        "indices": selected_idx.astype(np.int64, copy=False),
        "mean": mean.astype(np.float32, copy=False),
        "std": std.astype(np.float32, copy=False),
    }


def _select_top_variance_features(train_slice: np.ndarray, top_k: int | None) -> np.ndarray:
    n_features = train_slice.shape[1]
    if top_k is None or top_k <= 0 or top_k >= n_features:
        return np.arange(n_features, dtype=np.int64)

    variances = train_slice.var(axis=0, dtype=np.float64)
    top_idx = np.argpartition(variances, -top_k)[-top_k:]
    top_idx.sort()
    return top_idx.astype(np.int64, copy=False)


def _select_top_anova_features(
    train_slice: np.ndarray,
    y_train: np.ndarray,
    top_k: int | None,
) -> np.ndarray:
    n_features = train_slice.shape[1]
    if top_k is None or top_k <= 0 or top_k >= n_features:
        return np.arange(n_features, dtype=np.int64)

    f_scores, _ = f_classif(train_slice, y_train)
    f_scores = np.nan_to_num(f_scores, nan=0.0, posinf=0.0, neginf=0.0)
    top_idx = np.argpartition(f_scores, -top_k)[-top_k:]
    top_idx.sort()
    return top_idx.astype(np.int64, copy=False)


def _select_top_features(
    train_slice: np.ndarray,
    y_train: np.ndarray,
    top_k: int | None,
    method: str,
) -> np.ndarray:
    normalized = (method or "variance").lower()
    if normalized == "anova":
        return _select_top_anova_features(train_slice, y_train, top_k)
    return _select_top_variance_features(train_slice, top_k)


def _get_preprocess_cfg(cfg: dict) -> dict:
    preprocess_cfg = dict(DEFAULT_PREPROCESS_CFG)
    preprocess_cfg.update(cfg.get("preprocessing", {}))
    return preprocess_cfg


def _resolve_existing_path(root: str, candidates: List[str], asset_name: str) -> str:
    for name in candidates:
        path = os.path.join(root, name)
        if os.path.exists(path):
            return path
    tried = ", ".join(candidates)
    raise FileNotFoundError(
        f"Không tìm thấy {asset_name} trong {root}. Đã thử: {tried}"
    )


class OmicDataset(Dataset):
    def __init__(self, gene, meth, mirna, label, feature_names, patient_ids):
        self.gene = torch.from_numpy(gene)
        self.meth = torch.from_numpy(meth)
        self.mirna = torch.from_numpy(mirna)
        self.label = torch.from_numpy(label)
        self.feature_names = feature_names
        self.patient_ids = list(patient_ids)

    def __len__(self):
        return len(self.label)

    def __getitem__(self, idx):
        return {
            "gene": self.gene[idx],
            "meth": self.meth[idx],
            "mirna": self.mirna[idx],
            "label": self.label[idx],
        }
