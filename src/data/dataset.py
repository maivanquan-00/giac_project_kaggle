"""
dataset.py
----------
Load, split, preprocess, and package multi-omics data for GIAC.

Key guarantees:
  - Split first, normalize later.
  - Feature selection is fitted only on the training subset.
  - The same preprocessing metadata can be reused for evaluation/checkpoints.

Phase 20 changes:
  - ANOVA (f_classif) replaces variance for feature selection — supervised,
    respects class labels, captures signal missed by pure variance.
  - Stratified minority boost: extra features are selected specifically for
    GS-vs-rest and HM-SNV-vs-rest, then merged into the main set.
    This counters ANOVA being dominated by CIN/MSI sample counts.
  - fit_preprocessor now receives labels so minority boost can be applied.
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
    "gene_top_k": 4000,
    "meth_top_k": 4000,
    "mirna_top_k": 1881,
    "val_size": 0.1,
    "cv_folds": 5,
    # Extra features selected for minority classes (GS=class1, HM-SNV=class3)
    # These are merged into the main top-k set (dedup'd), so final size may
    # be slightly larger than top_k.
    "minority_boost_gene": 300,
    "minority_boost_meth": 300,
    "minority_boost_mirna": 0,
    # Class indices of the minority classes to boost
    "minority_classes": [1, 3],  # GS=1, HM-SNV=3
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
    root = cfg.get("data", {}).get("data_dir", cfg.get("data_dir"))
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
    preprocess = fit_preprocessor(raw, idx_train, split_cfg, train_labels=raw["labels"][idx_train])
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


def fit_preprocessor(raw: dict, idx_train: np.ndarray, split_cfg: dict,
                     train_labels: np.ndarray | None = None) -> dict:
    """Fit feature selection and normalization on the training subset only.

    Uses ANOVA F-test (f_classif) for supervised feature selection.
    Applies minority-class stratified boost: additional features are selected
    specifically for GS-vs-rest and HM-SNV-vs-rest, then merged with the main
    top-k set to ensure minority-relevant features are not filtered out.
    """
    minority_classes = split_cfg.get("minority_classes", [1, 3])
    return {
        "gene": _fit_modality_preprocessor(
            raw["gene"], idx_train, split_cfg["gene_top_k"],
            train_labels=train_labels,
            minority_boost=split_cfg.get("minority_boost_gene", 0),
            minority_classes=minority_classes,
        ),
        "meth": _fit_modality_preprocessor(
            raw["meth"], idx_train, split_cfg["meth_top_k"],
            train_labels=train_labels,
            minority_boost=split_cfg.get("minority_boost_meth", 0),
            minority_classes=minority_classes,
        ),
        "mirna": _fit_modality_preprocessor(
            raw["mirna"], idx_train, split_cfg["mirna_top_k"],
            train_labels=train_labels,
            minority_boost=split_cfg.get("minority_boost_mirna", 0),
            minority_classes=minority_classes,
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
    top_k: int | None,
    train_labels: np.ndarray | None = None,
    minority_boost: int = 0,
    minority_classes: list | None = None,
) -> dict:
    """Select top-k features by ANOVA F-test, with optional minority-class boost.

    Minority boost:
      For each minority class c in minority_classes, run a binary ANOVA
      (class c vs rest). Select the top `minority_boost` features from that
      binary test and merge them into the main selected set (union, dedup).
      This ensures features with weak global F-score but strong GS/HM-SNV
      signal are not dropped by the dominated main ANOVA.
    """
    train_slice = X[idx_train]
    n_features = train_slice.shape[1]

    if top_k is None or top_k <= 0 or top_k >= n_features:
        selected_idx = np.arange(n_features, dtype=np.int64)
    else:
        # Primary ANOVA: all classes
        if train_labels is not None:
            f_scores, _ = f_classif(train_slice, train_labels)
            f_scores = np.nan_to_num(f_scores, nan=0.0, posinf=0.0)
            selected_idx = np.argpartition(f_scores, -top_k)[-top_k:]
        else:
            # Fallback to variance if no labels provided
            variances = train_slice.var(axis=0, dtype=np.float64)
            selected_idx = np.argpartition(variances, -top_k)[-top_k:]
        selected_idx = np.sort(selected_idx).astype(np.int64)

        # Minority-class stratified boost
        if (minority_boost > 0 and train_labels is not None
                and minority_classes is not None):
            extra_idx_list = []
            for cls in minority_classes:
                mask = (train_labels == cls).astype(np.float32)
                # Skip if too few positives for a meaningful test
                if mask.sum() < 3:
                    continue
                binary_labels = (train_labels == cls).astype(np.int64)
                f_bin, _ = f_classif(train_slice, binary_labels)
                f_bin = np.nan_to_num(f_bin, nan=0.0, posinf=0.0)
                boost_k = min(minority_boost, n_features)
                extra = np.argpartition(f_bin, -boost_k)[-boost_k:]
                extra_idx_list.append(extra)
            if extra_idx_list:
                all_extra = np.concatenate(extra_idx_list)
                selected_idx = np.sort(
                    np.unique(np.concatenate([selected_idx, all_extra]))
                ).astype(np.int64)

    train_selected = train_slice[:, selected_idx]
    mean = train_selected.mean(axis=0, dtype=np.float64)
    std = train_selected.std(axis=0, dtype=np.float64)
    std = np.where(std < 1e-8, 1.0, std)

    return {
        "indices": selected_idx,
        "mean": mean.astype(np.float32, copy=False),
        "std": std.astype(np.float32, copy=False),
    }


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