"""
utils.py
--------
Các hàm tiện ích: metrics, logging, seed, checkpoint.
"""

import os
import random
import numpy as np
import torch
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, classification_report


def set_seed(seed: int):
    """Đặt seed cho reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark     = False


def compute_metrics(y_true, y_pred) -> dict:
    """Tính accuracy, precision, recall, f1 (macro + weighted).

    Primary metric = macro F1 (key 'f1') — conservative cho imbalanced multi-class.
    Secondary = weighted F1 (key 'f1_weighted') — báo song song để đối chiếu với
    MoXGATE paper (paper dùng weighted F1, đã confirm bằng reproduction 2026-05-07).
    """
    return {
        "accuracy":     accuracy_score(y_true, y_pred),
        "precision":    precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall":       recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1":           f1_score(y_true, y_pred, average="macro", zero_division=0),
        "f1_weighted":  f1_score(y_true, y_pred, average="weighted", zero_division=0),
    }


def compute_per_cancer_type_f1(labels, preds, cancer_types) -> dict:
    """Macro F1 breakdown per cancer type.

    Returns dict: {cancer_type_str: {"f1": float, "n": int}}
    Only meaningful for multi-cancer datasets (GI). For single-cancer
    datasets, returns a single-key dict.
    """
    labels = np.asarray(labels)
    preds = np.asarray(preds)
    cancer_types = np.asarray(cancer_types)
    unique_cts = sorted(set(cancer_types.tolist()))
    return {
        ct: {
            "f1": f1_score(labels[cancer_types == ct], preds[cancer_types == ct],
                           average="macro", zero_division=0),
            "n": int((cancer_types == ct).sum()),
        }
        for ct in unique_cts
    }


def print_metrics(metrics: dict, split: str = ""):
    prefix = f"[{split}] " if split else ""
    f1w = metrics.get("f1_weighted")
    f1w_str = f"  F1w={f1w:.4f}" if f1w is not None else ""
    print(
        f"{prefix}Acc={metrics['accuracy']:.4f}  "
        f"P={metrics['precision']:.4f}  "
        f"R={metrics['recall']:.4f}  "
        f"F1={metrics['f1']:.4f}{f1w_str}"
    )


def print_classification_report(y_true, y_pred, class_names=None):
    """In classification report chi tiết per-class P/R/F1."""
    print(classification_report(
        y_true, y_pred,
        target_names=class_names,
        zero_division=0,
        digits=4,
    ))


def save_confusion_matrix_csv(y_true, y_pred, path, class_names=None):
    """Lưu confusion matrix dạng số tuyệt đối ra CSV."""
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n_classes = max(int(y_true.max()), int(y_pred.max())) + 1
    if class_names is None:
        class_names = [f"Class_{i}" for i in range(n_classes)]
    cm = confusion_matrix(y_true, y_pred, labels=np.arange(n_classes))
    df = pd.DataFrame(
        cm,
        index=[f"True_{n}" for n in class_names],
        columns=[f"Pred_{n}" for n in class_names],
    )
    ensure_dir(os.path.dirname(path))
    df.to_csv(path)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def plot_split_class_distribution(split_to_labels: dict, path: str, title: str, class_names=None):
    ensure_dir(os.path.dirname(path))
    split_names = list(split_to_labels.keys())
    n_classes = max(int(np.max(labels)) for labels in split_to_labels.values()) + 1
    if class_names is None:
        class_names = [f"Class {i}" for i in range(n_classes)]

    counts = np.stack(
        [np.bincount(np.asarray(split_to_labels[name]), minlength=n_classes) for name in split_names],
        axis=0,
    )

    plt.figure(figsize=(10, 5))
    bottom = np.zeros(len(split_names), dtype=np.float64)
    for class_idx in range(n_classes):
        plt.bar(
            split_names,
            counts[:, class_idx],
            bottom=bottom,
            label=class_names[class_idx],
        )
        bottom += counts[:, class_idx]

    plt.title(title)
    plt.ylabel("Samples")
    plt.legend(loc="upper right", ncol=min(3, n_classes))
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def plot_training_curves(history: dict, path: str, title: str):
    ensure_dir(os.path.dirname(path))
    epochs = np.arange(1, len(history["train_loss"]) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].plot(epochs, history["train_loss"], label="Train loss")
    if "val_loss" in history and len(history["val_loss"]) == len(epochs):
        axes[0].plot(epochs, history["val_loss"], label="Val loss")
    axes[0].set_title(f"{title} - Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].legend()

    axes[1].plot(epochs, history["train_f1"], label="Train F1")
    axes[1].plot(epochs, history["val_f1"], label="Val F1")
    axes[1].set_title(f"{title} - Macro F1")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("F1")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close(fig)


def plot_confusion_matrix_figure(y_true, y_pred, path: str, title: str, class_names=None, normalize=True):
    ensure_dir(os.path.dirname(path))
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    n_classes = max(int(y_true.max()), int(y_pred.max())) + 1
    if class_names is None:
        class_names = [f"Class {i}" for i in range(n_classes)]

    cm = confusion_matrix(y_true, y_pred, labels=np.arange(n_classes))
    if normalize:
        row_sums = cm.sum(axis=1, keepdims=True)
        row_sums = np.where(row_sums == 0, 1, row_sums)
        cm = cm / row_sums

    plt.figure(figsize=(7, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt=".2f" if normalize else "d",
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
        cbar=True,
    )
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def plot_cv_metrics(results: list, path: str, title: str):
    ensure_dir(os.path.dirname(path))
    metric_names = ["accuracy", "precision", "recall", "f1"]
    folds = [result["fold"] for result in results]
    x = np.arange(len(folds))
    width = 0.2

    plt.figure(figsize=(12, 5))
    for idx, metric_name in enumerate(metric_names):
        values = [result["test_metrics"][metric_name] for result in results]
        plt.bar(x + (idx - 1.5) * width, values, width=width, label=metric_name.upper())

    plt.xticks(x, folds, rotation=0)
    plt.ylim(0.0, 1.0)
    plt.ylabel("Score")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=200)
    plt.close()


def save_checkpoint(model, optimizer, epoch, metrics, path, extra_state=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    state = {
        "epoch":     epoch,
        "model":     model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "metrics":   metrics,
    }
    if extra_state:
        state.update(extra_state)
    torch.save(state, path)


def load_checkpoint(model, optimizer, path, device):
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    print(f"  ✅ Loaded checkpoint từ epoch {ckpt['epoch']}: {ckpt['metrics']}")
    return ckpt["epoch"], ckpt["metrics"]


def find_optimal_thresholds(
    probs: np.ndarray,
    labels: np.ndarray,
    num_classes: int,
    n_rounds: int = 3,
    resolution: float = 0.02,
    min_class_samples: int = 5,
    max_offset: float = 0.10,
) -> np.ndarray:
    """Tìm per-class probability offsets tối ưu hoá macro F1 trên val set.

    Coordinate descent: mỗi vòng duyệt qua từng class, grid search offset_c.
    Prediction rule: argmax(probs[:, c] - offsets[c])
      offset_c < 0 → class c được predict nhiều hơn (dùng cho minority)
      offset_c > 0 → class c được predict ít hơn (dùng cho majority)

    Args:
        min_class_samples: class có ít hơn N mẫu trong val → bỏ qua (offset=0)
                           tránh overfit offset vào val set quá nhỏ.
        max_offset: giới hạn tìm kiếm ±max_offset (mặc định 0.10, không phải 0.30)

    Returns: offsets shape (num_classes,)
    """
    val_counts = np.bincount(labels, minlength=num_classes)
    calibrate_mask = val_counts >= min_class_samples  # chỉ calibrate class đủ mẫu

    offsets = np.zeros(num_classes, dtype=np.float64)
    grid = np.arange(-max_offset, max_offset + resolution / 2, resolution)
    for _ in range(n_rounds):
        improved = False
        for c in range(num_classes):
            if not calibrate_mask[c]:
                continue  # quá ít mẫu → giữ offset=0
            baseline = _f1_with_offsets(probs, labels, offsets)
            best_off, best_f1 = offsets[c], baseline
            for tau in grid:
                trial = offsets.copy()
                trial[c] = tau
                score = _f1_with_offsets(probs, labels, trial)
                if score > best_f1:
                    best_f1, best_off, improved = score, tau, True
            offsets[c] = best_off
        if not improved:
            break
    return offsets


def _f1_with_offsets(probs: np.ndarray, labels: np.ndarray, offsets: np.ndarray) -> float:
    return f1_score(labels, apply_threshold_offsets(probs, offsets), average="macro", zero_division=0)


def apply_threshold_offsets(probs: np.ndarray, offsets: np.ndarray) -> np.ndarray:
    """Predict argmax(probs - offsets). offsets[c] < 0 → class c ưu tiên hơn."""
    return (probs - offsets[np.newaxis, :]).argmax(axis=1)


class EarlyStopping:
    """Dừng training khi val F1 không cải thiện sau `patience` epochs."""

    def __init__(self, patience: int = 15, min_delta: float = 1e-4):
        self.patience   = patience
        self.min_delta  = min_delta
        self.best_score = None
        self.counter    = 0
        self.stop       = False

    def step(self, score: float) -> bool:
        if self.best_score is None or score > self.best_score + self.min_delta:
            self.best_score = score
            self.counter    = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.stop = True
        return self.stop
