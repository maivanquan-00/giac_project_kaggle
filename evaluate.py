"""
evaluate.py
-----------
Evaluate model đã train + xuất top-K gene per patient.
Chạy sau khi đã có checkpoint từ train.py:

  !python evaluate.py --config configs/config.yaml --checkpoint checkpoints/best_model.pt
"""

import argparse
import glob
import os
import yaml
import json
import pandas as pd
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report

from src.data.dataset        import build_datasets
from src.data.graph_builder  import build_hetero_graph
from src.model               import GIACModel
from src.utils               import set_seed, compute_metrics, print_metrics


SUBTYPE_NAMES = {0: "CIN", 1: "GS", 2: "MSI", 3: "HM-SNV", 4: "EBV"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",     default="configs/config.yaml")
    parser.add_argument("--checkpoint", default=None)
    parser.add_argument("--split",      default="test", choices=["val", "test"])
    parser.add_argument("--top_k",      type=int, default=50)
    return parser.parse_args()


def resolve_checkpoint_path(cfg: dict, user_checkpoint: str | None) -> str:
    if user_checkpoint:
        return user_checkpoint

    save_dir = cfg.get("logging", {}).get("save_dir", "checkpoints")
    default_ckpt = os.path.join(save_dir, "best_model.pt")
    if os.path.exists(default_ckpt):
        return default_ckpt

    fold_ckpts = sorted(glob.glob(os.path.join(save_dir, "best_model_fold_*.pt")))
    if fold_ckpts:
        return fold_ckpts[0]

    raise FileNotFoundError(
        "Không tìm thấy checkpoint. Hãy truyền --checkpoint hoặc kiểm tra logging.save_dir."
    )


@torch.no_grad()
def evaluate_with_interpretability(model, loader, graph, feature_names, top_k, device):
    model.eval()

    all_preds, all_labels = [], []
    all_patient_gates = []   # (N, 3) gate weights per patient

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}

        logits, _, mod_w = model(
            batch, graph, return_interpretability=True
        )
        preds = logits.argmax(dim=-1).cpu().tolist()
        all_preds.extend(preds)
        all_labels.extend(batch["label"].cpu().tolist())
        all_patient_gates.append(mod_w["patient"].cpu())

    import torch as _torch
    gates = _torch.cat(all_patient_gates, dim=0)  # (N, 3)

    metrics = compute_metrics(all_labels, all_preds)
    print("\n📋 Classification Report:")
    print(classification_report(
        all_labels, all_preds,
        target_names=[SUBTYPE_NAMES[i] for i in range(5)],
        digits=4,
    ))

    return metrics, {
        "labels": all_labels,
        "preds":  all_preds,
        "gates":  gates,  # (N, 3) — gene / meth / mirna gate weights
    }


def save_patient_report(interpretability_data: dict, output_path: str = "patient_features.csv"):
    """
    Xuất CSV: mỗi hàng là một bệnh nhân, gồm:
      - true_subtype, pred_subtype
      - top_genes (list), top_cpgs (list), top_mirnas (list)
    """
    rows = []
    n = len(interpretability_data["labels"])

    for i in range(n):
        # Format top features thành string "GENE:weight"
        def fmt(feat_list):
            return "; ".join([f"{f}:{w:.4f}" for f, w in feat_list[:10]])  # top 10 hiển thị

        rows.append({
            "patient_idx":   i,
            "true_subtype":  SUBTYPE_NAMES[interpretability_data["labels"][i]],
            "pred_subtype":  SUBTYPE_NAMES[interpretability_data["preds"][i]],
            "correct":       interpretability_data["labels"][i] == interpretability_data["preds"][i],
            "top_genes":     fmt(interpretability_data["gene"][i]),
            "top_cpgs":      fmt(interpretability_data["meth"][i]),
            "top_mirnas":    fmt(interpretability_data["mirna"][i]),
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    print(f"\n💾 Patient feature report saved: {output_path}")
    return df


def main():
    args = parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    set_seed(cfg["training"]["seed"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ── Data & Graph ─────────────────────────────────────────────────
    datasets, feature_names, dims, _ = build_datasets(cfg["data"], cfg["training"]["seed"])
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))

    loader = DataLoader(datasets[args.split], batch_size=32, shuffle=False)

    # ── Load model ────────────────────────────────────────────────────
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
    checkpoint_path = resolve_checkpoint_path(cfg, args.checkpoint)
    ckpt  = torch.load(checkpoint_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    print(f"✅ Loaded: {checkpoint_path}")

    # ── Evaluate ─────────────────────────────────────────────────────
    metrics, interp = evaluate_with_interpretability(
        model, loader, graph, feature_names, args.top_k, device
    )
    print_metrics(metrics, args.split.capitalize())

    # In patient gate statistics
    gates = interp["gates"]  # (N, 3)
    print(f"\n🔍 Patient Modality Gate Statistics (N={gates.shape[0]})")
    for i, name in enumerate(["Gene expression", "DNA methylation", "miRNA"]):
        print(f"   {name:20s}: mean={gates[:,i].mean():.4f}  std={gates[:,i].std():.4f}")

    # ── Summary: correct vs incorrect predictions ──────────────────────
    import torch as _torch
    labels_t = _torch.tensor(interp["labels"])
    preds_t  = _torch.tensor(interp["preds"])
    correct  = (labels_t == preds_t)
    print(f"\n✔️  Accuracy: {correct.float().mean().item():.4f}")
    print(f"   Correct: {correct.sum().item()} / {len(correct)}")


if __name__ == "__main__":
    main()
