"""
visualize_full_graph.py
-----------------------
Vẽ TOÀN BỘ Heterogeneous Graph của GIAC: tất cả ~3500 gene + ~3500 cpg + ~600 mirna nodes
cùng ~240K edges qua 13 relations.

3-cluster layout:
    - Gene cluster:  trên đỉnh (12 o'clock)
    - CpG cluster:   dưới-trái (8 o'clock)
    - miRNA cluster: dưới-phải (4 o'clock)
Trong mỗi cluster, nodes phân bố bằng golden-angle spiral cho mật độ đều.

Edges colored by relation type (13 colors), alpha rất thấp để tránh hairball.

Usage:
    python scripts/visualize_full_graph.py \\
        --config configs/config.yaml \\
        --output figures/giac_graph_gi.png

    # Custom edge alpha + node size:
    python scripts/visualize_full_graph.py \\
        --config configs/config_brca.yaml \\
        --output figures/giac_graph_brca.png \\
        --edge-alpha 0.03 --node-size 6

Notes:
    - Cần ~5-10 phút runtime (ANOVA feature selection + render 240K edges)
    - Output thường 200dpi → ~5-15 MB PNG; có thể PDF qua --format pdf
"""

import argparse
import os
import sys
import time
from pathlib import Path

import numpy as np
import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import LineCollection
import torch
from sklearn.feature_selection import f_classif

from src.data.dataset import load_aligned_data
from src.data.graph_builder import build_hetero_graph, RELATION_ORDER


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="configs/config.yaml")
    p.add_argument("--output", required=True, help="Output path (PNG/PDF)")
    p.add_argument("--format", choices=["png", "pdf"], default="png")
    p.add_argument("--node-size", type=float, default=4.0)
    p.add_argument("--edge-alpha", type=float, default=0.03)
    p.add_argument("--edge-width", type=float, default=0.1)
    p.add_argument("--figsize", type=int, default=22, help="Square figure side (inches)")
    p.add_argument("--dpi", type=int, default=200)
    p.add_argument("--cluster-radius", type=float, default=1.0,
                   help="Radius of each node cluster")
    p.add_argument("--cluster-distance", type=float, default=3.5,
                   help="Distance between cluster centers")
    p.add_argument("--show-self-loops", action="store_true",
                   help="Show self-loop relations (3 self_loops) in legend")
    return p.parse_args()


def select_top_features(X: np.ndarray, y: np.ndarray, k: int) -> np.ndarray:
    """ANOVA-based top-K feature selection.

    Args:
        X: (n_samples, n_features) — assume already log-transformed / β-values
        y: (n_samples,) — integer labels
        k: number of features to select

    Returns:
        idx: (k,) indices of top features by F-statistic
    """
    if k >= X.shape[1]:
        return np.arange(X.shape[1])
    # NaN-safe: replace NaNs with column mean for ANOVA only
    X_clean = X.copy()
    if np.isnan(X_clean).any():
        col_mean = np.nanmean(X_clean, axis=0)
        inds = np.where(np.isnan(X_clean))
        X_clean[inds] = np.take(col_mean, inds[1])
    F, _ = f_classif(X_clean, y)
    F = np.nan_to_num(F, nan=0.0)
    top_idx = np.argsort(F)[::-1][:k]
    return np.sort(top_idx)


def compute_3cluster_layout(n_gene, n_cpg, n_mirna, radius=1.0, cluster_dist=3.5):
    """Compute 2D position for all nodes in 3 circular clusters.

    Layout:
        gene  cluster at (0, +cluster_dist)         — top
        cpg   cluster at (-cluster_dist·cos30°, -cluster_dist·sin30°)  — bottom-left
        mirna cluster at (+cluster_dist·cos30°, -cluster_dist·sin30°)  — bottom-right

    Within each cluster: golden-angle spiral for uniform density.

    Returns:
        pos_dict: {('gene', i): (x, y), ('cpg', i): ..., ('mirna', i): ...}
    """
    GOLDEN_ANGLE = np.pi * (3.0 - np.sqrt(5.0))  # ≈ 137.5°

    cos30 = np.cos(np.pi / 6)
    sin30 = np.sin(np.pi / 6)
    centers = {
        "gene":  (0.0, cluster_dist),
        "cpg":   (-cluster_dist * cos30, -cluster_dist * sin30),
        "mirna": (cluster_dist * cos30, -cluster_dist * sin30),
    }
    n_nodes_dict = {"gene": n_gene, "cpg": n_cpg, "mirna": n_mirna}

    pos = {}
    for ntype, (cx, cy) in centers.items():
        n_nodes = n_nodes_dict[ntype]
        # Scale radius slightly by sqrt(n_nodes) so denser clusters spread out a bit
        eff_radius = radius * np.sqrt(n_nodes / 1000.0)
        for i in range(n_nodes):
            t = (i + 0.5) / n_nodes
            r = eff_radius * np.sqrt(t)
            angle = i * GOLDEN_ANGLE
            x = cx + r * np.cos(angle)
            y = cy + r * np.sin(angle)
            pos[(ntype, i)] = (x, y)
    return pos


def plot_graph(graph, pos, args):
    """Render the full graph to PNG/PDF."""
    t0 = time.time()
    fig, ax = plt.subplots(figsize=(args.figsize, args.figsize), dpi=args.dpi)

    n_gene  = graph["gene"].num_nodes
    n_cpg   = graph["cpg"].num_nodes
    n_mirna = graph["mirna"].num_nodes

    # ─── Plot edges per relation type ──────────────────────────────
    # 13 relations; use a perceptually-distinct colormap
    cmap = plt.get_cmap("tab20")
    relation_colors = [cmap(i / 13.0) for i in range(13)]

    total_edges = 0
    edge_counts_per_rel = {}
    print("[edges] Rendering 13 relations...")
    for i, (et, arrow, desc) in enumerate(RELATION_ORDER):
        if et not in graph.edge_index_dict:
            edge_counts_per_rel[desc] = 0
            continue
        ei = graph.edge_index_dict[et]
        n_edges = ei.shape[1]
        edge_counts_per_rel[desc] = n_edges
        if n_edges == 0:
            continue

        src_type, _, dst_type = et
        src_idx = ei[0].cpu().numpy()
        dst_idx = ei[1].cpu().numpy()

        # Skip self-loops in main render (still counted)
        is_self_loop = src_type == dst_type and arrow == "↔" and "self_loop" in desc.lower()
        if is_self_loop and not args.show_self_loops:
            # Skip plotting self-loop edges — they overlap each node
            continue

        # Build line segments (start_xy, end_xy) for LineCollection
        segments = np.empty((n_edges, 2, 2), dtype=np.float32)
        for j, (s, d) in enumerate(zip(src_idx, dst_idx)):
            segments[j, 0] = pos[(src_type, int(s))]
            segments[j, 1] = pos[(dst_type, int(d))]

        lc = LineCollection(
            segments,
            colors=[relation_colors[i]],
            linewidths=args.edge_width,
            alpha=args.edge_alpha,
            rasterized=True,
            zorder=1,
        )
        ax.add_collection(lc)
        total_edges += n_edges
        print(f"   [{i + 1:2d}] {desc:25s} → {n_edges:>7,} edges drawn")

    # ─── Plot nodes (after edges so they sit on top) ──────────────────
    print("[nodes] Plotting node clusters...")
    node_colors = {
        "gene":  "#3498db",   # blue
        "cpg":   "#27ae60",   # green
        "mirna": "#e67e22",   # orange
    }
    for ntype in ["gene", "cpg", "mirna"]:
        n_nodes = graph[ntype].num_nodes
        xs = np.array([pos[(ntype, i)][0] for i in range(n_nodes)])
        ys = np.array([pos[(ntype, i)][1] for i in range(n_nodes)])
        ax.scatter(
            xs, ys,
            s=args.node_size,
            c=node_colors[ntype],
            alpha=0.7,
            edgecolors="none",
            rasterized=True,
            zorder=2,
        )

    # ─── Cluster center labels ────────────────────────────────────────
    label_offset = 0.5
    cos30 = np.cos(np.pi / 6); sin30 = np.sin(np.pi / 6)
    label_positions = {
        "GENE":  (0.0, args.cluster_distance + label_offset + 0.8),
        "CpG":   (-args.cluster_distance * cos30 - 0.8, -args.cluster_distance * sin30 - 0.8),
        "miRNA": (args.cluster_distance * cos30 + 0.8, -args.cluster_distance * sin30 - 0.8),
    }
    for label, (lx, ly) in label_positions.items():
        ax.text(
            lx, ly, label,
            fontsize=22, fontweight="bold",
            ha="center", va="center",
            color="black",
            zorder=3,
        )

    # ─── Legend (node types + relations) ──────────────────────────────
    node_legend = [
        mpatches.Patch(color=node_colors["gene"],  label=f"Gene  (n={n_gene:,})"),
        mpatches.Patch(color=node_colors["cpg"],   label=f"CpG   (n={n_cpg:,})"),
        mpatches.Patch(color=node_colors["mirna"], label=f"miRNA (n={n_mirna:,})"),
    ]
    leg1 = ax.legend(
        handles=node_legend,
        loc="upper left",
        fontsize=12,
        title="Node types",
        title_fontsize=14,
        framealpha=0.9,
    )
    ax.add_artist(leg1)

    # Relations legend (only non-zero edges, exclude self-loops if hidden)
    relation_legend = []
    for i, (et, arrow, desc) in enumerate(RELATION_ORDER):
        src, rel, dst = et
        n_edges = edge_counts_per_rel[desc]
        if n_edges == 0:
            continue
        is_self_loop = src == dst and "self_loop" in desc.lower()
        if is_self_loop and not args.show_self_loops:
            continue
        label = f"{src} {arrow} {dst}  [{desc}]  ({n_edges:,})"
        relation_legend.append(
            mpatches.Patch(color=relation_colors[i], label=label)
        )
    if relation_legend:
        ax.legend(
            handles=relation_legend,
            loc="lower center",
            bbox_to_anchor=(0.5, -0.10),
            fontsize=10,
            ncol=2,
            title="Edge relations (color-coded)",
            title_fontsize=12,
            framealpha=0.9,
        )

    # ─── Title + cosmetics ────────────────────────────────────────────
    n_total_nodes = n_gene + n_cpg + n_mirna
    ax.set_title(
        f"GIAC Heterogeneous Graph — "
        f"{n_total_nodes:,} nodes ({n_gene:,} gene + {n_cpg:,} cpg + {n_mirna:,} mirna), "
        f"{total_edges:,} edges across 13 relations",
        fontsize=15, pad=20,
    )
    ax.set_aspect("equal")
    ax.axis("off")

    # Padding around
    all_x = [p[0] for p in pos.values()]
    all_y = [p[1] for p in pos.values()]
    pad = 0.5
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)

    print(f"[save] Writing {args.output} (dpi={args.dpi})...")
    plt.tight_layout()
    plt.savefig(args.output, dpi=args.dpi, bbox_inches="tight",
                format=args.format)
    plt.close()
    print(f"[done] Total time: {time.time() - t0:.1f}s")
    print(f"[done] Saved → {args.output}")


def main():
    args = parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    print(f"[config] {args.config}")
    print("[1/3] Loading aligned data...")
    t0 = time.time()
    raw = load_aligned_data(cfg)
    print(f"      gene shape  : {raw['gene'].shape}")
    print(f"      meth shape  : {raw['meth'].shape}")
    print(f"      mirna shape : {raw['mirna'].shape}")
    print(f"      labels      : {raw['labels'].shape}, classes={np.unique(raw['labels'])}")
    print(f"      time        : {time.time() - t0:.1f}s")

    print("[2/3] ANOVA feature selection (top-K)...")
    t0 = time.time()
    gene_k = cfg["preprocessing"]["gene_top_k"]
    meth_k = cfg["preprocessing"]["meth_top_k"]
    mirna_k = cfg["preprocessing"].get("mirna_top_k")  # None = use all

    gene_idx = select_top_features(raw["gene"], raw["labels"], gene_k)
    meth_idx = select_top_features(raw["meth"], raw["labels"], meth_k)
    if mirna_k is not None:
        mirna_idx = select_top_features(raw["mirna"], raw["labels"], mirna_k)
    else:
        mirna_idx = np.arange(raw["mirna"].shape[1])

    # Feature names from load_aligned_data — nested dict
    fn_all = raw.get("feature_names", {})
    gene_all  = fn_all.get("gene",  [str(i) for i in range(raw["gene"].shape[1])])
    cpg_all   = fn_all.get("meth",  [str(i) for i in range(raw["meth"].shape[1])])
    mirna_all = fn_all.get("mirna", [str(i) for i in range(raw["mirna"].shape[1])])

    feature_names = {
        "gene":  [gene_all[i]  for i in gene_idx],
        "meth":  [cpg_all[i]   for i in meth_idx],
        "mirna": [mirna_all[i] for i in mirna_idx],
    }
    print(f"      selected: gene={len(feature_names['gene'])}, "
          f"cpg={len(feature_names['meth'])}, mirna={len(feature_names['mirna'])}")
    print(f"      time    : {time.time() - t0:.1f}s")

    print("[3/3] Building HeteroGraph...")
    t0 = time.time()
    graph = build_hetero_graph(feature_names, cfg["data"], cfg["graph"], device="cpu")
    print(f"      time: {time.time() - t0:.1f}s")

    print("[layout] Computing 3-cluster positions...")
    t0 = time.time()
    pos = compute_3cluster_layout(
        n_gene=graph["gene"].num_nodes,
        n_cpg=graph["cpg"].num_nodes,
        n_mirna=graph["mirna"].num_nodes,
        radius=args.cluster_radius,
        cluster_dist=args.cluster_distance,
    )
    print(f"      time: {time.time() - t0:.1f}s")

    print("[render] Plotting graph...")
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    plot_graph(graph, pos, args)


if __name__ == "__main__":
    main()
