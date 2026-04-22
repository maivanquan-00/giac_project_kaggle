"""
graph_builder.py
----------------
Build the Heterogeneous Graph for the GIAC multi-omics pipeline.

Node types  : gene | cpg | mirna
Edge types  (7 total):

  Inter-omic (biology-driven):
    cpg   --[regulates]-->    gene   (emQTL: methylation controls expression)
    mirna --[targets]-->      gene   (miRTarBase: miRNA suppresses gene)
    cpg   --[coregulates]-->  mirna  (derived: both regulate same gene)
    mirna --[coregulates]-->  cpg    (reverse of above)

  Intra-omic (knowledge graph):
    gene  --[ppi]-->          gene   (STRING PPI: protein-protein interaction)
    gene  --[copathway]-->    gene   (Reactome: two genes in same pathway)
    mirna --[samefamily]-->   mirna  (miR_Family_Info: shared seed sequence)

Files used:
    GIAC_main/TCGA_emQTL_{COAD,ESCA,READ,STAD}.txt
    GIAC_main/TCGA_hallmark_pathway_meQTL_{COAD,...}.txt  (priority filter)
    hsa_MTI.csv                       (miRTarBase)
    9606.protein.links.v12.0.txt      (STRING PPI)
    9606.protein.aliases.v12.0.txt    (ENSP -> gene symbol)
    Ensembl2Reactome_All_Levels.txt   (Reactome pathway membership)
    hgnc_complete_set.txt             (Ensembl -> HGNC symbol)
    miR_Family_Info.txt               (miRNA seed family)
"""

import re
import os
import numpy as np
import pandas as pd
import torch
from torch_geometric.data import HeteroData


# ─────────────────────────────────────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────────────────────────────────────

def build_hetero_graph(
    feature_names: dict,
    cfg_data: dict,
    cfg_graph: dict,
    device: str = "cpu",
) -> HeteroData:
    """
    Build the heterogeneous graph. Called once per fold from train.py.

    Parameters
    ----------
    feature_names : {"gene": [...], "meth": [...], "mirna": [...]}
        Feature names AFTER ANOVA selection for this fold.
    cfg_data  : data section of config.yaml
    cfg_graph : graph section of config.yaml
    device    : "cpu" or "cuda"

    Returns
    -------
    HeteroData with node counts and edge_index tensors.
    """
    graph_dir = cfg_data["graph_dir"]
    giac_dir  = os.path.join(graph_dir, "GIAC_main")

    gene_names  = feature_names["gene"]
    cpg_names   = feature_names["meth"]
    mirna_names = feature_names["mirna"]

    # Normalised lookup dicts
    gene_idx  = {g.upper(): i for i, g in enumerate(gene_names)}
    cpg_idx   = {c: i for i, c in enumerate(cpg_names)}
    mirna_idx = {m.lower(): i for i, m in enumerate(mirna_names)}

    print("\n🔨 Building Heterogeneous Graph...")
    print(f"   Gene  nodes : {len(gene_names)}")
    print(f"   CpG   nodes : {len(cpg_names)}")
    print(f"   miRNA nodes : {len(mirna_names)}")

    graph = HeteroData()
    graph["gene"].num_nodes  = len(gene_names)
    graph["cpg"].num_nodes   = len(cpg_names)
    graph["mirna"].num_nodes = len(mirna_names)

    max_e   = cfg_graph.get("max_edges_per_node", 20)
    max_cor = cfg_graph.get("max_coregulation_edges", 10)

    # ── 1. CpG → Gene  (emQTL, optionally boosted by hallmark meQTL) ─────────
    hallmark_cpgs = _load_hallmark_cpgs(giac_dir, cfg_data.get("cancer_types", []))
    cpg_gene_edges = _load_emqtl_edges(
        giac_dir     = giac_dir,
        cancer_types = cfg_data.get("cancer_types", []),
        cpg_idx      = cpg_idx,
        gene_idx     = gene_idx,
        pval_thresh  = cfg_graph.get("emqtl_pval_threshold", 0.05),
        max_edges    = max_e,
        hallmark_cpgs = hallmark_cpgs,
    )
    if cpg_gene_edges is not None:
        graph["cpg", "regulates", "gene"].edge_index    = cpg_gene_edges
        graph["gene", "regulated_by", "cpg"].edge_index = cpg_gene_edges.flip(0)
        print(f"   CpG->Gene edges   : {cpg_gene_edges.shape[1]:,}")
    else:
        print("   ⚠️  emQTL: no edges found — using self-loop fallback")
        dummy = _self_loop_fallback(len(cpg_names), len(gene_names))
        graph["cpg", "regulates", "gene"].edge_index    = dummy
        graph["gene", "regulated_by", "cpg"].edge_index = dummy.flip(0)

    # ── 2. Gene ↔ Gene  (STRING PPI) ─────────────────────────────────────────
    if cfg_graph.get("use_ppi", True):
        ppi_edges = _load_ppi_edges(
            links_file   = os.path.join(graph_dir, "9606.protein.links.v12.0.txt"),
            alias_file   = os.path.join(graph_dir, "9606.protein.aliases.v12.0.txt"),
            gene_idx     = gene_idx,
            score_thresh = cfg_graph.get("ppi_score_threshold", 700),
        )
        if ppi_edges is not None:
            graph["gene", "ppi", "gene"].edge_index = ppi_edges
            print(f"   Gene-PPI edges     : {ppi_edges.shape[1] // 2:,} unique")

    # ── 3. Gene ↔ Gene  (Reactome co-pathway) ────────────────────────────────
    if cfg_graph.get("use_reactome", True):
        reactome_edges = _load_reactome_edges(
            reactome_file = os.path.join(graph_dir, "Ensembl2Reactome_All_Levels.txt"),
            hgnc_file     = os.path.join(graph_dir, "hgnc_complete_set.txt"),
            gene_idx      = gene_idx,
            max_pathway_size = cfg_graph.get("reactome_max_pathway_size", 50),
            max_edges        = cfg_graph.get("max_edges_per_node", 20),
        )
        if reactome_edges is not None:
            graph["gene", "copathway", "gene"].edge_index = reactome_edges
            print(f"   Gene-Pathway edges : {reactome_edges.shape[1] // 2:,} unique")

    # ── 4. miRNA → Gene  (miRTarBase) ─────────────────────────────────────────
    if cfg_graph.get("use_mirna", True):
        mirna_gene_edges = _load_mirna_edges(
            mti_file  = os.path.join(graph_dir, "hsa_MTI.csv"),
            mirna_idx = mirna_idx,
            gene_idx  = gene_idx,
        )
        if mirna_gene_edges is not None:
            graph["mirna", "targets", "gene"].edge_index    = mirna_gene_edges
            graph["gene", "targeted_by", "mirna"].edge_index = mirna_gene_edges.flip(0)
            print(f"   miRNA->Gene edges  : {mirna_gene_edges.shape[1]:,}")

    # ── 5. miRNA ↔ miRNA  (same seed family) ─────────────────────────────────
    if cfg_graph.get("use_mirna_family", True):
        family_edges = _load_mirna_family_edges(
            family_file = os.path.join(graph_dir, "miR_Family_Info.txt"),
            mirna_idx   = mirna_idx,
        )
        if family_edges is not None:
            graph["mirna", "samefamily", "mirna"].edge_index = family_edges
            print(f"   miRNA-Family edges : {family_edges.shape[1] // 2:,} unique")

    # ── 6. CpG ↔ miRNA  (co-regulation via shared target gene) ──────────────
    if cpg_gene_edges is not None and mirna_gene_edges is not None:
        c2m, m2c = _build_coregulation_edges(
            cpg_gene_edges   = cpg_gene_edges,
            mirna_gene_edges = mirna_gene_edges,
            n_cpg   = len(cpg_names),
            n_mirna = len(mirna_names),
            max_edges_per_node = max_cor,
        )
        if c2m is not None:
            graph["cpg",   "coregulates", "mirna"].edge_index = c2m
            graph["mirna", "coregulates", "cpg"].edge_index   = m2c
            print(f"   CpG<->miRNA edges  : {c2m.shape[1]:,}")

    # ── 7. Self-loops (one per node type) ────────────────────────────────────
    graph["gene",  "self_loop", "gene"].edge_index  = _identity_edges(len(gene_names))
    graph["cpg",   "self_loop", "cpg"].edge_index   = _identity_edges(len(cpg_names))
    graph["mirna", "self_loop", "mirna"].edge_index = _identity_edges(len(mirna_names))

    return graph.to(device)


# ─────────────────────────────────────────────────────────────────────────────
#  1. emQTL  (CpG -> Gene)
# ─────────────────────────────────────────────────────────────────────────────

def _load_hallmark_cpgs(giac_dir: str, cancer_types: list) -> set:
    """
    Load CpG IDs from hallmark pathway meQTL files.
    These CpGs are biologically prioritised — used to boost edge priority
    in emQTL loading (hallmark CpGs are always kept before non-hallmark ones).
    """
    hallmark = set()
    for ct in cancer_types:
        fpath = os.path.join(giac_dir, f"TCGA_hallmark_pathway_meQTL_{ct}.txt")
        if not os.path.exists(fpath):
            continue
        try:
            df = pd.read_csv(fpath, sep="\t", nrows=5)
            cpg_col = _find_col(df.columns.tolist(),
                                ["CpG", "cpg", "probe", "Probe", "SNP", "methylation"])
            if cpg_col is None:
                continue
            for chunk in pd.read_csv(fpath, sep="\t", chunksize=100_000,
                                     usecols=[cpg_col], dtype=str):
                hallmark.update(chunk[cpg_col].str.strip().dropna().tolist())
        except Exception:
            pass
    if hallmark:
        print(f"   Hallmark meQTL CpGs loaded: {len(hallmark):,}")
    return hallmark


def _load_emqtl_edges(
    giac_dir: str,
    cancer_types: list,
    cpg_idx: dict,
    gene_idx: dict,
    pval_thresh: float,
    max_edges: int,
    hallmark_cpgs: set,
) -> torch.Tensor | None:
    """
    Load CpG->Gene edges from emQTL files.
    Hallmark CpGs get priority slots; remaining slots filled by p-value order.
    """
    src_list, dst_list = [], []
    cpg_edge_count = {}

    for ct in cancer_types:
        fpath = os.path.join(giac_dir, f"TCGA_emQTL_{ct}.txt")
        if not os.path.exists(fpath):
            print(f"   ⚠️  Missing: TCGA_emQTL_{ct}.txt")
            continue

        header_df = pd.read_csv(fpath, sep="\t", nrows=2)
        cols = header_df.columns.tolist()
        cpg_col  = _find_col(cols, ["CpG", "cpg", "probe", "Probe"])
        gene_col = _find_col(cols, ["Gene", "gene", "symbol", "Symbol"])
        pval_col = _find_col(cols, ["p-value", "pvalue", "p_value", "P.Value", "pval"])

        if not all([cpg_col, gene_col, pval_col]):
            print(f"   ⚠️  {ct}: unrecognised columns {cols[:5]}")
            continue

        print(f"   Parsing emQTL {ct}...", end=" ", flush=True)
        count_before = len(src_list)

        rows_hallmark = []
        rows_normal   = []

        for chunk in pd.read_csv(
            fpath, sep="\t", chunksize=200_000,
            usecols=[cpg_col, gene_col, pval_col],
            dtype={cpg_col: str, gene_col: str, pval_col: float},
        ):
            chunk = chunk[chunk[pval_col] < pval_thresh]
            for row in chunk.itertuples(index=False, name=None):
                c = str(row[0]).strip()
                g = str(row[1]).strip().upper()
                p = row[2]
                if c not in cpg_idx or g not in gene_idx:
                    continue
                if c in hallmark_cpgs:
                    rows_hallmark.append((c, g, p))
                else:
                    rows_normal.append((c, g, p))

        # Process hallmark rows first (priority), then normal
        for rows in [rows_hallmark, rows_normal]:
            rows.sort(key=lambda x: x[2])   # sort by p-value ascending
            for c, g, _ in rows:
                c_i = cpg_idx[c]
                if cpg_edge_count.get(c_i, 0) >= max_edges:
                    continue
                src_list.append(c_i)
                dst_list.append(gene_idx[g])
                cpg_edge_count[c_i] = cpg_edge_count.get(c_i, 0) + 1

        print(f"{len(src_list) - count_before:,} edges")

    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────────────────────────────────────
#  2. STRING PPI  (Gene <-> Gene)
# ─────────────────────────────────────────────────────────────────────────────

def _load_ppi_edges(
    links_file: str,
    alias_file: str,
    gene_idx: dict,
    score_thresh: int = 700,
) -> torch.Tensor | None:
    if not os.path.exists(links_file) or not os.path.exists(alias_file):
        return None

    print("   Building ENSP->symbol map (aliases)...", end=" ", flush=True)
    alias_df = pd.read_csv(alias_file, sep="\t", comment="#",
                           names=["protein_id", "alias", "source"])
    alias_df["alias_upper"] = alias_df["alias"].astype(str).str.strip().str.upper()
    valid = set(gene_idx.keys())
    ensp_to_gene = (
        alias_df[alias_df["alias_upper"].isin(valid)]
        .groupby("protein_id")["alias_upper"]
        .first()
        .to_dict()
    )
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
            g1 = ensp_to_gene.get(row[0], "")
            g2 = ensp_to_gene.get(row[1], "")
            if not g1 or not g2 or g1 not in gene_idx or g2 not in gene_idx:
                continue
            i1, i2 = gene_idx[g1], gene_idx[g2]
            key = (min(i1, i2), max(i1, i2))
            if key in seen:
                continue
            seen.add(key)
            src_list += [i1, i2]
            dst_list += [i2, i1]

    print(f"{len(src_list) // 2:,} unique edges")
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────────────────────────────────────
#  3. Reactome co-pathway  (Gene <-> Gene)
# ─────────────────────────────────────────────────────────────────────────────

def _load_reactome_edges(
    reactome_file: str,
    hgnc_file: str,
    gene_idx: dict,
    max_pathway_size: int = 50,
    max_edges: int = 20,
) -> torch.Tensor | None:
    """
    Two genes sharing a Reactome pathway -> co-pathway edge.

    reactome_file : Ensembl2Reactome_All_Levels.txt
        Columns: EnsemblID | PathwayID | URL | PathwayName | Evidence | Species
    hgnc_file     : hgnc_complete_set.txt
        Contains ensembl_gene_id and symbol columns for Ensembl -> symbol map.
    """
    if not os.path.exists(reactome_file):
        print("   ⚠️  Ensembl2Reactome_All_Levels.txt not found — skipping co-pathway edges")
        return None

    # ── Build Ensembl -> gene symbol map ────────────────────────────────────
    ensembl_to_sym = {}
    if os.path.exists(hgnc_file):
        print("   Building Ensembl->symbol map (HGNC)...", end=" ", flush=True)
        try:
            hgnc = pd.read_csv(hgnc_file, sep="\t", low_memory=False,
                               usecols=["symbol", "ensembl_gene_id"])
            hgnc = hgnc.dropna(subset=["symbol", "ensembl_gene_id"])
            for _, row in hgnc.iterrows():
                sym = str(row["symbol"]).strip().upper()
                eid = str(row["ensembl_gene_id"]).strip()
                if sym in gene_idx:
                    ensembl_to_sym[eid] = sym
            print(f"{len(ensembl_to_sym):,} Ensembl IDs mapped")
        except Exception as e:
            print(f"HGNC parse error: {e}")

    # ── Parse Reactome file ──────────────────────────────────────────────────
    print("   Parsing Reactome pathways...", end=" ", flush=True)
    pathway_to_genes: dict[str, set] = {}

    try:
        for chunk in pd.read_csv(
            reactome_file, sep="\t", header=None, chunksize=200_000,
            names=["ensembl", "pathway_id", "url", "pathway_name", "evidence", "species"],
            dtype=str,
        ):
            chunk = chunk[chunk["species"].str.strip() == "Homo sapiens"]
            for row in chunk.itertuples(index=False, name=None):
                eid = str(row[0]).strip()
                pid = str(row[1]).strip()
                # Map Ensembl -> symbol
                sym = ensembl_to_sym.get(eid, "")
                if not sym:
                    # Fallback: try using Ensembl ID directly as symbol
                    sym = eid.upper()
                if sym not in gene_idx:
                    continue
                pathway_to_genes.setdefault(pid, set()).add(sym)
    except Exception as e:
        print(f"parse error: {e}")
        return None

    print(f"{len(pathway_to_genes):,} pathways loaded")

    # ── Build edges: pairs of genes in same pathway ──────────────────────────
    print("   Building co-pathway edges...", end=" ", flush=True)
    src_list, dst_list = [], []
    seen = set()
    gene_edge_count: dict[int, int] = {}

    for pid, gene_set in pathway_to_genes.items():
        # Skip pathways that are too large (to avoid dense cliques)
        if len(gene_set) > max_pathway_size:
            continue
        gene_list = [gene_idx[g] for g in gene_set if g in gene_idx]
        if len(gene_list) < 2:
            continue
        for a in range(len(gene_list)):
            for b in range(a + 1, len(gene_list)):
                i1, i2 = gene_list[a], gene_list[b]
                if (gene_edge_count.get(i1, 0) >= max_edges or
                        gene_edge_count.get(i2, 0) >= max_edges):
                    continue
                key = (min(i1, i2), max(i1, i2))
                if key in seen:
                    continue
                seen.add(key)
                src_list += [i1, i2]
                dst_list += [i2, i1]
                gene_edge_count[i1] = gene_edge_count.get(i1, 0) + 1
                gene_edge_count[i2] = gene_edge_count.get(i2, 0) + 1

    print(f"{len(src_list) // 2:,} unique edges")
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────────────────────────────────────
#  4. miRTarBase  (miRNA -> Gene)
# ─────────────────────────────────────────────────────────────────────────────

def _load_mirna_edges(
    mti_file: str,
    mirna_idx: dict,
    gene_idx: dict,
) -> torch.Tensor | None:
    if not os.path.exists(mti_file):
        return None

    print("   Parsing miRTarBase (hsa_MTI)...", end=" ", flush=True)
    df = pd.read_csv(mti_file)
    mirna_col = _find_col(df.columns.tolist(), ["miRNA", "mirna", "mature_mirna"])
    gene_col  = _find_col(df.columns.tolist(),
                          ["Target Gene", "target_gene", "gene_symbol", "Gene Symbol"])
    if not mirna_col or not gene_col:
        print(f"unrecognised columns {df.columns.tolist()[:5]}")
        return None

    # base name map: strip -5p/-3p suffix to match TCGA precursor names
    base_to_indices: dict[str, list] = {}
    for tcga_name, idx in mirna_idx.items():
        base = re.sub(r"-\d+$", "", tcga_name.lower().strip())
        base_to_indices.setdefault(base, []).append(idx)

    src_list, dst_list = [], []
    seen: set = set()

    for row in df[[mirna_col, gene_col]].itertuples(index=False, name=None):
        m_raw = str(row[0]).strip().lower()
        g_raw = str(row[1]).strip().upper()
        m_base = re.sub(r"-[35]p$", "", m_raw)
        if g_raw not in gene_idx or m_base not in base_to_indices:
            continue
        g_i = gene_idx[g_raw]
        for m_i in base_to_indices[m_base]:
            if (m_i, g_i) in seen:
                continue
            seen.add((m_i, g_i))
            src_list.append(m_i)
            dst_list.append(g_i)

    print(f"{len(src_list):,} edges")
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────────────────────────────────────
#  5. miRNA family  (miRNA <-> miRNA, same seed)
# ─────────────────────────────────────────────────────────────────────────────

def _load_mirna_family_edges(
    family_file: str,
    mirna_idx: dict,
) -> torch.Tensor | None:
    """
    miR_Family_Info.txt (TargetScan) format:
        miR Family  Seed+m8  Species  MiRBase ID  ...
    Two miRNAs in the same 'miR Family' -> samefamily edge.
    """
    if not os.path.exists(family_file):
        print("   ⚠️  miR_Family_Info.txt not found — skipping miRNA family edges")
        return None

    print("   Parsing miRNA family info...", end=" ", flush=True)
    try:
        df = pd.read_csv(family_file, sep="\t", dtype=str)
    except Exception:
        try:
            df = pd.read_csv(family_file, sep="\t", dtype=str, encoding="latin-1")
        except Exception as e:
            print(f"parse error: {e}")
            return None

    family_col = _find_col(df.columns.tolist(),
                           ["miR Family", "miR_Family", "family", "Family"])
    mirna_col  = _find_col(df.columns.tolist(),
                           ["MiRBase ID", "miRBase_ID", "miRNA", "mature_miRNA"])
    species_col = _find_col(df.columns.tolist(), ["Species", "species", "Species ID"])

    if not family_col or not mirna_col:
        print(f"unrecognised columns {df.columns.tolist()[:5]}")
        return None

    # Filter human miRNAs only (species 9606 or 'Homo sapiens')
    if species_col:
        df = df[df[species_col].astype(str).str.contains("9606|sapiens", na=False)]

    # Build family -> list of mirna indices
    family_to_indices: dict[str, list] = {}
    for _, row in df[[family_col, mirna_col]].iterrows():
        fam  = str(row[family_col]).strip()
        name = str(row[mirna_col]).strip().lower()
        # Try exact match first, then base match
        if name in mirna_idx:
            family_to_indices.setdefault(fam, []).append(mirna_idx[name])
        else:
            base = re.sub(r"-[35]p$", "", name)
            base2 = re.sub(r"-\d+$", "", base)
            for cand_name, cand_idx in mirna_idx.items():
                if re.sub(r"-\d+$", "", cand_name) == base2:
                    family_to_indices.setdefault(fam, []).append(cand_idx)
                    break

    src_list, dst_list = [], []
    seen: set = set()

    for fam, indices in family_to_indices.items():
        unique = list(set(indices))
        if len(unique) < 2:
            continue
        for a in range(len(unique)):
            for b in range(a + 1, len(unique)):
                i1, i2 = unique[a], unique[b]
                key = (min(i1, i2), max(i1, i2))
                if key in seen:
                    continue
                seen.add(key)
                src_list += [i1, i2]
                dst_list += [i2, i1]

    print(f"{len(src_list) // 2:,} unique edges")
    if not src_list:
        return None
    return torch.tensor([src_list, dst_list], dtype=torch.long)


# ─────────────────────────────────────────────────────────────────────────────
#  6. CpG <-> miRNA  (co-regulation via shared target gene)
# ─────────────────────────────────────────────────────────────────────────────

def _build_coregulation_edges(
    cpg_gene_edges: torch.Tensor,
    mirna_gene_edges: torch.Tensor,
    n_cpg: int,
    n_mirna: int,
    max_edges_per_node: int = 10,
) -> tuple:
    print("   Building CpG<->miRNA co-regulation edges...", end=" ", flush=True)

    gene_to_cpg: dict[int, set] = {}
    for i in range(cpg_gene_edges.shape[1]):
        g = cpg_gene_edges[1, i].item()
        gene_to_cpg.setdefault(g, set()).add(cpg_gene_edges[0, i].item())

    gene_to_mirna: dict[int, set] = {}
    for i in range(mirna_gene_edges.shape[1]):
        g = mirna_gene_edges[1, i].item()
        gene_to_mirna.setdefault(g, set()).add(mirna_gene_edges[0, i].item())

    c2m_src, c2m_dst = [], []
    m2c_src, m2c_dst = [], []
    cpg_count: dict[int, int] = {}
    mir_count: dict[int, int] = {}
    seen: set = set()

    for g, cpg_set in gene_to_cpg.items():
        mirna_set = gene_to_mirna.get(g, set())
        if not mirna_set:
            continue
        for c in cpg_set:
            if cpg_count.get(c, 0) >= max_edges_per_node:
                continue
            for m in mirna_set:
                if mir_count.get(m, 0) >= max_edges_per_node:
                    continue
                key = (c, m)
                if key in seen:
                    continue
                seen.add(key)
                c2m_src.append(c);  c2m_dst.append(m)
                m2c_src.append(m);  m2c_dst.append(c)
                cpg_count[c] = cpg_count.get(c, 0) + 1
                mir_count[m] = mir_count.get(m, 0) + 1

    print(f"{len(c2m_src):,} edges")
    if not c2m_src:
        return None, None

    c2m = torch.tensor([c2m_src, c2m_dst], dtype=torch.long)
    m2c = torch.tensor([m2c_src, m2c_dst], dtype=torch.long)
    return c2m, m2c


# ─────────────────────────────────────────────────────────────────────────────
#  Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _find_col(columns: list, candidates: list) -> str | None:
    col_lower = [c.lower() for c in columns]
    for cand in candidates:
        for i, c in enumerate(col_lower):
            if cand.lower() == c or cand.lower() in c:
                return columns[i]
    return None


def _identity_edges(n: int) -> torch.Tensor:
    idx = torch.arange(n, dtype=torch.long)
    return torch.stack([idx, idx], dim=0)


def _self_loop_fallback(n_src: int, n_dst: int, n: int = 500) -> torch.Tensor:
    rng = np.random.default_rng(0)
    s = rng.integers(0, n_src, n)
    d = rng.integers(0, n_dst, n)
    return torch.tensor([s.tolist(), d.tolist()], dtype=torch.long)