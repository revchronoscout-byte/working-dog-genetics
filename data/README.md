# Data

Raw genotype files are **not** committed (see `.gitignore`). Download them into `data/raw/`.

## 1. Belgian shepherds (Malinois, Tervuren, Sheepdog)

- Source: Dryad, doi:10.5061/dryad.pg4f4qrzs
- URL: https://datadryad.org/dataset/doi:10.5061/dryad.pg4f4qrzs
- Start with the 173k Illumina CanineHD set: `173k_prephased_highcall.{bed,bim,fam}` (363 dogs)
- Larger alternative: `Imputed.{bed,bim,fam}` (870 dogs, ~5 GB). Use only if needed.
- Reference genome: CanFam3.1

**To check first:** whether the `.fam` file or README includes breed/variety labels (Malinois vs. Tervuren vs. Sheepdog). If not, use PCA clusters or request labels from the study authors.

## 2. German Shepherd Dogs

- Source: Zenodo record 6040187, "SNP genotypes for healthy and CIM-affected GSDs"
- URL: https://zenodo.org/record/6040187
- Illumina CanineHD BeadChip, ~220k SNPs

## Expected layout

```
data/raw/belgian/173k_prephased_highcall.bed|bim|fam
data/raw/gsd/<files from Zenodo>
```

Note: the two datasets come from different arrays. Merging them requires restricting to shared SNPs, aligning strands, and checking that both use the same reference build. Analyze each dataset separately first.
