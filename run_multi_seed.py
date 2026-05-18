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
    """Extract test metrics block từ train.py stdout.

    Hai format:
    1. CV mode: '📈 5-fold CV summary' với mean ± std
    2. Fixed-test mode (ESCA scenario): single '[Raw  ] Acc=... F1=...' line

    Returns {metric_name: {"mean": x, "std": y}} for both.
    """
    # Try CV format first
    pattern = re.compile(
        r"^\s+([A-Z_0-9]+)\s*:\s*mean=([\d.]+)\s+std=([\d.]+)",
        re.MULTILINE,
    )
    matches = pattern.findall(stdout)
    if matches:
        return {name.lower(): {"mean": float(m), "std": float(s)} for name, m, s in matches}

    # Fallback: fixed-test (1 split) — parse '[Raw  ] Acc=X P=X R=X F1=X F1w=X'
    m = re.search(
        r"\[Raw\s*\]\s+Acc=([\d.]+)\s+P=([\d.]+)\s+R=([\d.]+)\s+F1=([\d.]+)\s+F1w=([\d.]+)",
        stdout,
    )
    if m:
        return {
            "accuracy":    {"mean": float(m.group(1)), "std": 0.0},
            "precision":   {"mean": float(m.group(2)), "std": 0.0},
            "recall":      {"mean": float(m.group(3)), "std": 0.0},
            "f1":          {"mean": float(m.group(4)), "std": 0.0},
            "f1_weighted": {"mean": float(m.group(5)), "std": 0.0},
        }
    return None


def parse_per_fold_f1(stdout: str) -> list[float]:
    """Extract per-fold test F1 (macro RAW) — line dạng: '✅ Test F1  raw=0.7006  cal=0.6973'."""
    return [float(v) for v in re.findall(r"✅ Test F1\s+raw=([\d.]+)", stdout)]


def parse_per_cancer_type(stdout: str) -> dict | None:
    """Extract per-cancer-type 5-fold mean ± std từ train.py stdout.

    Format:
        🧬 Per-cancer-type F1 (5-fold mean ± std):
          Cancer  N/fold   F1 mean   F1 std
            COAD    68.0    0.6982   0.1002
            STAD    76.0    0.6720   0.0776
    """
    # Find header, then look for data rows in the following window.
    # Cũ dùng regex span-newline phức tạp → fail silently. Đơn giản hoá.
    header_match = re.search(r"Per-cancer-type F1 \(5-fold mean.*?\):", stdout)
    if not header_match:
        return None
    start = header_match.end()
    section = stdout[start:start + 2000]
    # Match rows: leading whitespace, ALL-CAPS cancer-type token, 3 numbers.
    rows = re.findall(
        r"^\s+([A-Z][A-Z0-9_-]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*$",
        section, re.MULTILINE,
    )
    if not rows:
        return None
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
    """Extract '⚖️ Overfit indicator' block. Supports cả format cũ (no SWA) và mới
    (SWA enabled: 'Vanilla Val F1', 'Vanilla Test F1', 'SWA Test F1')."""
    marker = "Overfit indicator"
    pos = stdout.rfind(marker)
    if pos < 0:
        return None
    section = stdout[pos:pos + 1200]
    out = {}
    m = re.search(r"Train\s+F1\s*\(at best val\)\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
    if m:
        out["train_f1"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
    # Best Val F1 (old format) hoặc Vanilla Val F1 (new format SWA)
    m = re.search(r"(?:Best|Vanilla)\s+Val\s+F1\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
    if m:
        out["best_val_f1"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
    # Test F1 (old) hoặc Vanilla Test F1 (new). Match Vanilla first.
    m = re.search(r"Vanilla\s+Test\s+F1\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
    if m:
        out["test_f1_vanilla"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
        out["test_f1"] = out["test_f1_vanilla"]   # back-compat
    else:
        m = re.search(r"Test\s+F1\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
        if m:
            out["test_f1"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
    m = re.search(r"SWA\s+Test\s+F1\s*:\s*mean=([\d.]+)\s+std=([\d.]+)", section)
    if m:
        out["test_f1_swa"] = {"mean": float(m.group(1)), "std": float(m.group(2))}
    m = re.search(r"Train.Val gap\s*:\s*mean=([+\-\d.]+)", section)
    if m:
        out["train_val_gap"] = float(m.group(1))
    m = re.search(r"Val.Test gap\s*(?:\(vanilla\))?\s*:\s*mean=([+\-\d.]+)", section)
    if m:
        out["val_test_gap"] = float(m.group(1))
    m = re.search(r"Stop epoch\s*:\s*mean=([\d.]+)\s+range=\[(\d+),(\d+)\]", section)
    if m:
        out["stop_epoch"] = {
            "mean": float(m.group(1)),
            "min": int(m.group(2)), "max": int(m.group(3)),
        }
    return out if out else None


def parse_vanilla_vs_swa(stdout: str) -> dict | None:
    """Extract '🪶 Vanilla vs SWA' comparison block từ summarize_cv.

    Format (new, when SWA enabled):
        🪶 Vanilla vs SWA — 5-fold mean ± std  (40.6 snapshots/fold avg, range=[20,59])
          split metric          vanilla              SWA          Δ mean    Δ std
          val  Acc    0.8716 ± 0.0270  0.8680 ± 0.0260  -0.0037  -0.0010
          ...
          test F1m   ...

    Returns: {
      "val":  {"accuracy": {"vanilla_mean": ..., "vanilla_std": ..., "swa_mean": ..., "swa_std": ...}, ...},
      "test": {...},
      "n_swa_avg_mean": float, "n_swa_avg_min": int, "n_swa_avg_max": int,
    }
    """
    marker = "Vanilla vs SWA"
    pos = stdout.rfind(marker)
    if pos < 0:
        return None
    section = stdout[pos:pos + 2000]
    # Header với n_swa_avg
    m = re.search(r"\(([\d.]+)\s+snapshots/fold avg,\s*range=\[(\d+),(\d+)\]\)", section)
    n_avg_mean = float(m.group(1)) if m else None
    n_avg_min = int(m.group(2)) if m else None
    n_avg_max = int(m.group(3)) if m else None
    # Data rows
    rows = re.findall(
        r"^\s+(val|test)\s+(Acc|F1w|F1m)\s+([\d.]+)\s*±\s*([\d.]+)\s+([\d.]+)\s*±\s*([\d.]+)\s+([+\-][\d.]+)\s+([+\-][\d.]+)",
        section, re.MULTILINE,
    )
    if not rows:
        return None
    metric_map = {"Acc": "accuracy", "F1w": "f1_weighted", "F1m": "f1"}
    out = {"val": {}, "test": {}}
    for split, mlabel, vm, vs, sm, ss, _dm, _ds in rows:
        out[split][metric_map[mlabel]] = {
            "vanilla_mean": float(vm), "vanilla_std": float(vs),
            "swa_mean":     float(sm), "swa_std":     float(ss),
        }
    if n_avg_mean is not None:
        out["n_swa_avg_mean"] = n_avg_mean
        out["n_swa_avg_min"]  = n_avg_min
        out["n_swa_avg_max"]  = n_avg_max
    return out


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


def parse_class_names(stdout: str) -> dict | None:
    """Extract class index → name mapping từ train.py per-fold output.

    Format (in per-fold output):
        🎯 Per-class F1 - Fold 1  (raw → calibrated)
           0:Basal     0.8840 → 0.9081  (+0.0241)
           1:Her2      0.8000 → 0.8193  (+0.0193)
    """
    # Match: "   {idx}:{name}   {raw} → ..."
    rows = re.findall(
        r"^\s+(\d+):(\S+)\s+[\d.]+\s+→",
        stdout,
        re.MULTILINE,
    )
    if not rows:
        return None
    # Take last occurrence per class (most reliable, after all folds run)
    out = {}
    for idx, name in rows:
        out[idx] = name
    return out if out else None


def aggregate_vanilla_vs_swa(seed_vs_data: dict, n_folds: int = 5) -> dict | None:
    """Aggregate vanilla vs SWA stats across seeds dùng law of total variance.

    Input: {seed: {"val": {metric: {vanilla_mean, vanilla_std, swa_mean, swa_std}},
                   "test": {...}, "n_swa_avg_mean": ...}}
    Output: {"val": {metric: {"vanilla": {mean, std_pooled, ...}, "swa": {...}, "delta_mean", "delta_std"}},
             "test": {...}, "n_swa_avg": ...}
    """
    if not seed_vs_data:
        return None
    out = {"val": {}, "test": {}}
    seeds = list(seed_vs_data.keys())

    def _pool(per_seed_means, per_seed_stds):
        means = np.array(per_seed_means)
        stds  = np.array(per_seed_stds)
        within_var  = float((stds ** 2).mean())
        between_var = float(means.std(ddof=0) ** 2)
        pooled_std  = float(np.sqrt(within_var + between_var))
        return {"mean": float(means.mean()), "std_pooled": pooled_std,
                "per_seed_means": means.tolist(), "per_seed_stds": stds.tolist()}

    for split in ("val", "test"):
        for metric in ("accuracy", "f1_weighted", "f1"):
            van_means = [seed_vs_data[s][split][metric]["vanilla_mean"] for s in seeds
                         if metric in seed_vs_data[s].get(split, {})]
            van_stds  = [seed_vs_data[s][split][metric]["vanilla_std"]  for s in seeds
                         if metric in seed_vs_data[s].get(split, {})]
            swa_means = [seed_vs_data[s][split][metric]["swa_mean"] for s in seeds
                         if metric in seed_vs_data[s].get(split, {})]
            swa_stds  = [seed_vs_data[s][split][metric]["swa_std"]  for s in seeds
                         if metric in seed_vs_data[s].get(split, {})]
            if not van_means or not swa_means:
                continue
            van_agg = _pool(van_means, van_stds)
            swa_agg = _pool(swa_means, swa_stds)
            out[split][metric] = {
                "vanilla": van_agg,
                "swa": swa_agg,
                "delta_mean": swa_agg["mean"] - van_agg["mean"],
                "delta_std":  swa_agg["std_pooled"] - van_agg["std_pooled"],
            }
    # SWA snapshot count
    snap_means = [seed_vs_data[s].get("n_swa_avg_mean") for s in seeds
                  if seed_vs_data[s].get("n_swa_avg_mean") is not None]
    if snap_means:
        out["n_swa_avg_mean"] = float(np.mean(snap_means))
    return out


def aggregate_seeds(seed_results: list[dict], n_folds: int = 5) -> dict:
    """Aggregate stats qua nhiều seeds.

    Returns 3 loại uncertainty:
        - std_of_means: var(seed_means)  → seed stability (small)
        - std_pooled: √(E[within_seed_var] + var(seed_means)) → total std across all runs
        - ci95_half: half-width của 95% CI cho mean estimate, dùng t-distribution
                    = t_critical × std_pooled / √n_total_runs
    """
    if not seed_results:
        return {}
    # Approximation cho t_critical (df=n_total-1, α=0.025 two-tailed)
    # Common values: df=4→2.776, df=9→2.262, df=14→2.145, df=19→2.093, df=29→2.045
    def t_critical(df):
        # Simplified lookup; for df>30, approaches 1.96
        if df <= 1: return 12.71
        if df <= 4: return 2.776
        if df <= 9: return 2.262
        if df <= 14: return 2.145
        if df <= 19: return 2.093
        if df <= 29: return 2.045
        return 1.96

    metric_names = sorted(set().union(*[r.keys() for r in seed_results if r]))
    out = {}
    for m in metric_names:
        means = [r[m]["mean"] for r in seed_results if r and m in r]
        stds = [r[m].get("std", 0.0) for r in seed_results if r and m in r]
        if not means:
            continue
        means_arr = np.array(means)
        stds_arr = np.array(stds)
        n_seeds = len(means)
        n_total = n_seeds * max(n_folds, 1)
        # Law of total variance
        within_var = float((stds_arr ** 2).mean())
        between_var = float(means_arr.std(ddof=0) ** 2)
        std_pooled = float(np.sqrt(within_var + between_var))
        # 95% CI for the mean
        sem = std_pooled / np.sqrt(max(n_total, 1))
        ci95_half = float(t_critical(n_total - 1) * sem)
        out[m] = {
            "mean_of_means": float(means_arr.mean()),
            "std_of_means": float(means_arr.std(ddof=0)),
            "std_pooled":   std_pooled,
            "sem":          float(sem),
            "ci95_half":    ci95_half,
            "n_seeds": n_seeds,
            "n_total_runs": n_total,
            "per_seed_means": means,
            "per_seed_stds":  stds,
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
    seed_class_names = {}
    seed_vanilla_vs_swa = {}   # SWA enabled runs: vanilla vs SWA per-seed stats

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
        class_names = parse_class_names(stdout)
        attn = parse_attention_stats(stdout)
        overfit = parse_overfit_indicator(stdout)
        modelft = parse_model_features(stdout)
        vs_swa = parse_vanilla_vs_swa(stdout)

        if cv:
            print(
                f"\n✅ Seed {seed} done — "
                f"Acc={cv.get('accuracy', {}).get('mean', 0):.4f}  "
                f"F1w={cv.get('f1_weighted', {}).get('mean', 0):.4f}  "
                f"F1macro={cv.get('f1', {}).get('mean', 0):.4f}",
                flush=True,
            )
            seed_summaries[seed] = cv
        else:
            print(f"\n⚠️  Seed {seed}: không parse được test metrics từ log", flush=True)

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
        if class_names:
            seed_class_names[seed] = class_names
        if vs_swa:
            seed_vanilla_vs_swa[seed] = vs_swa

    # ── Aggregate ─────────────────────────────────────────────
    # Detect n_folds from per_fold parsing (default 5 if no data)
    detected_n_folds = max((len(f) for f in seed_per_fold.values()), default=5)
    aggregated = aggregate_seeds(list(seed_summaries.values()), n_folds=detected_n_folds)
    aggregated_vs_swa = aggregate_vanilla_vs_swa(seed_vanilla_vs_swa, n_folds=detected_n_folds)
    is_swa = aggregated_vs_swa is not None
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

    # ── Detect fixed-test scenario (1 "fold" per seed) ──
    n_folds = max((len(f) for f in seed_per_fold.values()), default=5)
    is_fixed_test = n_folds == 1

    # ── Begin paste block ──
    n_runs = len(args.seeds) * n_folds
    if is_fixed_test:
        # Fixed-test: within-seed std = 0 (1 fold) → std_pooled = std_of_means
        acc_str = f"{acc.get('mean_of_means', 0):.4f} ± {acc.get('std_of_means', 0):.4f}"
        f1w_str = f"{f1_w.get('mean_of_means', 0):.4f} ± {f1_w.get('std_of_means', 0):.4f}"
        title = f"## [{timestamp_iso}] `{cfg_short}` — Acc: **{acc_str}**  |  Weighted F1: **{f1w_str}**"
        runs_label = f"{len(args.seeds)} × 1 fixed-test split"
    else:
        # CV scenario: report 95% CI as primary (tightest defensible), std as secondary.
        mean_v = f1_macro.get('mean_of_means', 0)
        ci95 = f1_macro.get('ci95_half', 0)
        std_pooled = f1_macro.get('std_pooled', 0)
        title = (f"## [{timestamp_iso}] `{cfg_short}` — "
                 f"Macro F1: **{mean_v:.4f} ± {ci95:.4f}** (95% CI, {n_runs} runs)  "
                 f"·  std: {std_pooled:.4f}")
        runs_label = f"{len(args.seeds)} × {n_folds} folds = {n_runs} runs"
    print(title)
    print()
    print(f"**Config:** `{args.config}`  |  **Seeds:** {args.seeds}  |  **N runs:** {runs_label}")
    print()

    # Aggregate metrics table
    if is_fixed_test:
        print("| Metric | Mean ± Std | Per-seed means |")
        print("|--------|------------|----------------|")
        label_map = [
            ("accuracy",    "**Accuracy**"),
            ("f1_weighted", "**Weighted F1**"),
            ("f1",          "Macro F1"),
            ("precision",   "Precision (macro)"),
            ("recall",      "Recall (macro)"),
        ]
    else:
        print("| Metric | Mean ± 95% CI | Std (all runs) | Per-seed means |")
        print("|--------|----------------|----------------|-----------------|")
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
        if is_fixed_test:
            print(f"| {label} | {s['mean_of_means']:.4f} ± {s['std_of_means']:.4f} | {per_seed_str} |")
        else:
            print(f"| {label} | {s['mean_of_means']:.4f} ± {s['ci95_half']:.4f} "
                  f"| {s['std_pooled']:.4f} | {per_seed_str} |")
    if is_swa:
        model_label = "SWA always-pick (v3)"
    else:
        model_label = "vanilla (best-ckpt)"
    print()
    print(f"_Selected model: **{model_label}**._")
    print()

    # ── Vanilla vs SWA comparison (15-run aggregated) ──
    if is_swa:
        snap_mean = aggregated_vs_swa.get("n_swa_avg_mean", 0)
        print(f"**Vanilla vs SWA — {n_runs}-run aggregated** "
              f"(SWA averaged {snap_mean:.0f} snapshots/fold):")
        print()
        print("| Split | Metric | Vanilla mean ± std | SWA mean ± std | Δ mean | Δ std |")
        print("|---|---|---|---|---|---|")
        for split in ("val", "test"):
            for metric, mlabel in (("accuracy", "Acc"), ("f1_weighted", "F1w"), ("f1", "F1 macro")):
                d = aggregated_vs_swa.get(split, {}).get(metric)
                if not d:
                    continue
                van = d["vanilla"]; swa = d["swa"]
                bold = "**" if split == "test" else ""
                print(f"| {bold}{split}{bold} | {bold}{mlabel}{bold} "
                      f"| {van['mean']:.4f} ± {van['std_pooled']:.4f} "
                      f"| {swa['mean']:.4f} ± {swa['std_pooled']:.4f} "
                      f"| {d['delta_mean']:+.4f} | {d['delta_std']:+.4f} |")
        print()

    # Per-fold breakdown (compact) — SKIP cho fixed-test vì degenerate (1 split = same as per-seed)
    if seed_per_fold and not is_fixed_test:
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
        # Use class names parsed from train.py output (per-dataset correct).
        # Fallback to GI defaults if parsing failed.
        if seed_class_names:
            class_names = next(iter(seed_class_names.values()))   # consistent across seeds
        else:
            class_names = {"0": "CIN", "1": "GS", "2": "MSI", "3": "HM-SNV", "4": "EBV"}
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
        print("**Overfit indicator (vanilla training trajectory, mean across seeds):**")
        print()
        print("| Metric | Value | Note |")
        print("|---|---|---|")
        has_swa_overfit = any("test_f1_swa" in seed_overfit[s] for s in seed_overfit)
        if has_swa_overfit:
            keys = [
                ("train_f1",        "Train F1 (at best val)", ""),
                ("best_val_f1",     "Vanilla Val F1",          ""),
                ("test_f1_vanilla", "Vanilla Test F1",         ""),
                ("test_f1_swa",     "SWA Test F1",             "**= reported model**"),
            ]
        else:
            keys = [
                ("train_f1",    "Train F1 (at best val)", ""),
                ("best_val_f1", "Best Val F1",             ""),
                ("test_f1",     "Test F1",                 ""),
            ]
        for k, label, note in keys:
            vals = [seed_overfit[s][k]["mean"] for s in seed_overfit if k in seed_overfit[s]]
            if vals:
                print(f"| {label} | {np.mean(vals):.4f} | {note} |")
        tv_gaps = [seed_overfit[s].get("train_val_gap", 0.0) for s in seed_overfit
                   if "train_val_gap" in seed_overfit[s]]
        if tv_gaps:
            avg_gap = np.mean(tv_gaps)
            note = "OK" if avg_gap < 0.10 else ("⚠️ overfit nhẹ" if avg_gap < 0.20 else "🚨 strong overfit")
            print(f"| Train−Val gap | {avg_gap:+.4f} | {note} |")
        vt_gaps = [seed_overfit[s].get("val_test_gap", 0.0) for s in seed_overfit
                   if "val_test_gap" in seed_overfit[s]]
        if vt_gaps:
            avg_gap = np.mean(vt_gaps)
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
        "aggregated_vanilla_vs_swa": aggregated_vs_swa,
        "per_seed_cv_summary": {str(k): v for k, v in seed_summaries.items()},
        "per_seed_per_fold_f1": {str(k): v for k, v in seed_per_fold.items()},
        "per_seed_per_cancer_type": {str(k): v for k, v in seed_per_ct.items()},
        "per_seed_per_class_f1": {str(k): v for k, v in seed_per_class.items()},
        "per_seed_attention": {str(k): v for k, v in seed_attn.items()},
        "per_seed_overfit": {str(k): v for k, v in seed_overfit.items()},
        "per_seed_model_features": {str(k): v for k, v in seed_modelft.items()},
        "per_seed_vanilla_vs_swa": {str(k): v for k, v in seed_vanilla_vs_swa.items()},
    }
    summary_path = out_root / "multi_seed_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"💾 JSON backup (KHÔNG cần download): {summary_path}")


if __name__ == "__main__":
    main()
