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
    """Tính accuracy, precision, recall, f1 (macro)."""
    return {
        "accuracy":  accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="macro", zero_division=0),
        "recall":    recall_score(y_true, y_pred, average="macro", zero_division=0),
        "f1":        f1_score(y_true, y_pred, average="macro", zero_division=0),
    }


def print_metrics(metrics: dict, split: str = ""):
    prefix = f"[{split}] " if split else ""
    print(
        f"{prefix}Acc={metrics['accuracy']:.4f}  "
        f"P={metrics['precision']:.4f}  "
        f"R={metrics['recall']:.4f}  "
        f"F1={metrics['f1']:.4f}"
    )


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
    print(f"  💾 Saved checkpoint: {path}")


def load_checkpoint(model, optimizer, path, device):
    ckpt = torch.load(path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    optimizer.load_state_dict(ckpt["optimizer"])
    print(f"  ✅ Loaded checkpoint từ epoch {ckpt['epoch']}: {ckpt['metrics']}")
    return ckpt["epoch"], ckpt["metrics"]


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
