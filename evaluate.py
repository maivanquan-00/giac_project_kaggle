"""
evaluate.py
-----------
Evaluate model đã train + xuất top-K gene per patient.
Chạy sau khi đã có checkpoint từ train.py:

  !python evaluate.py --config configs/config.yaml --checkpoint checkpoints/best_model.pt
"""

import argparse
import yaml
import json
import pandas as pd
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report

from src.data.dataset        import build_datasets
from src.data.graph_builder  import build_hetero_graph
from src.model               import GIACModel
from src.models.sparse_attention import get_top_k_features
from src.utils               import set_seed, compute_metrics, print_metrics


SUBTYPE_NAMES = {0: "CIN", 1: "GS", 2: "MSI", 3: "HM-SNV", 4: "EBV"}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config",     default="configs/config.yaml")
    parser.add_argument("--checkpoint", default="checkpoints/best_model.pt")
    parser.add_argument("--split",      default="test", choices=["val", "test"])
    parser.add_argument("--top_k",      type=int, default=50)
    return parser.parse_args()


@torch.no_grad()
def evaluate_with_interpretability(model, loader, graph, feature_names, top_k, device):
    model.eval()

    all_preds, all_labels    = [], []
    all_gene_features        = []   # top-K gene per patient
    all_meth_features        = []
    all_mirna_features       = []

    for batch in loader:
        batch = {k: v.to(device) for k, v in batch.items()}

        logits, sparse_weights, mod_w = model(
            batch, graph, return_interpretability=True
        )
        preds = logits.argmax(dim=-1).cpu().tolist()
        all_preds.extend(preds)
        all_labels.extend(batch["label"].cpu().tolist())

        # Trích xuất top-K features cho batch này
        top_features = get_top_k_features(sparse_weights, feature_names, k=top_k)
        all_gene_features.extend(top_features["gene"])
        all_meth_features.extend(top_features["meth"])
        all_mirna_features.extend(top_features["mirna"])

    metrics = compute_metrics(all_labels, all_preds)
    print("\n📋 Classification Report:")
    print(classification_report(
        all_labels, all_preds,
        target_names=[SUBTYPE_NAMES[i] for i in range(5)],
        digits=4,
    ))

    return metrics, {
        "gene":  all_gene_features,
        "meth":  all_meth_features,
        "mirna": all_mirna_features,
        "labels": all_labels,
        "preds":  all_preds,
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
    ckpt  = torch.load(args.checkpoint, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    print(f"✅ Loaded: {args.checkpoint}")

    # ── Evaluate ─────────────────────────────────────────────────────
    metrics, interp = evaluate_with_interpretability(
        model, loader, graph, feature_names, args.top_k, device
    )
    print_metrics(metrics, args.split.capitalize())

    # In modality weights của model
    w = model.sparse_cross_attn.modality_weights.detach().cpu()
    print(f"\n🔬 Modality weights (learned):")
    print(f"   Gene expression : {w[0]:.4f}")
    print(f"   DNA methylation : {w[1]:.4f}")
    print(f"   miRNA           : {w[2]:.4f}")

    # ── Xuất patient report ──────────────────────────────────────────
    save_patient_report(interp, output_path="patient_features.csv")

    # ── Summary: top genes overall ───────────────────────────────────
    print("\n🧬 Top 20 genes xuất hiện nhiều nhất trên toàn bộ bệnh nhân:")
    from collections import Counter
    all_genes = []
    for patient_genes in interp["gene"]:
        all_genes.extend([g for g, _ in patient_genes])
    top20 = Counter(all_genes).most_common(20)
    for gene, count in top20:
        print(f"   {gene:20s}  {count} patients")


if __name__ == "__main__":
    main()
