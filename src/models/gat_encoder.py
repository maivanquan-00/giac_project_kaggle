"""
train.py
--------
Train GIAC with either a single split or stratified cross-validation.
"""
 
import argparse
import os
 
import numpy as np
import torch
from torch.utils.data import DataLoader
import yaml
 
from src.data.dataset import build_cv_datasets, build_datasets
from src.data.graph_builder import build_hetero_graph
from src.model import GIACModel
from src.utils import (
    EarlyStopping,
    compute_metrics,
    ensure_dir,
    plot_confusion_matrix_figure,
    plot_cv_metrics,
    plot_split_class_distribution,
    plot_training_curves,
    print_classification_report,
    print_metrics,
    save_checkpoint,
    save_confusion_matrix_csv,
    set_seed,
)
 
 
SUBTYPE_NAMES = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]
 
 
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--cv-folds", type=int, default=None)
    return parser.parse_args()
 
 
# ─────────────────────────────────────────────────────────────────────────────
#  Training & evaluation loops
# ─────────────────────────────────────────────────────────────────────────────
 
def train_epoch(model, loader, optimizer, graph, device, scheduler=None):
    model.train()
    total_loss = 0.0
    all_preds, all_labels = [], []
 
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        optimizer.zero_grad()
 
        logits, attn_info = model(batch, graph)
        loss = model.compute_loss(logits, batch["label"], attn_info)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        if scheduler is not None:
            scheduler.step()
 
        total_loss += loss.item()
        all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())
 
    metrics = compute_metrics(all_labels, all_preds)
    metrics["loss"] = total_loss / max(len(loader), 1)
    return metrics
 
 
@torch.no_grad()
def eval_epoch(model, loader, graph, device, return_predictions=False):
    model.eval()
    all_preds, all_labels = [], []
 
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        logits, _ = model(batch, graph)
        all_preds.extend(logits.argmax(dim=-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())
 
    metrics = compute_metrics(all_labels, all_preds)
    if return_predictions:
        return metrics, all_labels, all_preds
    return metrics
 
 
@torch.no_grad()
def collect_attn_stats(model, loader, graph, device):
    """Collect cross-attention statistics on test set for interpretability."""
    model.eval()
    cpg_weights, mirna_weights = [], []
    modality_w = None
 
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        _, _, attn = model(batch, graph, return_interpretability=True)
        cpg_weights.append(attn["cpg_attn"].cpu())
        mirna_weights.append(attn["mirna_attn"].cpu())
        modality_w = attn["modality_weights"].cpu()
 
    cpg_all   = torch.cat(cpg_weights,   dim=0)
    mirna_all = torch.cat(mirna_weights, dim=0)
 
    return {
        "cpg_attn_mean":   cpg_all.mean().item(),
        "cpg_attn_std":    cpg_all.std().item(),
        "mirna_attn_mean": mirna_all.mean().item(),
        "mirna_attn_std":  mirna_all.std().item(),
        "modality_weights": modality_w.tolist() if modality_w is not None else [0.5, 0.5],
    }
 
 
# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────
 
def make_loaders(datasets, train_batch_size):
    train_loader = DataLoader(
        datasets["train"], batch_size=train_batch_size,
        shuffle=True, num_workers=2, pin_memory=True,
    )
    val_loader   = DataLoader(datasets["val"],   batch_size=64, shuffle=False)
    test_loader  = DataLoader(datasets["test"],  batch_size=64, shuffle=False)
    return train_loader, val_loader, test_loader
 
 
def compute_class_weights(dataset, num_classes, device):
    labels  = dataset.label.cpu().numpy()
    counts  = np.bincount(labels, minlength=num_classes).astype(np.float32)
    counts  = np.clip(counts, a_min=1.0, a_max=None)
    weights = len(labels) / (num_classes * counts)
    weights = weights / weights.mean()
    return torch.tensor(weights, dtype=torch.float32, device=device)
 
 
# ─────────────────────────────────────────────────────────────────────────────
#  One split / fold
# ─────────────────────────────────────────────────────────────────────────────
 
def fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name):
    train_loader, val_loader, test_loader = make_loaders(
        datasets, cfg["training"]["batch_size"]
    )
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
    model.set_class_weights(
        compute_class_weights(datasets["train"], cfg["model"]["num_classes"], device)
    )
 
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=cfg["training"]["learning_rate"],
        weight_decay=cfg["training"]["weight_decay"],
    )
 
    scheduler_name = cfg["training"].get("scheduler", "onecycle").lower()
    if scheduler_name == "onecycle":
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer,
            max_lr=cfg["training"].get("max_learning_rate",
                                       cfg["training"]["learning_rate"] * 5),
            epochs=cfg["training"]["epochs"],
            steps_per_epoch=max(len(train_loader), 1),
            pct_start=cfg["training"].get("onecycle_pct_start", 0.1),
            div_factor=cfg["training"].get("onecycle_div_factor", 10.0),
            final_div_factor=cfg["training"].get("onecycle_final_div_factor", 100.0),
        )
        step_per_batch = True
    else:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer, T_max=cfg["training"]["epochs"]
        )
        step_per_batch = False
 
    early_stop = EarlyStopping(patience=cfg["training"]["patience"])
 
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n\U0001f9e0 {fold_name} model parameters: {n_params:,}")
    print(f"\U0001f680 Starting training {fold_name.lower()}...\n")
    print(f"\U0001f5d3\ufe0f  Scheduler: {scheduler_name}")
 
    best_val_f1 = 0.0
    save_dir = cfg["logging"]["save_dir"]
    viz_dir  = os.path.join(save_dir, "visualizations",
                             fold_name.lower().replace(" ", "_"))
    ensure_dir(viz_dir)
    ckpt_name = ("best_model.pt" if fold_name == "Single split"
                 else f"best_model_{fold_name.lower().replace(' ', '_')}.pt")
    ckpt_path = os.path.join(save_dir, ckpt_name)
    history   = {"train_loss": [], "train_f1": [], "val_f1": []}
 
    plot_split_class_distribution(
        {k: datasets[k].label.cpu().numpy() for k in ["train", "val", "test"]},
        path=os.path.join(viz_dir, "class_distribution.png"),
        title=f"{fold_name} - Class Distribution",
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
    )
 
    for epoch in range(1, cfg["training"]["epochs"] + 1):
        tr = train_epoch(model, train_loader, optimizer, graph, device,
                         scheduler=scheduler if step_per_batch else None)
        vl = eval_epoch(model, val_loader, graph, device)
        if not step_per_batch:
            scheduler.step()
 
        history["train_loss"].append(tr["loss"])
        history["train_f1"].append(tr["f1"])
        history["val_f1"].append(vl["f1"])
 
        log_interval = cfg["logging"].get("log_interval", 5)
        if epoch % log_interval == 0 or epoch == 1:
            print(f"{fold_name} | Epoch {epoch:3d}/{cfg['training']['epochs']}")
            print_metrics(tr, "Train")
            print_metrics(vl, "Val  ")
            w = model.cross_attn.modality_weights
            print(f"       modality_w: cpg={w[0]:.3f}  mirna={w[1]:.3f}")
 
        if vl["f1"] > best_val_f1:
            best_val_f1 = vl["f1"]
            save_checkpoint(
                model, optimizer, epoch, vl,
                path=ckpt_path,
                extra_state={
                    "preprocessing": metadata["preprocess"],
                    "split_info":    metadata["split_info"],
                    "feature_names": feature_names,
                    "dims": dims,
                    "fold_name": fold_name,
                    "config": cfg,
                    "history": history,
                },
            )
 
        if early_stop.step(vl["f1"]):
            print(f"\u23f9\ufe0f  Early stopping at epoch {epoch} ({fold_name})")
            break
 
    # ── Test evaluation ───────────────────────────────────────────────────
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    test_metrics, test_labels, test_preds = eval_epoch(
        model, test_loader, graph, device, return_predictions=True
    )
 
    print(f"\n\U0001f4ca Test results - {fold_name}")
    print_metrics(test_metrics, "Test ")
    print(f"\u2705 Best val F1: {best_val_f1:.4f}")
    print(f"\u2705 Test F1:     {test_metrics['f1']:.4f}")
 
    plot_training_curves(history, path=os.path.join(viz_dir, "training_curves.png"),
                         title=fold_name)
    plot_confusion_matrix_figure(
        test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test.png"),
        title=f"{fold_name} - Test Confusion Matrix",
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]], normalize=True,
    )
    print(f"\n\U0001f4cb Classification Report - {fold_name}")
    print_classification_report(test_labels, test_preds,
                                class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]])
    save_confusion_matrix_csv(
        test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]],
    )
 
    # ── Cross-attention statistics ─────────────────────────────────────────
    attn_stats = collect_attn_stats(model, test_loader, graph, device)
    mw = attn_stats["modality_weights"]
    print(f"\n\U0001f50d Cross-Attention Statistics - {fold_name}")
    print(f"   cpg   : mean_attn={attn_stats['cpg_attn_mean']:.4f}  "
          f"std={attn_stats['cpg_attn_std']:.4f}  global_w={mw[0]:.3f}")
    print(f"   mirna : mean_attn={attn_stats['mirna_attn_mean']:.4f}  "
          f"std={attn_stats['mirna_attn_std']:.4f}  global_w={mw[1]:.3f}")
 
    return {
        "fold":        fold_name,
        "best_val_f1": best_val_f1,
        "test_metrics": test_metrics,
        "checkpoint":  ckpt_path,
        "viz_dir":     viz_dir,
    }
 
 
# ─────────────────────────────────────────────────────────────────────────────
#  CV summary
# ─────────────────────────────────────────────────────────────────────────────
 
def summarize_cv(results):
    metric_names = ["accuracy", "precision", "recall", "f1"]
    print("\n\U0001f4c8 5-fold CV summary")
    for name in metric_names:
        vals = np.array([r["test_metrics"][name] for r in results], dtype=np.float64)
        print(f"  {name.upper():9s}: mean={vals.mean():.4f}  std={vals.std(ddof=0):.4f}")
 
 
# ─────────────────────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────────────────────
 
def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
 
    set_seed(cfg["training"]["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\U0001f5a5\ufe0f  Device: {device}")
 
    cv_folds = (args.cv_folds if args.cv_folds is not None
                else cfg.get("preprocessing", {}).get("cv_folds", 5))
 
    if cv_folds and cv_folds > 1:
        fold_packages = build_cv_datasets(cfg, cfg["training"]["seed"], n_splits=cv_folds)
        results = []
        for fp in fold_packages:
            fold_no = fp["fold"]
            datasets, feature_names, dims, metadata = fp["datasets"]
            print(f"\n\U0001f4d0 Fold {fold_no}: "
                  f"gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
            results.append(
                fit_one_split(cfg, datasets, feature_names, dims,
                              metadata, device, fold_name=f"Fold {fold_no}")
            )
        summarize_cv(results)
        plot_cv_metrics(
            results,
            path=os.path.join(cfg["logging"]["save_dir"], "visualizations",
                              "cv_metrics_summary.png"),
            title="5-Fold CV Test Metrics",
        )
    else:
        datasets, feature_names, dims, metadata = build_datasets(
            cfg, cfg["training"]["seed"]
        )
        print(f"\n\U0001f4d0 Feature dims: gene={dims['gene']}, "
              f"meth={dims['meth']}, mirna={dims['mirna']}")
        fit_one_split(cfg, datasets, feature_names, dims,
                      metadata, device, fold_name="Single split")
 
 
if __name__ == "__main__":
    main()
 