"""
train.py
--------
Train GIAC với single split hoặc stratified cross-validation.

Đánh giá theo chuẩn paper:
  - Best checkpoint chọn theo val (macro F1 hoặc val loss).
  - Report raw argmax test metrics: macro F1 (primary) + weighted F1 (secondary),
    accuracy, precision, recall (macro).
  - KHÔNG SWA, KHÔNG threshold calibration.

Kết quả tổng hợp được ghi ra `<save_dir>/cv_summary.json` cho run_multi_seed.py đọc.
"""

import argparse
import json
import os
import numpy as np
import torch
from torch.utils.data import DataLoader, WeightedRandomSampler
import yaml
from sklearn.metrics import f1_score

from src.data.dataset import build_cv_datasets, build_datasets, build_fixed_cohort_test_datasets
from src.data.graph_builder import build_hetero_graph, get_edge_stats
from src.model import GIACModel
from src.utils import (
    EarlyStopping, compute_metrics, compute_per_cancer_type_f1, ensure_dir,
    plot_confusion_matrix_figure, plot_cv_metrics,
    plot_split_class_distribution, plot_training_curves,
    print_classification_report, print_confusion_matrix_text, print_metrics,
    save_checkpoint, save_confusion_matrix_csv, set_seed,
)

_DEFAULT_subtype_names = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]


def build_model(dims, cfg_model, cfg_train):
    """Chọn kiến trúc theo cfg_model['arch'] ('v1' mặc định | 'v2' patient-conditioned GAT)."""
    arch = str(cfg_model.get("arch", "v1")).lower()
    if arch == "v2":
        from src.model_v2 import GIACModelV2
        return GIACModelV2(dims, cfg_model, cfg_train)
    return GIACModel(dims, cfg_model, cfg_train)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--cv-folds", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None,
                        help="Override training.seed in config. Use cho multi-seed runs.")
    parser.add_argument("--save-dir", type=str, default=None,
                        help="Override logging.save_dir. Use để tách output từng seed.")
    parser.add_argument("--gene-top-k", type=int, default=None, help="Override preprocessing.gene_top_k (sweep K).")
    parser.add_argument("--meth-top-k", type=int, default=None, help="Override preprocessing.meth_top_k (sweep K).")
    parser.add_argument("--mirna-top-k", type=int, default=None, help="Override preprocessing.mirna_top_k (sweep K).")
    parser.add_argument("--topk-seq", type=int, default=None,
                        help="Override model.topk_seq (sweep số token CpG/miRNA: 16/32/48/64...).")
    parser.add_argument("--topk-selection", choices=["zscore", "random"], default=None,
                        help="Tiêu chí chọn top-K: zscore (mặc định) | random (ablation).")
    parser.add_argument("--epochs", type=int, default=None,
                        help="Override training.epochs (giảm để chạy nhanh khi ablation).")
    parser.add_argument("--no-gat", action="store_true",
                        help="Ablation: tắt GAT message passing (chỉ node_emb + cross-attention).")
    parser.add_argument("--no-film", action="store_true",
                        help="Ablation: tắt FiLM γ/β học được (dùng z = E + E·value).")
    parser.add_argument("--no-pos", action="store_true",
                        help="Ablation: tắt rank positional encoding của top-K.")
    parser.add_argument("--gat-init-residual", type=float, default=None,
                        help="GCNII initial residual α (0=off, ~0.1-0.3 chống over-smoothing).")
    return parser.parse_args()


def _augment_minority(batch, minority_class=None, noise_std: float = 0.10):
    """Add Gaussian noise vào sample của minority class(es) mỗi training step.

    `minority_class` có thể là int (1 class) hoặc list/tuple (nhiều classes).
    Nếu None → no-op. Bắt buộc đọc từ config (KHÔNG hardcode default class).
    """
    if minority_class is None:
        return batch
    classes = [minority_class] if isinstance(minority_class, int) else list(minority_class)
    if not classes:
        return batch
    mask = torch.zeros_like(batch["label"], dtype=torch.bool)
    for c in classes:
        mask = mask | (batch["label"] == c)
    if mask.any():
        for key in ("gene", "meth", "mirna"):
            batch[key][mask] = batch[key][mask] + torch.randn_like(batch[key][mask]) * noise_std
    return batch


def train_epoch(model, loader, optimizer, graph, device, scheduler=None, minority_aug_cfg=None):
    model.train()
    total_loss, all_preds, all_labels = 0.0, [], []
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        if minority_aug_cfg and minority_aug_cfg.get("enabled", True):
            cls = minority_aug_cfg.get("class", None)
            batch = _augment_minority(
                batch,
                minority_class=cls,
                noise_std=minority_aug_cfg.get("noise_std", 0.10),
            )
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
        cw = attn["cpg_attn"]        # (B, K)
        mw_a = attn["mirna_attn"]    # (B, K)
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
        "cpg_std":    _m(cpg_std),
        "cpg_max":    _m(cpg_max),
        "cpg_nnz":    _m(cpg_nnz),
        "mirna_std":  _m(mirna_std),
        "mirna_max":  _m(mirna_max),
        "mirna_nnz":  _m(mirna_nnz),
        "modality_w_cpg":   w[0],
        "modality_w_mirna": w[1],
    }


def make_loaders(datasets, batch_size, balanced_sampler: bool = False,
                 class_sampling_power: float = 1.0):
    if balanced_sampler:
        # Class-aware sampling. power=1.0 → full inverse-frequency; power=0.5 →
        # sqrt-inverse (boost minority nhẹ hơn).
        labels = datasets["train"].label.cpu().numpy()
        class_counts = np.bincount(labels).astype(np.float32)
        class_sampling_power = float(class_sampling_power)
        class_weights = 1.0 / np.power(np.maximum(class_counts, 1.0), class_sampling_power)
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


def _selection_score(m, selection):
    """Giá trị chọn checkpoint (CAO = tốt hơn). Hỗ trợ:
    val_f1 (macro, default) · val_f1_weighted · val_accuracy · val_loss."""
    if selection == "val_loss":
        return -m["loss"]
    if selection == "val_f1_weighted":
        return m["f1_weighted"]
    if selection == "val_accuracy":
        return m["accuracy"]
    if selection == "val_acc_f1w":          # cân bằng CẢ Acc lẫn Weighted F1
        return 0.5 * (m["accuracy"] + m["f1_weighted"])
    return m["f1"]


def compute_per_class_f1(labels, preds, num_classes):
    vals = f1_score(
        labels,
        preds,
        labels=np.arange(num_classes),
        average=None,
        zero_division=0,
    )
    return {int(i): float(v) for i, v in enumerate(vals)}


def fit_one_split(cfg, datasets, feature_names, dims, metadata, device, fold_name):
    subtype_names = cfg["training"].get("subtype_names", _DEFAULT_subtype_names)
    num_classes = cfg["model"]["num_classes"]
    balanced = cfg["training"].get("balanced_sampler", False)
    train_loader, val_loader, test_loader = make_loaders(
        datasets,
        cfg["training"]["batch_size"],
        balanced_sampler=balanced,
        class_sampling_power=cfg["training"].get("class_sampling_power", 1.0),
    )
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))
    edge_stats = get_edge_stats(graph)
    model = build_model(dims, cfg["model"], cfg["training"]).to(device)

    # Class weight strategy (focal alpha):
    #   - use_class_weights=false → neutral (all ones)
    #   - use_manual_focal_alpha=false (default) → compute từ class frequency
    #   - use_manual_focal_alpha=true → giữ focal_alpha từ config nguyên vẹn
    if not cfg["training"].get("use_class_weights", True):
        model.set_class_weights(torch.ones(num_classes, dtype=torch.float32, device=device))
    elif not cfg["training"].get("use_manual_focal_alpha", False):
        model.set_class_weights(compute_class_weights(datasets["train"], num_classes, device))

    base_wd   = cfg["training"]["weight_decay"]
    emb_wd    = cfg["training"].get("node_emb_weight_decay", base_wd * 5)
    base_lr   = cfg["training"]["learning_rate"]
    node_emb_ids = {id(p) for p in model.gat.node_emb.parameters()}
    # v2: patient-injection params (value_scale/value_gamma) → KHÔNG weight decay,
    # tránh dìm tín hiệu bệnh nhân về 0. Rỗng với v1.
    inject_ids = set()
    if hasattr(model.gat, "value_scale"):
        inject_ids = {id(p) for p in list(model.gat.value_scale.parameters())
                      + list(model.gat.value_gamma.parameters())}
    param_groups = [
        {"params": [p for p in model.parameters()
                    if id(p) not in node_emb_ids and id(p) not in inject_ids],
         "lr": base_lr, "weight_decay": base_wd},
        {"params": list(model.gat.node_emb.parameters()), "lr": base_lr, "weight_decay": emb_wd},
    ]
    if inject_ids:
        param_groups.append(
            {"params": list(model.gat.value_scale.parameters())
             + list(model.gat.value_gamma.parameters()),
             "lr": base_lr, "weight_decay": 0.0}
        )
    optimizer = torch.optim.AdamW(param_groups)

    sched_name = cfg["training"].get("scheduler", "onecycle").lower()
    max_lr = cfg["training"].get("max_learning_rate", base_lr * 5)
    if sched_name == "onecycle":
        scheduler = torch.optim.lr_scheduler.OneCycleLR(
            optimizer, max_lr=[max_lr] * len(param_groups),
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

    early_stop = EarlyStopping(
        patience=cfg["training"]["patience"],
        min_epochs=cfg["training"].get("min_epochs", 0),
    )
    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    selection = cfg["training"].get("model_selection_metric", "val_f1")
    best_loss = float("inf")
    best_sel  = float("-inf")
    save_dir  = cfg["logging"]["save_dir"]
    viz_dir   = os.path.join(save_dir, "visualizations", fold_name.lower().replace(" ", "_"))
    ensure_dir(viz_dir)
    ckpt_name = "best_model.pt" if fold_name == "Single split" else f"best_model_{fold_name.lower().replace(' ', '_')}.pt"
    ckpt_path = os.path.join(save_dir, ckpt_name)
    history   = {"train_loss": [], "train_f1": [], "val_f1": [], "val_loss": []}

    plot_split_class_distribution(
        {k: datasets[k].label.cpu().numpy() for k in ["train", "val", "test"]},
        path=os.path.join(viz_dir, "class_distribution.png"),
        title=f"{fold_name} - Class Distribution",
        class_names=subtype_names[:num_classes],
    )
    with open(os.path.join(viz_dir, "edge_stats.json"), "w", encoding="utf-8") as f:
        json.dump(edge_stats, f, indent=2)

    epoch = 0
    for epoch in range(1, cfg["training"]["epochs"] + 1):
        tr = train_epoch(
            model,
            train_loader,
            optimizer,
            graph,
            device,
            scheduler=scheduler if step_per_batch else None,
            minority_aug_cfg=cfg["training"].get("minority_augmentation", {"enabled": True}),
        )
        vl = eval_epoch(model, val_loader, graph, device)
        if not step_per_batch:
            scheduler.step()

        history["train_loss"].append(tr["loss"])
        history["train_f1"].append(tr["f1"])
        history["val_f1"].append(vl["f1"])
        history["val_loss"].append(vl["loss"])

        sel_score = _selection_score(vl, selection)   # cao = tốt
        improved = sel_score > best_sel
        if improved:
            best_sel = sel_score
        if vl["loss"] < best_loss:
            best_loss = vl["loss"]

        if improved:
            save_checkpoint(model, optimizer, epoch, vl, path=ckpt_path,
                extra_state={"preprocessing": metadata["preprocess"],
                             "split_info": metadata["split_info"],
                             "feature_names": feature_names, "dims": dims,
                             "fold_name": fold_name, "config": cfg, "history": history})

        if early_stop.step(sel_score):
            break
    stop_epoch = epoch

    # ── Load best checkpoint + standard eval ──────────────────────────────
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    test_m, test_labels, test_preds = eval_epoch(
        model, test_loader, graph, device, return_predictions=True
    )
    val_m = eval_epoch(model, val_loader, graph, device)
    val_f1 = val_m["f1"]
    per_class_f1 = compute_per_class_f1(test_labels, test_preds, num_classes)

    print(f"\n[{fold_name}] Test (best-checkpoint model):")
    print_metrics(test_m, "test")
    print(f"  Best val macro F1 = {val_f1:.4f}  |  stop epoch = {stop_epoch}")

    plot_training_curves(history, path=os.path.join(viz_dir, "training_curves.png"), title=fold_name)
    plot_confusion_matrix_figure(test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test.png"),
        title=f"{fold_name} - Test",
        class_names=subtype_names[:num_classes], normalize=True)
    save_confusion_matrix_csv(test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
        class_names=subtype_names[:num_classes])
    if cfg["logging"].get("print_classification_report", False):
        print(f"\n  Classification report - {fold_name}:")
        print_classification_report(test_labels, test_preds,
                                    class_names=subtype_names[:num_classes])
        print(f"\n  Confusion matrix - {fold_name} (hàng=true, cột=pred):")
        print_confusion_matrix_text(test_labels, test_preds,
                                    class_names=subtype_names[:num_classes])

    print("  Per-class F1: " + "  ".join(
        f"{name}={per_class_f1[i]:.4f}" for i, name in enumerate(subtype_names[:num_classes])
    ))

    attn = collect_attn_stats(model, test_loader, graph, device)
    print(f"  Attention cpg  : std={attn['cpg_std']:.4f} max={attn['cpg_max']:.4f} "
          f"nnz={attn['cpg_nnz']:.3f} w={attn['modality_w_cpg']:.3f}")
    print(f"  Attention mirna: std={attn['mirna_std']:.4f} max={attn['mirna_max']:.4f} "
          f"nnz={attn['mirna_nnz']:.3f} w={attn['modality_w_mirna']:.3f}")

    film = model.gat.film_summary()
    print(f"  FiLM cpg γ={film['cpg_gamma']:+.4f} β={film['cpg_beta']:+.4f}  ·  "
          f"mirna γ={film['mirna_gamma']:+.4f} β={film['mirna_beta']:+.4f}")

    # Per-cancer-type F1 (multi-cancer datasets như GI)
    per_ct_f1 = {}
    test_cancer_types = getattr(datasets["test"], "cancer_types", None)
    if test_cancer_types is not None and len(set(test_cancer_types)) > 0:
        per_ct_f1 = compute_per_cancer_type_f1(test_labels, test_preds, test_cancer_types)
        if len(per_ct_f1) > 1:
            print(f"  Per-cancer-type F1:")
            for ct, info in sorted(per_ct_f1.items()):
                print(f"    {ct:>8}  n={info['n']:<4}  F1={info['f1']:.4f}")

    # Train F1 at the epoch of best val F1 — overfit indicator
    train_f1_at_best = None
    if history["val_f1"]:
        best_idx = int(np.argmax(history["val_f1"]))
        train_f1_at_best = history["train_f1"][best_idx]

    return {
        "fold": fold_name,
        "best_val_f1": val_f1,
        "val_metrics": val_m,
        "test_metrics": test_m,
        "per_class_f1": per_class_f1,
        "checkpoint": ckpt_path,
        "viz_dir": viz_dir,
        "per_ct_f1": per_ct_f1,
        "attn": attn,
        "film": film,
        "best_val_loss": best_loss,
        "stop_epoch": stop_epoch,
        "n_params": n_params,
        "dims": dims,
        "train_f1_at_best_val": train_f1_at_best,
    }


def build_summary(results, class_names, mode, n_folds):
    """Tổng hợp kết quả các fold thành dict JSON-serializable cho run_multi_seed.py."""
    summary = {"mode": mode, "n_folds": n_folds, "class_names": list(class_names)}

    # ── Headline metrics (mean ± std across folds) ──
    metric_names = ["accuracy", "precision", "recall", "f1", "f1_weighted"]
    summary["metrics"] = {}
    for name in metric_names:
        vals = np.array([r["test_metrics"][name] for r in results
                         if r["test_metrics"].get(name) is not None])
        if vals.size:
            summary["metrics"][name] = {"mean": float(vals.mean()), "std": float(vals.std(ddof=0))}

    summary["per_fold_f1"] = [float(r["test_metrics"]["f1"]) for r in results]

    # ── Per-class F1 ──
    num_classes = max((max(r.get("per_class_f1", {0: 0}).keys()) for r in results), default=-1) + 1
    pcf = {}
    for c in range(num_classes):
        vals = np.array([r["per_class_f1"][c] for r in results if c in r.get("per_class_f1", {})])
        if vals.size:
            pcf[str(c)] = {"mean": float(vals.mean()), "std": float(vals.std(ddof=0))}
    summary["per_class_f1"] = pcf

    # ── Per-cancer-type F1 ──
    all_per_ct = [r.get("per_ct_f1", {}) for r in results]
    unique_cts = sorted(set().union(*[d.keys() for d in all_per_ct])) if all_per_ct else []
    pct = {}
    if len(unique_cts) > 1:
        for ct in unique_cts:
            f1_vals = np.array([d[ct]["f1"] for d in all_per_ct if ct in d])
            n_vals  = np.array([d[ct]["n"]  for d in all_per_ct if ct in d])
            if f1_vals.size:
                pct[ct] = {"n_per_fold": float(n_vals.mean()),
                           "f1_mean": float(f1_vals.mean()),
                           "f1_std": float(f1_vals.std(ddof=0))}
    summary["per_cancer_type_f1"] = pct

    # ── Attention stats ──
    attn_list = [r.get("attn", {}) for r in results if r.get("attn")]
    attn_keys = ["cpg_std", "cpg_max", "cpg_nnz", "modality_w_cpg",
                 "mirna_std", "mirna_max", "mirna_nnz", "modality_w_mirna"]
    attn_out = {}
    for k in attn_keys:
        vals = np.array([a[k] for a in attn_list if k in a])
        if vals.size:
            attn_out[k] = {"mean": float(vals.mean()), "std": float(vals.std(ddof=0))}
    summary["attention"] = attn_out

    # ── FiLM γ, β ──
    film_list = [r.get("film", {}) for r in results if r.get("film")]
    film_out = {}
    for k in ["cpg_gamma", "cpg_beta", "mirna_gamma", "mirna_beta"]:
        vals = np.array([f[k] for f in film_list if k in f])
        if vals.size:
            film_out[k] = {"mean": float(vals.mean()), "std": float(vals.std(ddof=0))}
    summary["film"] = film_out

    # ── Overfit indicator ──
    train_f1s = [r.get("train_f1_at_best_val") for r in results if r.get("train_f1_at_best_val") is not None]
    val_f1s   = [r["val_metrics"]["f1"] for r in results if r.get("val_metrics")]
    test_f1s  = [r["test_metrics"]["f1"] for r in results if r.get("test_metrics")]
    stop_epochs = [r.get("stop_epoch") for r in results if r.get("stop_epoch") is not None]
    overfit = {}
    if train_f1s:
        tf = np.array(train_f1s)
        overfit["train_f1"] = {"mean": float(tf.mean()), "std": float(tf.std(ddof=0))}
    if val_f1s:
        vv = np.array(val_f1s)
        overfit["val_f1"] = {"mean": float(vv.mean()), "std": float(vv.std(ddof=0))}
    if test_f1s:
        tev = np.array(test_f1s)
        overfit["test_f1"] = {"mean": float(tev.mean()), "std": float(tev.std(ddof=0))}
    if train_f1s and val_f1s and len(train_f1s) == len(val_f1s):
        overfit["train_val_gap"] = float((np.array(train_f1s) - np.array(val_f1s)).mean())
    if val_f1s and test_f1s and len(val_f1s) == len(test_f1s):
        overfit["val_test_gap"] = float((np.array(val_f1s) - np.array(test_f1s)).mean())
    if stop_epochs:
        se = np.array(stop_epochs)
        overfit["stop_epoch"] = {"mean": float(se.mean()), "min": int(se.min()), "max": int(se.max())}
    summary["overfit"] = overfit

    # ── Model & feature counts ──
    n_params_list = [r.get("n_params") for r in results if r.get("n_params")]
    dims_list = [r.get("dims") for r in results if r.get("dims")]
    mf = {}
    if n_params_list:
        mf["params"] = int(np.mean(n_params_list))
    if dims_list:
        mf["gene"]  = int(np.mean([d["gene"] for d in dims_list]))
        mf["meth"]  = int(np.mean([d["meth"] for d in dims_list]))
        mf["mirna"] = int(np.mean([d["mirna"] for d in dims_list]))
    summary["model_features"] = mf

    return summary


def print_summary(summary):
    n_folds = summary["n_folds"]
    names = summary.get("class_names", [])

    print(f"\n{n_folds}-fold CV summary (test set, best-checkpoint model):")
    for name in ["accuracy", "precision", "recall", "f1", "f1_weighted"]:
        s = summary["metrics"].get(name)
        if s:
            print(f"  {name:12s}: mean={s['mean']:.4f}  std={s['std']:.4f}")

    pct = summary.get("per_cancer_type_f1", {})
    if len(pct) > 1:
        print(f"\nPer-cancer-type F1 ({n_folds}-fold mean ± std):")
        print(f"  {'Cancer':>8}  {'N/fold':>6}  {'F1 mean':>8}  {'F1 std':>7}")
        for ct, d in sorted(pct.items()):
            print(f"  {ct:>8}  {d['n_per_fold']:>6.1f}  {d['f1_mean']:>8.4f}  {d['f1_std']:>7.4f}")

    pcf = summary.get("per_class_f1", {})
    if pcf:
        print(f"\nPer-class F1 ({n_folds}-fold mean ± std):")
        print(f"  {'Class':>12}  {'F1 mean':>8}  {'F1 std':>7}")
        for c in sorted(pcf, key=int):
            label = names[int(c)] if int(c) < len(names) else f"class {c}"
            print(f"  {label:>12}  {pcf[c]['mean']:>8.4f}  {pcf[c]['std']:>7.4f}")

    attn = summary.get("attention", {})
    if attn:
        print(f"\nAttention stats ({n_folds}-fold mean ± std):")
        for k in ["cpg_std", "cpg_max", "cpg_nnz", "modality_w_cpg",
                  "mirna_std", "mirna_max", "mirna_nnz", "modality_w_mirna"]:
            if k in attn:
                print(f"  {k:18s}: mean={attn[k]['mean']:.4f}  std={attn[k]['std']:.4f}")

    film = summary.get("film", {})
    if film:
        print(f"\nFiLM γ, β ({n_folds}-fold mean ± std, baseline γ=1 β=0):")
        for k in ["cpg_gamma", "cpg_beta", "mirna_gamma", "mirna_beta"]:
            if k in film:
                drift = film[k]["mean"] - (1.0 if k.endswith("gamma") else 0.0)
                print(f"  {k:14s}: mean={film[k]['mean']:+.4f}  std={film[k]['std']:.4f}  drift={drift:+.4f}")

    of = summary.get("overfit", {})
    if of:
        print(f"\nOverfit indicator ({n_folds}-fold):")
        if "train_f1" in of:
            print(f"  Train F1 (at best val): mean={of['train_f1']['mean']:.4f}  std={of['train_f1']['std']:.4f}")
        if "val_f1" in of:
            print(f"  Val F1                : mean={of['val_f1']['mean']:.4f}  std={of['val_f1']['std']:.4f}")
        if "test_f1" in of:
            print(f"  Test F1               : mean={of['test_f1']['mean']:.4f}  std={of['test_f1']['std']:.4f}")
        if "train_val_gap" in of:
            print(f"  Train−Val gap         : {of['train_val_gap']:+.4f}  (>0.20 → overfit mạnh)")
        if "val_test_gap" in of:
            print(f"  Val−Test gap          : {of['val_test_gap']:+.4f}  (>0.05 → val không đại diện test)")
        if "stop_epoch" in of:
            se = of["stop_epoch"]
            print(f"  Stop epoch            : mean={se['mean']:.1f}  range=[{se['min']},{se['max']}]")

    mf = summary.get("model_features", {})
    if mf:
        print(f"\nModel & features ({n_folds}-fold mean):")
        if "params" in mf: print(f"  Params      : {mf['params']:,}")
        if "gene" in mf:   print(f"  Gene feats  : {mf['gene']:,}")
        if "meth" in mf:   print(f"  Meth feats  : {mf['meth']:,}")
        if "mirna" in mf:  print(f"  miRNA feats : {mf['mirna']:,}")


def _write_summary(summary, save_dir):
    ensure_dir(save_dir)
    path = os.path.join(save_dir, "cv_summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nSaved summary: {path}")


def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    if args.seed is not None:
        cfg["training"]["seed"] = args.seed
    if args.save_dir is not None:
        cfg["logging"]["save_dir"] = args.save_dir
    if args.gene_top_k is not None:
        cfg["preprocessing"]["gene_top_k"] = args.gene_top_k
    if args.meth_top_k is not None:
        cfg["preprocessing"]["meth_top_k"] = args.meth_top_k
    if args.mirna_top_k is not None:
        cfg["preprocessing"]["mirna_top_k"] = args.mirna_top_k
    if args.topk_seq is not None:
        cfg["model"]["topk_seq"] = args.topk_seq
    if args.topk_selection is not None:
        cfg["model"]["topk_selection"] = args.topk_selection
    if args.epochs is not None:
        cfg["training"]["epochs"] = args.epochs
        # min_epochs không được vượt epochs (tránh không bao giờ early-stop được)
        if cfg["training"].get("min_epochs", 0) > args.epochs:
            cfg["training"]["min_epochs"] = max(1, args.epochs // 2)
    if args.no_gat:
        cfg["model"]["use_gat"] = False
    if args.no_film:
        cfg["model"]["use_film"] = False
    if args.no_pos:
        cfg["model"]["use_pos_emb"] = False
    if args.gat_init_residual is not None:
        cfg["model"]["gat_init_residual"] = args.gat_init_residual

    seed = cfg["training"]["seed"]
    set_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}  |  Seed: {seed}")

    num_classes = cfg["model"]["num_classes"]
    class_names = cfg["training"].get("subtype_names", _DEFAULT_subtype_names)[:num_classes]
    save_dir = cfg["logging"]["save_dir"]

    test_cohort = cfg.get("data", {}).get("test_cohort")
    cv_folds = args.cv_folds or cfg.get("preprocessing", {}).get("cv_folds", 5)

    if test_cohort:
        datasets, feature_names, dims, metadata = build_fixed_cohort_test_datasets(cfg, seed)
        print(f"Dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
        res = fit_one_split(cfg, datasets, feature_names, dims, metadata, device,
                            f"Fixed-test {test_cohort}")
        summary = build_summary([res], class_names, mode="fixed_test", n_folds=1)
        print_summary(summary)
        _write_summary(summary, save_dir)
    elif cv_folds and cv_folds > 1:
        fold_packages = build_cv_datasets(cfg, seed, n_splits=cv_folds)
        results = []
        for fp in fold_packages:
            fn = fp["fold"]
            datasets, feature_names, dims, metadata = fp["datasets"]
            print(f"\nFold {fn}: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
            results.append(fit_one_split(cfg, datasets, feature_names, dims, metadata, device, f"Fold {fn}"))
        summary = build_summary(results, class_names, mode="cv", n_folds=len(results))
        print_summary(summary)
        _write_summary(summary, save_dir)
        plot_cv_metrics(results,
            path=os.path.join(save_dir, "visualizations", "cv_metrics_summary.png"),
            title=f"{len(results)}-Fold CV Test Metrics")
    else:
        datasets, feature_names, dims, metadata = build_datasets(cfg, seed)
        print(f"Dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
        res = fit_one_split(cfg, datasets, feature_names, dims, metadata, device, "Single split")
        summary = build_summary([res], class_names, mode="single", n_folds=1)
        print_summary(summary)
        _write_summary(summary, save_dir)


if __name__ == "__main__":
    main()
