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
 
import math
import re
import os
import numpy as np
import pandas as pd
import torch
from torch_geometric.data import HeteroData


def _uniform_attr(n_edges: int) -> torch.Tensor:
    """Edge attribute tensor of all 1.0 for relations without confidence scores."""
    return torch.ones((n_edges, 1), dtype=torch.float32)
 
 
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
 
    print(f"\n🔨 Xây dựng Heterogeneous Graph...")
    print(f"   Gene  nodes : {len(gene_names)}")
    print(f"   CpG   nodes : {len(cpg_names)}")
    print(f"   miRNA nodes : {len(mirna_names)}")
 
    graph = HeteroData()
    graph["gene"].num_nodes  = len(gene_names)
    graph["cpg"].num_nodes   = len(cpg_names)
    graph["mirna"].num_nodes = len(mirna_names)
 
    # ── Cạnh 1: CpG → Gene  (emQTL, weighted by -log10(p)) ───────────
    cpg_gene_edges, cpg_gene_attr = _load_emqtl_edges(
        giac_dir     = giac_dir,
        cancer_types = cfg_data["cancer_types"],
        cpg_idx      = cpg_idx,
        gene_idx     = gene_idx,
        pval_thresh  = cfg_graph["emqtl_pval_threshold"],
        max_edges    = cfg_graph["max_edges_per_node"],
    )
    if cpg_gene_edges is not None:
        graph["cpg", "regulates", "gene"].edge_index    = cpg_gene_edges
        graph["cpg", "regulates", "gene"].edge_attr     = cpg_gene_attr
        graph["gene", "regulated_by", "cpg"].edge_index = cpg_gene_edges.flip(0)
        graph["gene", "regulated_by", "cpg"].edge_attr  = cpg_gene_attr
        print(f"   CpG→Gene edges  : {cpg_gene_edges.shape[1]:,}")
    else:
        print("   ⚠️  emQTL: không có cạnh")

    # ── Cạnh 2: Gene ↔ Gene  (STRING PPI, weighted by score/1000) ────
    if cfg_graph.get("use_ppi", True):
        alias_file = os.path.join(graph_dir, "9606.protein.aliases.v12.0.txt")
        links_file = os.path.join(graph_dir, "9606.protein.links.v12.0.txt")
        ppi_edges, ppi_attr = _load_ppi_edges(
            links_file   = links_file,
            alias_file   = alias_file,
            gene_idx     = gene_idx,
            score_thresh = cfg_graph.get("ppi_score_threshold", 700),
        )
        if ppi_edges is not None:
            graph["gene", "ppi", "gene"].edge_index = ppi_edges
            graph["gene", "ppi", "gene"].edge_attr  = ppi_attr
            print(f"   Gene↔Gene edges : {ppi_edges.shape[1]:,}")
        else:
            print("   ⚠️  STRING PPI: không đọc được file")

    # ── Cạnh 3: miRNA → Gene  (hsa_MTI.csv, uniform 1.0) ─────────────
    mirna_edges = None
    if cfg_graph.get("use_mirna", True):
        mti_file    = os.path.join(graph_dir, "hsa_MTI.csv")
        mirna_edges = _load_mirna_edges(
            mti_file             = mti_file,
            mirna_idx            = mirna_idx,
            gene_idx             = gene_idx,
            max_targets_per_mirna = cfg_graph.get("max_targets_per_mirna", 50),
        )
        if mirna_edges is not None:
            graph["mirna", "targets", "gene"].edge_index    = mirna_edges
            graph["mirna", "targets", "gene"].edge_attr     = _uniform_attr(mirna_edges.shape[1])
            graph["gene", "targeted_by", "mirna"].edge_index = mirna_edges.flip(0)
            graph["gene", "targeted_by", "mirna"].edge_attr  = _uniform_attr(mirna_edges.shape[1])
            print(f"   miRNA→Gene edges: {mirna_edges.shape[1]:,}")
        else:
            print("   ⚠️  miRTarBase: không đọc được file")

    # ── Cạnh 4: Gene ↔ Gene (Reactome co-pathway, uniform 1.0) ───────
    if cfg_graph.get("use_reactome", True):
        reactome_edges = _load_reactome_edges(
            reactome_file    = os.path.join(graph_dir, "Ensembl2Reactome_All_Levels.txt"),
            hgnc_file        = os.path.join(graph_dir, "hgnc_complete_set.txt"),
            gene_idx         = gene_idx,
            max_pathway_size = cfg_graph.get("reactome_max_pathway_size", 50),
            max_edges        = cfg_graph.get("max_edges_per_node", 20),
        )
        if reactome_edges is not None:
            graph["gene", "copathway", "gene"].edge_index = reactome_edges
            graph["gene", "copathway", "gene"].edge_attr  = _uniform_attr(reactome_edges.shape[1])
            print(f"   Gene-Pathway edges : {reactome_edges.shape[1] // 2:,} unique")

    # ── Cạnh 5: miRNA ↔ miRNA (same seed family, uniform 1.0) ────────
    if cfg_graph.get("use_mirna_family", True):
        family_edges = _load_mirna_family_edges(
            family_file = os.path.join(graph_dir, "miR_Family_Info.txt"),
            mirna_idx   = mirna_idx,
        )
        if family_edges is not None:
            graph["mirna", "samefamily", "mirna"].edge_index = family_edges
            graph["mirna", "samefamily", "mirna"].edge_attr  = _uniform_attr(family_edges.shape[1])
            print(f"   miRNA-Family edges : {family_edges.shape[1] // 2:,} unique")

    # ── Cạnh 6: CpG ↔ miRNA (co-regulation, uniform 1.0) ─────────────
    if cpg_gene_edges is not None and mirna_edges is not None:
        cpg_mirna_edges, mirna_cpg_edges = _build_coregulation_edges(
            cpg_gene_edges   = cpg_gene_edges,
            mirna_gene_edges = mirna_edges,
            n_cpg            = len(cpg_names),
            n_mirna          = len(mirna_names),
            max_edges_per_node = cfg_graph.get("max_coregulation_edges", 20),
        )
        if cpg_mirna_edges is not None:
            graph["cpg",   "coregulates", "mirna"].edge_index = cpg_mirna_edges
            graph["cpg",   "coregulates", "mirna"].edge_attr  = _uniform_attr(cpg_mirna_edges.shape[1])
            graph["mirna", "coregulates", "cpg"].edge_index   = mirna_cpg_edges
            graph["mirna", "coregulates", "cpg"].edge_attr    = _uniform_attr(mirna_cpg_edges.shape[1])
            print(f"   CpG↔miRNA edges : {cpg_mirna_edges.shape[1]:,}")

    # ── Cạnh 7: CpG ↔ CpG (cùng CpG island, uniform 1.0) ─────────────
    if cfg_graph.get("use_cpg_island", False):
        manifest_file = cfg_data.get("manifest_file", "")
        if manifest_file:
            island_edges = _load_cpg_island_edges(
                manifest_file      = manifest_file,
                cpg_idx            = cpg_idx,
                relation_filter    = cfg_graph.get("cpg_island_relation", "Island"),
                max_edges_per_node = cfg_graph.get("max_edges_per_node", 20),
            )
            if island_edges is not None:
                graph["cpg", "sameisland", "cpg"].edge_index = island_edges
                graph["cpg", "sameisland", "cpg"].edge_attr  = _uniform_attr(island_edges.shape[1])
                print(f"   CpG-Island edges: {island_edges.shape[1] // 2:,} unique")
        else:
            print("   ⚠️  use_cpg_island=true nhưng manifest_file chưa set trong config")

    # Self-loops (uniform 1.0)
    for nt, count in [("gene", len(gene_names)), ("cpg", len(cpg_names)), ("mirna", len(mirna_names))]:
        ei = _identity_edges(count)
        graph[nt, "self_loop", nt].edge_index = ei
        graph[nt, "self_loop", nt].edge_attr  = _uniform_attr(count)

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
    gene_idx: dict,   # UPPER keys
    pval_thresh: float,
    max_edges: int,
):
    """Load CpG → Gene edges from TCGA emQTL files.

    Returns (edge_index, edge_attr) where edge_attr = -log10(p) / 30 clipped to [0, 1],
    so higher confidence = closer to 1.0. Returns (None, None) when no edges.
    """
    src_list, dst_list, w_list = [], [], []
    cpg_edge_count = {}

    for ct in cancer_types:
        fpath = os.path.join(giac_dir, f"TCGA_emQTL_{ct}.txt")
        if not os.path.exists(fpath):
            print(f"   ⚠️  Không tìm thấy: TCGA_emQTL_{ct}.txt")
            continue

        header_df = pd.read_csv(fpath, sep="\t", nrows=2)
        cols = header_df.columns.tolist()

        cpg_col  = _find_col(cols, ["CpG", "cpg", "probe", "Probe"])
        gene_col = _find_col(cols, ["Gene", "gene", "symbol", "Symbol"])
        pval_col = _find_col(cols, ["p-value", "pvalue", "p_value", "P.Value", "pval"])

        if not all([cpg_col, gene_col, pval_col]):
            print(f"   ⚠️  {ct}: không nhận ra cột (found: {cols[:5]})")
            continue

        print(f"   Parsing emQTL {ct}... ", end="", flush=True)
        count_before = len(src_list)

        for chunk in pd.read_csv(
            fpath, sep="\t", chunksize=200_000,
            usecols=[cpg_col, gene_col, pval_col],
            dtype={cpg_col: str, gene_col: str, pval_col: float},
        ):
            chunk = chunk[chunk[pval_col] < pval_thresh]
            for row in chunk.itertuples(index=False, name=None):
                c_name = str(row[0]).strip()
                g_name = str(row[1]).strip().upper()
                pval   = float(row[2])

                if c_name not in cpg_idx or g_name not in gene_idx:
                    continue
                c_i = cpg_idx[c_name]
                if cpg_edge_count.get(c_i, 0) >= max_edges:
                    continue
                # Confidence: -log10(p) clipped at 30 (= p≤1e-30), normalize to [0,1]
                w = min(-math.log10(max(pval, 1e-30)), 30.0) / 30.0
                src_list.append(c_i)
                dst_list.append(gene_idx[g_name])
                w_list.append(w)
                cpg_edge_count[c_i] = cpg_edge_count.get(c_i, 0) + 1

        print(f"{len(src_list) - count_before:,} edges")

    if not src_list:
        return None, None
    edge_index = torch.tensor([src_list, dst_list], dtype=torch.long)
    edge_attr = torch.tensor(w_list, dtype=torch.float32).unsqueeze(-1)
    return edge_index, edge_attr
 
 
# ─────────────────────────────────────────────
#  STRING PPI
# ─────────────────────────────────────────────
def _load_ppi_edges(
    links_file: str,
    alias_file: str,
    gene_idx: dict,   # UPPER keys
    score_thresh: int = 700,
):
    """Load STRING PPI edges with combined_score as confidence.

    Returns (edge_index, edge_attr) where edge_attr = combined_score / 1000
    (range [0, 1], threshold cuts at score_thresh / 1000).
    """
    if not os.path.exists(links_file) or not os.path.exists(alias_file):
        return None, None

    print("   Building ENSP→symbol map từ alias file...", end=" ", flush=True)

    alias_df = pd.read_csv(alias_file, sep="\t", comment="#",
                           names=["protein_id", "alias", "source"])

    alias_df["alias_upper"] = alias_df["alias"].astype(str).str.strip().str.upper()
    valid_genes = set(gene_idx.keys())
    preferred   = alias_df[alias_df["alias_upper"].isin(valid_genes)]

    ensp_to_gene = (
        preferred.groupby("protein_id")["alias_upper"]
        .first()
        .to_dict()
    )
    print(f"{len(ensp_to_gene):,} proteins mapped")

    print("   Parsing STRING links...", end=" ", flush=True)
    src_list, dst_list, w_list = [], [], []
    seen = set()

    for chunk in pd.read_csv(
        links_file, sep=" ", chunksize=500_000,
        dtype={"protein1": str, "protein2": str, "combined_score": int},
    ):
        chunk = chunk[chunk["combined_score"] >= score_thresh]
        for row in chunk.itertuples(index=False, name=None):
            p1, p2, score = row[0], row[1], int(row[2])
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
            w = score / 1000.0
            src_list += [i1, i2]
            dst_list += [i2, i1]
            w_list += [w, w]

    print(f"{len(src_list)//2:,} unique edges")

    if not src_list:
        return None, None
    edge_index = torch.tensor([src_list, dst_list], dtype=torch.long)
    edge_attr = torch.tensor(w_list, dtype=torch.float32).unsqueeze(-1)
    return edge_index, edge_attr
 
 
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
 
    if not os.path.exists(mti_file):
        return None
 
    print("   Parsing hsa_MTI.csv...", end=" ", flush=True)
    df = pd.read_csv(mti_file)
 
    mirna_col = _find_col(df.columns.tolist(), ["miRNA", "mirna", "mature_mirna"])
    gene_col  = _find_col(df.columns.tolist(), ["Target Gene", "target_gene",
                                                  "gene_symbol", "Gene Symbol"])
    if not mirna_col or not gene_col:
        print(f"không nhận ra cột (found: {df.columns.tolist()[:5]})")
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
            if mirna_target_count.get(m_i, 0) >= max_targets_per_mirna:
                continue
            key = (m_i, g_i)
            if key in seen:
                continue
            seen.add(key)
            src_list.append(m_i)
            dst_list.append(g_i)
            mirna_target_count[m_i] = mirna_target_count.get(m_i, 0) + 1
 
    print(f"{len(src_list):,} edges")
 
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)
 
 
# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
 
 
# ─────────────────────────────────────────────
#  Co-regulation edges: CpG ↔ miRNA
#  Nếu CpG_i và miRNA_j cùng regulate Gene_k
#  → thêm cạnh CpG_i → miRNA_j và ngược lại
#  Tạo vòng khép kín: CpG → Gene → miRNA → Gene → CpG
# ─────────────────────────────────────────────
def _build_coregulation_edges(
    cpg_gene_edges: torch.Tensor,    # (2, E1): src=cpg_idx, dst=gene_idx
    mirna_gene_edges: torch.Tensor,  # (2, E2): src=mirna_idx, dst=gene_idx
    n_cpg: int,
    n_mirna: int,
    max_edges_per_node: int = 20,    # giới hạn để tránh đồ thị quá dày
) -> tuple:
    """
    Tìm các cặp (CpG, miRNA) cùng regulate ít nhất 1 gene chung.
    Trả về (cpg_mirna_edges, mirna_cpg_edges) dạng (2, E).
    """
    print("   Building CpG↔miRNA co-regulation edges...", end=" ", flush=True)
 
    # Build dict: gene_idx → set of cpg_idx
    gene_to_cpg = {}
    for i in range(cpg_gene_edges.shape[1]):
        c_i = cpg_gene_edges[0, i].item()
        g_i = cpg_gene_edges[1, i].item()
        gene_to_cpg.setdefault(g_i, set()).add(c_i)
 
    # Build dict: gene_idx → set of mirna_idx
    gene_to_mirna = {}
    for i in range(mirna_gene_edges.shape[1]):
        m_i = mirna_gene_edges[0, i].item()
        g_i = mirna_gene_edges[1, i].item()
        gene_to_mirna.setdefault(g_i, set()).add(m_i)
 
    # Tìm shared genes → tạo CpG↔miRNA edges
    cpg_mirna_src, cpg_mirna_dst = [], []
    mirna_cpg_src, mirna_cpg_dst = [], []
    cpg_edge_count   = {}
    mirna_edge_count = {}
    seen = set()
 
    for g_i, cpg_set in gene_to_cpg.items():
        mirna_set = gene_to_mirna.get(g_i, set())
        if not mirna_set:
            continue
        for c_i in cpg_set:
            if cpg_edge_count.get(c_i, 0) >= max_edges_per_node:
                continue
            for m_i in mirna_set:
                if mirna_edge_count.get(m_i, 0) >= max_edges_per_node:
                    continue
                key = (c_i, m_i)
                if key in seen:
                    continue
                seen.add(key)
                cpg_mirna_src.append(c_i)
                cpg_mirna_dst.append(m_i)
                mirna_cpg_src.append(m_i)
                mirna_cpg_dst.append(c_i)
                cpg_edge_count[c_i]   = cpg_edge_count.get(c_i, 0) + 1
                mirna_edge_count[m_i] = mirna_edge_count.get(m_i, 0) + 1
 
    print(f"{len(cpg_mirna_src):,} edges")
 
    if not cpg_mirna_src:
        return None, None
 
    cpg_mirna = torch.tensor([cpg_mirna_src, cpg_mirna_dst], dtype=torch.long)
    mirna_cpg = torch.tensor([mirna_cpg_src, mirna_cpg_dst], dtype=torch.long)
    return cpg_mirna, mirna_cpg
 
 
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
 
# ─────────────────────────────────────────────
#  Reactome co-pathway  (Gene ↔ Gene)
# ─────────────────────────────────────────────
 
def _load_reactome_edges(reactome_file, hgnc_file, gene_idx, max_pathway_size=50, max_edges=20):
    if not os.path.exists(reactome_file):
        print("   ⚠️  Ensembl2Reactome_All_Levels.txt không tìm thấy")
        return None
 
    # Ensembl → gene symbol map
    ensembl_to_sym = {}
    if os.path.exists(hgnc_file):
        try:
            hgnc = pd.read_csv(hgnc_file, sep="\t", low_memory=False,
                               usecols=["symbol", "ensembl_gene_id"])
            hgnc = hgnc.dropna(subset=["symbol", "ensembl_gene_id"])
            for _, row in hgnc.iterrows():
                sym = str(row["symbol"]).strip().upper()
                eid = str(row["ensembl_gene_id"]).strip()
                if sym in gene_idx:
                    ensembl_to_sym[eid] = sym
        except Exception:
            pass
 
    pathway_to_genes = {}
    try:
        for chunk in pd.read_csv(
            reactome_file, sep="\t", header=None, chunksize=200_000,
            names=["ensembl", "pathway_id", "url", "pathway_name", "evidence", "species"],
            dtype=str,
        ):
            chunk = chunk[chunk["species"].str.strip() == "Homo sapiens"]
            for row in chunk.itertuples(index=False, name=None):
                sym = ensembl_to_sym.get(str(row[0]).strip(), "")
                if not sym or sym not in gene_idx:
                    continue
                pathway_to_genes.setdefault(str(row[1]).strip(), set()).add(sym)
    except Exception as e:
        print(f"   ⚠️  Reactome parse error: {e}")
        return None
 
    src_list, dst_list = [], []
    seen = set()
    edge_count = {}
 
    for pid, gset in pathway_to_genes.items():
        if len(gset) > max_pathway_size:
            continue
        glist = [gene_idx[g] for g in gset if g in gene_idx]
        for a in range(len(glist)):
            for b in range(a + 1, len(glist)):
                i1, i2 = glist[a], glist[b]
                if edge_count.get(i1, 0) >= max_edges or edge_count.get(i2, 0) >= max_edges:
                    continue
                key = (min(i1, i2), max(i1, i2))
                if key in seen:
                    continue
                seen.add(key)
                src_list += [i1, i2]; dst_list += [i2, i1]
                edge_count[i1] = edge_count.get(i1, 0) + 1
                edge_count[i2] = edge_count.get(i2, 0) + 1
 
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)
 
 
# ─────────────────────────────────────────────
#  CpG island  (CpG ↔ CpG)
# ─────────────────────────────────────────────

def _load_cpg_island_edges(
    manifest_file: str,
    cpg_idx: dict,
    relation_filter: str = "Island",   # "Island" | "Island+Shore" | "all"
    max_edges_per_node: int = 20,
) -> "torch.Tensor | None":
    """
    Đọc Illumina 450K manifest, tìm các CpG probe cùng UCSC CpG island,
    thêm cạnh vô hướng giữa chúng.

    relation_filter:
        "Island"       — chỉ probes có Relation_to_UCSC_CpG_Island == "Island"
        "Island+Shore" — Island + N_Shore + S_Shore
        "all"          — mọi probe có UCSC_CpG_Islands_Name không rỗng
    """
    if not os.path.exists(manifest_file):
        print("   ⚠️  Illumina manifest không tìm thấy")
        return None

    print("   Parsing Illumina 450K manifest...", end=" ", flush=True)

    # File có header [Heading]/[Assay] — tìm dòng bắt đầu bằng "IlmnID"
    skiprows = None
    try:
        with open(manifest_file, encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if line.startswith("IlmnID"):
                    skiprows = i
                    break
    except Exception as e:
        print(f"lỗi đọc file: {e}")
        return None

    if skiprows is None:
        print("   ⚠️  Không tìm thấy header IlmnID trong manifest")
        return None

    try:
        df = pd.read_csv(
            manifest_file,
            skiprows=skiprows,
            usecols=["Name", "UCSC_CpG_Islands_Name", "Relation_to_UCSC_CpG_Island"],
            dtype=str,
            encoding="utf-8",
            low_memory=False,
        )
    except Exception:
        try:
            df = pd.read_csv(
                manifest_file,
                skiprows=skiprows,
                usecols=["Name", "UCSC_CpG_Islands_Name", "Relation_to_UCSC_CpG_Island"],
                dtype=str,
                encoding="latin-1",
                low_memory=False,
            )
        except Exception as e:
            print(f"lỗi parse CSV: {e}")
            return None

    # Lọc theo relation
    valid_relations: set
    if relation_filter == "Island":
        valid_relations = {"Island"}
    elif relation_filter == "Island+Shore":
        valid_relations = {"Island", "N_Shore", "S_Shore"}
    else:
        valid_relations = None  # type: ignore

    df = df.dropna(subset=["UCSC_CpG_Islands_Name", "Relation_to_UCSC_CpG_Island"])
    df = df[df["UCSC_CpG_Islands_Name"].str.strip() != ""]
    if valid_relations is not None:
        df = df[df["Relation_to_UCSC_CpG_Island"].str.strip().isin(valid_relations)]

    # Group by island → list probe indices (chỉ giữ probe có trong cpg_idx)
    island_to_cpg: dict[str, list[int]] = {}
    for _, row in df.iterrows():
        probe = str(row["Name"]).strip()
        island = str(row["UCSC_CpG_Islands_Name"]).strip()
        if probe in cpg_idx:
            island_to_cpg.setdefault(island, []).append(cpg_idx[probe])

    # Build edges với cap per-node
    src_list, dst_list = [], []
    seen: set[tuple[int, int]] = set()
    edge_count: dict[int, int] = {}

    for island, indices in island_to_cpg.items():
        unique = list(set(indices))
        if len(unique) < 2:
            continue
        for a in range(len(unique)):
            for b in range(a + 1, len(unique)):
                i1, i2 = unique[a], unique[b]
                if edge_count.get(i1, 0) >= max_edges_per_node:
                    continue
                if edge_count.get(i2, 0) >= max_edges_per_node:
                    continue
                key = (min(i1, i2), max(i1, i2))
                if key in seen:
                    continue
                seen.add(key)
                src_list += [i1, i2]
                dst_list += [i2, i1]
                edge_count[i1] = edge_count.get(i1, 0) + 1
                edge_count[i2] = edge_count.get(i2, 0) + 1

    print(f"{len(src_list) // 2:,} unique CpG-island edges")
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────
#  miRNA family  (miRNA ↔ miRNA)
# ─────────────────────────────────────────────
 
def _load_mirna_family_edges(family_file, mirna_idx):
    if not os.path.exists(family_file):
        print("   ⚠️  miR_Family_Info.txt không tìm thấy")
        return None
 
    try:
        df = pd.read_csv(family_file, sep="\t", dtype=str)
    except Exception:
        try:
            df = pd.read_csv(family_file, sep="\t", dtype=str, encoding="latin-1")
        except Exception as e:
            print(f"   ⚠️  miR_Family_Info parse error: {e}")
            return None
 
    family_col  = _find_col(df.columns.tolist(), ["miR Family", "miR_Family", "family"])
    mirna_col   = _find_col(df.columns.tolist(), ["MiRBase ID", "miRBase_ID", "miRNA"])
    species_col = _find_col(df.columns.tolist(), ["Species", "species", "Species ID"])
 
    if not family_col or not mirna_col:
        print(f"   ⚠️  miR_Family_Info: không nhận ra cột {df.columns.tolist()[:5]}")
        return None
 
    if species_col:
        df = df[df[species_col].astype(str).str.contains("9606|sapiens", na=False)]
 
    def normalize_mature(name: str) -> str:
        """
        'hsa-miR-21-5p' → 'hsa-mir-21'
        'hsa-miR-21-3p' → 'hsa-mir-21'
        Only strips -5p / -3p suffix, nothing else.
        """
        name = name.strip().lower()
        return re.sub(r'-[35]p$', '', name)
 
    # Build TCGA-normalised base -> list of indices (uses module-level _normalize_tcga_mirna)
    tcga_base_to_idx = {}
    for tcga_name, idx in mirna_idx.items():
        base = _normalize_tcga_mirna(tcga_name)
        tcga_base_to_idx.setdefault(base, []).append(idx)
 
    # Build family → list of mirna indices
    family_to_indices = {}
    for _, row in df[[family_col, mirna_col]].iterrows():
        fam  = str(row[family_col]).strip()
        base = normalize_mature(str(row[mirna_col]))
        for idx in tcga_base_to_idx.get(base, []):
            family_to_indices.setdefault(fam, []).append(idx)
 
    # Cap: skip families with > 20 members (likely normalization artifact)
    MAX_FAMILY_SIZE = 20
 
    src_list, dst_list = [], []
    seen = set()
 
    for fam, indices in family_to_indices.items():
        unique = list(set(indices))
        if len(unique) < 2 or len(unique) > MAX_FAMILY_SIZE:
            continue
        for a in range(len(unique)):
            for b in range(a + 1, len(unique)):
                i1, i2 = unique[a], unique[b]
                key = (min(i1, i2), max(i1, i2))
                if key in seen:
                    continue
                seen.add(key)
                src_list += [i1, i2]; dst_list += [i2, i1]
 
    print(f"   Parsing miRNA family info... {len(src_list) // 2:,} unique edges")
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)