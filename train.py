"""
train.py
--------
Train GIAC with either a single split or stratified cross-validation.
"""
 
import argparse
import json
import os
import numpy as np
import torch
from torch.optim.swa_utils import AveragedModel
from torch.utils.data import DataLoader, WeightedRandomSampler
import yaml
from sklearn.metrics import f1_score

from src.data.dataset import build_cv_datasets, build_datasets, build_fixed_cohort_test_datasets
from src.data.graph_builder import build_hetero_graph, get_edge_stats
from src.model import GIACModel
from src.utils import (
    EarlyStopping, compute_metrics, compute_per_cancer_type_f1, ensure_dir,
    find_optimal_thresholds, apply_threshold_offsets,
    plot_confusion_matrix_figure, plot_cv_metrics,
    plot_split_class_distribution, plot_training_curves,
    print_classification_report, print_metrics,
    save_checkpoint, save_confusion_matrix_csv, set_seed,
)
 
_DEFAULT_subtype_names = ["CIN", "GS", "MSI", "HM-SNV", "EBV"]


def _inner_model(model):
    """Unwrap AveragedModel để truy cập compute_loss / cross_attn / gat."""
    return model.module if hasattr(model, "module") else model


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/config.yaml")
    parser.add_argument("--cv-folds", type=int, default=None)
    parser.add_argument("--seed", type=int, default=None,
                        help="Override training.seed in config. Use cho multi-seed runs.")
    parser.add_argument("--save-dir", type=str, default=None,
                        help="Override logging.save_dir. Use để tách output từng seed.")
    return parser.parse_args()
 
 
def _augment_minority(batch, minority_class=None, noise_std: float = 0.10):
    """Add Gaussian noise vào sample của minority class(es) mỗi training step.

    `minority_class` có thể là int (1 class) hoặc list/tuple (nhiều classes).
    Nếu None → no-op. Trước đây hardcoded default=3 (HM-SNV) — sai cho BRCA
    (Normal=4), đã fix 2026-05-10: bắt buộc đọc từ config.
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
            # `class` default = None → no-op (an toàn). Bắt buộc set ở config
            # nếu muốn aug. Trước đây hardcode default=3 → sai cho BRCA Normal=4.
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
    inner = _inner_model(model)
    total_loss, n_batches, all_preds, all_labels = 0.0, 0, [], []
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        logits, attn_info = model(batch, graph)
        total_loss += inner.compute_loss(logits, batch["label"], attn_info).item()
        n_batches += 1
        all_preds.extend(logits.argmax(-1).cpu().tolist())
        all_labels.extend(batch["label"].cpu().tolist())
    m = compute_metrics(all_labels, all_preds)
    m["loss"] = total_loss / max(n_batches, 1)
    if return_predictions:
        return m, all_labels, all_preds
    return m
 
 
@torch.no_grad()
def collect_probabilities(model, loader, graph, device):
    """Trả về softmax probabilities và labels từ loader. Dùng cho threshold calibration."""
    model.eval()
    all_probs, all_labels = [], []
    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}
        logits, _ = model(batch, graph)
        all_probs.append(torch.softmax(logits, dim=-1).cpu().numpy())
        all_labels.extend(batch["label"].cpu().tolist())
    return np.concatenate(all_probs, axis=0), np.array(all_labels)


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
 
 
def make_loaders(datasets, batch_size, balanced_sampler: bool = False,
                 class_sampling_power: float = 1.0):
    if balanced_sampler:
        # Class-aware sampling. power=1.0 gives full inverse-frequency balancing;
        # power=0.5 is a softer sqrt-inverse sampler that boosts minority
        # classes without making each class equally likely.
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
        effective_mass = class_counts * class_weights
        effective_dist = effective_mass / effective_mass.sum()
        print(
            "⚖️  Class-aware sampler: "
            f"power={class_sampling_power:.2f}, "
            f"expected_dist={[round(float(x), 3) for x in effective_dist]}"
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
    balanced = cfg["training"].get("balanced_sampler", False)
    train_loader, val_loader, test_loader = make_loaders(
        datasets,
        cfg["training"]["batch_size"],
        balanced_sampler=balanced,
        class_sampling_power=cfg["training"].get("class_sampling_power", 1.0),
    )
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))
    edge_stats = get_edge_stats(graph)
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)

    # Class weight strategy:
    #   - Default (use_manual_focal_alpha=false): compute từ class frequency, override
    #     focal_alpha trong config. Đây là behavior cũ.
    #   - Manual (use_manual_focal_alpha=true): giữ focal_alpha từ config nguyên vẹn
    #     để tune thủ công cho minority class (vd: HM-SNV alpha=12).
    if not cfg["training"].get("use_class_weights", True):
        neutral_alpha = torch.ones(cfg["model"]["num_classes"], dtype=torch.float32, device=device)
        model.set_class_weights(neutral_alpha)
        print("⚖️  Using neutral class weights / focal_alpha: all ones")
    elif not cfg["training"].get("use_manual_focal_alpha", False):
        computed_alpha = compute_class_weights(datasets["train"], cfg["model"]["num_classes"], device)
        model.set_class_weights(computed_alpha)
        print(f"⚖️  Using computed focal_alpha: {[round(x, 4) for x in computed_alpha.detach().cpu().tolist()]}")
    else:
        manual_alpha = cfg["training"]["focal_alpha"]
        print(f"✨ Using MANUAL focal_alpha from config: {manual_alpha}")
 
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

    # ── Stochastic Weight Averaging (Izmailov 2018) — v3 pure ──
    # v3: KEEP main scheduler (OneCycle) running để vanilla preserved. SWA chỉ
    # collect averages on top, không dùng SWALR (vì SWALR pause OneCycle gây
    # disturbance lớn — xem testnew.md run 2 vs 3). Tradeoff: snapshots ko diverse
    # nếu OneCycle decay quá nhanh, nhưng baseline vanilla giữ nguyên.
    # Model dùng LayerNorm only → không cần torch.optim.swa_utils.update_bn().
    swa_cfg = (cfg["training"].get("swa") or {})
    swa_enabled = bool(swa_cfg.get("enabled", False))
    swa_start = int(swa_cfg.get("start_epoch", 30))
    swa_update_freq = max(1, int(swa_cfg.get("update_freq", 1)))
    swa_model = None
    if swa_enabled:
        swa_model = AveragedModel(model)
        print(
            f"🪶 SWA enabled (v3 pure — main scheduler keeps running): "
            f"start_epoch={swa_start}, update_freq={swa_update_freq}"
        )

    # EarlyStopping — bump min_epochs để đảm bảo SWA có collection window
    min_epochs_es = cfg["training"].get("min_epochs", 0)
    if swa_enabled:
        min_epochs_es = max(min_epochs_es, swa_start + 10)
    early_stop = EarlyStopping(
        patience=cfg["training"]["patience"],
        min_epochs=min_epochs_es,
    )
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
        class_names=subtype_names[:cfg["model"]["num_classes"]],
    )
    with open(os.path.join(viz_dir, "edge_stats.json"), "w", encoding="utf-8") as f:
        json.dump(edge_stats, f, indent=2)
 
    for epoch in range(1, cfg["training"]["epochs"] + 1):
        # v3: main scheduler luôn chạy, SWA chỉ collect on top
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
        # SWA collect (không pause main scheduler — vanilla preserved)
        if swa_enabled and epoch >= swa_start:
            if (epoch - swa_start) % swa_update_freq == 0:
                swa_model.update_parameters(model)
 
        history["train_loss"].append(tr["loss"])
        history["train_f1"].append(tr["f1"])
        history["val_f1"].append(vl["f1"])
        history["val_loss"].append(vl["loss"])
 
        if epoch % log_every == 0 or epoch == 1:
            w = model.cross_attn.modality_weights.detach()
            print(
                f"{fold_name} | Ep {epoch:3d}/{cfg['training']['epochs']}"
                f" | train F1={tr['f1']:.4f}"
                f" | val F1={vl['f1']:.4f} loss={vl['loss']:.4f}"
                f" | mw=[c={w[0]:.2f},m={w[1]:.2f}]"
            )
 
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
 
    # ── Load best_ckpt (vanilla) + eval ──
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    test_m_best, test_labels_best, test_preds_best = eval_epoch(
        model, test_loader, graph, device, return_predictions=True
    )
    val_m_best = eval_epoch(model, val_loader, graph, device)
    val_f1_best = val_m_best["f1"]

    # ── SWA: evaluate (v3 always-pick policy if enabled) ──
    eval_model = model
    selected = "vanilla"
    test_m, test_labels, test_preds = test_m_best, test_labels_best, test_preds_best
    selected_val_f1 = val_f1_best
    val_metrics_vanilla = val_m_best
    test_metrics_vanilla = test_m_best
    val_metrics_swa = None
    test_metrics_swa = None
    n_swa_avg = 0
    if swa_enabled and swa_model is not None:
        # Model dùng LayerNorm (không có BN running stats) → skip update_bn.
        swa_val_m = eval_epoch(swa_model, val_loader, graph, device)
        swa_test_m, swa_test_labels, swa_test_preds = eval_epoch(
            swa_model, test_loader, graph, device, return_predictions=True
        )
        val_metrics_swa = swa_val_m
        test_metrics_swa = swa_test_m
        n_swa_avg = int(swa_model.n_averaged.item())
        # Always-pick SWA: vanilla preserved trong training (OneCycle ko bị động),
        # SWA averaging giảm fold-to-fold variance trên test. Cả 2 set metrics
        # đều report để so sánh trong báo cáo.
        eval_model = swa_model
        selected = "swa"
        test_m = swa_test_m
        test_labels = swa_test_labels
        test_preds = swa_test_preds
        selected_val_f1 = swa_val_m["f1"]
        swa_ckpt_path = ckpt_path.replace(".pt", "_swa.pt")
        torch.save({"model": swa_model.state_dict(), "n_averaged": n_swa_avg}, swa_ckpt_path)

    per_class_f1 = compute_per_class_f1(test_labels, test_preds, cfg["model"]["num_classes"])
    per_class_f1_vanilla = compute_per_class_f1(
        test_labels_best, test_preds_best, cfg["model"]["num_classes"]
    )

    # ── Threshold calibration (val-fitted, applied to test) ───────────────
    num_classes = cfg["model"]["num_classes"]
    val_probs, val_labels_arr = collect_probabilities(eval_model, val_loader, graph, device)
    offsets = find_optimal_thresholds(val_probs, val_labels_arr, num_classes)
    test_probs, _ = collect_probabilities(eval_model, test_loader, graph, device)
    test_preds_cal = apply_threshold_offsets(test_probs, offsets)
    test_m_cal = compute_metrics(test_labels, test_preds_cal.tolist())
    per_class_f1_cal = compute_per_class_f1(test_labels, test_preds_cal.tolist(), num_classes)

    # ── Per-fold output: compact, side-by-side khi SWA enabled ──
    if swa_enabled and swa_model is not None:
        print(f"\n📊 {fold_name} — Vanilla vs SWA  ({n_swa_avg} snapshots averaged)")
        print(f"   {'':<6s} {'vanilla':>10s} {'SWA':>10s} {'Δ':>10s}")
        for split_lbl, vm, sm in (("val ", val_m_best, swa_val_m),
                                  ("test", test_m_best, swa_test_m)):
            for k, klabel in (("accuracy", "Acc"), ("f1_weighted", "F1w"), ("f1", "F1m")):
                v, s = vm.get(k, 0), sm.get(k, 0)
                print(f"   {split_lbl} {klabel:<3s}: {v:>10.4f} {s:>10.4f} {s-v:>+10.4f}")
        gain = test_m_cal["f1"] - test_m["f1"]
        print(f"   → SELECTED: {selected}  |  test cal F1m gain: {gain:+.4f}")
    else:
        gain = test_m_cal["f1"] - test_m["f1"]
        print(f"\n📊 Test - {fold_name}")
        print_metrics(test_m,     "Raw  ")
        print_metrics(test_m_cal, "Cal  ")
        print(f"✅ Best val F1: {selected_val_f1:.4f}  |  Calibration gain: {gain:+.4f}")
        print(f"✅ Test F1  raw={test_m['f1']:.4f}  cal={test_m_cal['f1']:.4f}")
 
    plot_training_curves(history, path=os.path.join(viz_dir, "training_curves.png"), title=fold_name)
    plot_confusion_matrix_figure(test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test.png"),
        title=f"{fold_name} - Test",
        class_names=subtype_names[:cfg["model"]["num_classes"]], normalize=True)
    if cfg["logging"].get("print_classification_report", False):
        print(f"\n\U0001f4cb Classification Report - {fold_name}  (model={selected})")
        print_classification_report(test_labels, test_preds,
                                    class_names=subtype_names[:cfg["model"]["num_classes"]])
    # Per-class F1: hiển thị vanilla + SWA side-by-side khi SWA enabled
    if swa_enabled and swa_model is not None:
        print(f"\n🎯 Per-class F1 - {fold_name}  (vanilla → SWA → cal)")
        for idx, name in enumerate(subtype_names[:cfg["model"]["num_classes"]]):
            v = per_class_f1_vanilla[idx]
            s = per_class_f1[idx]   # SWA (= selected)
            c = per_class_f1_cal[idx]
            print(f"   {idx}:{name:<8s}  van={v:.4f}  swa={s:.4f} ({s-v:+.4f})  cal={c:.4f}")
    else:
        print(f"\n🎯 Per-class F1 - {fold_name}  (raw → calibrated)")
        for idx, name in enumerate(subtype_names[:cfg["model"]["num_classes"]]):
            raw = per_class_f1[idx]
            cal = per_class_f1_cal[idx]
            print(f"   {idx}:{name:<8s}  {raw:.4f} → {cal:.4f}  ({cal-raw:+.4f})")
    save_confusion_matrix_csv(test_labels, test_preds,
        path=os.path.join(viz_dir, "confusion_matrix_test_absolute.csv"),
        class_names=subtype_names[:cfg["model"]["num_classes"]])

    attn = collect_attn_stats(eval_model, test_loader, graph, device)
    print(f"\n\U0001f50d Attention Stats - {fold_name}  (model={selected})")
    print(f"   cpg  : std={attn['cpg_std']:.4f}  max={attn['cpg_max']:.4f}  nnz={attn['cpg_nnz']:.3f}  global_w={attn['modality_w_cpg']:.3f}")
    print(f"   mirna: std={attn['mirna_std']:.4f}  max={attn['mirna_max']:.4f}  nnz={attn['mirna_nnz']:.3f}  global_w={attn['modality_w_mirna']:.3f}")

    # Phase 2.1a — FiLM γ, β values (init γ=1, β=0). Đọc từ selected model.
    inner_eval = _inner_model(eval_model)
    film = {
        "cpg_gamma":   inner_eval.gat.film_cpg_gamma.item(),
        "cpg_beta":    inner_eval.gat.film_cpg_beta.item(),
        "mirna_gamma": inner_eval.gat.film_mirna_gamma.item(),
        "mirna_beta":  inner_eval.gat.film_mirna_beta.item(),
    }
    print(f"\U0001f3da️  FiLM (γ=1 β=0 baseline)  cpg γ={film['cpg_gamma']:+.4f} β={film['cpg_beta']:+.4f}  ·  mirna γ={film['mirna_gamma']:+.4f} β={film['mirna_beta']:+.4f}")

    # Per-cancer-type F1 (multi-cancer datasets như GI). Khi SWA enabled, in cả
    # vanilla + SWA side-by-side để so sánh trong báo cáo.
    per_ct_f1 = {}
    per_ct_f1_vanilla = {}
    test_cancer_types = getattr(datasets["test"], "cancer_types", None)
    if test_cancer_types is not None and len(set(test_cancer_types)) > 0:
        per_ct_f1 = compute_per_cancer_type_f1(test_labels, test_preds, test_cancer_types)
        if swa_enabled and swa_model is not None:
            per_ct_f1_vanilla = compute_per_cancer_type_f1(
                test_labels_best, test_preds_best, test_cancer_types
            )
        if len(per_ct_f1) > 1:
            if swa_enabled and swa_model is not None:
                print(f"\n\U0001f9ec Per-cancer-type F1 - {fold_name}  (vanilla → SWA)")
                print(f"   {'Cancer':>8}  {'N':>5}  {'vanilla':>8}  {'SWA':>8}  {'Δ':>+8}")
                for ct, info in sorted(per_ct_f1.items()):
                    v = per_ct_f1_vanilla.get(ct, {}).get("f1", 0)
                    s = info["f1"]
                    print(f"   {ct:>8}  {info['n']:>5}  {v:>8.4f}  {s:>8.4f}  {s-v:>+8.4f}")
            else:
                print(f"\n\U0001f9ec Per-cancer-type F1 - {fold_name}")
                print(f"   {'Cancer':>8}  {'N':>5}  {'F1':>6}")
                for ct, info in sorted(per_ct_f1.items()):
                    print(f"   {ct:>8}  {info['n']:>5}  {info['f1']:.4f}")

    # Train F1 at the epoch of best val F1 — overfit indicator
    train_f1_at_best = None
    if history["val_f1"]:
        best_idx = int(np.argmax(history["val_f1"]))
        train_f1_at_best = history["train_f1"][best_idx]

    return {"fold": fold_name, "best_val_f1": selected_val_f1, "test_metrics": test_m,
            "test_metrics_calibrated": test_m_cal, "per_class_f1_calibrated": per_class_f1_cal,
            "threshold_offsets": offsets.tolist(),
            "checkpoint": ckpt_path, "viz_dir": viz_dir, "per_ct_f1": per_ct_f1,
            "per_ct_f1_vanilla": per_ct_f1_vanilla,
            "per_class_f1": per_class_f1,
            "per_class_f1_vanilla": per_class_f1_vanilla,
            "attn": attn, "film": film,
            "best_val_loss": best_loss, "stop_epoch": epoch,
            "n_params": n_params, "dims": dims,
            "train_f1_at_best_val": train_f1_at_best,
            "swa_enabled": swa_enabled,
            "selected": selected,
            "val_metrics_vanilla": val_metrics_vanilla,
            "val_metrics_swa": val_metrics_swa,
            "test_metrics_vanilla": test_metrics_vanilla,
            "test_metrics_swa": test_metrics_swa,
            "n_swa_avg": n_swa_avg}
 
 
def summarize_cv(results):
    swa_results = [r for r in results if r.get("swa_enabled")]
    is_swa = len(swa_results) > 0
    selected_label = "SWA (always-pick v3)" if is_swa else "vanilla (best-ckpt)"

    # ── 1. Headline: 5-fold CV summary of selected model ──
    print(f"\n\U0001f4c8 5-fold CV summary — model = {selected_label}")
    metric_names = ["accuracy", "precision", "recall", "f1", "f1_weighted"]
    for name in metric_names:
        vals = np.array([r["test_metrics"].get(name) for r in results
                         if r["test_metrics"].get(name) is not None])
        if not vals.size:
            continue
        label = name.upper()
        if name == "f1":
            cal_vals = np.array([r.get("test_metrics_calibrated", {}).get("f1", 0) for r in results])
            gain = cal_vals.mean() - vals.mean()
            print(f"  {label:11s}: mean={vals.mean():.4f}  std={vals.std(ddof=0):.4f}  "
                  f"| cal={cal_vals.mean():.4f} ({gain:+.4f})")
        else:
            print(f"  {label:11s}: mean={vals.mean():.4f}  std={vals.std(ddof=0):.4f}")

    # ── 2. Vanilla vs SWA comparison (chỉ khi SWA enabled) ──
    if is_swa:
        n_avg = np.array([r["n_swa_avg"] for r in swa_results])
        print(f"\n\U0001fab6 Vanilla vs SWA — 5-fold mean ± std  "
              f"({n_avg.mean():.1f} snapshots/fold avg, range=[{int(n_avg.min())},{int(n_avg.max())}])")
        print(f"  {'split':<5s} {'metric':<4s}  {'vanilla':>16s}  {'SWA':>16s}  {'Δ mean':>+8s}  {'Δ std':>+8s}")
        for split, key_van, key_swa in [
            ("val ",  "val_metrics_vanilla",  "val_metrics_swa"),
            ("test",  "test_metrics_vanilla", "test_metrics_swa"),
        ]:
            for metric, mlabel in (("accuracy", "Acc"), ("f1_weighted", "F1w"), ("f1", "F1m")):
                van = np.array([r[key_van].get(metric, 0) for r in swa_results])
                sw  = np.array([r[key_swa].get(metric, 0) for r in swa_results
                                if r.get(key_swa) is not None])
                if not sw.size:
                    continue
                d_mean = sw.mean() - van.mean()
                d_std  = sw.std(ddof=0) - van.std(ddof=0)
                print(f"  {split} {mlabel:<3s}   "
                      f"{van.mean():.4f} ± {van.std(ddof=0):.4f}  "
                      f"{sw.mean():.4f} ± {sw.std(ddof=0):.4f}  "
                      f"{d_mean:+.4f}  {d_std:+.4f}")

    # ── 3. Per-cancer-type F1 ──
    all_per_ct = [r.get("per_ct_f1", {}) for r in results]
    unique_cts = sorted(set().union(*[d.keys() for d in all_per_ct]))
    if len(unique_cts) > 1:
        if is_swa:
            all_per_ct_van = [r.get("per_ct_f1_vanilla", {}) for r in results]
            print(f"\n\U0001f9ec Per-cancer-type F1 (5-fold mean ± std) — vanilla vs SWA:")
            print(f"  {'Cancer':>8}  {'N/fold':>6}  {'vanilla':>16s}  {'SWA':>16s}  {'Δ mean':>+8s}")
            for ct in unique_cts:
                van_vals = np.array([d[ct]["f1"] for d in all_per_ct_van if ct in d])
                sw_vals  = np.array([d[ct]["f1"] for d in all_per_ct     if ct in d])
                n_vals   = np.array([d[ct]["n"]  for d in all_per_ct     if ct in d])
                if not (van_vals.size and sw_vals.size):
                    continue
                d_mean = sw_vals.mean() - van_vals.mean()
                print(f"  {ct:>8}  {n_vals.mean():>6.1f}  "
                      f"{van_vals.mean():.4f} ± {van_vals.std(ddof=0):.4f}  "
                      f"{sw_vals.mean():.4f} ± {sw_vals.std(ddof=0):.4f}  "
                      f"{d_mean:+.4f}")
        else:
            print(f"\n\U0001f9ec Per-cancer-type F1 (5-fold mean ± std):")
            print(f"  {'Cancer':>8}  {'N/fold':>6}  {'F1 mean':>8}  {'F1 std':>7}")
            for ct in unique_cts:
                f1_vals = np.array([d[ct]["f1"] for d in all_per_ct if ct in d])
                n_vals  = np.array([d[ct]["n"]  for d in all_per_ct if ct in d])
                print(f"  {ct:>8}  {n_vals.mean():>6.1f}  {f1_vals.mean():>8.4f}  {f1_vals.std(ddof=0):>7.4f}")

    # ── 4. Per-class F1 ──
    num_classes = max((max(r.get("per_class_f1", {0: 0}).keys()) for r in results), default=-1) + 1
    if num_classes > 0:
        if is_swa:
            print(f"\n🎯 Per-class F1 (5-fold mean ± std) — vanilla vs SWA:")
            print(f"  {'Class':>5}  {'vanilla':>16s}  {'SWA':>16s}  {'Δ mean':>+8s}")
            for class_idx in range(num_classes):
                van = np.array([r["per_class_f1_vanilla"].get(class_idx, 0) for r in results
                                if r.get("per_class_f1_vanilla")])
                sw  = np.array([r["per_class_f1"].get(class_idx, 0) for r in results
                                if class_idx in r.get("per_class_f1", {})])
                if not sw.size:
                    continue
                d_mean = sw.mean() - van.mean() if van.size else 0
                print(f"  {class_idx:>5}  "
                      f"{van.mean():.4f} ± {van.std(ddof=0):.4f}  "
                      f"{sw.mean():.4f} ± {sw.std(ddof=0):.4f}  "
                      f"{d_mean:+.4f}")
        else:
            print(f"\n🎯 Per-class F1 (5-fold mean ± std):")
            print(f"  {'Class':>12}  {'F1 mean':>8}  {'F1 std':>7}")
            for class_idx in range(num_classes):
                vals = np.array([r["per_class_f1"][class_idx] for r in results
                                 if class_idx in r.get("per_class_f1", {})])
                if vals.size:
                    print(f"  {class_idx:>12}  {vals.mean():>8.4f}  {vals.std(ddof=0):>7.4f}")

    # ── 5. Attention stats (from selected model) ──
    attn_list = [r.get("attn", {}) for r in results if r.get("attn")]
    if attn_list:
        print(f"\n🔍 Attention Stats (5-fold mean ± std)  [from {selected_label}]:")
        attn_keys = [
            "cpg_std", "cpg_max", "cpg_nnz", "modality_w_cpg",
            "mirna_std", "mirna_max", "mirna_nnz", "modality_w_mirna",
        ]
        for k in attn_keys:
            vals = np.array([a[k] for a in attn_list if k in a])
            if vals.size:
                print(f"  {k:18s}: mean={vals.mean():.4f}  std={vals.std(ddof=0):.4f}")

    # ── 6. FiLM γ, β (from selected model) ──
    film_list = [r.get("film", {}) for r in results if r.get("film")]
    if film_list:
        print(f"\n\U0001f3da️  FiLM γ, β (5-fold mean ± std, baseline γ=1 β=0)  [from {selected_label}]:")
        for k in ["cpg_gamma", "cpg_beta", "mirna_gamma", "mirna_beta"]:
            vals = np.array([f[k] for f in film_list if k in f])
            if vals.size:
                drift = vals.mean() - (1.0 if k.endswith("gamma") else 0.0)
                print(f"  {k:14s}: mean={vals.mean():+.4f}  std={vals.std(ddof=0):.4f}  drift={drift:+.4f}")

    # ── 7. Model size & feature counts ──
    n_params_list = [r.get("n_params") for r in results if r.get("n_params")]
    dims_list = [r.get("dims") for r in results if r.get("dims")]
    if n_params_list and dims_list:
        print(f"\n📐 Model & Features (5-fold mean):")
        print(f"  Params       : {int(np.mean(n_params_list)):,}")
        print(f"  Gene feats   : {int(np.mean([d['gene'] for d in dims_list])):,}")
        print(f"  Meth feats   : {int(np.mean([d['meth'] for d in dims_list])):,}")
        print(f"  miRNA feats  : {int(np.mean([d['mirna'] for d in dims_list])):,}")

    # ── 8. Overfit indicator (vanilla training trajectory — luôn dùng vanilla
    #    để gap interpretation nhất quán, kể cả khi SWA picked) ──
    train_f1s    = [r.get("train_f1_at_best_val") for r in results if r.get("train_f1_at_best_val") is not None]
    test_f1_van  = [r["test_metrics_vanilla"]["f1"] for r in results if r.get("test_metrics_vanilla")]
    val_f1_van   = [r["val_metrics_vanilla"]["f1"]  for r in results if r.get("val_metrics_vanilla")]
    test_f1_swa  = [r["test_metrics_swa"]["f1"]     for r in results if r.get("test_metrics_swa")]
    stop_epochs  = [r.get("stop_epoch") for r in results if r.get("stop_epoch") is not None]
    if train_f1s and val_f1_van and test_f1_van:
        tf = np.array(train_f1s); vv = np.array(val_f1_van); tev = np.array(test_f1_van)
        print(f"\n⚖️  Overfit indicator (vanilla training trajectory, 5-fold):")
        print(f"  Train F1 (at best val) : mean={tf.mean():.4f}  std={tf.std(ddof=0):.4f}")
        print(f"  Vanilla Val F1         : mean={vv.mean():.4f}  std={vv.std(ddof=0):.4f}")
        print(f"  Vanilla Test F1        : mean={tev.mean():.4f}  std={tev.std(ddof=0):.4f}")
        if test_f1_swa:
            tes = np.array(test_f1_swa)
            print(f"  SWA Test F1            : mean={tes.mean():.4f}  std={tes.std(ddof=0):.4f}  Δ vs vanilla = {tes.mean()-tev.mean():+.4f}")
        print(f"  Train−Val gap          : mean={(tf-vv).mean():+.4f}  (gap > 0.20 → strong overfit)")
        print(f"  Val−Test gap (vanilla) : mean={(vv-tev).mean():+.4f}  (gap > 0.05 → val không đại diện)")
        if stop_epochs:
            se = np.array(stop_epochs)
            print(f"  Stop epoch             : mean={se.mean():.1f}  range=[{se.min()},{se.max()}]")


def main():
    args = parse_args()
    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    # CLI overrides (cho multi-seed runs)
    if args.seed is not None:
        cfg["training"]["seed"] = args.seed
        print(f"\U0001f527 Override seed = {args.seed}")
    if args.save_dir is not None:
        cfg["logging"]["save_dir"] = args.save_dir
        print(f"\U0001f527 Override save_dir = {args.save_dir}")

    seed = cfg["training"]["seed"]
    set_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\U0001f5a5\ufe0f  Device: {device}  |  Seed: {seed}")

    test_cohort = cfg.get("data", {}).get("test_cohort")
    cv_folds = args.cv_folds or cfg.get("preprocessing", {}).get("cv_folds", 5)

    if test_cohort:
        datasets, feature_names, dims, metadata = build_fixed_cohort_test_datasets(cfg, seed)
        print(f"\n\U0001f4d0 Dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
        fit_one_split(cfg, datasets, feature_names, dims, metadata, device,
                      f"Fixed-test {test_cohort}")
    elif cv_folds and cv_folds > 1:
        fold_packages = build_cv_datasets(cfg, seed, n_splits=cv_folds)
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
        datasets, feature_names, dims, metadata = build_datasets(cfg, seed)
        print(f"\n\U0001f4d0 Dims: gene={dims['gene']}, meth={dims['meth']}, mirna={dims['mirna']}")
        fit_one_split(cfg, datasets, feature_names, dims, metadata, device, "Single split")
 
 
if __name__ == "__main__":
    main()
