"""
train.py
--------
Train GIAC with either a single split or stratified cross-validation.
"""
 
import argparse
import os
import numpy as np
import torch
from torch.utils.data import DataLoader, WeightedRandomSampler
import yaml
 
from src.data.dataset import build_cv_datasets, build_datasets
from src.data.graph_builder import build_hetero_graph
from src.model import GIACModel
from src.utils import (
    EarlyStopping, compute_metrics, ensure_dir,
    plot_confusion_matrix_figure, plot_cv_metrics,
    plot_split_class_distribution, plot_training_curves,
    print_classification_report, print_metrics,
    save_checkpoint, save_confusion_matrix_csv, set_seed,
)
 
SUBTYPE_NAMES = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]
 
 
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--cv-folds", type=int, default=None)
    return parser.parse_args()
 
 
def _augment_minority(batch, minority_class: int = 3, noise_std: float = 0.10):
    """Add Gaussian noise to HM-SNV samples each training step.
    Forces the model to generalize instead of memorising the ~15 unique
    HM-SNV training patients; features are already z-scored so std=0.10
    is a mild perturbation (~10 % of one standard deviation)."""
    mask = batch["label"] == minority_class
    if mask.any():
        for key in ("gene", "meth", "mirna"):
            batch[key][mask] = batch[key][mask] + torch.randn_like(batch[key][mask]) * noise_std
    return batch


def train_epoch(model, loader, optimizer, graph, device, scheduler=None):
    model.train()
    total_loss, all_preds, all_labels = 0.0, [], []
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        batch = _augment_minority(batch)
        optimizer.zero_grad()
        logits, attn_info = model(batch, graph)
        loss = model.compute_loss(logits, batch["label"], attn_info)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        if scheduler is not None:
            scheduler.step()
        total_loss += loss.item()
        all_preds.extend(logits.argmax(-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())
    m = compute_metrics(all_labels, all_preds)
    m["loss"] = total_loss / max(len(loader), 1)
    return m
 
 
@torch.no_grad()
def eval_epoch(model, loader, graph, device, return_predictions=False):
    model.eval()
    total_loss, n_batches, all_preds, all_labels = 0.0, 0, [], []
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        logits, attn_info = model(batch, graph)
        total_loss += model.compute_loss(logits, batch["label"], attn_info).item()
        n_batches += 1
        all_preds.extend(logits.argmax(-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())
    m = compute_metrics(all_labels, all_preds)
    m["loss"] = total_loss / max(n_batches, 1)
    if return_predictions:
        return m, all_labels, all_preds
    return m
 
 
@torch.no_grad()
def collect_attn_stats(model, loader, graph, device):
    model.eval()
    cpg_std, cpg_max, cpg_nnz = [], [], []
    mirna_std, mirna_max, mirna_nnz = [], [], []
    mw = None
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        _, _, attn = model(batch, graph, return_interpretability=True)
        # attn["cpg_attn"]: (B, K) — attention weights over K tokens per patient
        # std over K tokens measures concentration; max measures peak; nnz measures sparsity
        cw = attn["cpg_attn"]   # (B, K)
        mw_a = attn["mirna_attn"]  # (B, K)
        cpg_std.append(cw.std(dim=1).cpu())
        cpg_max.append(cw.max(dim=1).values.cpu())
        cpg_nnz.append((cw > 1e-6).float().mean(dim=1).cpu())
        mirna_std.append(mw_a.std(dim=1).cpu())
        mirna_max.append(mw_a.max(dim=1).values.cpu())
        mirna_nnz.append((mw_a > 1e-6).float().mean(dim=1).cpu())
        mw = attn["modality_weights"].detach().cpu()

    def _m(lst): return torch.cat(lst).mean().item()
    w = mw.tolist() if mw is not None else [0.5, 0.5]
    return {
        "cpg_std":    _m(cpg_std),    # std over K tokens — >0 means non-uniform attention
        "cpg_max":    _m(cpg_max),    # avg peak weight — >1/K means selective attention
        "cpg_nnz":    _m(cpg_nnz),    # fraction non-zero tokens (entmax15 sparsity)
        "mirna_std":  _m(mirna_std),
        "mirna_max":  _m(mirna_max),
        "mirna_nnz":  _m(mirna_nnz),
        "modality_w_cpg":   w[0],
        "modality_w_mirna": w[1],
    }
 
 
def make_loaders(datasets, batch_size, balanced_sampler: bool = False):
    if balanced_sampler:
        # Class-balanced sampling: each class contributes ~equal mass per epoch.
        # Counters severe imbalance (HM-SNV=19 vs CIN=624) so minority classes
        # actually get gradient updates instead of being drowned out.
        labels = datasets["train"].label.cpu().numpy()
        class_counts = np.bincount(labels).astype(np.float32)
        class_weights = 1.0 / np.maximum(class_counts, 1.0)
        sample_weights = class_weights[labels]
        sampler = WeightedRandomSampler(
            weights=torch.from_numpy(sample_weights).double(),
            num_samples=len(labels),
            replacement=True,
        )
        tl = DataLoader(datasets["train"], batch_size=batch_size, sampler=sampler,
                        num_workers=2, pin_memory=True)
    else:
        tl = DataLoader(datasets["train"], batch_size=batch_size, shuffle=True,
                        num_workers=2, pin_memory=True)
    vl  = DataLoader(datasets["val"],   batch_size=64, shuffle=False)
    tel = DataLoader(datasets["test"],  batch_size=64, shuffle=False)
    return tl, vl, tel
 
 
def compute_class_weights(dataset, num_classes, device):
    labels  = dataset.label.cpu().numpy()
    counts  = np.bincount(labels, minlength=num_classes).astype(np.float32)
    counts  = np.clip(counts, 1.0, None)
    weights = len(labels) / (num_classes * counts)
    return torch.tensor(weights / weights.mean(), dtype=torch.float32, device=device)
 
 
def fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name):
    balanced = cfg["training"].get("balanced_sampler", False)
    train_loader, val_loader, test_loader = make_loaders(
        datasets, cfg["training"]["batch_size"], balanced_sampler=balanced
    )
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
    model.set_class_weights(compute_class_weights(datasets["train"], cfg["model"]["num_classes"], device))
 
    base_wd   = cfg["training"]["weight_decay"]
    emb_wd    = cfg["training"].get("node_emb_weight_decay", base_wd * 5)
    base_lr   = cfg["training"]["learning_rate"]
    node_emb_ids = {id(p) for p in model.gat.node_emb.parameters()}
    optimizer = torch.optim.AdamW([
        {"params": [p for p in model.parameters() if id(p) not in node_emb_ids], "lr": base_lr, "weight_decay": base_wd},
        {"params": list(model.gat.node_emb.parameters()), "lr": base_lr, "weight_decay": emb_wd},
    ])
 
    sched_name = cfg["training"].get("scheduler", "onecycle").lower()
    max_lr = cfg["training"].get("max_learning_rate", base_lr * 5)
    if sched_name == "onecycle":
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer, max_lr=[max_lr, max_lr],
            epochs=cfg["training"]["epochs"],
            steps_per_epoch=max(len(train_loader), 1),
            pct_start=cfg["training"].get("onecycle_pct_start", 0.1),
            div_factor=cfg["training"].get("onecycle_div_factor", 10.0),
            final_div_factor=cfg["training"].get("onecycle_final_div_factor", 100.0),
        )
        step_per_batch = True
    else:
        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=cfg["training"]["epochs"])
        step_per_batch = False
 
    early_stop = EarlyStopping(patience=cfg["training"]["patience"])
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"\n\U0001f9e0 {fold_name} params: {n_params:,}")
    print(f"\U0001f680 Training {fold_name}...  scheduler={sched_name}")
 
    selection = cfg["training"].get("model_selection_metric", "val_f1")
    best_loss = float("inf")
    best_f1   = 0.0
    save_dir  = cfg["logging"]["save_dir"]
    viz_dir   = os.path.join(save_dir, "visualizations", fold_name.lower().replace(" ", "_"))
    ensure_dir(viz_dir)
    ckpt_name = "best_model.pt" if fold_name == "Single split" else f"best_model_{fold_name.lower().replace(' ', '_')}.pt"
    ckpt_path = os.path.join(save_dir, ckpt_name)
    history   = {"train_loss": [], "train_f1": [], "val_f1": [], "val_loss": []}
    log_every = cfg["logging"].get("log_interval", 5)
 
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
        history["val_loss"].append(vl["loss"])
 
        if epoch % log_every == 0 or epoch == 1:
            print(f"{fold_name} | Epoch {epoch:3d}/{cfg['training']['epochs']}")
            print_metrics(tr, "Train")
            print_metrics(vl, "Val  ")
            w = model.cross_attn.modality_weights.detach()
            print(f"       modality_w: cpg={w[0]:.3f} mirna={w[1]:.3f}  |  val_loss={vl['loss']:.4f}")
 
        improved = False
        if selection == "val_loss":
            if vl["loss"] < best_loss:
                best_loss, improved = vl["loss"], True
        else:
            if vl["f1"] > best_f1:
                improved = True
        if vl["f1"] > best_f1:
            best_f1 = vl["f1"]
        if vl["loss"] < best_loss:
            best_loss = vl["loss"]
 
        if improved:
            save_checkpoint(model, optimizer, epoch, vl, path=ckpt_path,
                extra_state={"preprocessing": metadata["preprocess"],
                             "split_info": metadata["split_info"],
                             "feature_names": feature_names, "dims": dims,
                             "fold_name": fold_name, "config": cfg, "history": history})
 
        es_score = -vl["loss"] if selection == "val_loss" else vl["f1"]
        if early_stop.step(es_score):
            print(f"\u23f9\ufe0f  Early stopping at epoch {epoch} ({fold_name})")
            break
 
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    test_m, test_labels, test_preds = eval_epoch(model, test_loader, graph, device, return_predictions=True)
 
    print(f"\n\U0001f4ca Test - {fold_name}")
    print_metrics(test_m, "Test ")
    print(f"\u2705 Best val F1: {best_f1:.4f}  |  Best val loss: {best_loss:.4f}")
    print(f"\u2705 Test F1:     {test_m['f1']:.4f}")
 
    plot_training_curves(history, path=os.path.join(viz_dir, "training_curves.png"), title=fold_name)
    plot_confusion_matrix_figure(test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test.png"),
        title=f"{fold_name} - Test",
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]], normalize=True)
    print(f"\n\U0001f4cb Classification Report - {fold_name}")
    print_classification_report(test_labels, test_preds,
                                class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]])
    save_confusion_matrix_csv(test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
        class_names=SUBTYPE_NAMES[:cfg["model"]["num_classes"]])
 
    attn = collect_attn_stats(model, test_loader, graph, device)
    print(f"\n\U0001f50d Attention Stats - {fold_name}")
    print(f"   cpg  : std={attn['cpg_std']:.4f}  max={attn['cpg_max']:.4f}  nnz={attn['cpg_nnz']:.3f}  global_w={attn['modality_w_cpg']:.3f}")
    print(f"   mirna: std={attn['mirna_std']:.4f}  max={attn['mirna_max']:.4f}  nnz={attn['mirna_nnz']:.3f}  global_w={attn['modality_w_mirna']:.3f}")
 
    return {"fold": fold_name, "best_val_f1": best_f1, "test_metrics": test_m,
            "checkpoint": ckpt_path, "viz_dir": viz_dir}
 
 
def summarize_cv(results):
    print("\n\U0001f4c8 5-fold CV summary")
    for name in ["accuracy", "precision", "recall", "f1"]:
        vals = np.array([r["test_metrics"][name] for r in results])
        print(f"  {name.upper():9s}: mean={vals.mean():.4f}  std={vals.std(ddof=0):.4f}")
 
 
def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)
    set_seed(cfg["training"]["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\U0001f5a5\ufe0f  Device: {device}")
 
    cv_folds = args.cv_folds or cfg.get("preprocessing", {}).get("cv_folds", 5)
    if cv_folds and cv_folds > 1:
        fold_packages = build_cv_datasets(cfg, cfg["training"]["seed"], n_splits=cv_folds)
        results = []
        for fp in fold_packages:
            fn = fp["fold"]
            datasets, feature_names, dims, metadata = fp["datasets"]
            print(f"\n\U0001f4d0 Fold {fn}: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
            results.append(fit_one_split(cfg, datasets, feature_names, dims, metadata, device, f"Fold {fn}"))
        summarize_cv(results)
        plot_cv_metrics(results,
            path=os.path.join(cfg["logging"]["save_dir"], "visualizations", "cv_metrics_summary.png"),
            title="5-Fold CV Test Metrics")
    else:
        datasets, feature_names, dims, metadata = build_datasets(cfg, cfg["training"]["seed"])
        print(f"\n\U0001f4d0 Dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
        fit_one_split(cfg, datasets, feature_names, dims, metadata, device, "Single split")
 
 
if __name__ == "__main__":
    main()
