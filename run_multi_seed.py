"""
run_multi_seed.py
-----------------
Wrapper chạy train.py với nhiều seeds, aggregate kết quả mean ± std.

Usage:
    python run_multi_seed.py --config configs/config.yaml
    python run_multi_seed.py --config configs/config_brca.yaml --seeds 42 123 2024
    python run_multi_seed.py --config configs/config_ucec.yaml --output-dir results/ucec_multiseed

Tại sao cần script này:
    - Mỗi config hiện chỉ chạy 1 seed × 5 folds = 5 runs.
    - Để có statistical significance cần multi-seed: 3 seeds × 5 folds = 15 runs.
    - Script này chạy train.py 3 lần (mỗi lần 1 seed), parse output, aggregate.

Output:
    {output_dir}/
      ├── seed_42/checkpoints/...        (output gốc của train.py)
      ├── seed_123/checkpoints/...
      ├── seed_2024/checkpoints/...
      ├── seed_42/stdout.log             (full log)
      ├── seed_123/stdout.log
      ├── seed_2024/stdout.log
      └── multi_seed_summary.json        (aggregated mean ± std)
"""

import argparse
import json
import os
import re
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


def parse_cv_summary(stdout: str) -> dict | None:
    """Extract '5-fold CV summary' block từ train.py stdout.

    Train.py prints:
        📈 5-fold CV summary
          ACCURACY   : mean=0.8331  std=0.0495
          PRECISION  : mean=0.6892  std=0.0719
          RECALL     : mean=0.7087  std=0.0488
          F1         : mean=0.6886  std=0.0567
          F1_WEIGHTED: mean=0.8388  std=0.0454
    """
    pattern = re.compile(
        r"^\s+([A-Z_]+)\s*:\s*mean=([\d.]+)\s+std=([\d.]+)\s*$",
        re.MULTILINE,
    )
    matches = pattern.findall(stdout)
    if not matches:
        return None
    return {name.lower(): {"mean": float(m), "std": float(s)} for name, m, s in matches}


def parse_per_fold_f1(stdout: str) -> list[float]:
    """Extract per-fold test F1 (macro) — line dạng: '✅ Test F1:     0.7006'."""
    return [float(v) for v in re.findall(r"✅ Test F1:\s+([\d.]+)", stdout)]


def parse_per_cancer_type(stdout: str) -> dict | None:
    """Extract per-cancer-type 5-fold mean ± std từ train.py stdout.

    Format:
        🧬 Per-cancer-type F1 (5-fold mean ± std):
          Cancer  N/fold   F1 mean   F1 std
            COAD    68.0    0.6982   0.1002
            STAD    76.0    0.6720   0.0776
    """
    section = re.search(
        r"Per-cancer-type F1 \(5-fold mean.*?\):\s*\n.*?Cancer.*?\n((?:\s+\S+\s+[\d.]+\s+[\d.]+\s+[\d.]+\s*\n?)+)",
        stdout,
    )
    if not section:
        return None
    rows = re.findall(r"^\s+(\S+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$",
                      section.group(1), re.MULTILINE)
    return {ct: {"n_per_fold": float(n), "f1_mean": float(m), "f1_std": float(s)}
            for ct, n, m, s in rows}


def aggregate_seeds(seed_results: list[dict]) -> dict:
    """Aggregate stats qua nhiều seeds.

    Mỗi seed_result có format từ parse_cv_summary:
        {"f1": {"mean": 0.69, "std": 0.06}, "f1_weighted": {...}, ...}

    Output: mean ± std OF MEANS (i.e., "mean of seed means", "std of seed means").
    Std của std cũng có thể compute nhưng ít ý nghĩa — bỏ qua.
    """
    if not seed_results:
        return {}
    metric_names = sorted(set().union(*[r.keys() for r in seed_results if r]))
    out = {}
    for m in metric_names:
        means = [r[m]["mean"] for r in seed_results if r and m in r]
        if not means:
            continue
        means_arr = np.array(means)
        out[m] = {
            "mean_of_means": float(means_arr.mean()),
            "std_of_means": float(means_arr.std(ddof=0)),
            "n_seeds": len(means),
            "per_seed_means": means,
        }
    return out


def main():
    args = parse_args()

    cfg_name = Path(args.config).stem
    if args.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output_dir = f"results/{cfg_name}_multiseed_{timestamp}"

    out_root = Path(args.output_dir)
    out_root.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output root: {out_root}")
    print(f"🌱 Seeds: {args.seeds}")
    print(f"⚙️  Config: {args.config}")

    seed_summaries = {}
    seed_per_fold = {}
    seed_per_ct = {}

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

        # Stream subprocess output → notebook cell line-by-line + capture for parsing
        # Đồng thời lưu vào log file (backup, không bắt buộc download).
        captured_lines = []
        with open(log_path, "w", encoding="utf-8") as log_f:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,                    # line-buffered
                encoding="utf-8",
                errors="replace",
            )
            for line in proc.stdout:
                print(line, end="", flush=True)   # → cell live
                log_f.write(line)                  # → file backup
                captured_lines.append(line)
            proc.wait()

        stdout = "".join(captured_lines)

        if proc.returncode != 0:
            print(f"\n❌ Seed {seed} FAILED with returncode={proc.returncode}")
            continue

        cv = parse_cv_summary(stdout)
        per_fold = parse_per_fold_f1(stdout)
        per_ct = parse_per_cancer_type(stdout)

        if cv:
            print(f"\n✅ Seed {seed} done — F1 macro = {cv.get('f1', {}).get('mean', 0):.4f}, "
                  f"F1 weighted = {cv.get('f1_weighted', {}).get('mean', 0):.4f}", flush=True)
            seed_summaries[seed] = cv
        else:
            print(f"\n⚠️  Seed {seed}: không parse được CV summary từ log", flush=True)

        if per_fold:
            seed_per_fold[seed] = per_fold
        if per_ct:
            seed_per_ct[seed] = per_ct

    # ── Aggregate ─────────────────────────────────────────────
    aggregated = aggregate_seeds(list(seed_summaries.values()))
    f1_macro = aggregated.get("f1", {})
    f1_w = aggregated.get("f1_weighted", {})
    acc = aggregated.get("accuracy", {})
    cfg_short = Path(args.config).stem
    timestamp_iso = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Single PASTE-READY markdown block ──────────────────────
    # User chỉ cần copy block giữa hai dòng "═══" rồi paste vào docs/RESULTS.md
    print("\n\n")
    print("═" * 78)
    print(" 📋 COPY KHỐI BÊN DƯỚI (đến dòng ═ tiếp theo) → PASTE VÀO ĐẦU docs/RESULTS.md")
    print("═" * 78)
    print()  # blank line

    # ── Begin paste block ──
    title = f"## [{timestamp_iso}] `{cfg_short}` — Macro F1: **{f1_macro.get('mean_of_means', 0):.4f} ± {f1_macro.get('std_of_means', 0):.4f}**"
    print(title)
    print()
    print(f"**Config:** `{args.config}`  |  **Seeds:** {args.seeds}  |  **N runs:** {len(args.seeds)} × {len(next(iter(seed_per_fold.values()), [1,2,3,4,5]))} folds")
    print()

    # Aggregate metrics table
    print("| Metric | Mean ± Std | Per-seed means |")
    print("|--------|------------|----------------|")
    label_map = [
        ("f1",          "**Macro F1**"),
        ("f1_weighted", "Weighted F1"),
        ("accuracy",    "Accuracy"),
        ("precision",   "Precision (macro)"),
        ("recall",      "Recall (macro)"),
    ]
    for key, label in label_map:
        if key not in aggregated:
            continue
        s = aggregated[key]
        per_seed_str = ", ".join(f"{v:.4f}" for v in s["per_seed_means"])
        print(f"| {label} | {s['mean_of_means']:.4f} ± {s['std_of_means']:.4f} | {per_seed_str} |")
    print()

    # Per-fold breakdown (compact)
    if seed_per_fold:
        n_folds = max((len(f) for f in seed_per_fold.values()), default=5)
        header = "| Seed | " + " | ".join(f"Fold {i+1}" for i in range(n_folds)) + " | Mean |"
        sep = "|------|" + "|".join("---" for _ in range(n_folds)) + "|------|"
        print("**Per-fold F1 (macro):**")
        print()
        print(header)
        print(sep)
        for seed, folds in seed_per_fold.items():
            folds_str = " | ".join(f"{f:.4f}" for f in folds)
            mean = np.mean(folds) if folds else 0
            print(f"| {seed} | {folds_str} | {mean:.4f} |")
        print()

    # Per-cancer-type (only if multi-cancer)
    if seed_per_ct:
        all_cts = sorted(set().union(*[d.keys() for d in seed_per_ct.values()]))
        if len(all_cts) > 1:
            print("**Per-cancer-type F1 (mean across seeds):**")
            print()
            seeds_list = list(seed_per_ct.keys())
            header = "| Cancer | " + " | ".join(f"Seed {s}" for s in seeds_list) + " | Avg |"
            sep = "|--------|" + "|".join("---" for _ in seeds_list) + "|------|"
            print(header)
            print(sep)
            for ct in all_cts:
                vals = []
                row_cells = []
                for seed in seeds_list:
                    if ct in seed_per_ct[seed]:
                        v = seed_per_ct[seed][ct]["f1_mean"]
                        vals.append(v)
                        row_cells.append(f"{v:.4f}")
                    else:
                        row_cells.append("—")
                avg = np.mean(vals) if vals else 0
                print(f"| {ct} | " + " | ".join(row_cells) + f" | {avg:.4f} |")
            print()

    print("---")
    print()
    # ── End paste block ──

    print("═" * 78)
    print(" ↑↑↑ COPY KHỐI BÊN TRÊN — PASTE VÀO ĐẦU docs/RESULTS.md (sau dòng tiêu đề) ↑↑↑")
    print("═" * 78)
    print()

    # Save JSON backup (silent, không in)
    summary = {
        "config": args.config,
        "seeds": args.seeds,
        "timestamp": datetime.now().isoformat(),
        "aggregated": aggregated,
        "per_seed_cv_summary": {str(k): v for k, v in seed_summaries.items()},
        "per_seed_per_fold_f1": {str(k): v for k, v in seed_per_fold.items()},
        "per_seed_per_cancer_type": {str(k): v for k, v in seed_per_ct.items()},
    }
    summary_path = out_root / "multi_seed_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"💾 JSON backup (KHÔNG cần download): {summary_path}")


if __name__ == "__main__":
    main()
