"""
utils.py
--------
Các hàm tiện ích: metrics, logging, seed, checkpoint.
"""

import os
import random
import numpy as np
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report


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


def save_checkpoint(model, optimizer, epoch, metrics, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save({
        "epoch":     epoch,
        "model":     model.state_dict(),
        "optimizer": optimizer.state_dict(),
        "metrics":   metrics,
    }, path)
    print(f"  💾 Saved checkpoint: {path}")


def load_checkpoint(model, optimizer, path, device):
    ckpt = torch.load(path, map_location=device)
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
