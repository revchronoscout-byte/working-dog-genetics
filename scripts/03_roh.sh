#!/usr/bin/env bash
# Runs of homozygosity (ROH) for genomic inbreeding.
# Usage: bash scripts/03_roh.sh belgian
set -euo pipefail

NAME="$1"
QC="data/processed/${NAME}_qc"
OUT="results/${NAME}_roh"
mkdir -p results

# Settings are a common starting point for ~170k-SNP canine arrays.
# Long ROH (>= 1 Mb here) reflect recent inbreeding: both copies of a
# chromosome segment were inherited from the same recent ancestor.
plink --dog --bfile "$QC" \
  --homozyg \
  --homozyg-kb 1000 \
  --homozyg-snp 50 \
  --homozyg-density 50 \
  --homozyg-gap 1000 \
  --homozyg-window-snp 50 \
  --homozyg-window-het 1 \
  --homozyg-window-missing 5 \
  --out "$OUT"

echo "ROH done: ${OUT}.hom (segments), ${OUT}.hom.indiv (per-dog totals)"
echo "Compute F_ROH with: python analysis/froh.py ${OUT}.hom.indiv ${QC}.bim"
