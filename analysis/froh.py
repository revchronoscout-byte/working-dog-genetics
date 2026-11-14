"""Compute genomic inbreeding (F_ROH) per dog from PLINK --homozyg output.

F_ROH = total length of runs of homozygosity / length of autosomal genome covered

Usage:
    python analysis/froh.py results/belgian_roh.hom.indiv data/processed/belgian_qc.bim
"""
import sys

import pandas as pd

indiv_path, bim_path = sys.argv[1], sys.argv[2]

indiv = pd.read_csv(indiv_path, sep=r"\s+")
bim = pd.read_csv(bim_path, sep=r"\s+", header=None,
                  names=["CHR", "SNP", "CM", "BP", "A1", "A2"])

# Autosomal length covered by the array: first to last SNP on each chromosome.
span = bim.groupby("CHR")["BP"].agg(lambda bp: bp.max() - bp.min()).sum()
genome_kb = span / 1000

indiv["F_ROH"] = indiv["KB"] / genome_kb

out = indiv_path.replace(".hom.indiv", "_froh.csv")
indiv[["FID", "IID", "NSEG", "KB", "F_ROH"]].to_csv(out, index=False)

print(f"Autosomal span covered: {genome_kb / 1e6:.2f} Gb")
print(indiv["F_ROH"].describe().round(3).to_string())
print(f"Saved {out}")
