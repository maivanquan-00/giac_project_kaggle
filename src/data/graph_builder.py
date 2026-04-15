"""
graph_builder.py
----------------
Xây dựng Heterogeneous Graph từ các file thực tế:

  Đường dẫn gốc: /content/drive/MyDrive/ĐATN_2025.2/Heterogeneous_Graph/

  File sử dụng:
    GIAC_main/TCGA_emQTL_{COAD,ESCA,READ,STAD}.txt  → cạnh CpG → Gene
    hsa_MTI.csv                                      → cạnh miRNA → Gene
    9606.protein.links.v12.0.txt                     → cạnh Gene ↔ Gene (PPI)
    9606.protein.aliases.v12.0.txt                   → map ENSP protein ID → gene symbol

Đồ thị nodes:
    'gene'  : gene nodes  (F_gene nodes)
    'cpg'   : CpG nodes   (F_cpg nodes)
    'mirna' : miRNA nodes (F_mirna nodes)
"""

import os
import numpy as np
import pandas as pd
import torch
from torch_geometric.data import HeteroData


# ─────────────────────────────────────────────
#  Hàm chính
# ─────────────────────────────────────────────
def build_hetero_graph(
    feature_names: dict,
    cfg_data: dict,
    cfg_graph: dict,
    device: str = "cpu",
) -> HeteroData:
    """
    Parameters
    ----------
    feature_names : {'gene': [...], 'meth': [...], 'mirna': [...]}
    cfg_data      : config.yaml['data']
    cfg_graph     : config.yaml['graph']
    device        : 'cpu' hoặc 'cuda'
    """
    graph_dir = cfg_data["graph_dir"]
    giac_dir  = os.path.join(graph_dir, "GIAC_main")

    gene_names  = feature_names["gene"]
    cpg_names   = feature_names["meth"]
    mirna_names = feature_names["mirna"]

    gene_idx  = {g: i for i, g in enumerate(gene_names)}
    cpg_idx   = {c: i for i, c in enumerate(cpg_names)}
    mirna_idx = {m: i for i, m in enumerate(mirna_names)}

    print(f"\n🔨 Xây dựng Heterogeneous Graph...")
    print(f"   Gene  nodes : {len(gene_names)}")
    print(f"   CpG   nodes : {len(cpg_names)}")
    print(f"   miRNA nodes : {len(mirna_names)}")

    graph = HeteroData()
    graph["gene"].num_nodes  = len(gene_names)
    graph["cpg"].num_nodes   = len(cpg_names)
    graph["mirna"].num_nodes = len(mirna_names)

    # ── Cạnh 1: CpG → Gene  (emQTL) ──────────────────────────────────
    cpg_gene_edges = _load_emqtl_edges(
        giac_dir    = giac_dir,
        cancer_types = cfg_data["cancer_types"],
        cpg_idx     = cpg_idx,
        gene_idx    = gene_idx,
        pval_thresh = cfg_graph["emqtl_pval_threshold"],
        max_edges   = cfg_graph["max_edges_per_node"],
    )
    if cpg_gene_edges is not None:
        graph["cpg", "regulates", "gene"].edge_index = cpg_gene_edges
        print(f"   CpG→Gene edges  : {cpg_gene_edges.shape[1]:,}")
    else:
        print("   ⚠️  emQTL: không có cạnh → dùng self-loop fallback")
        graph["cpg", "regulates", "gene"].edge_index = _self_loop_edges(
            len(cpg_names), len(gene_names)
        )

    # ── Cạnh 2: Gene ↔ Gene  (STRING PPI) ────────────────────────────
    if cfg_graph.get("use_ppi", True):
        alias_file = os.path.join(graph_dir, "9606.protein.aliases.v12.0.txt")
        links_file = os.path.join(graph_dir, "9606.protein.links.v12.0.txt")
        ppi_edges  = _load_ppi_edges(
            links_file  = links_file,
            alias_file  = alias_file,
            gene_idx    = gene_idx,
            score_thresh = cfg_graph.get("ppi_score_threshold", 700),
        )
        if ppi_edges is not None:
            graph["gene", "interacts", "gene"].edge_index = ppi_edges
            print(f"   Gene↔Gene edges : {ppi_edges.shape[1]:,}")
        else:
            print("   ⚠️  STRING PPI: không đọc được file")

    # ── Cạnh 3: miRNA → Gene  (hsa_MTI.csv) ──────────────────────────
    if cfg_graph.get("use_mirna", True):
        mti_file   = os.path.join(graph_dir, "hsa_MTI.csv")
        mirna_edges = _load_mirna_edges(
            mti_file  = mti_file,
            mirna_idx = mirna_idx,
            gene_idx  = gene_idx,
        )
        if mirna_edges is not None:
            graph["mirna", "targets", "gene"].edge_index = mirna_edges
            print(f"   miRNA→Gene edges: {mirna_edges.shape[1]:,}")
        else:
            print("   ⚠️  miRTarBase: không đọc được file")

    return graph.to(device)


# ─────────────────────────────────────────────
#  Parse emQTL  (TCGA_emQTL_COAD.txt ...)
# ─────────────────────────────────────────────
def _load_emqtl_edges(
    giac_dir: str,
    cancer_types: list,
    cpg_idx: dict,
    gene_idx: dict,
    pval_thresh: float,
    max_edges: int,
) -> torch.Tensor | None:
    """
    Format file TCGA_emQTL_*.txt từ DNMIVD:
    Đọc header thực tế của file để xác định tên cột đúng.
    Thường có dạng: CpG  Gene  beta  p-value  FDR  ...
    """
    src_list, dst_list = [], []
    cpg_edge_count = {}  # giới hạn max_edges mỗi CpG

    for ct in cancer_types:
        fpath = os.path.join(giac_dir, f"TCGA_emQTL_{ct}.txt")
        if not os.path.exists(fpath):
            print(f"   ⚠️  Không tìm thấy: TCGA_emQTL_{ct}.txt")
            continue

        # Đọc 2 dòng đầu để kiểm tra header
        header_df = pd.read_csv(fpath, sep="\t", nrows=2)
        cols = header_df.columns.tolist()

        # Tự động detect tên cột CpG, Gene, p-value
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
            for row in chunk.itertuples(index=False):
                c_name = getattr(row, cpg_col)
                g_name = getattr(row, gene_col)
                if c_name not in cpg_idx or g_name not in gene_idx:
                    continue
                c_i = cpg_idx[c_name]
                if cpg_edge_count.get(c_i, 0) >= max_edges:
                    continue
                src_list.append(c_i)
                dst_list.append(gene_idx[g_name])
                cpg_edge_count[c_i] = cpg_edge_count.get(c_i, 0) + 1

        print(f"{len(src_list) - count_before:,} edges")

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────
#  Parse STRING PPI
#  9606.protein.links.v12.0.txt  +  9606.protein.aliases.v12.0.txt
# ─────────────────────────────────────────────
def _load_ppi_edges(
    links_file: str,
    alias_file: str,
    gene_idx: dict,
    score_thresh: int = 700,
) -> torch.Tensor | None:
    """
    links file format (space-separated, có header):
      protein1  protein2  combined_score
      9606.ENSP00000...  9606.ENSP00000...  999

    alias file format (tab-separated):
      #string_protein_id  alias  source
      9606.ENSP00000...   TP53   BioMart_HUGO

    Bước:
      1. Đọc alias file → map ENSP → gene symbol
      2. Đọc links file → lọc score, map sang gene symbol → lấy edges
    """
    if not os.path.exists(links_file) or not os.path.exists(alias_file):
        return None

    print("   Building ENSP→symbol map từ alias file...", end=" ", flush=True)

    # Đọc alias file — giữ lại các alias từ nguồn gene symbol
    alias_df = pd.read_csv(alias_file, sep="\t", comment="#",
                           names=["protein_id", "alias", "source"])
    # Ưu tiên nguồn BioMart_HUGO hoặc HGNC
    preferred = alias_df[alias_df["source"].str.contains(
        "BioMart_HUGO|HGNC|gene_name", case=False, na=False
    )]
    # Nếu không có nguồn ưu tiên, lấy tất cả
    if len(preferred) == 0:
        preferred = alias_df

    # Tạo map: ENSP_full_id → gene_symbol (lấy alias đầu tiên cho mỗi protein)
    ensp_to_gene = (
        preferred.groupby("protein_id")["alias"]
        .first()
        .to_dict()
    )
    print(f"{len(ensp_to_gene):,} proteins mapped")

    # Đọc links file theo chunk
    print("   Parsing STRING links...", end=" ", flush=True)
    src_list, dst_list = [], []
    seen = set()  # tránh duplicate

    for chunk in pd.read_csv(
        links_file, sep=" ", chunksize=500_000,
        dtype={"protein1": str, "protein2": str, "combined_score": int},
    ):
        chunk = chunk[chunk["combined_score"] >= score_thresh]
        for row in chunk.itertuples(index=False):
            p1 = row.protein1  # "9606.ENSP00000..."
            p2 = row.protein2

            g1 = ensp_to_gene.get(p1, "")
            g2 = ensp_to_gene.get(p2, "")

            if g1 not in gene_idx or g2 not in gene_idx:
                continue
            i1, i2 = gene_idx[g1], gene_idx[g2]

            # Undirected → thêm cả 2 chiều, tránh duplicate
            key = (min(i1, i2), max(i1, i2))
            if key in seen:
                continue
            seen.add(key)
            src_list += [i1, i2]
            dst_list += [i2, i1]

    print(f"{len(src_list)//2:,} unique edges")

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────
#  Parse miRTarBase  (hsa_MTI.csv)
# ─────────────────────────────────────────────
def _load_mirna_edges(
    mti_file: str,
    mirna_idx: dict,
    gene_idx: dict,
) -> torch.Tensor | None:
    """
    hsa_MTI.csv format (miRTarBase):
      miRNA  Target Gene  Species(miRNA)  Species(Target Gene)  Experiments  ...
    Cột quan trọng: 'miRNA' và 'Target Gene'
    """
    if not os.path.exists(mti_file):
        return None

    print("   Parsing hsa_MTI.csv...", end=" ", flush=True)

    df = pd.read_csv(mti_file)

    # Tự động detect tên cột
    mirna_col = _find_col(df.columns.tolist(), ["miRNA", "mirna", "mature_mirna"])
    gene_col  = _find_col(df.columns.tolist(), ["Target Gene", "target_gene",
                                                  "gene_symbol", "Gene Symbol"])
    if not mirna_col or not gene_col:
        print(f"không nhận ra cột (found: {df.columns.tolist()[:5]})")
        return None

    src_list, dst_list = [], []
    seen = set()

    for row in df[[mirna_col, gene_col]].itertuples(index=False):
        m = str(getattr(row, mirna_col)).strip()
        g = str(getattr(row, gene_col)).strip()
        if m not in mirna_idx or g not in gene_idx:
            continue
        key = (mirna_idx[m], gene_idx[g])
        if key in seen:
            continue
        seen.add(key)
        src_list.append(mirna_idx[m])
        dst_list.append(gene_idx[g])

    print(f"{len(src_list):,} edges")

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────
def _find_col(columns: list, candidates: list) -> str | None:
    """Tìm tên cột khớp với danh sách candidates (case-insensitive)."""
    col_lower = [c.lower() for c in columns]
    for cand in candidates:
        for i, c in enumerate(col_lower):
            if cand.lower() == c or cand.lower() in c:
                return columns[i]
    return None


def _self_loop_edges(n_src: int, n_dst: int, n: int = 500) -> torch.Tensor:
    """Fallback: random edges khi không có file."""
    rng = np.random.default_rng(0)
    src = rng.integers(0, n_src, n)
    dst = rng.integers(0, n_dst, n)
    return torch.tensor([src.tolist(), dst.tolist()], dtype=torch.long)
