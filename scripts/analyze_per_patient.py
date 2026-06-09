"""
analyze_per_patient.py
----------------------
Phân tích interpretability PER-BỆNH-NHÂN của GIAC (không cần train lại).

Cho mỗi bệnh nhân trong test set: trích cross-attention (cpg/mirna), map về TÊN
feature thật (CpG probe / miRNA), và tính các chỉ số trả lời 3 câu:
  1. Attention có "cá thể" không?  -> mỗi bệnh nhân chú ý feature khác nhau (distinct top-1).
  2. Có "random/pick bừa" không?   -> độ tập trung (max-attn, effective tokens). Cao = KHÔNG random.
  3. Có ý nghĩa sinh học không?     -> bệnh nhân cùng subtype có chụm vào feature chung không.

Cách chạy (từ gốc repo):
    python scripts/analyze_per_patient.py --ckpt-dir ckpt/ir03 --cv-folds 5
    # seed mặc định lấy từ config lưu trong checkpoint.

Output (trong <ckpt-dir>/interpretability/):
    per_patient.csv          — mỗi dòng 1 bệnh nhân: top-N CpG/miRNA + trọng số + đúng/sai
    subtype_top_features.csv — feature được chú ý nhiều nhất theo từng subtype
    diversity_summary.json   — metric cá thể/độ tập trung/độ chụm theo subtype
    subtype_attention_heatmap.png (nếu có matplotlib)
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict

import numpy as np
import torch

# Cho phép chạy trực tiếp `python scripts/analyze_per_patient.py` từ gốc repo:
# thêm thư mục gốc repo (cha của scripts/) vào sys.path để import được `src`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data.dataset import build_cv_datasets
from src.data.graph_builder import build_hetero_graph
from src.model import GIACModel
from src.utils import set_seed


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--ckpt-dir", required=True,
                   help="Thư mục chứa best_model_fold_1.pt ... (save_dir lúc train).")
    p.add_argument("--cv-folds", type=int, default=5)
    p.add_argument("--seed", type=int, default=None,
                   help="Mặc định lấy từ config trong checkpoint (phải khớp lúc train).")
    p.add_argument("--out-dir", type=str, default=None)
    p.add_argument("--topn", type=int, default=5, help="Số feature top hiển thị mỗi bệnh nhân.")
    return p.parse_args()


def _ckpt_path(ckpt_dir, fold):
    return os.path.join(ckpt_dir, f"best_model_fold_{fold}.pt")


@torch.no_grad()
def run_fold(cfg, fold_pkg, ckpt_path, device, topn):
    datasets, feature_names, dims, _ = fold_pkg["datasets"]
    test = datasets["test"]
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device=str(device))
    model = GIACModel(dims, cfg["model"], cfg["training"]).to(device)
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    model.load_state_dict(ckpt["model"])
    model.eval()

    batch = {k: getattr(test, k).to(device) for k in ("gene", "meth", "mirna")}
    batch["label"] = test.label.to(device)
    logits, _, attn = model(batch, graph, return_interpretability=True)

    preds = logits.argmax(-1).cpu().numpy()
    labels = test.label.numpy()
    cpg_attn = attn["cpg_attn"].cpu()        # (N, K_seq)
    mir_attn = attn["mirna_attn"].cpu()
    mw = attn["modality_weights"].cpu().numpy().tolist()

    meth, mirna = test.meth, test.mirna       # (N, n_feat) đã z-score
    K = cfg["model"].get("topk_seq", 32)

    # Nếu bật modality_summary thì token đầu là summary -> bỏ để khớp top-K.
    def _strip_summary(a, k_real):
        return a[:, 1:] if a.shape[1] == k_real + 1 else a
    k_meth = min(K, meth.shape[1])
    k_mir = min(K, mirna.shape[1])
    cpg_attn = _strip_summary(cpg_attn, k_meth)
    mir_attn = _strip_summary(mir_attn, k_mir)

    rows = []
    for i in range(len(labels)):
        # top-K idx PHẢI tái lập đúng cách model chọn: |value| giảm dần (sorted=True).
        cpg_idx = meth[i].abs().topk(k_meth).indices.tolist()
        mir_idx = mirna[i].abs().topk(k_mir).indices.tolist()
        cpg_pairs = [(feature_names["meth"][cpg_idx[j]], float(cpg_attn[i, j])) for j in range(k_meth)]
        mir_pairs = [(feature_names["mirna"][mir_idx[j]], float(mir_attn[i, j])) for j in range(k_mir)]
        cpg_pairs.sort(key=lambda x: -x[1])
        mir_pairs.sort(key=lambda x: -x[1])
        rows.append({
            "patient_id": test.patient_ids[i],
            "cancer_type": test.cancer_types[i] if test.cancer_types else "",
            "true": int(labels[i]),
            "pred": int(preds[i]),
            "correct": int(labels[i] == preds[i]),
            "w_cpg": round(mw[0], 4),
            "w_mirna": round(mw[1], 4),
            "cpg_attn_vec": cpg_attn[i].numpy(),
            "mir_attn_vec": mir_attn[i].numpy(),
            "top_cpg": cpg_pairs[:topn],
            "top_mirna": mir_pairs[:topn],
        })
    return rows


def _concentration(vecs):
    """Trả mean max-attn, mean effective #tokens (1/sum p^2), mean nnz."""
    maxs, eff, nnz = [], [], []
    for v in vecs:
        v = np.asarray(v, dtype=np.float64)
        s = v.sum()
        if s <= 0:
            continue
        p = v / s
        maxs.append(p.max())
        eff.append(1.0 / np.square(p).sum())
        nnz.append(float((v > 1e-6).mean()))
    return {
        "mean_max_attn": round(float(np.mean(maxs)), 4),
        "mean_effective_tokens": round(float(np.mean(eff)), 2),
        "mean_nnz_frac": round(float(np.mean(nnz)), 4),
        "K": len(np.asarray(vecs[0])) if vecs else 0,
    }


def diversity_report(rows, subtype_names):
    out = {}
    for mod, key in (("cpg", "top_cpg"), ("mirna", "top_mirna")):
        top1 = [r[key][0][0] for r in rows if r[key]]
        n = len(top1)
        distinct = len(set(top1))
        vecs = [r["cpg_attn_vec" if mod == "cpg" else "mir_attn_vec"] for r in rows]
        conc = _concentration(vecs)
        # Độ chụm theo subtype: với mỗi subtype, feature top-1 phổ biến nhất + tỷ lệ.
        by_sub = defaultdict(list)
        for r in rows:
            if r[key]:
                by_sub[r["true"]].append(r[key][0][0])
        sub_concentration = {}
        for s, feats in by_sub.items():
            c = Counter(feats).most_common(1)[0]
            name = subtype_names[s] if s < len(subtype_names) else f"class{s}"
            sub_concentration[name] = {
                "n_patients": len(feats),
                "top1_feature": c[0],
                "top1_share": round(c[1] / len(feats), 3),
            }
        out[mod] = {
            "n_patients": n,
            "distinct_top1_features": distinct,
            "distinct_top1_frac": round(distinct / max(n, 1), 3),
            "concentration": conc,
            "per_subtype_top1": sub_concentration,
        }
    return out


def write_per_patient_csv(rows, path, topn):
    cols = (["patient_id", "cancer_type", "true_subtype", "pred_subtype", "correct",
             "w_cpg", "w_mirna"]
            + [f"cpg_top{j+1}" for j in range(topn)]
            + [f"mirna_top{j+1}" for j in range(topn)])
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            cpg = [f"{n}:{a:.3f}" for n, a in r["top_cpg"]] + [""] * topn
            mir = [f"{n}:{a:.3f}" for n, a in r["top_mirna"]] + [""] * topn
            w.writerow([r["patient_id"], r["cancer_type"], r["true"], r["pred"], r["correct"],
                        r["w_cpg"], r["w_mirna"], *cpg[:topn], *mir[:topn]])


def write_subtype_top_csv(rows, path, subtype_names, topk=10):
    # Gom mean attention theo (subtype, feature) cho cả 2 modality.
    agg = defaultdict(lambda: defaultdict(list))   # subtype -> feat -> [attn...]
    for r in rows:
        for n, a in r["top_cpg"]:
            agg[r["true"]][("cpg", n)].append(a)
        for n, a in r["top_mirna"]:
            agg[r["true"]][("mirna", n)].append(a)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["subtype", "modality", "feature", "mean_attn", "n_patients_selected"])
        for s in sorted(agg):
            name = subtype_names[s] if s < len(subtype_names) else f"class{s}"
            ranked = sorted(agg[s].items(), key=lambda kv: -np.mean(kv[1]))[:topk]
            for (mod, feat), vals in ranked:
                w.writerow([name, mod, feat, round(float(np.mean(vals)), 4), len(vals)])


def maybe_heatmap(rows, subtype_names, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"  (bỏ heatmap, thiếu matplotlib: {e})")
        return
    # Top-15 CpG theo tổng attention toàn bộ; ma trận subtype × feature.
    totals = defaultdict(float)
    for r in rows:
        for n, a in r["top_cpg"]:
            totals[n] += a
    top_feats = [n for n, _ in sorted(totals.items(), key=lambda kv: -kv[1])[:15]]
    subs = sorted({r["true"] for r in rows})
    mat = np.zeros((len(subs), len(top_feats)))
    cnt = np.zeros_like(mat)
    for r in rows:
        si = subs.index(r["true"])
        d = dict(r["top_cpg"])
        for fi, fn in enumerate(top_feats):
            if fn in d:
                mat[si, fi] += d[fn]; cnt[si, fi] += 1
    mat = np.divide(mat, np.maximum(cnt, 1))
    fig, ax = plt.subplots(figsize=(max(8, len(top_feats) * 0.6), 0.6 * len(subs) + 2))
    im = ax.imshow(mat, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(top_feats))); ax.set_xticklabels(top_feats, rotation=90, fontsize=7)
    ax.set_yticks(range(len(subs)))
    ax.set_yticklabels([subtype_names[s] if s < len(subtype_names) else f"class{s}" for s in subs])
    ax.set_title("Mean CpG attention theo subtype (top-15 CpG)")
    fig.colorbar(im, ax=ax, fraction=0.025)
    fig.tight_layout(); fig.savefig(path, dpi=150); plt.close(fig)
    print(f"  Saved heatmap: {path}")


def main():
    args = parse_args()
    # Lấy config TỪ checkpoint để kiến trúc khớp tuyệt đối với lúc train.
    probe = torch.load(_ckpt_path(args.ckpt_dir, 1), map_location="cpu", weights_only=False)
    cfg = probe["config"]
    seed = args.seed if args.seed is not None else cfg["training"]["seed"]
    set_seed(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    subtype_names = cfg["training"].get("subtype_names", [])
    out_dir = args.out_dir or os.path.join(args.ckpt_dir, "interpretability")
    os.makedirs(out_dir, exist_ok=True)
    print(f"Device: {device} | Seed: {seed} | ckpt-dir: {args.ckpt_dir}")
    if cfg["model"].get("topk_selection", "zscore") == "random":
        print("  ⚠️  topk_selection=random → mapping feature KHÔNG đáng tin (chọn ngẫu nhiên mỗi forward).")

    folds = build_cv_datasets(cfg, seed, n_splits=args.cv_folds)
    all_rows = []
    for fp in folds:
        path = _ckpt_path(args.ckpt_dir, fp["fold"])
        if not os.path.isfile(path):
            print(f"  ⚠️  thiếu {path} — bỏ fold {fp['fold']}")
            continue
        print(f"Fold {fp['fold']}: phân tích {len(fp['datasets'][0]['test'])} bệnh nhân test...")
        all_rows.extend(run_fold(cfg, fp, path, device, args.topn))

    if not all_rows:
        print("Không có dữ liệu (thiếu checkpoint?). Dừng.")
        return

    write_per_patient_csv(all_rows, os.path.join(out_dir, "per_patient.csv"), args.topn)
    write_subtype_top_csv(all_rows, os.path.join(out_dir, "subtype_top_features.csv"), subtype_names)
    div = diversity_report(all_rows, subtype_names)
    with open(os.path.join(out_dir, "diversity_summary.json"), "w", encoding="utf-8") as f:
        json.dump(div, f, indent=2, ensure_ascii=False)
    maybe_heatmap(all_rows, subtype_names, os.path.join(out_dir, "subtype_attention_heatmap.png"))

    # ── In tóm tắt trả lời 3 câu ──
    print(f"\n===== TÓM TẮT INTERPRETABILITY ({len(all_rows)} bệnh nhân) =====")
    for mod in ("cpg", "mirna"):
        d = div[mod]; c = d["concentration"]
        print(f"\n[{mod.upper()}]")
        print(f"  Cá thể?  distinct top-1 = {d['distinct_top1_features']}/{d['n_patients']} "
              f"({d['distinct_top1_frac']*100:.0f}% bệnh nhân có feature top-1 KHÁC nhau)")
        print(f"  Random?  max-attn TB = {c['mean_max_attn']}  |  effective tokens = "
              f"{c['mean_effective_tokens']}/{c['K']}  (thấp = tập trung, KHÔNG random)")
        print(f"  Theo subtype (feature top-1 phổ biến nhất + tỷ lệ chụm):")
        for s, info in d["per_subtype_top1"].items():
            print(f"    {s:>8}: {info['top1_feature']:<16} chụm {info['top1_share']*100:.0f}% "
                  f"({info['n_patients']} bn)")
    print(f"\nOutput đã lưu ở: {out_dir}")
    print("Đọc: distinct top-1 cao + max-attn cao + subtype chụm vào feature riêng = interpretable THẬT.")


if __name__ == "__main__":
    main()
