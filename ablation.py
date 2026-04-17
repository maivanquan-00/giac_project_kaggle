"""
ablation.py
-----------
Modality ablation study: train fold 1 with different modality combinations
to identify which modalities contribute signal vs noise.

Usage (trên Kaggle):
    python ablation.py --config configs/config.yaml
"""

import argparse
import os

import numpy as np
import torch
from torch.utils.data import DataLoader
import yaml

from src.data.dataset import build_cv_datasets
from src.data.graph_builder import build_hetero_graph
from src.model import GIACModel
from src.utils import (
    compute_metrics,
    print_classification_report,
    print_metrics,
    set_seed,
)


SUBTYPE_NAMES = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]

ABLATION_CONFIGS = {
    "gene_only":  {"gene": True,  "meth": False, "mirna": False},
    "meth_only":  {"gene": False, "meth": True,  "mirna": False},
    "mirna_only": {"gene": False, "meth": False, "mirna": True},
    "gene+meth":  {"gene": True,  "meth": True,  "mirna": False},
    "gene+mirna": {"gene": True,  "meth": False, "mirna": True},
    "all":        {"gene": True,  "meth": True,  "mirna": True},
}

ABLATION_EPOCHS = 80
ABLATION_PATIENCE = 15


def mask_batch(batch: dict, config: dict) -> dict:
    """Zero-out modalities disabled in config."""
    masked = dict(batch)
    for key in ["gene", "meth", "mirna"]:
        if not config.get(key, True):
            masked[key] = torch.zeros_like(batch[key])
    return masked


def train_epoch_ablation(model, loader, optimizer, graph, device, modality_config):
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        batch = mask_batch(batch, modality_config)

        optimizer.zero_grad()
        logits = model(batch, graph)
        loss = model.compute_loss(logits, batch["label"])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss += loss.item()
        all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())

    metrics = compute_metrics(all_labels, all_preds)
    metrics["loss"] = total_loss / max(len(loader), 1)
    return metrics


@torch.no_grad()
def eval_epoch_ablation(model, loader, graph, device, modality_config,
                        return_predictions=False):
    model.eval()
    all_preds, all_labels = [], []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        batch = mask_batch(batch, modality_config)
        logits = model(batch, graph)
        all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())

    metrics = compute_metrics(all_labels, all_preds)
    if return_predictions:
        return metrics, all_labels, all_preds
    return metrics


def run_one_config(cfg, config_name, modality_config,
                   train_loader, val_loader, test_loader,
                   graph, dims, datasets, device):
    """Train + evaluate one modality config. Returns result dict."""
    print(f"\n{'='*60}")
    print(f"🔬 Ablation: {config_name}")
    print(f"   Gene={'✅' if modality_config['gene'] else '❌'}  "
          f"Meth={'✅' if modality_config['meth'] else '❌'}  "
          f"miRNA={'✅' if modality_config['mirna'] else '❌'}")
    print(f"{'='*60}")

    # Fresh model + optimizer for each config
    set_seed(cfg["training"]["seed"])
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)

    # Class weights
    labels = datasets["train"].label.cpu().numpy()
    n_cls = cfg["model"]["num_classes"]
    counts = np.bincount(labels, minlength=n_cls).astype(np.float32)
    counts = np.clip(counts, a_min=1.0, a_max=None)
    weights = len(labels) / (n_cls * counts)
    weights = weights / weights.mean()
    model.set_class_weights(torch.tensor(weights, dtype=torch.float32, device=device))

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=cfg["training"]["learning_rate"],
        weight_decay=cfg["training"]["weight_decay"],
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=ABLATION_EPOCHS
    )

    best_val_f1 = 0.0
    best_state = None
    patience_counter = 0

    for epoch in range(1, ABLATION_EPOCHS + 1):
        train_metrics = train_epoch_ablation(
            model, train_loader, optimizer, graph, device, modality_config
        )
        val_metrics = eval_epoch_ablation(
            model, val_loader, graph, device, modality_config
        )
        scheduler.step()

        if val_metrics["f1"] > best_val_f1:
            best_val_f1 = val_metrics["f1"]
            best_state = {k: v.cpu().clone() for k, v in model.state_dict().items()}
            patience_counter = 0
        else:
            patience_counter += 1
            if patience_counter >= ABLATION_PATIENCE:
                print(f"   ⏹️  Early stop at epoch {epoch}")
                break

        if epoch % 20 == 0 or epoch == 1:
            print(
                f"   Epoch {epoch:3d}: "
                f"Train F1={train_metrics['f1']:.4f}  "
                f"Val F1={val_metrics['f1']:.4f}"
            )

    # Load best model and evaluate on test
    model.load_state_dict({k: v.to(device) for k, v in best_state.items()})
    test_metrics, test_labels, test_preds = eval_epoch_ablation(
        model, test_loader, graph, device, modality_config,
        return_predictions=True,
    )

    print(f"\n   ✅ Best Val F1 = {best_val_f1:.4f}")
    print_metrics(test_metrics, "Test ")

    # Per-class report for this config
    n_cls = cfg["model"]["num_classes"]
    print(f"\n   📋 Per-class breakdown ({config_name}):")
    print_classification_report(
        test_labels, test_preds,
        class_names=SUBTYPE_NAMES[:n_cls],
    )

    return {
        "config": config_name,
        "best_val_f1": best_val_f1,
        "test": test_metrics,
    }


def run_ablation_one_fold(cfg, fold_no, fold_package, device):
    """Run all 6 ablation configs on a single fold. Returns dict of results."""
    datasets, feature_names, dims, metadata = fold_package["datasets"]

    train_loader = DataLoader(
        datasets["train"],
        batch_size=cfg["training"]["batch_size"],
        shuffle=True,
        num_workers=2,
        pin_memory=True,
    )
    val_loader = DataLoader(datasets["val"], batch_size=64, shuffle=False)
    test_loader = DataLoader(datasets["test"], batch_size=64, shuffle=False)

    graph = build_hetero_graph(
        feature_names, cfg["data"], cfg["graph"], device=str(device)
    )

    fold_results = {}
    for config_name, modality_config in ABLATION_CONFIGS.items():
        res = run_one_config(
            cfg, config_name, modality_config,
            train_loader, val_loader, test_loader,
            graph, dims, datasets, device,
        )
        fold_results[config_name] = res

    # ── Per-fold summary ─────────────────────────────────────────
    print(f"\n{'='*74}")
    print(f"📊 ABLATION SUMMARY — Fold {fold_no}")
    print(f"{'='*74}")
    print(f"{'Config':<15} {'Val F1':>8} {'Test Acc':>10} {'Test P':>8} {'Test R':>8} {'Test F1':>8}")
    print("-" * 74)
    for config_name, res in fold_results.items():
        t = res["test"]
        print(
            f"{config_name:<15} {res['best_val_f1']:>8.4f} "
            f"{t['accuracy']:>10.4f} {t['precision']:>8.4f} "
            f"{t['recall']:>8.4f} {t['f1']:>8.4f}"
        )
    print(f"{'='*74}")

    return fold_results


def print_cross_fold_summary(all_fold_results):
    """Print mean ± std across folds for each ablation config."""
    config_names = list(ABLATION_CONFIGS.keys())
    metric_keys = ["accuracy", "precision", "recall", "f1"]

    print(f"\n{'#'*78}")
    print(f"##  📊 ABLATION — 5-FOLD CROSS-VALIDATED SUMMARY")
    print(f"{'#'*78}\n")

    # ── Table 1: Test F1 per fold ────────────────────────────────
    print(f"{'Config':<15}", end="")
    for fold_no in range(1, len(all_fold_results) + 1):
        print(f" {'Fold '+str(fold_no):>8}", end="")
    print(f" {'Mean':>8} {'Std':>8}")
    print("-" * (15 + 10 * len(all_fold_results) + 18))

    for config_name in config_names:
        f1_values = []
        for fold_results in all_fold_results:
            f1_values.append(fold_results[config_name]["test"]["f1"])
        arr = np.array(f1_values)

        print(f"{config_name:<15}", end="")
        for v in f1_values:
            print(f" {v:>8.4f}", end="")
        print(f" {arr.mean():>8.4f} {arr.std():>8.4f}")

    # ── Table 2: Full summary (mean ± std) ───────────────────────
    print(f"\n{'='*74}")
    print(f"{'Config':<15} {'Val F1':>12} {'Test Acc':>12} {'Test P':>12} {'Test R':>12} {'Test F1':>12}")
    print("-" * 74)

    for config_name in config_names:
        val_f1s = np.array([fr[config_name]["best_val_f1"] for fr in all_fold_results])
        test_metrics = {
            mk: np.array([fr[config_name]["test"][mk] for fr in all_fold_results])
            for mk in metric_keys
        }

        def fmt(arr):
            return f"{arr.mean():.3f}±{arr.std():.3f}"

        print(
            f"{config_name:<15} "
            f"{fmt(val_f1s):>12} "
            f"{fmt(test_metrics['accuracy']):>12} "
            f"{fmt(test_metrics['precision']):>12} "
            f"{fmt(test_metrics['recall']):>12} "
            f"{fmt(test_metrics['f1']):>12}"
        )
    print(f"{'='*74}")


def main():
    parser = argparse.ArgumentParser(description="Modality ablation study (5-fold)")
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--folds", type=int, default=5, help="Number of CV folds")
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg["training"]["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🖥️  Device: {device}")

    n_folds = args.folds
    print(f"📐 Building {n_folds}-fold CV for ablation study...")
    fold_packages = build_cv_datasets(
        cfg["data"], cfg["training"]["seed"], n_splits=n_folds
    )

    all_fold_results = []
    for fold_package in fold_packages:
        fold_no = fold_package["fold"]
        dims = fold_package["datasets"][2]
        print(
            f"\n\n{'*'*78}"
            f"\n*  ABLATION — Fold {fold_no}/{n_folds}"
            f"\n*  gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}"
            f"\n{'*'*78}"
        )
        fold_results = run_ablation_one_fold(cfg, fold_no, fold_package, device)
        all_fold_results.append(fold_results)

    print_cross_fold_summary(all_fold_results)


if __name__ == "__main__":
    main()
