# Spectral Geometry of Accessible Quantum Tangents

Reproducibility and falsification-oriented numerical experiments for **“Spectral Geometry of Accessible Quantum Tangents: Beyond Isotropic Readout-Rank Laws.”**

The repository is intentionally designed so that a scientific disagreement does not make the workflow “fail.” CI failures are reserved for implementation invariants: wrong derivatives, loss of normalization, violation of the Fisher contraction beyond tolerance, broken symmetry support, incorrect readout ranks, or disagreement between the optimized simulator and an independent small-n reference implementation. Research results are always written to artifacts, whether they support or contradict the manuscript.

## Start here

Run the software checks locally:

```bash
python -m pip install -e '.[dev]'
pytest
aqt run --profile profiles/smoke.json --output results/smoke
```

Reproduce the numerical protocol stated in the manuscript:

```bash
aqt run --profile profiles/reproduce_paper.json --output results/reproduction
aqt analyze --input 'results/reproduction/raw.csv' --output results/reproduction-analysis
```

The reproduction profile uses n=6,8,10, depth d=6n, 48 Gaussian parameter-space tangent directions, six independent circuits for each nonconserving family, and twelve U(1) circuits per size. See `docs/REPRODUCTION_NOTES.md` for the scheduling inconsistency found in the confirmatory notebook and how it is handled.

## GitHub Actions

Open **Actions -> Research experiment suite -> Run workflow** and choose one prespecified profile. Sixteen deterministic shards are executed, their raw outputs are retained separately, and a final job merges the circuit-level data, bootstraps confidence intervals, runs exact isotropic controls, and uploads a consolidated analysis artifact.

Recommended order:

1. `reproduce_paper`
2. `pra_core`
3. `pra_depth`
4. `pra_spectrum`
5. `pra_orientation`
6. `pra_basis`
7. `pra_noise`
8. `pra_directions`
9. `pra_large_n`

Do not start by tuning profiles after looking at outcomes. If a profile is changed after results are known, record the change and treat it as exploratory rather than confirmatory.

## What the PRA-oriented suite adds

- two additional generic circuit architectures, so “generic” is not identified with one entangler;
- n=12 in the core replication and a selected n=14 finite-size extension;
- a full depth sweep instead of only d=6n;
- more circuit instances and tangent directions;
- unbiased U-statistics for both Tr(C^2) and Tr(C^3);
- repeated cross-fitted rank-r spectral recovery instead of relying only on an in-sample spectrum;
- Haar-random rank-matched readout controls at fixed covariance, directly testing the relative-orientation theorem;
- Z/X/Y/random-local measurement-basis robustness;
- exact classical readout bit-flip noise channels;
- Gaussian/Rademacher/coordinate tangent-ensemble robustness;
- an independent explicit-matrix simulator for small-n verification;
- exact Monte Carlo controls for the isotropic Beta projector law.

The detailed rationale and falsification criteria are in `docs/EXPERIMENT_DESIGN.md` and `docs/CLAIM_TEST_MATRIX.md`.

## Output conventions

`raw.csv` contains one row per fixed circuit and readout order. `circuit_id` is the independent statistical unit. Tangent directions within a fixed circuit are never used as independent bootstrap observations. `pairwise_purity` estimates Tr(C^2) without the diagonal self-overlap bias; `deff_pairwise=1/pairwise_purity` is labeled a diagnostic rather than an unbiased estimator. `trC3_u_stat` is a distinct-triple U-statistic. `crossfit_kyfan` is estimated on held-out tangent directions.

For the reproduction profile, `paper_reproduction_comparison.csv` shows the rerun minus the manuscript values. No tolerance is used to suppress or automatically “fix” a discrepancy.

## Data availability

Workflow artifacts are sufficient for immediate independent checking, but a manuscript submission should archive the final release and result bundle in a persistent repository (for example Zenodo) and cite its DOI. See `docs/DATA_AVAILABILITY.md`.
