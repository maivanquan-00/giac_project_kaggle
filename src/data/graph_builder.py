"""
graph_builder.py
----------------
Xây dựng Heterogeneous Graph từ các file thực tế.
 
File sử dụng:
    GIAC_main/TCGA_emQTL_{COAD,ESCA,READ,STAD}.txt  → cạnh CpG → Gene
    hsa_MTI.csv                                      → cạnh miRNA → Gene
    9606.protein.links.v12.0.txt                     → cạnh Gene ↔ Gene (PPI)
    9606.protein.aliases.v12.0.txt                   → map ENSP → gene symbol
 
Nguyên tắc matching tên:
    - Tất cả gene symbol được normalize về UPPERCASE trước khi lookup
    - gene_idx, cpg_idx, mirna_idx đều dùng key đã normalize
    - Đảm bảo match nhất quán dù CSV dùng mixed case
"""
 
import re
import os
import numpy as np
import pandas as pd
import torch
from torch_geometric.data import HeteroData


# 8 relations in fixed order (3 file curated: emQTL + miRTarBase + PPI, + self-loops).
RELATION_ORDER = [
    (("cpg",   "regulates",    "gene"),  "→", "emQTL"),
    (("gene",  "regulated_by", "cpg"),   "→", "emQTL reverse"),
    (("gene",  "ppi",          "gene"),  "↔", "STRING PPI"),
    (("mirna", "targets",      "gene"),  "→", "miRTarBase"),
    (("gene",  "targeted_by",  "mirna"), "→", "miRTarBase reverse"),
    (("gene",  "self_loop",    "gene"),  "↔", "identity"),
    (("cpg",   "self_loop",    "cpg"),   "↔", "identity"),
    (("mirna", "self_loop",    "mirna"), "↔", "identity"),
]


def _print_relation_summary(graph) -> None:
    """Numbered table of all 8 declared relations with edge counts + max node degree.

    Cột `max deg` = degree lớn nhất của 1 node trong quan hệ đó (max của in/out).
    Dùng để phát hiện "hub nổ degree" khi bỏ cap — degree càng to → đồ thị càng nặng
    và càng dễ over-smoothing trong GAT.
    """
    print("\n📋 Graph relations (8 declared):")
    total = 0
    n_active = 0
    max_deg_global = 0
    for i, (et, arrow, desc) in enumerate(RELATION_ORDER, start=1):
        src, rel, dst = et
        ei = graph[et].edge_index if et in graph.edge_index_dict else None
        n_edges = int(ei.shape[1]) if ei is not None else 0
        deg = 0
        if ei is not None and n_edges > 0:
            deg = max(int(torch.bincount(ei[0]).max()), int(torch.bincount(ei[1]).max()))
            max_deg_global = max(max_deg_global, deg)
        marker = "✓" if n_edges > 0 else "✗"
        rel_str = f"{src:5s} {arrow}{rel:15s}{arrow} {dst:5s}"
        print(f"   [{i:2d}] {marker} {rel_str}  ({desc:20s}) : {n_edges:>8,} edges  (max deg {deg:>5,})")
        total += n_edges
        if n_edges > 0:
            n_active += 1
    print(f"   {'─' * 74}")
    print(f"   Total: {n_active}/8 active, {total:,} edges  |  max node degree = {max_deg_global:,}")
    _print_degree_distribution(graph)


def _print_degree_distribution(graph) -> None:
    """Phân bố degree mỗi node-type (tổng qua các relation, bỏ self-loop).

    Để thấy đồ thị 'dày' thật hay chỉ vài hub: nhìn avg/median (thấp = thưa) vs
    max (cao = có hub). Nếu median thấp mà max cao → thưa + vài hub sinh học.
    """
    print("   ── Node degree (bỏ self-loop) ──")
    for nt in ["gene", "cpg", "mirna"]:
        n = graph[nt].num_nodes
        deg = torch.zeros(n, dtype=torch.long)
        for (s, r, d), ei in graph.edge_index_dict.items():
            if r == "self_loop":
                continue
            if s == nt:
                deg += torch.bincount(ei[0].cpu(), minlength=n)
            if d == nt:
                deg += torch.bincount(ei[1].cpu(), minlength=n)
        degf = deg.float()
        connected = int((deg > 0).sum())
        p95 = int(torch.quantile(degf, 0.95).item()) if n > 0 else 0
        print(f"     {nt:5s}: avg={degf.mean():.1f}  median={int(degf.median())}  "
              f"p95={p95}  max={int(deg.max())}  "
              f"| deg>50: {int((deg > 50).sum())} node  | có cạnh: {connected}/{n}")
 
 
def build_hetero_graph(
    feature_names: dict,
    cfg_data: dict,
    cfg_graph: dict,
    device: str = "cpu",
) -> HeteroData:
 
    graph_dir = cfg_data["graph_dir"]
    giac_dir  = cfg_data.get("emqtl_dir") or os.path.join(graph_dir, "GIAC_main")
 
    gene_names  = feature_names["gene"]
    cpg_names   = feature_names["meth"]
    mirna_names = feature_names["mirna"]
 
    # ── Normalize keys: gene → UPPER, cpg → giữ nguyên (cg12345 format), mirna → lower ──
    gene_idx  = {g.upper(): i for i, g in enumerate(gene_names)}
    cpg_idx   = {c: i for i, c in enumerate(cpg_names)}          # cg... không đổi
    mirna_idx = {m.lower(): i for i, m in enumerate(mirna_names)} # hsa-... lowercase
 
    graph = HeteroData()
    graph["gene"].num_nodes  = len(gene_names)
    graph["cpg"].num_nodes   = len(cpg_names)
    graph["mirna"].num_nodes = len(mirna_names)

    # ── 1+2: CpG ↔ Gene  (TCGA emQTL) ─────────────────────────────────
    cpg_gene_edges = None
    if cfg_graph.get("use_emqtl", True):
        cpg_gene_edges = _load_emqtl_edges(
            giac_dir     = giac_dir,
            cancer_types = cfg_data["cancer_types"],
            cpg_idx      = cpg_idx,
            gene_idx     = gene_idx,
            pval_thresh  = cfg_graph["emqtl_pval_threshold"],
            max_edges    = cfg_graph["max_edges_per_node"],
        )
        if cpg_gene_edges is not None:
            graph["cpg", "regulates", "gene"].edge_index    = cpg_gene_edges
            graph["gene", "regulated_by", "cpg"].edge_index = cpg_gene_edges.flip(0)

    # ── 3: Gene ↔ Gene  (STRING PPI) ──────────────────────────────────
    if cfg_graph.get("use_ppi", True):
        ppi_edges = _load_ppi_edges(
            links_file   = os.path.join(graph_dir, "9606.protein.links.v12.0.txt"),
            alias_file   = os.path.join(graph_dir, "9606.protein.aliases.v12.0.txt"),
            gene_idx     = gene_idx,
            score_thresh = cfg_graph.get("ppi_score_threshold", 700),
        )
        if ppi_edges is not None:
            graph["gene", "ppi", "gene"].edge_index = ppi_edges

    # ── 4+5: miRNA ↔ Gene  (miRTarBase) ───────────────────────────────
    mirna_edges = None
    if cfg_graph.get("use_mirna", True):
        mirna_edges = _load_mirna_edges(
            mti_file              = os.path.join(graph_dir, "hsa_MTI.csv"),
            mirna_idx             = mirna_idx,
            gene_idx              = gene_idx,
            max_targets_per_mirna = cfg_graph.get("max_targets_per_mirna", 50),
        )
        if mirna_edges is not None:
            graph["mirna", "targets", "gene"].edge_index    = mirna_edges
            graph["gene", "targeted_by", "mirna"].edge_index = mirna_edges.flip(0)

    # ── self-loops ────────────────────────────────────────────────────
    for nt, count in [("gene", len(gene_names)), ("cpg", len(cpg_names)), ("mirna", len(mirna_names))]:
        graph[nt, "self_loop", nt].edge_index = _identity_edges(count)

    _print_relation_summary(graph)
    return graph.to(device)


def get_edge_stats(graph) -> dict:
    """Per-relation edge counts from a HeteroData graph.

    Returns dict with `per_relation`, `total_edges`, `n_relations_total`,
    `n_relations_active`. Use to audit which of the 13 declared relations
    actually carry edges in a given fold.
    """
    per_rel = {}
    total = 0
    for et, ei in graph.edge_index_dict.items():
        rel = f"{et[0]}-{et[1]}-{et[2]}"
        n = int(ei.shape[1]) if ei is not None else 0
        per_rel[rel] = n
        total += n
    n_active = sum(1 for v in per_rel.values() if v > 0)
    return {
        "per_relation": per_rel,
        "total_edges": total,
        "n_relations_total": len(per_rel),
        "n_relations_active": n_active,
    }
 
 
# ─────────────────────────────────────────────
#  emQTL
# ─────────────────────────────────────────────
def _load_emqtl_edges(
    giac_dir: str,
    cancer_types: list,
    cpg_idx: dict,
    gene_idx: dict,
    pval_thresh: float,
    max_edges: int,
) -> torch.Tensor | None:
    """Load CpG → Gene edges from TCGA emQTL files. Returns None when no edges.

    Cap ĐỐI XỨNG theo p-value (max_edges áp cho CẢ 2 đầu):
      - Gom mọi cặp (CpG, gene) pval<thresh, dedup giữ p-value nhỏ nhất (qua nhiều
        file ung thư COAD/ESCA/READ/STAD).
      - Sort theo p-value tăng dần, greedy giữ cạnh nếu CẢ degree(CpG) < cap VÀ
        degree(gene) < cap → mỗi gene giữ `max_edges` CpG mạnh nhất, mỗi CpG giữ
        `max_edges` gene mạnh nhất.
    Khác cap cũ (chỉ chặn out-degree CpG → gene popular vẫn hub 400+): cap này
    chặn HUB GENE (in-degree) → đồ thị thưa đều, defensible. max_edges=None = ko cap.
    """
    # 1) Gom candidate: (c_i, g_i) → p-value nhỏ nhất
    best_pval: dict = {}
    for ct in cancer_types:
        fpath = os.path.join(giac_dir, f"TCGA_emQTL_{ct}.txt")
        if not os.path.isfile(fpath):
            if os.path.isdir(fpath):
                print(f"   ⚠️  TCGA_emQTL_{ct}.txt là DIRECTORY (not file) — skip emQTL cho {ct}")
            continue

        header_df = pd.read_csv(fpath, sep="\t", nrows=2)
        cols = header_df.columns.tolist()
        cpg_col  = _find_col(cols, ["CpG", "cpg", "probe", "Probe"])
        gene_col = _find_col(cols, ["Gene", "gene", "symbol", "Symbol"])
        pval_col = _find_col(cols, ["p-value", "pvalue", "p_value", "P.Value", "pval"])
        if not all([cpg_col, gene_col, pval_col]):
            continue

        for chunk in pd.read_csv(
            fpath, sep="\t", chunksize=200_000,
            usecols=[cpg_col, gene_col, pval_col],
            dtype={cpg_col: str, gene_col: str, pval_col: float},
        ):
            chunk = chunk[chunk[pval_col] < pval_thresh]
            for row in chunk.itertuples(index=False, name=None):
                c_name = str(row[0]).strip()
                g_name = str(row[1]).strip().upper()
                if c_name not in cpg_idx or g_name not in gene_idx:
                    continue
                key = (cpg_idx[c_name], gene_idx[g_name])
                pv = float(row[2])
                if key not in best_pval or pv < best_pval[key]:
                    best_pval[key] = pv

    if not best_pval:
        return None

    # 2) Sort theo p-value, greedy cap đối xứng cả 2 đầu
    items = sorted(best_pval.items(), key=lambda kv: kv[1])
    cpg_deg, gene_deg = {}, {}
    src_list, dst_list = [], []
    for (c_i, g_i), _pv in items:
        if max_edges is not None and (cpg_deg.get(c_i, 0) >= max_edges
                                      or gene_deg.get(g_i, 0) >= max_edges):
            continue
        src_list.append(c_i)
        dst_list.append(g_i)
        cpg_deg[c_i]  = cpg_deg.get(c_i, 0) + 1
        gene_deg[g_i] = gene_deg.get(g_i, 0) + 1

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)
 
 
# ─────────────────────────────────────────────
#  STRING PPI
# ─────────────────────────────────────────────
def _load_ppi_edges(
    links_file: str,
    alias_file: str,
    gene_idx: dict,
    score_thresh: int = 700,
) -> torch.Tensor | None:
    """Load STRING PPI edges. Returns None when files missing or no edges."""
    if not os.path.isfile(links_file) or not os.path.isfile(alias_file):
        return None

    alias_df = pd.read_csv(alias_file, sep="\t", comment="#",
                           names=["protein_id", "alias", "source"])
    alias_df["alias_upper"] = alias_df["alias"].astype(str).str.strip().str.upper()
    valid_genes = set(gene_idx.keys())
    preferred = alias_df[alias_df["alias_upper"].isin(valid_genes)]
    ensp_to_gene = preferred.groupby("protein_id")["alias_upper"].first().to_dict()

    src_list, dst_list = [], []
    seen = set()
    for chunk in pd.read_csv(
        links_file, sep=" ", chunksize=500_000,
        dtype={"protein1": str, "protein2": str, "combined_score": int},
    ):
        chunk = chunk[chunk["combined_score"] >= score_thresh]
        for row in chunk.itertuples(index=False, name=None):
            p1, p2 = row[0], row[1]
            g1 = ensp_to_gene.get(p1, "")
            g2 = ensp_to_gene.get(p2, "")
            if not g1 or not g2:
                continue
            if g1 not in gene_idx or g2 not in gene_idx:
                continue
            i1, i2 = gene_idx[g1], gene_idx[g2]
            key = (min(i1, i2), max(i1, i2))
            if key in seen:
                continue
            seen.add(key)
            src_list += [i1, i2]
            dst_list += [i2, i1]

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)
 
 
# ─────────────────────────────────────────────
#  miRNA name normalisation (shared helper)
# ─────────────────────────────────────────────
def _normalize_tcga_mirna(name: str) -> str:
    """Strip precursor-isoform suffix (-1/-2/-3) from TCGA/GDC stem-loop IDs.

    Correctly handles:
        hsa-mir-21-1   → hsa-mir-21   (isoform suffix, remove)
        hsa-mir-100-1  → hsa-mir-100  (isoform suffix, remove)
        hsa-mir-100    → hsa-mir-100  (number is part of name, keep)
        hsa-mir-21     → hsa-mir-21   (no suffix, unchanged)

    The old `re.sub(r'-\\d+$', ...)` was too greedy and would convert
    hsa-mir-100 → hsa-mir, breaking the lookup for many miRNA families.
    """
    name = name.strip().lower()
    m = re.match(r'^(hsa-(?:mir|let)-\S+?)-([1-9])$', name)
    return m.group(1) if m else name


# ─────────────────────────────────────────────
#  miRTarBase
# ─────────────────────────────────────────────
def _load_mirna_edges(
    mti_file: str,
    mirna_idx: dict,  # lowercase keys
    gene_idx: dict,   # UPPER keys
    max_targets_per_mirna: int = 50,
) -> torch.Tensor | None:
 
    if not os.path.isfile(mti_file):
        return None

    df = pd.read_csv(mti_file)

    mirna_col = _find_col(df.columns.tolist(), ["miRNA", "mirna", "mature_mirna"])
    gene_col  = _find_col(df.columns.tolist(), ["Target Gene", "target_gene",
                                                  "gene_symbol", "Gene Symbol"])
    if not mirna_col or not gene_col:
        print(f"   ⚠️  hsa_MTI.csv không nhận ra cột (found: {df.columns.tolist()[:5]})")
        return None
 
    # Map: base miRNA name (lowercase, bỏ -5p/-3p) → list indices trong mirna_idx
    # Vì mirna_idx keys là "hsa-let-7a-1" (lowercase, có số precursor)
    # MTI file dùng "hsa-let-7a-5p" (mature, có -5p/-3p)
    base_to_indices = {}
    for tcga_name, idx in mirna_idx.items():
        base = _normalize_tcga_mirna(tcga_name)
        base_to_indices.setdefault(base, []).append(idx)
 
    src_list, dst_list = [], []
    seen = set()
 
    mirna_target_count = {}   # m_i → number of targets already added

    for row in df[[mirna_col, gene_col]].itertuples(index=False, name=None):
        m_raw = str(row[0]).strip().lower()
        g_raw = str(row[1]).strip().upper()  # gene → UPPER
 
        # Normalize mature miRNA: bỏ -5p/-3p
        m_base = re.sub(r'-[35]p$', '', m_raw)
 
        if g_raw not in gene_idx or m_base not in base_to_indices:
            continue
 
        g_i = gene_idx[g_raw]
        for m_i in base_to_indices[m_base]:
            if max_targets_per_mirna is not None and mirna_target_count.get(m_i, 0) >= max_targets_per_mirna:
                continue                               # None → không giới hạn số target/miRNA
            key = (m_i, g_i)
            if key in seen:
                continue
            seen.add(key)
            src_list.append(m_i)
            dst_list.append(g_i)
            mirna_target_count[m_i] = mirna_target_count.get(m_i, 0) + 1

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)
 
 
# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
 
 
def _find_col(columns: list, candidates: list) -> str | None:
    col_lower = [c.lower() for c in columns]
    for cand in candidates:
        for i, c in enumerate(col_lower):
            if cand.lower() == c or cand.lower() in c:
                return columns[i]
    return None
 
 
def _identity_edges(n_nodes: int) -> torch.Tensor:
    idx = torch.arange(n_nodes, dtype=torch.long)
    return torch.stack([idx, idx], dim=0)
