"""Plot PC1 vs PC2 from PLINK --pca output.

Usage:
    python analysis/plot_pca.py results/belgian [labels.csv]

labels.csv (optional): columns IID,group  e.g. dog123,Malinois
If no labels are given, all dogs are drawn in one color.
"""
import sys

import matplotlib.pyplot as plt
import pandas as pd

prefix = sys.argv[1]
labels_path = sys.argv[2] if len(sys.argv) > 2 else None

vec = pd.read_csv(f"{prefix}.eigenvec", sep=r"\s+", header=None)
vec.columns = ["FID", "IID"] + [f"PC{i}" for i in range(1, vec.shape[1] - 1)]
val = pd.read_csv(f"{prefix}.eigenval", header=None)[0]
pct = 100 * val / val.sum()  # share among the computed PCs, not total variance

if labels_path:
    labels = pd.read_csv(labels_path)
    vec = vec.merge(labels, on="IID", how="left").fillna({"group": "unlabeled"})
else:
    vec["group"] = "all dogs"

fig, ax = plt.subplots(figsize=(6, 5))
for group, d in vec.groupby("group"):
    ax.scatter(d["PC1"], d["PC2"], s=12, alpha=0.7, label=group)
ax.set_xlabel(f"PC1 ({pct[0]:.1f}% of top-PC variance)")
ax.set_ylabel(f"PC2 ({pct[1]:.1f}% of top-PC variance)")
ax.set_title("Population structure")
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(f"{prefix}_pca.png", dpi=200)
print(f"Saved {prefix}_pca.png")
