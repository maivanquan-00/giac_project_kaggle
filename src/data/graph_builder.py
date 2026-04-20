# """
# graph_builder.py
# ----------------
# Xây dựng Heterogeneous Graph từ các file thực tế.

# File sử dụng:
#     GIAC_main/TCGA_emQTL_{COAD,ESCA,READ,STAD}.txt  → cạnh CpG → Gene
#     hsa_MTI.csv                                      → cạnh miRNA → Gene
#     9606.protein.links.v12.0.txt                     → cạnh Gene ↔ Gene (PPI)
#     9606.protein.aliases.v12.0.txt                   → map ENSP → gene symbol

# Nguyên tắc matching tên:
#     - Tất cả gene symbol được normalize về UPPERCASE trước khi lookup
#     - gene_idx, cpg_idx, mirna_idx đều dùng key đã normalize
#     - Đảm bảo match nhất quán dù CSV dùng mixed case
# """

# import re
# import os
# import numpy as np
# import pandas as pd
# import torch
# from torch_geometric.data import HeteroData


# def build_hetero_graph(
#     feature_names: dict,
#     cfg_data: dict,
#     cfg_graph: dict,
#     device: str = "cpu",
# ) -> HeteroData:

#     graph_dir = cfg_data["graph_dir"]
#     giac_dir  = os.path.join(graph_dir, "GIAC_main")

#     gene_names  = feature_names["gene"]
#     cpg_names   = feature_names["meth"]
#     mirna_names = feature_names["mirna"]

#     # ── Normalize keys: gene → UPPER, cpg → giữ nguyên (cg12345 format), mirna → lower ──
#     gene_idx  = {g.upper(): i for i, g in enumerate(gene_names)}
#     cpg_idx   = {c: i for i, c in enumerate(cpg_names)}          # cg... không đổi
#     mirna_idx = {m.lower(): i for i, m in enumerate(mirna_names)} # hsa-... lowercase

#     print(f"\n🔨 Xây dựng Heterogeneous Graph...")
#     print(f"   Gene  nodes : {len(gene_names)}")
#     print(f"   CpG   nodes : {len(cpg_names)}")
#     print(f"   miRNA nodes : {len(mirna_names)}")

#     graph = HeteroData()
#     graph["gene"].num_nodes  = len(gene_names)
#     graph["cpg"].num_nodes   = len(cpg_names)
#     graph["mirna"].num_nodes = len(mirna_names)

#     # ── Cạnh 1: CpG → Gene  (emQTL) ──────────────────────────────────
#     cpg_gene_edges = _load_emqtl_edges(
#         giac_dir     = giac_dir,
#         cancer_types = cfg_data["cancer_types"],
#         cpg_idx      = cpg_idx,
#         gene_idx     = gene_idx,   # UPPER keys
#         pval_thresh  = cfg_graph["emqtl_pval_threshold"],
#         max_edges    = cfg_graph["max_edges_per_node"],
#     )
#     if cpg_gene_edges is not None:
#         graph["cpg", "regulates", "gene"].edge_index    = cpg_gene_edges
#         graph["gene", "regulated_by", "cpg"].edge_index = cpg_gene_edges.flip(0)
#         print(f"   CpG→Gene edges  : {cpg_gene_edges.shape[1]:,}")
#     else:
#         print("   ⚠️  emQTL: không có cạnh → dùng self-loop fallback")
#         dummy = _self_loop_edges(len(cpg_names), len(gene_names))
#         graph["cpg", "regulates", "gene"].edge_index    = dummy
#         graph["gene", "regulated_by", "cpg"].edge_index = dummy.flip(0)

#     # ── Cạnh 2: Gene ↔ Gene  (STRING PPI) ────────────────────────────
#     if cfg_graph.get("use_ppi", True):
#         alias_file = os.path.join(graph_dir, "9606.protein.aliases.v12.0.txt")
#         links_file = os.path.join(graph_dir, "9606.protein.links.v12.0.txt")
#         ppi_edges  = _load_ppi_edges(
#             links_file   = links_file,
#             alias_file   = alias_file,
#             gene_idx     = gene_idx,   # UPPER keys
#             score_thresh = cfg_graph.get("ppi_score_threshold", 700),
#         )
#         if ppi_edges is not None:
#             graph["gene", "interacts", "gene"].edge_index = ppi_edges
#             print(f"   Gene↔Gene edges : {ppi_edges.shape[1]:,}")
#         else:
#             print("   ⚠️  STRING PPI: không đọc được file")

#     # ── Cạnh 3: miRNA → Gene  (hsa_MTI.csv) ──────────────────────────
#     if cfg_graph.get("use_mirna", True):
#         mti_file    = os.path.join(graph_dir, "hsa_MTI.csv")
#         mirna_edges = _load_mirna_edges(
#             mti_file  = mti_file,
#             mirna_idx = mirna_idx,   # lowercase keys
#             gene_idx  = gene_idx,    # UPPER keys
#         )
#         if mirna_edges is not None:
#             graph["mirna", "targets", "gene"].edge_index    = mirna_edges
#             graph["gene", "targeted_by", "mirna"].edge_index = mirna_edges.flip(0)
#             print(f"   miRNA→Gene edges: {mirna_edges.shape[1]:,}")
#         else:
#             print("   ⚠️  miRTarBase: không đọc được file")

#     # Self-loops
#     graph["gene",  "self_loop", "gene"].edge_index  = _identity_edges(len(gene_names))
#     graph["cpg",   "self_loop", "cpg"].edge_index   = _identity_edges(len(cpg_names))
#     graph["mirna", "self_loop", "mirna"].edge_index = _identity_edges(len(mirna_names))

#     return graph.to(device)


# # ─────────────────────────────────────────────
# #  emQTL
# # ─────────────────────────────────────────────
# def _load_emqtl_edges(
#     giac_dir: str,
#     cancer_types: list,
#     cpg_idx: dict,
#     gene_idx: dict,   # UPPER keys
#     pval_thresh: float,
#     max_edges: int,
# ) -> torch.Tensor | None:

#     src_list, dst_list = [], []
#     cpg_edge_count = {}

#     for ct in cancer_types:
#         fpath = os.path.join(giac_dir, f"TCGA_emQTL_{ct}.txt")
#         if not os.path.exists(fpath):
#             print(f"   ⚠️  Không tìm thấy: TCGA_emQTL_{ct}.txt")
#             continue

#         header_df = pd.read_csv(fpath, sep="\t", nrows=2)
#         cols = header_df.columns.tolist()

#         cpg_col  = _find_col(cols, ["CpG", "cpg", "probe", "Probe"])
#         gene_col = _find_col(cols, ["Gene", "gene", "symbol", "Symbol"])
#         pval_col = _find_col(cols, ["p-value", "pvalue", "p_value", "P.Value", "pval"])

#         if not all([cpg_col, gene_col, pval_col]):
#             print(f"   ⚠️  {ct}: không nhận ra cột (found: {cols[:5]})")
#             continue

#         print(f"   Parsing emQTL {ct}... ", end="", flush=True)
#         count_before = len(src_list)

#         for chunk in pd.read_csv(
#             fpath, sep="\t", chunksize=200_000,
#             usecols=[cpg_col, gene_col, pval_col],
#             dtype={cpg_col: str, gene_col: str, pval_col: float},
#         ):
#             chunk = chunk[chunk[pval_col] < pval_thresh]
#             for row in chunk.itertuples(index=False, name=None):
#                 c_name = str(row[0]).strip()          # CpG: giữ nguyên
#                 g_name = str(row[1]).strip().upper()  # Gene: normalize UPPER

#                 if c_name not in cpg_idx or g_name not in gene_idx:
#                     continue
#                 c_i = cpg_idx[c_name]
#                 if cpg_edge_count.get(c_i, 0) >= max_edges:
#                     continue
#                 src_list.append(c_i)
#                 dst_list.append(gene_idx[g_name])
#                 cpg_edge_count[c_i] = cpg_edge_count.get(c_i, 0) + 1

#         print(f"{len(src_list) - count_before:,} edges")

#     if not src_list:
#         return None
#     return torch.tensor([src_list, dst_list], dtype=torch.long)


# # ─────────────────────────────────────────────
# #  STRING PPI
# # ─────────────────────────────────────────────
# def _load_ppi_edges(
#     links_file: str,
#     alias_file: str,
#     gene_idx: dict,   # UPPER keys
#     score_thresh: int = 700,
# ) -> torch.Tensor | None:

#     if not os.path.exists(links_file) or not os.path.exists(alias_file):
#         return None

#     print("   Building ENSP→symbol map từ alias file...", end=" ", flush=True)

#     alias_df = pd.read_csv(alias_file, sep="\t", comment="#",
#                            names=["protein_id", "alias", "source"])

#     # Normalize alias về UPPER để match gene_idx (đã là UPPER keys)
#     alias_df["alias_upper"] = alias_df["alias"].astype(str).str.strip().str.upper()

#     # Chỉ giữ alias khớp với gene_idx (đã UPPER)
#     valid_genes = set(gene_idx.keys())  # UPPER set
#     preferred   = alias_df[alias_df["alias_upper"].isin(valid_genes)]

#     ensp_to_gene = (
#         preferred.groupby("protein_id")["alias_upper"]
#         .first()
#         .to_dict()
#     )  # ENSP → UPPER gene symbol
#     print(f"{len(ensp_to_gene):,} proteins mapped")

#     print("   Parsing STRING links...", end=" ", flush=True)
#     src_list, dst_list = [], []
#     seen = set()

#     for chunk in pd.read_csv(
#         links_file, sep=" ", chunksize=500_000,
#         dtype={"protein1": str, "protein2": str, "combined_score": int},
#     ):
#         chunk = chunk[chunk["combined_score"] >= score_thresh]
#         for row in chunk.itertuples(index=False, name=None):
#             p1, p2 = row[0], row[1]
#             g1 = ensp_to_gene.get(p1, "")
#             g2 = ensp_to_gene.get(p2, "")

#             if not g1 or not g2:
#                 continue
#             if g1 not in gene_idx or g2 not in gene_idx:
#                 continue

#             i1, i2 = gene_idx[g1], gene_idx[g2]
#             key = (min(i1, i2), max(i1, i2))
#             if key in seen:
#                 continue
#             seen.add(key)
#             src_list += [i1, i2]
#             dst_list += [i2, i1]

#     print(f"{len(src_list)//2:,} unique edges")

#     if not src_list:
#         return None
#     return torch.tensor([src_list, dst_list], dtype=torch.long)


# # ─────────────────────────────────────────────
# #  miRTarBase
# # ─────────────────────────────────────────────
# def _load_mirna_edges(
#     mti_file: str,
#     mirna_idx: dict,  # lowercase keys
#     gene_idx: dict,   # UPPER keys
# ) -> torch.Tensor | None:

#     if not os.path.exists(mti_file):
#         return None

#     print("   Parsing hsa_MTI.csv...", end=" ", flush=True)
#     df = pd.read_csv(mti_file)

#     mirna_col = _find_col(df.columns.tolist(), ["miRNA", "mirna", "mature_mirna"])
#     gene_col  = _find_col(df.columns.tolist(), ["Target Gene", "target_gene",
#                                                   "gene_symbol", "Gene Symbol"])
#     if not mirna_col or not gene_col:
#         print(f"không nhận ra cột (found: {df.columns.tolist()[:5]})")
#         return None

#     # Map: base miRNA name (lowercase, bỏ -5p/-3p) → list indices trong mirna_idx
#     # Vì mirna_idx keys là "hsa-let-7a-1" (lowercase, có số precursor)
#     # MTI file dùng "hsa-let-7a-5p" (mature, có -5p/-3p)
#     base_to_indices = {}
#     for tcga_name, idx in mirna_idx.items():
#         base = re.sub(r'-\d+$', '', tcga_name.lower().strip())  # bỏ -1, -2 cuối
#         base_to_indices.setdefault(base, []).append(idx)

#     src_list, dst_list = [], []
#     seen = set()

#     for row in df[[mirna_col, gene_col]].itertuples(index=False, name=None):
#         m_raw = str(row[0]).strip().lower()
#         g_raw = str(row[1]).strip().upper()  # gene → UPPER

#         # Normalize mature miRNA: bỏ -5p/-3p
#         m_base = re.sub(r'-[35]p$', '', m_raw)

#         if g_raw not in gene_idx or m_base not in base_to_indices:
#             continue

#         g_i = gene_idx[g_raw]
#         for m_i in base_to_indices[m_base]:
#             key = (m_i, g_i)
#             if key in seen:
#                 continue
#             seen.add(key)
#             src_list.append(m_i)
#             dst_list.append(g_i)

#     print(f"{len(src_list):,} edges")

#     if not src_list:
#         return None
#     return torch.tensor([src_list, dst_list], dtype=torch.long)


# # ─────────────────────────────────────────────
# #  Helpers
# # ─────────────────────────────────────────────
# def _find_col(columns: list, candidates: list) -> str | None:
#     col_lower = [c.lower() for c in columns]
#     for cand in candidates:
#         for i, c in enumerate(col_lower):
#             if cand.lower() == c or cand.lower() in c:
#                 return columns[i]
#     return None


# def _self_loop_edges(n_src: int, n_dst: int, n: int = 500) -> torch.Tensor:
#     rng = np.random.default_rng(0)
#     src = rng.integers(0, n_src, n)
#     dst = rng.integers(0, n_dst, n)
#     return torch.tensor([src.tolist(), dst.tolist()], dtype=torch.long)


# def _identity_edges(n_nodes: int) -> torch.Tensor:
#     idx = torch.arange(n_nodes, dtype=torch.long)
#     return torch.stack([idx, idx], dim=0)

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


def build_hetero_graph(
    feature_names: dict,
    cfg_data: dict,
    cfg_graph: dict,
    device: str = "cpu",
) -> HeteroData:

    graph_dir = cfg_data["graph_dir"]
    giac_dir  = os.path.join(graph_dir, "GIAC_main")

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

    # ── Cạnh 1: CpG → Gene  (emQTL) ──────────────────────────────────
    cpg_gene_edges = _load_emqtl_edges(
        giac_dir     = giac_dir,
        cancer_types = cfg_data["cancer_types"],
        cpg_idx      = cpg_idx,
        gene_idx     = gene_idx,   # UPPER keys
        pval_thresh  = cfg_graph["emqtl_pval_threshold"],
        max_edges    = cfg_graph["max_edges_per_node"],
    )
    if cpg_gene_edges is not None:
        graph["cpg", "regulates", "gene"].edge_index    = cpg_gene_edges
        graph["gene", "regulated_by", "cpg"].edge_index = cpg_gene_edges.flip(0)
        print(f"   CpG→Gene edges  : {cpg_gene_edges.shape[1]:,}")
    else:
        print("   ⚠️  emQTL: không có cạnh → dùng self-loop fallback")
        dummy = _self_loop_edges(len(cpg_names), len(gene_names))
        graph["cpg", "regulates", "gene"].edge_index    = dummy
        graph["gene", "regulated_by", "cpg"].edge_index = dummy.flip(0)

    # ── Cạnh 2: Gene ↔ Gene  (STRING PPI) ────────────────────────────
    if cfg_graph.get("use_ppi", True):
        alias_file = os.path.join(graph_dir, "9606.protein.aliases.v12.0.txt")
        links_file = os.path.join(graph_dir, "9606.protein.links.v12.0.txt")
        ppi_edges  = _load_ppi_edges(
            links_file   = links_file,
            alias_file   = alias_file,
            gene_idx     = gene_idx,   # UPPER keys
            score_thresh = cfg_graph.get("ppi_score_threshold", 700),
        )
        if ppi_edges is not None:
            graph["gene", "interacts", "gene"].edge_index = ppi_edges
            print(f"   Gene↔Gene edges : {ppi_edges.shape[1]:,}")
        else:
            print("   ⚠️  STRING PPI: không đọc được file")

    # ── Cạnh 3: miRNA → Gene  (hsa_MTI.csv) ──────────────────────────
    if cfg_graph.get("use_mirna", True):
        mti_file    = os.path.join(graph_dir, "hsa_MTI.csv")
        mirna_edges = _load_mirna_edges(
            mti_file  = mti_file,
            mirna_idx = mirna_idx,   # lowercase keys
            gene_idx  = gene_idx,    # UPPER keys
        )
        if mirna_edges is not None:
            graph["mirna", "targets", "gene"].edge_index    = mirna_edges
            graph["gene", "targeted_by", "mirna"].edge_index = mirna_edges.flip(0)
            print(f"   miRNA→Gene edges: {mirna_edges.shape[1]:,}")
        else:
            print("   ⚠️  miRTarBase: không đọc được file")


    # ── Cạnh 4: CpG ↔ miRNA (co-regulation qua gene trung gian) ───────
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
            graph["mirna", "coregulates", "cpg"].edge_index   = mirna_cpg_edges
            print(f"   CpG↔miRNA edges : {cpg_mirna_edges.shape[1]:,}")

    # Self-loops
    graph["gene",  "self_loop", "gene"].edge_index  = _identity_edges(len(gene_names))
    graph["cpg",   "self_loop", "cpg"].edge_index   = _identity_edges(len(cpg_names))
    graph["mirna", "self_loop", "mirna"].edge_index = _identity_edges(len(mirna_names))

    return graph.to(device)


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
) -> torch.Tensor | None:

    src_list, dst_list = [], []
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
                c_name = str(row[0]).strip()          # CpG: giữ nguyên
                g_name = str(row[1]).strip().upper()  # Gene: normalize UPPER

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
#  STRING PPI
# ─────────────────────────────────────────────
def _load_ppi_edges(
    links_file: str,
    alias_file: str,
    gene_idx: dict,   # UPPER keys
    score_thresh: int = 700,
) -> torch.Tensor | None:

    if not os.path.exists(links_file) or not os.path.exists(alias_file):
        return None

    print("   Building ENSP→symbol map từ alias file...", end=" ", flush=True)

    alias_df = pd.read_csv(alias_file, sep="\t", comment="#",
                           names=["protein_id", "alias", "source"])

    # Normalize alias về UPPER để match gene_idx (đã là UPPER keys)
    alias_df["alias_upper"] = alias_df["alias"].astype(str).str.strip().str.upper()

    # Chỉ giữ alias khớp với gene_idx (đã UPPER)
    valid_genes = set(gene_idx.keys())  # UPPER set
    preferred   = alias_df[alias_df["alias_upper"].isin(valid_genes)]

    ensp_to_gene = (
        preferred.groupby("protein_id")["alias_upper"]
        .first()
        .to_dict()
    )  # ENSP → UPPER gene symbol
    print(f"{len(ensp_to_gene):,} proteins mapped")

    print("   Parsing STRING links...", end=" ", flush=True)
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

    print(f"{len(src_list)//2:,} unique edges")

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────
#  miRTarBase
# ─────────────────────────────────────────────
def _load_mirna_edges(
    mti_file: str,
    mirna_idx: dict,  # lowercase keys
    gene_idx: dict,   # UPPER keys
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
        base = re.sub(r'-\d+$', '', tcga_name.lower().strip())  # bỏ -1, -2 cuối
        base_to_indices.setdefault(base, []).append(idx)

    src_list, dst_list = [], []
    seen = set()

    for row in df[[mirna_col, gene_col]].itertuples(index=False, name=None):
        m_raw = str(row[0]).strip().lower()
        g_raw = str(row[1]).strip().upper()  # gene → UPPER

        # Normalize mature miRNA: bỏ -5p/-3p
        m_base = re.sub(r'-[35]p$', '', m_raw)

        if g_raw not in gene_idx or m_base not in base_to_indices:
            continue

        g_i = gene_idx[g_raw]
        for m_i in base_to_indices[m_base]:
            key = (m_i, g_i)
            if key in seen:
                continue
            seen.add(key)
            src_list.append(m_i)
            dst_list.append(g_i)

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


def _self_loop_edges(n_src: int, n_dst: int, n: int = 500) -> torch.Tensor:
    rng = np.random.default_rng(0)
    src = rng.integers(0, n_src, n)
    dst = rng.integers(0, n_dst, n)
    return torch.tensor([src.tolist(), dst.tolist()], dtype=torch.long)


def _identity_edges(n_nodes: int) -> torch.Tensor:
    idx = torch.arange(n_nodes, dtype=torch.long)
    return torch.stack([idx, idx], dim=0)