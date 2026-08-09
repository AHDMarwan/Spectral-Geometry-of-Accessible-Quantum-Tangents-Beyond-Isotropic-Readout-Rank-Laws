# Spectral Geometry of Accessible Quantum Tangents

Reproducibility, falsification, and outcome-blind numerical experiments for **“Spectral Geometry of Accessible Quantum Tangents: Beyond Isotropic Readout-Rank Laws.”**

## Current scientific protocol: rigorous-v2

The current experiment suite is `rigorous-v2`. It was defined as a fresh outcome-blind campaign: previous numerical values, confidence intervals, plots, and trends are not used to tune seeds, sample sizes, ansatz inclusion, success thresholds, or analysis choices.

The full protocol is frozen in `docs/RIGOROUS_PROTOCOL_V2.md`.

The design principle is simple: a scientific result is never made to “pass” CI. GitHub Actions fails only for technical invalidity such as missing scheduled jobs, nonregular tangents, normalization failures, broken horizontality, `F_full > F_Q` beyond tolerance, nonfinite endpoints, or violation of an exact empirical covariance/projector bound. Results that contradict the theoretical narrative are retained and reported normally.

Legacy reproduction and earlier PRA-oriented profiles remain in the repository only for provenance. They are not inputs to rigorous-v2 inference.

## Local checks

```bash
python -m pip install -e '.[dev]'
pytest
python -m aqt.rigorous run \
  --profile profiles/v2_smoke.json \
  --output results/v2-smoke
python -m aqt.rigorous validate \
  --profile profiles/v2_smoke.json \
  --raw 'results/v2-smoke/raw.csv' \
  --output results/v2-smoke/validation.json
```

## GitHub Actions

Open **Actions -> Rigorous v2 outcome-blind experiments -> Run workflow** and choose one frozen campaign. The workflow executes 32 deterministic shards, records the environment for every shard, applies a technical-validity gate, performs circuit-level/family-balanced analysis, and uploads raw plus processed artifacts.

Recommended order:

1. `v2_convergence` — establish how many tangent directions are needed.
2. `v2_primary` — main family-robust finite-size inference.
3. `v2_depth` — depth onset/saturation.
4. `v2_spectrum` — dedicated spectral/Ky-Fan study with 512 tangents.
5. `v2_orientation` — explicit rank-matched Haar orientation calibration.
6. `v2_basis` — measurement-basis scope.
7. `v2_directions` — tangent-ensemble scope.
8. `v2_large_n` — selected `n=14,16` extension.
9. `v2_n18` — targeted stress test, used only if precision gates pass.
10. `v2_n20_optional` — optional stress test; never promoted to a primary claim merely because it finishes.

Do not edit a frozen profile after inspecting its output and still call the rerun confirmatory. Any post-outcome modification must receive a new profile name/seed and be labeled exploratory.

## What rigorous-v2 changes

- new independent master seeds, separated from all previous experiment outcomes;
- a separate `src/aqt/rigorous.py` experiment engine;
- fixed circuit instance as the independent statistical unit;
- 10,000-resample circuit-level confidence intervals;
- equal weighting of generic ansatz families rather than circuit-count-weighted pooling;
- leave-one-family-out sensitivity analysis for every generic aggregate;
- nested `M=32,64,128,256` tangent convergence using prefixes of one fixed direction draw;
- memory-bounded exact tangent batching, with batched/unbatched equivalence tests;
- explicit numerical checks for state norm, horizontality, probability normalization, zero-sum probability tangents, and Fisher contraction;
- exact first two Haar-Grassmann moments for rank-matched random-orientation retention at fixed empirical covariance;
- direct Monte Carlo calibration of that orientation null at moderate sizes;
- empirical projector/covariance bound checks as a technical invariant;
- a dedicated 512-direction spectral campaign with `Tr(C^2)`, `Tr(C^3)`, empirical spectra, Ky-Fan recovery, and repeated train/test cross-fitting;
- separate depth, basis, and tangent-ensemble studies so the scope of any conclusion is explicit;
- large-n results accepted for inference only when circuit-count, numerical-validity, and precision diagnostics pass.

## Main outputs

Each shard writes `raw.csv`; spectral and explicit random-orientation campaigns additionally write `spectrum.csv` and `random_readout_null.csv` when applicable.

The aggregate analysis writes:

- `family_summary.csv` — family-specific circuit bootstrap estimates and precision flags;
- `pooled_summary.csv` — equal-weight-per-family generic estimates and U(1) estimates;
- `leave_one_family_out.csv` — architecture sensitivity;
- `tangent_convergence_by_circuit.csv` and `tangent_convergence_summary.csv` when nested M prefixes exist;
- `orientation_summary.csv` — physical-minus-rank-baseline and standardized Haar-orientation diagnostics;
- `spectral_diagnostics.csv` for spectral profiles;
- `numerical_audit.csv`;
- `technical_validation.json`.

`pairwise_purity` is the distinct-pair U-statistic estimate of `Tr(C^2)`; `deff_pairwise=1/pairwise_purity` remains a reciprocal diagnostic rather than an unbiased estimator of effective dimension. Full spectral-shape claims are reserved for the dedicated spectral campaign.

## Reporting policy

Every manuscript table based on rigorous-v2 should state the number of independent circuits, tangent count, confidence interval, ansatz family, system size, depth, measurement basis, and relevant quality flag. Family-specific results appear alongside any generic aggregate. No scheduled cell is removed because it weakens a claim.

No simulation through `n=20` is described as an asymptotic proof. Large-n runs are finite-size evidence only.

## Data availability

A manuscript release should archive the exact Git commit, frozen profile JSON files, raw shard artifacts, merged analysis tables, technical validation, environment manifests, and generated figures under a persistent DOI. See `docs/DATA_AVAILABILITY.md`.
