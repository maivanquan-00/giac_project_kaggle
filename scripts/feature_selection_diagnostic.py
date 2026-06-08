"""
feature_selection_diagnostic.py
-------------------------------
Soi phân bố ANOVA F-score để quyết định số features cho mỗi modality —
thay vì đoán top-K. Trả lời 2 câu hỏi:
  1. Đuôi (quanh cutoff top-K hiện tại) còn tín hiệu hay đã là nhiễu?
  2. Bao nhiêu feature thực sự "có ý nghĩa" (pass FDR Benjamini-Hochberg)?

Chạy (trên Kaggle, nơi có data):
    python scripts/feature_selection_diagnostic.py --config configs/config.yaml
    python scripts/feature_selection_diagnostic.py --config configs/config_4class.yaml

Lưu ý: tính F-score trên TOÀN BỘ mẫu đã filter (không split) — đây là diagnostic
để xem phân bố, không phải bước selection (pipeline thật vẫn fit ANOVA trên train
mỗi fold). Phân bố full-data là đại diện tốt để chọn ngưỡng.
"""

import argparse
import os
import sys
import numpy as np
import yaml
from scipy import stats
from sklearn.feature_selection import f_classif

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.data.dataset import load_aligned_data, _get_preprocess_cfg


def benjamini_hochberg(pvals: np.ndarray, alpha: float) -> int:
    """Số test pass FDR-BH ở mức alpha. Trả về số feature significant."""
    m = len(pvals)
    if m == 0:
        return 0
    order = np.argsort(pvals)
    sorted_p = pvals[order]
    thresh = (np.arange(1, m + 1) / m) * alpha
    passed = sorted_p <= thresh
    if not passed.any():
        return 0
    # largest index passing → mọi p nhỏ hơn đều significant
    k_max = np.where(passed)[0].max()
    return int(k_max + 1)


def analyze_modality(name: str, X: np.ndarray, y: np.ndarray, current_top_k, brief: bool = False):
    n_samples, n_total = X.shape
    n_classes = len(np.unique(y))

    # Pre-filter constant features (như pipeline)
    stds = X.std(axis=0, dtype=np.float64)
    var_mask = stds > 1e-10
    Xv = X[:, var_mask]
    n_var = Xv.shape[1]

    F_raw, p_raw = f_classif(Xv, y)
    F = np.nan_to_num(F_raw, nan=0.0, posinf=1e10, neginf=0.0)
    p = np.nan_to_num(p_raw, nan=1.0, posinf=1.0, neginf=0.0)

    F_sorted = np.sort(F)[::-1]   # giảm dần

    # F critical cho p<0.05 / 0.01 (uncorrected) — null mean ≈ 1.0
    df1 = n_classes - 1
    df2 = n_samples - n_classes
    F_crit_05 = stats.f.ppf(0.95, df1, df2)
    F_crit_01 = stats.f.ppf(0.99, df1, df2)

    if brief:
        n_fdr05 = benjamini_hochberg(p, 0.05)
        n_sig = int((F > F_crit_05).sum())   # significant chưa hiệu chỉnh
        if n_var > 5000:
            # pool lớn (gene/CpG): significance bão hoà → giữ top_k thực dụng
            sug = f"signal bão hoà → giữ top_k {current_top_k if current_top_k else 3500}"
        else:
            # pool nhỏ (miRNA): cắt theo số significant
            sug = f"pool nhỏ → cắt mirna_top_k ≈ {n_fdr05}"
        print(f"  {name:5s}: {n_var:>6} var | FDR<0.05={n_fdr05:>6} | F>Fcrit={n_sig:>6} | {sug}")
        return

    print(f"\n{'='*66}")
    print(f"  {name.upper()}  |  {n_total} features ({n_var} biến thiên), "
          f"N={n_samples}, classes={n_classes}")
    print(f"  F_crit: p<0.05 → F>{F_crit_05:.2f}   p<0.01 → F>{F_crit_01:.2f}   (null mean F≈1.0)")
    print(f"{'='*66}")

    # F-score tại các rank
    ranks = [100, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 5000]
    if current_top_k:
        ranks.append(int(current_top_k))
    ranks = sorted(set(r for r in ranks if r <= n_var))
    print("  F-score tại rank (sắp xếp giảm dần):")
    for r in ranks:
        tag = "  ← top_k hiện tại" if current_top_k and r == int(current_top_k) else ""
        noise = "  [≈ nhiễu]" if F_sorted[r - 1] < F_crit_05 else ""
        print(f"    rank {r:>5}:  F = {F_sorted[r-1]:8.2f}{noise}{tag}")

    # Độ phẳng đuôi quanh cutoff hiện tại
    if current_top_k:
        k = int(current_top_k)
        if k < n_var:
            f_at = F_sorted[k - 1]
            f_after = F_sorted[min(k + 500, n_var) - 1]
            drop = (f_at - f_after) / max(f_at, 1e-9) * 100
            print(f"\n  Đuôi quanh cutoff {k}: F[{k}]={f_at:.2f} → F[{min(k+500,n_var)}]={f_after:.2f} "
                  f"(giảm {drop:.0f}% qua 500 feature)")
            if f_at < F_crit_05:
                print(f"    → cutoff đang nằm DƯỚI ngưỡng ý nghĩa (F<{F_crit_05:.2f}) "
                      f"→ đang lấy cả NHIỄU, K quá lớn.")
            elif drop < 5:
                print(f"    → đuôi RẤT PHẲNG (giảm <5%) → còn nhiều feature tương đương, "
                      f"cutoff cứng tuỳ tiện.")
            else:
                print(f"    → vẫn đang dốc → có thể CÒN tín hiệu sau cutoff (K hơi nhỏ?).")

    # Đếm theo ngưỡng
    n_sig_raw = int((p < 0.05).sum())
    n_f_gt2 = int((F > 2).sum())
    n_f_gt5 = int((F > 5).sum())
    n_f_gt10 = int((F > 10).sum())
    print(f"\n  Số feature theo ngưỡng:")
    print(f"    F > 2  : {n_f_gt2:>6}     F > 5 : {n_f_gt5:>6}     F > 10: {n_f_gt10:>6}")
    print(f"    p<0.05 (chưa hiệu chỉnh): {n_sig_raw}")
    print(f"  ── FDR Benjamini-Hochberg (gợi ý SỐ FEATURE nên giữ) ──")
    for a in (0.01, 0.05, 0.10):
        n_fdr = benjamini_hochberg(p, a)
        print(f"    FDR < {a:<4}: {n_fdr:>6} feature significant")

    # Cumulative F-mass
    total_mass = F_sorted.sum()
    for r in [1000, 2000, 3500]:
        if r <= n_var:
            frac = F_sorted[:r].sum() / max(total_mass, 1e-9) * 100
            print(f"  Top-{r} chiếm {frac:.1f}% tổng F-mass")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/config.yaml")
    ap.add_argument("--brief", action="store_true", help="In gọn 1 dòng/modality (số FDR + gợi ý K).")
    args = ap.parse_args()

    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    pre = _get_preprocess_cfg(cfg)

    raw = load_aligned_data(cfg)
    y = raw["labels"]
    dist = dict(zip(*np.unique(y, return_counts=True)))
    print(f"\n📊 {args.config}  |  classes={dist}")

    for name, key, topk_key in [
        ("gene",  "gene",  "gene_top_k"),
        ("meth",  "meth",  "meth_top_k"),
        ("mirna", "mirna", "mirna_top_k"),
    ]:
        analyze_modality(name, raw[key], y, pre.get(topk_key), brief=args.brief)

    if not args.brief:
        print(f"\n{'='*66}")
        print("  ĐỌC KẾT QUẢ:")
        print("  - FDR<0.05 = số feature 'có ý nghĩa thống kê' → ứng viên cho số K.")
        print("  - Nếu F tại cutoff < F_crit → đang lấy nhiễu (giảm K).")
        print("  - Nếu đuôi vẫn dốc / FDR>top_k → đang cắt mất tín hiệu (tăng K).")
        print(f"{'='*66}")


if __name__ == "__main__":
    main()
