# -*- coding: utf-8 -*-
"""Map top-attention CpG (per_patient.csv) -> gene bang manifest Illumina 450K.
Tap trung lop hiem: 2=MSI, 3=HM-SNV, 4=EBV.
"""
import csv, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PP   = os.path.join(ROOT, "docs", "per_patient.csv")
MAN  = os.path.join(ROOT, "data", "humanmethylation450_15017482_v1-2.csv")

SUBTYPE = {0: "CIN", 1: "GS", 2: "MSI", 3: "HM-SNV", 4: "EBV"}

# 1) gom tat ca cg + weight tu per_patient.csv
rows = list(csv.DictReader(open(PP, encoding="utf-8")))
wanted = set()
for r in rows:
    for k in ("cpg_top1", "cpg_top2", "cpg_top3", "cpg_top4", "cpg_top5"):
        cg = r[k].split(":")[0]
        if cg:
            wanted.add(cg)
print(f"[i] {len(rows)} benh nhan, {len(wanted)} cg ID duy nhat trong top-5")

# 2) doc manifest -> map chi cac cg can
cg2gene, cg2grp, cg2isl = {}, {}, {}
with open(MAN, encoding="utf-8", errors="ignore") as f:
    # bo qua header tro toi dong bat dau bang 'IlmnID'
    for line in f:
        if line.startswith("IlmnID,"):
            header = next(csv.reader([line]))
            break
    idx = {c: i for i, c in enumerate(header)}
    gi  = idx["UCSC_RefGene_Name"]
    gri = idx["UCSC_RefGene_Group"]
    isi = idx["Relation_to_UCSC_CpG_Island"]
    ni  = idx["Name"]
    for parts in csv.reader(f):
        if len(parts) <= gi:
            continue
        name = parts[ni]
        if name in wanted:
            genes = parts[gi].split(";")
            # gene dau tien khac rong, unique giu thu tu
            uniq = []
            for g in genes:
                if g and g not in uniq:
                    uniq.append(g)
            cg2gene[name] = "/".join(uniq) if uniq else "(intergenic)"
            grp = parts[gri].split(";")
            cg2grp[name] = grp[0] if grp and grp[0] else "-"
            cg2isl[name] = parts[isi] if parts[isi] else "-"
print(f"[i] map duoc {len(cg2gene)}/{len(wanted)} cg ra annotation")

# 3) xuat bang cho lop hiem
out_lines = []
for target in (4, 3, 2):  # EBV, HM-SNV, MSI
    pats = [r for r in rows if int(r["true_subtype"]) == target]
    out_lines.append(f"\n===== {SUBTYPE[target]} (class {target}) — {len(pats)} benh nhan =====")
    for r in pats:
        cgs = []
        for k in ("cpg_top1", "cpg_top2", "cpg_top3"):
            cg, w = r[k].split(":")
            g = cg2gene.get(cg, "?")
            grp = cg2grp.get(cg, "?")
            isl = cg2isl.get(cg, "?")
            cgs.append(f"{cg}->{g} [{grp},{isl}] w={w}")
        ok = "OK" if r["correct"] == "1" else "MISS"
        out_lines.append(f"  {r['patient_id']} ({r['cancer_type']}) pred={SUBTYPE[int(r['pred_subtype'])]} [{ok}]")
        for c in cgs:
            out_lines.append(f"      {c}")

txt = "\n".join(out_lines)
print(txt)
open(os.path.join(ROOT, "docs", "cpg_gene_rareclass.txt"), "w", encoding="utf-8").write(txt)

# 4) gene xuat hien lap lai trong tung lop hiem (tin hieu)
from collections import Counter
print("\n===== GENE LAP LAI theo lop (top-3 CpG) =====")
for target in (4, 3, 2):
    pats = [r for r in rows if int(r["true_subtype"]) == target]
    cnt = Counter()
    for r in pats:
        seen = set()
        for k in ("cpg_top1", "cpg_top2", "cpg_top3"):
            cg = r[k].split(":")[0]
            g = cg2gene.get(cg, "?")
            for gg in g.split("/"):
                if gg and gg not in ("(intergenic)", "?") and gg not in seen:
                    cnt[gg] += 1
                    seen.add(gg)
    common = [f"{g}({n})" for g, n in cnt.most_common(12) if n >= 2]
    print(f"  {SUBTYPE[target]}: " + (", ".join(common) if common else "(khong gene nao lap >=2)"))
