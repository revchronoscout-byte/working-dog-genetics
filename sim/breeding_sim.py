"""Forward simulation of a closed working-dog breeding program with cloning.

Model (v0, deliberately simple):
- Closed population of N breeding dogs per generation, L unlinked biallelic loci.
- Founders drawn under Hardy-Weinberg with allele frequencies p ~ Uniform(0.05, 0.5).
- At generation 0, K elite donors are chosen from the founders and their cells are
  biobanked, so their genotypes are fixed forever.
- Each generation, a share C of the N new dogs are clones of a randomly chosen
  banked donor. The rest come from random mating among the previous generation
  (clones included), with Mendelian inheritance at every locus.
- Diversity is tracked as expected heterozygosity He = mean over loci of 2p(1-p).
  Inbreeding relative to the founders: F_t = 1 - He_t / He_0.
- Effective population size from heterozygosity decay over T generations:
  He_T / He_0 = (1 - 1/(2 Ne))^T  ->  Ne = 1 / (2 * (1 - (He_T/He_0)^(1/T)))

Known simplifications (next steps): no linkage, no selection on performance,
random rather than merit-based donor choice, no overlapping generations.

Usage:
    python sim/breeding_sim.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

N = 200            # breeding dogs per generation
L = 2000           # loci
GENERATIONS = 15
REPS = 20
SCENARIOS = [      # (share of dogs that are clones, number of banked donors)
    (0.00, 0),
    (0.25, 10),
    (0.25, 2),
    (0.50, 10),
    (0.50, 2),
]
OUT = Path("results")


def expected_het(geno):
    """Mean expected heterozygosity across loci. geno: (n_dogs, L, 2) of 0/1."""
    p = geno.mean(axis=(0, 2))
    return float(np.mean(2 * p * (1 - p)))


def make_offspring(parents, n, rng):
    """Random mating: each offspring gets one random allele per locus from each of two parents."""
    n_par, n_loci, _ = parents.shape
    kids = np.empty((n, n_loci, 2), dtype=np.int8)
    for side in range(2):
        idx = rng.integers(0, n_par, size=n)                      # one parent per offspring
        which = rng.integers(0, 2, size=(n, n_loci))              # which allele that parent passes
        kids[:, :, side] = np.take_along_axis(parents[idx], which[:, :, None], axis=2)[:, :, 0]
    return kids


def run(clone_share, n_donors, rng):
    p0 = rng.uniform(0.05, 0.5, size=L)
    pop = (rng.random((N, L, 2)) < p0[None, :, None]).astype(np.int8)
    donors = pop[rng.choice(N, size=n_donors, replace=False)] if n_donors else None

    he0 = expected_het(pop)
    f = [0.0]
    n_clones = int(round(clone_share * N))
    for _ in range(GENERATIONS):
        kids = make_offspring(pop, N - n_clones, rng)
        if n_clones:
            clones = donors[rng.integers(0, n_donors, size=n_clones)]
            kids = np.concatenate([kids, clones])
        pop = kids
        f.append(1 - expected_het(pop) / he0)
    return np.array(f)


def ne_from_f(f_final, t):
    ratio = 1 - f_final
    return 1 / (2 * (1 - ratio ** (1 / t)))


def main():
    rng = np.random.default_rng(2026)
    OUT.mkdir(exist_ok=True)
    rows, curves = [], {}
    for share, k in SCENARIOS:
        runs = np.array([run(share, k, rng) for _ in range(REPS)])
        mean = runs.mean(axis=0)
        label = "No cloning" if share == 0 else f"{int(share * 100)}% clones, {k} donors"
        curves[label] = mean
        rows.append({
            "scenario": label,
            "clone_share": share,
            "donors": k,
            f"F_gen{GENERATIONS}_mean": round(mean[-1], 4),
            f"F_gen{GENERATIONS}_sd": round(runs[:, -1].std(), 4),
            "Ne_estimate": round(ne_from_f(mean[-1], GENERATIONS), 1),
        })

    summary = pd.DataFrame(rows)
    summary.to_csv(OUT / "sim_summary.csv", index=False)
    print(summary.to_string(index=False))

    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, mean in curves.items():
        ax.plot(range(GENERATIONS + 1), mean, marker="o", ms=3, label=label)
    ax.set_xlabel("Generation")
    ax.set_ylabel("Inbreeding F (loss of heterozygosity vs. founders)")
    ax.set_title(f"Simulated breeding program (N={N} dogs/generation, {REPS} reps)")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "sim_inbreeding.png", dpi=200)
    print(f"Saved {OUT / 'sim_inbreeding.png'}")


if __name__ == "__main__":
    main()
