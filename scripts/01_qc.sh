#!/usr/bin/env bash
# Quality control on a PLINK binary dataset.
# Usage: bash scripts/01_qc.sh data/raw/belgian/173k_prephased_highcall belgian
#   $1 = input prefix (path without .bed/.bim/.fam)
#   $2 = short name for outputs
set -euo pipefail

IN="$1"
NAME="$2"
OUT_DIR="data/processed"
mkdir -p "$OUT_DIR"

# --dog          : dog chromosome set (38 autosomes + X, Y, MT)
# --autosome     : keep autosomes only (ROH and inbreeding use autosomes)
# --geno 0.05    : drop SNPs missing in >5% of dogs
# --mind 0.10    : drop dogs missing >10% of SNPs
# --maf 0.01     : drop near-monomorphic SNPs
plink --dog \
  --bfile "$IN" \
  --autosome \
  --geno 0.05 \
  --mind 0.10 \
  --maf 0.01 \
  --make-bed \
  --out "$OUT_DIR/${NAME}_qc"

echo "QC done: $OUT_DIR/${NAME}_qc.{bed,bim,fam}"
