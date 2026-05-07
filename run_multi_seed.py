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

    # ── Aggregate & PRINT TO CELL (copy-paste friendly) ────────
    aggregated = aggregate_seeds(list(seed_summaries.values()))

    print("\n\n" + "█" * 70)
    print("█" + " " * 22 + "MULTI-SEED FINAL SUMMARY" + " " * 22 + "█")
    print("█" * 70)
    print(f"\nConfig    : {args.config}")
    print(f"Seeds     : {args.seeds}")
    print(f"N runs    : {len(args.seeds)} seeds × CV folds = {len(args.seeds) * 5} (assuming 5-fold)")
    print(f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ── Aggregate metric table ────────────────────────────────
    print("\n┌─────────────────────────────────────────────────────────────────┐")
    print("│  AGGREGATE (mean of seed-means ± std of seed-means)             │")
    print("├─────────────────────────────────────────────────────────────────┤")
    metric_order = ["accuracy", "precision", "recall", "f1", "f1_weighted"]
    for m in metric_order:
        if m not in aggregated:
            continue
        s = aggregated[m]
        label = m.upper().replace("F1_WEIGHTED", "F1 (weighted)").replace("F1", "F1 (macro)" if m == "f1" else "F1 (weighted)")
        per_seed_str = ", ".join(f"{v:.4f}" for v in s["per_seed_means"])
        print(f"│  {label:14s}: {s['mean_of_means']:.4f} ± {s['std_of_means']:.4f}   "
              f"per-seed: [{per_seed_str}]  │")
    print("└─────────────────────────────────────────────────────────────────┘")

    # ── Markdown table — copy-paste vào docs/issues/ ─────────
    print("\n📋 MARKDOWN TABLE (copy-paste vào docs/issues/):")
    print("```")
    print(f"| Config | Macro F1 | Weighted F1 | Accuracy |")
    print(f"|--------|----------|-------------|----------|")
    f1_macro = aggregated.get("f1", {})
    f1_w = aggregated.get("f1_weighted", {})
    acc = aggregated.get("accuracy", {})
    cfg_short = Path(args.config).stem
    print(f"| {cfg_short} | {f1_macro.get('mean_of_means', 0):.4f} ± {f1_macro.get('std_of_means', 0):.4f} | "
          f"{f1_w.get('mean_of_means', 0):.4f} ± {f1_w.get('std_of_means', 0):.4f} | "
          f"{acc.get('mean_of_means', 0):.4f} ± {acc.get('std_of_means', 0):.4f} |")
    print("```")

    # ── Per-seed per-fold F1 (chi tiết) ───────────────────────
    if seed_per_fold:
        print("\n📊 PER-FOLD F1 (macro) — debug fold variance:")
        print(f"{'Seed':>6} | " + " | ".join(f"Fold{i+1}" for i in range(5)) + " |  Mean")
        print("-" * 55)
        for seed, folds in seed_per_fold.items():
            folds_str = " | ".join(f"{f:.4f}" for f in folds)
            mean = np.mean(folds) if folds else 0
            print(f"{seed:>6} | {folds_str} | {mean:.4f}")

    # ── Per-cancer-type breakdown (nếu có) ─────────────────────
    if seed_per_ct:
        print("\n🧬 PER-CANCER-TYPE F1 (avg over seeds):")
        all_cts = sorted(set().union(*[d.keys() for d in seed_per_ct.values()]))
        print(f"{'Cancer':>8} | " + " | ".join(f"Seed {s}" for s in seed_per_ct.keys()) + " |   Avg")
        print("-" * (12 + 11 * len(seed_per_ct) + 8))
        for ct in all_cts:
            row = []
            vals = []
            for seed, ct_dict in seed_per_ct.items():
                if ct in ct_dict:
                    f1m = ct_dict[ct]["f1_mean"]
                    row.append(f"{f1m:.4f}")
                    vals.append(f1m)
                else:
                    row.append("  N/A ")
            avg = np.mean(vals) if vals else 0
            print(f"{ct:>8} | " + " | ".join(row) + f" | {avg:.4f}")

    # ── JSON backup (KHÔNG cần download — đã có trong cell) ───
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

    # ── Cũng in raw JSON ra cell (copy nếu muốn save offline) ─
    print("\n💾 RAW JSON (in case bạn muốn copy-paste lưu offline):")
    print("```json")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print("```")
    print(f"\n(Backup file đã lưu tại: {summary_path} — không cần download nếu output cell đã đủ)")


if __name__ == "__main__":
    main()
