"""
run_multi_seed.py
-----------------
Wrapper chạy train.py với nhiều seeds, aggregate kết quả mean ± std.

Usage:
    python run_multi_seed.py --config configs/config.yaml
    python run_multi_seed.py --config configs/config_brca.yaml --seeds 42 123 2024
    python run_multi_seed.py --config configs/config_ucec.yaml --output-dir results/ucec_multiseed

Cơ chế:
    - train.py ghi kết quả tổng hợp ra `<save_dir>/cv_summary.json` mỗi seed.
    - Script này đọc các JSON đó (KHÔNG parse stdout) rồi aggregate qua các seeds.

Output:
    {output_dir}/
      ├── seed_42/checkpoints/cv_summary.json   (do train.py ghi)
      ├── seed_42/stdout.log                     (full log)
      ├── ...
      └── multi_seed_summary.json                (aggregated mean ± std + markdown report)
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import numpy as np


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path tới config YAML")
    parser.add_argument("--seeds", type=int, nargs="+", default=[42, 123, 2024],
                        help="List seeds (default: 42 123 2024)")
    parser.add_argument("--output-dir", default=None,
                        help="Root dir cho output. Default: results/<config_name>_multiseed_<timestamp>")
    parser.add_argument("--cv-folds", type=int, default=None,
                        help="Override cv_folds (pass through to train.py)")
    parser.add_argument("--python", default=sys.executable,
                        help="Python executable (default: current sys.executable)")
    return parser.parse_args()


def aggregate_seeds(seed_metrics, n_folds=5):
    """Aggregate headline metrics qua nhiều seeds dùng law of total variance.

    Input : list các dict {metric: {"mean": x, "std": y}} (1 dict / seed).
    Output: {metric: {mean_of_means, std_of_means, std_pooled, n_seeds,
                      n_total_runs, per_seed_means, per_seed_stds}}

    std_pooled = √(E[within_seed_var] + var(seed_means)) → total std across runs.
    Không dùng 95% CI để giữ convention std chuẩn (đối chiếu MoXGATE baseline).
    """
    if not seed_metrics:
        return {}
    metric_names = sorted(set().union(*[r.keys() for r in seed_metrics if r]))
    out = {}
    for m in metric_names:
        means = [r[m]["mean"] for r in seed_metrics if r and m in r]
        stds  = [r[m].get("std", 0.0) for r in seed_metrics if r and m in r]
        if not means:
            continue
        means_arr = np.array(means)
        stds_arr = np.array(stds)
        within_var  = float((stds_arr ** 2).mean())
        between_var = float(means_arr.std(ddof=0) ** 2)
        std_pooled  = float(np.sqrt(within_var + between_var))
        out[m] = {
            "mean_of_means": float(means_arr.mean()),
            "std_of_means":  float(means_arr.std(ddof=0)),
            "std_pooled":    std_pooled,
            "n_seeds":       len(means),
            "n_total_runs":  len(means) * max(n_folds, 1),
            "per_seed_means": means,
            "per_seed_stds":  stds,
        }
    return out


def load_seed_summary(seed_dir: Path):
    path = seed_dir / "checkpoints" / "cv_summary.json"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    args = parse_args()

    cfg_name = Path(args.config).stem
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_dir = f"results/{cfg_name}_multiseed_{timestamp}"

    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    print(f"Output root: {out_root}")
    print(f"Seeds: {args.seeds}")
    print(f"Config: {args.config}")

    seed_summaries = {}

    for seed in args.seeds:
        seed_dir = out_root / f"seed_{seed}"
        seed_dir.mkdir(exist_ok=True)
        save_dir = seed_dir / "checkpoints"
        log_path = seed_dir / "stdout.log"

        print(f"\n{'='*60}")
        print(f"  Running seed={seed}  ({args.seeds.index(seed)+1}/{len(args.seeds)})")
        print(f"{'='*60}", flush=True)

        cmd = [
            args.python, "-u", "train.py",   # -u = unbuffered → live output
            "--config", args.config,
            "--seed", str(seed),
            "--save-dir", str(save_dir),
        ]
        if args.cv_folds is not None:
            cmd += ["--cv-folds", str(args.cv_folds)]

        print(f"$ {' '.join(cmd)}", flush=True)

        with open(log_path, "w", encoding="utf-8") as log_f:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                encoding="utf-8",
                errors="replace",
            )
            for line in proc.stdout:
                print(line, end="", flush=True)
                log_f.write(line)
            proc.wait()

        if proc.returncode != 0:
            print(f"\nSeed {seed} FAILED with returncode={proc.returncode}")
            continue

        summary = load_seed_summary(seed_dir)
        if summary is None:
            print(f"\nSeed {seed}: không tìm thấy cv_summary.json")
            continue

        seed_summaries[seed] = summary
        m = summary.get("metrics", {})
        print(
            f"\nSeed {seed} done — "
            f"Acc={m.get('accuracy', {}).get('mean', 0):.4f}  "
            f"F1w={m.get('f1_weighted', {}).get('mean', 0):.4f}  "
            f"F1macro={m.get('f1', {}).get('mean', 0):.4f}",
            flush=True,
        )

    if not seed_summaries:
        print("\nKhông có seed nào thành công — không thể aggregate.")
        return

    # ── Aggregate ─────────────────────────────────────────────
    n_folds = max((s.get("n_folds", 5) for s in seed_summaries.values()), default=5)
    is_fixed = n_folds == 1
    aggregated = aggregate_seeds([s.get("metrics", {}) for s in seed_summaries.values()], n_folds=n_folds)

    f1_macro = aggregated.get("f1", {})
    f1_w = aggregated.get("f1_weighted", {})
    acc = aggregated.get("accuracy", {})
    cfg_short = Path(args.config).stem
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    seeds_done = list(seed_summaries.keys())
    n_runs = len(seeds_done) * n_folds

    # ── Markdown report (paste-ready vào docs/RESULTS.md) ──
    print("\n")
    if is_fixed:
        acc_str = f"{acc.get('mean_of_means', 0):.4f} ± {acc.get('std_of_means', 0):.4f}"
        f1w_str = f"{f1_w.get('mean_of_means', 0):.4f} ± {f1_w.get('std_of_means', 0):.4f}"
        print(f"## [{ts}] `{cfg_short}` — Acc: {acc_str}  |  Weighted F1: {f1w_str}")
        runs_label = f"{len(seeds_done)} × 1 fixed-test split"
    else:
        mean_v = f1_macro.get("mean_of_means", 0)
        std_p = f1_macro.get("std_pooled", 0)
        print(f"## [{ts}] `{cfg_short}` — Macro F1: {mean_v:.4f} ± {std_p:.4f} ({n_runs}-run std)")
        runs_label = f"{len(seeds_done)} × {n_folds} folds = {n_runs} runs"
    print()
    print(f"**Config:** `{args.config}`  |  **Seeds:** {seeds_done}  |  **N runs:** {runs_label}")
    print()

    # Headline metrics table
    print("| Metric | Mean ± std | Per-seed means |")
    print("|--------|------------|----------------|")
    for key, label in [
        ("accuracy",    "**Accuracy**"),
        ("f1_weighted", "**Weighted F1**"),
        ("f1",          "Macro F1"),
        ("precision",   "Precision (macro)"),
        ("recall",      "Recall (macro)"),
    ]:
        if key not in aggregated:
            continue
        s = aggregated[key]
        per_seed_str = ", ".join(f"{v:.4f}" for v in s["per_seed_means"])
        std = s["std_of_means"] if is_fixed else s["std_pooled"]
        print(f"| {label} | {s['mean_of_means']:.4f} ± {std:.4f} | {per_seed_str} |")
    print()

    # Per-fold F1 (skip fixed-test: 1 split = per-seed)
    if not is_fixed:
        print("**Per-fold F1 (macro):**")
        print()
        header = "| Seed | " + " | ".join(f"Fold {i+1}" for i in range(n_folds)) + " | Mean |"
        print(header)
        print("|------|" + "|".join("---" for _ in range(n_folds)) + "|------|")
        for seed in seeds_done:
            folds = seed_summaries[seed].get("per_fold_f1", [])
            folds_str = " | ".join(f"{f:.4f}" for f in folds)
            mean = np.mean(folds) if folds else 0
            print(f"| {seed} | {folds_str} | {mean:.4f} |")
        print()

    # Per-cancer-type F1 (multi-cancer)
    seed_per_ct = {seed: seed_summaries[seed].get("per_cancer_type_f1", {}) for seed in seeds_done}
    all_cts = sorted(set().union(*[d.keys() for d in seed_per_ct.values()])) if seed_per_ct else []
    if len(all_cts) > 1:
        print("**Per-cancer-type F1 (mean across seeds):**")
        print()
        print("| Cancer | " + " | ".join(f"Seed {s}" for s in seeds_done) + " | Avg |")
        print("|--------|" + "|".join("---" for _ in seeds_done) + "|------|")
        for ct in all_cts:
            vals, cells = [], []
            for seed in seeds_done:
                if ct in seed_per_ct[seed]:
                    v = seed_per_ct[seed][ct]["f1_mean"]
                    vals.append(v)
                    cells.append(f"{v:.4f}")
                else:
                    cells.append("—")
            avg = np.mean(vals) if vals else 0
            print(f"| {ct} | " + " | ".join(cells) + f" | {avg:.4f} |")
        print()

    # Per-class F1
    seed_per_class = {seed: seed_summaries[seed].get("per_class_f1", {}) for seed in seeds_done}
    class_names = next(iter(seed_summaries.values())).get("class_names", [])
    all_classes = sorted(set().union(*[d.keys() for d in seed_per_class.values()]), key=int) if seed_per_class else []
    if all_classes:
        print("**Per-class F1 (mean across seeds):**")
        print()
        print("| Class | " + " | ".join(f"Seed {s}" for s in seeds_done) + " | Avg |")
        print("|-------|" + "|".join("---" for _ in seeds_done) + "|------|")
        for cls in all_classes:
            vals, cells = [], []
            for seed in seeds_done:
                if cls in seed_per_class[seed]:
                    v = seed_per_class[seed][cls]["mean"]
                    vals.append(v)
                    cells.append(f"{v:.4f}")
                else:
                    cells.append("—")
            avg = np.mean(vals) if vals else 0
            name = class_names[int(cls)] if int(cls) < len(class_names) else f"class {cls}"
            print(f"| {cls} ({name}) | " + " | ".join(cells) + f" | {avg:.4f} |")
        print()

    # Attention stats
    seed_attn = {seed: seed_summaries[seed].get("attention", {}) for seed in seeds_done}
    if any(seed_attn.values()):
        print("**Attention stats (mean across seeds):**")
        print()
        print("| Modality | std | max | nnz | global w |")
        print("|---|---|---|---|---|")
        for mod in ["cpg", "mirna"]:
            row = [mod]
            for stat in ["std", "max", "nnz"]:
                key = f"{mod}_{stat}"
                vals = [seed_attn[s][key]["mean"] for s in seeds_done if key in seed_attn[s]]
                row.append(f"{np.mean(vals):.3f}" if vals else "—")
            gkey = f"modality_w_{mod}"
            gvals = [seed_attn[s][gkey]["mean"] for s in seeds_done if gkey in seed_attn[s]]
            row.append(f"{np.mean(gvals):.3f}" if gvals else "—")
            print("| " + " | ".join(row) + " |")
        print()

    # Overfit indicator
    seed_overfit = {seed: seed_summaries[seed].get("overfit", {}) for seed in seeds_done}
    if any(seed_overfit.values()):
        print("**Overfit indicator (mean across seeds):**")
        print()
        print("| Metric | Value | Note |")
        print("|---|---|---|")
        for k, label in [("train_f1", "Train F1 (at best val)"),
                         ("val_f1", "Val F1"),
                         ("test_f1", "Test F1")]:
            vals = [seed_overfit[s][k]["mean"] for s in seeds_done if k in seed_overfit[s]]
            if vals:
                print(f"| {label} | {np.mean(vals):.4f} |  |")
        tv = [seed_overfit[s]["train_val_gap"] for s in seeds_done if "train_val_gap" in seed_overfit[s]]
        if tv:
            g = np.mean(tv)
            note = "OK" if g < 0.10 else ("overfit nhẹ" if g < 0.20 else "overfit mạnh")
            print(f"| Train−Val gap | {g:+.4f} | {note} |")
        vt = [seed_overfit[s]["val_test_gap"] for s in seeds_done if "val_test_gap" in seed_overfit[s]]
        if vt:
            g = np.mean(vt)
            note = "OK" if abs(g) < 0.05 else "val không đại diện test"
            print(f"| Val−Test gap | {g:+.4f} | {note} |")
        stops = [seed_overfit[s]["stop_epoch"]["mean"] for s in seeds_done if "stop_epoch" in seed_overfit[s]]
        if stops:
            print(f"| Stop epoch (mean) | {np.mean(stops):.1f} | sớm = nghi ngờ overfit |")
        print()

    # Model & features
    seed_mf = {seed: seed_summaries[seed].get("model_features", {}) for seed in seeds_done}
    first_mf = next((v for v in seed_mf.values() if v), None)
    if first_mf:
        print("**Model & features:**")
        print()
        parts = []
        if "params" in first_mf:
            parts.append(f"params={first_mf['params']:,}")
        for k in ["gene", "meth", "mirna"]:
            if k in first_mf:
                parts.append(f"{k}={first_mf[k]}")
        print("- " + "  ·  ".join(parts))
        print()

    print("---")

    # ── Save JSON backup ──
    out_summary = {
        "config": args.config,
        "seeds": seeds_done,
        "timestamp": datetime.now().isoformat(),
        "n_folds": n_folds,
        "aggregated_metrics": aggregated,
        "per_seed_summary": {str(k): v for k, v in seed_summaries.items()},
    }
    summary_path = out_root / "multi_seed_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(out_summary, f, indent=2, ensure_ascii=False)
    print(f"\nSaved: {summary_path}")


if __name__ == "__main__":
    main()
