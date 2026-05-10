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
        r"^\s+([A-Z_0-9]+)\s*:\s*mean=([\d.]+)\s+std=([\d.]+)\s*$",
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


def parse_model_features(stdout: str) -> dict | None:
    """Extract '📐 Model & Features (5-fold mean)' block.

    Format:
        📐 Model & Features (5-fold mean):
          Params       : 750,000
          Gene feats   : 2,612
          Meth feats   : 2,742
          miRNA feats  : 588
    """
    marker = "Model & Features"
    pos = stdout.rfind(marker)
    if pos < 0:
        return None
    section = stdout[pos:pos + 600]
    out = {}
    for key, label in [("params", "Params"), ("gene", "Gene feats"),
                       ("meth", "Meth feats"), ("mirna", "miRNA feats")]:
        m = re.search(rf"{label}\s*:\s*([\d,]+)", section)
        if m:
            out[key] = int(m.group(1).replace(",", ""))
    return out if out else None


def parse_attention_stats(stdout: str) -> dict | None:
    """Extract '🔍 Attention Stats (5-fold mean ± std)' block từ summarize_cv.

    Format:
        🔍 Attention Stats (5-fold mean ± std):
          cpg_std           : mean=0.0488  std=0.0061
          cpg_max           : mean=0.2266  std=0.0285
          ...
    """
    marker = "Attention Stats (5-fold mean"
    pos = stdout.rfind(marker)
    if pos < 0:
        return None
    section = stdout[pos:pos + 1500]
    rows = re.findall(
        r"^\s+([\w_]+)\s*:\s*mean=([\d.]+)\s+std=([\d.]+)\s*$",
        section, re.MULTILINE,
    )
    return {name: {"mean": float(m), "std": float(s)} for name, m, s in rows}


def parse_overfit_indicator(stdout: str) -> dict | None:
    """Extract '⚖️ Overfit indicator (5-fold)' block.

    Format:
        ⚖️  Overfit indicator (5-fold):
          Best Val F1   : mean=0.7499  std=0.0532
          Test  F1      : mean=0.6594  std=0.0154
          Val−Test gap  : mean=+0.0905  (gap > 0.05 → overfit nghi ngờ)
          Stop epoch    : mean=78.4  range=[60,96]
    """
    marker = "Overfit indicator"
    pos = stdout.rfind(marker)
    if pos < 0:
        return None
    section = stdout[pos:pos + 800]
    out = {}
    m = re.search(r"Best Val F1\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
    if m:
        out["best_val_f1"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
    m = re.search(r"Test\s+F1\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
    if m:
        out["test_f1"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
    m = re.search(r"Val.Test gap\s*:\s*mean=([+\-\d.]+)", section)
    if m:
        out["val_test_gap"] = float(m.group(1))
    m = re.search(r"Stop epoch\s*:\s*mean=([\d.]+)\s+range=\[(\d+),(\d+)\]", section)
    if m:
        out["stop_epoch"] = {
            "mean": float(m.group(1)),
            "min": int(m.group(2)), "max": int(m.group(3)),
        }
    return out if out else None


def parse_per_class_f1(stdout: str) -> dict | None:
    """Extract per-class 5-fold mean ± std từ train.py stdout.

    Format:
        🎯 Per-class F1 (5-fold mean ± std):
                 Class   F1 mean   F1 std
                     0    0.9100   0.0200
    """
    marker = "Per-class F1 (5-fold mean"
    marker_pos = stdout.rfind(marker)
    if marker_pos < 0:
        return None
    section = stdout[marker_pos:]
    rows = re.findall(
        r"^\s+(\d+)\s+([0-9]*\.?[0-9]+)\s+([0-9]*\.?[0-9]+)\s*$",
        section,
        re.MULTILINE,
    )
    return {cls: {"f1_mean": float(m), "f1_std": float(s)} for cls, m, s in rows}


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
    seed_per_class = {}
    seed_attn = {}
    seed_overfit = {}
    seed_modelft = {}

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
        per_class = parse_per_class_f1(stdout)
        attn = parse_attention_stats(stdout)
        overfit = parse_overfit_indicator(stdout)
        modelft = parse_model_features(stdout)

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
        if per_class:
            seed_per_class[seed] = per_class
        if attn:
            seed_attn[seed] = attn
        if overfit:
            seed_overfit[seed] = overfit
        if modelft:
            seed_modelft[seed] = modelft

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

    if seed_per_class:
        class_names = {
            "0": "CIN",
            "1": "GS",
            "2": "MSI",
            "3": "HM-SNV",
            "4": "EBV",
        }
        all_classes = sorted(set().union(*[d.keys() for d in seed_per_class.values()]), key=int)
        print("**Per-class F1 (mean across seeds):**")
        print()
        seeds_list = list(seed_per_class.keys())
        header = "| Class | " + " | ".join(f"Seed {s}" for s in seeds_list) + " | Avg |"
        sep = "|-------|" + "|".join("---" for _ in seeds_list) + "|------|"
        print(header)
        print(sep)
        for cls in all_classes:
            vals = []
            row_cells = []
            for seed in seeds_list:
                if cls in seed_per_class[seed]:
                    v = seed_per_class[seed][cls]["f1_mean"]
                    vals.append(v)
                    row_cells.append(f"{v:.4f}")
                else:
                    row_cells.append("—")
            avg = np.mean(vals) if vals else 0
            print(f"| {cls} ({class_names.get(cls, 'class ' + cls)}) | " + " | ".join(row_cells) + f" | {avg:.4f} |")
        print()

    # ── Attention stats (mean ± std across seeds) ──────────────────
    if seed_attn:
        print("**Attention stats (mean across folds, then averaged across seeds):**")
        print()
        print("| Modality | std | max | nnz | global w |")
        print("|---|---|---|---|---|")
        for mod in ["cpg", "mirna"]:
            row = [mod]
            for stat in ["std", "max", "nnz"]:
                key = f"{mod}_{stat}"
                vals = [seed_attn[s][key]["mean"] for s in seed_attn if key in seed_attn[s]]
                row.append(f"{np.mean(vals):.3f}" if vals else "—")
            gkey = f"modality_w_{mod}"
            gvals = [seed_attn[s][gkey]["mean"] for s in seed_attn if gkey in seed_attn[s]]
            row.append(f"{np.mean(gvals):.3f}" if gvals else "—")
            print("| " + " | ".join(row) + " |")
        print()

    # ── Overfit indicator (Train vs Val vs Test) ───────────────────
    if seed_overfit:
        print("**Overfit indicator (mean across seeds):**")
        print()
        print("| Metric | Value | Note |")
        print("|---|---|---|")
        keys = [
            ("best_val_f1", "Best Val F1", ""),
            ("test_f1",     "Test F1",     ""),
        ]
        for k, label, note in keys:
            vals = [seed_overfit[s][k]["mean"] for s in seed_overfit if k in seed_overfit[s]]
            if vals:
                print(f"| {label} | {np.mean(vals):.4f} | {note} |")
        gaps = [seed_overfit[s].get("val_test_gap", 0.0) for s in seed_overfit
                if "val_test_gap" in seed_overfit[s]]
        if gaps:
            avg_gap = np.mean(gaps)
            note = "OK" if abs(avg_gap) < 0.05 else "⚠️ val không đại diện test"
            print(f"| Val−Test gap | {avg_gap:+.4f} | {note} |")
        stops = [seed_overfit[s]["stop_epoch"]["mean"] for s in seed_overfit
                 if "stop_epoch" in seed_overfit[s]]
        if stops:
            print(f"| Stop epoch (mean) | {np.mean(stops):.1f} | sớm = overfit nghi ngờ |")
        print()

    # ── Model & feature counts ──────────────────────────────────────
    if seed_modelft:
        # Same across seeds typically; use first
        first = next(iter(seed_modelft.values()))
        print("**Model & features:**")
        print()
        parts = []
        if "params" in first:  parts.append(f"params={first['params']:,}")
        if "gene"   in first:  parts.append(f"gene={first['gene']}")
        if "meth"   in first:  parts.append(f"meth={first['meth']}")
        if "mirna"  in first:  parts.append(f"mirna={first['mirna']}")
        print("- " + "  ·  ".join(parts))
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
        "per_seed_per_class_f1": {str(k): v for k, v in seed_per_class.items()},
        "per_seed_attention": {str(k): v for k, v in seed_attn.items()},
        "per_seed_overfit": {str(k): v for k, v in seed_overfit.items()},
        "per_seed_model_features": {str(k): v for k, v in seed_modelft.items()},
    }
    summary_path = out_root / "multi_seed_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"💾 JSON backup (KHÔNG cần download): {summary_path}")


if __name__ == "__main__":
    main()
