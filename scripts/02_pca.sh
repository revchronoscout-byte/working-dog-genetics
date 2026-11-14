#!/usr/bin/env bash
# LD pruning + PCA for population structure.
# Usage: bash scripts/02_pca.sh belgian
set -euo pipefail

NAME="$1"
QC="data/processed/${NAME}_qc"
OUT="results/${NAME}"
mkdir -p results

# Prune SNPs in strong linkage disequilibrium so PCA isn't dominated by
# blocks of correlated markers: 50-SNP window, step 5, r^2 threshold 0.2.
plink --dog --bfile "$QC" \
  --indep-pairwise 50 5 0.2 \
  --out "data/processed/${NAME}_prune"

# Top 10 principal components on the pruned SNP set.
plink --dog --bfile "$QC" \
  --extract "data/processed/${NAME}_prune.prune.in" \
  --pca 10 \
  --out "$OUT"

echo "PCA done: ${OUT}.eigenvec / ${OUT}.eigenval"
echo "Plot with: python analysis/plot_pca.py ${OUT}"
