# V3 n=20 orientation confirmation: frozen decision rules

## Scientific purpose

This is a fresh-seed, out-of-sample `n=20` confirmation run designed after the exploratory asymptotic-bridge analysis and before any `v3_n20_orientation_confirmatory` outcomes are generated. Its role is to distinguish three finite-size physical regimes at depth `d=6n`:

1. practical rank typicality with a small systematic physical-orientation bias (`SU2-HaarU4-brickwork`),
2. an architecture-specific rank-law failure at one-body readout (`RY-RZ-CZ-line`), and
3. symmetry-induced positive alignment (`U1-RZ-XY-line`).

The random-Grassmann theorem is an analytic null model. This experiment does not assume that a physical readout is Haar-random and does not claim to prove the physical `n -> infinity` limit.

## Frozen design

- profile: `v3_n20_orientation_confirmatory`
- master seed: `77125101`
- qubits: `n=20`
- depth: `d=6n=120`
- families: `RY-RZ-CZ-line`, `SU2-HaarU4-brickwork`, `U1-RZ-XY-line`
- independent circuits: 12 per family
- tangent directions per fixed circuit: 64 normalized Gaussian directions
- measurement basis: `Z`
- readout orders: `k=1,2`
- bit-flip rate: zero
- independent experimental unit: fixed circuit instance
- uncertainty: 10,000 circuit-bootstrap resamples
- practical rank-equivalence band: `0.90 <= rho_k <= 1.10`

No family, circuit, metric, seed, or readout order will be removed because it weakens a prediction.

## Primary decision rules

All decisions are family-specific and are evaluated at `n=20` separately for `k=1` and `k=2` unless stated otherwise.

### H1: Haar-U4 practical rank typicality

For `SU2-HaarU4-brickwork`, practical rank typicality is confirmed for a readout order only if the entire circuit-bootstrap 95% CI for `rho_k` lies inside `[0.90,1.10]`.

### H2: Haar-U4 systematic negative physical bias

For `SU2-HaarU4-brickwork`, a systematic negative orientation bias is confirmed for a readout order only if the entire 95% CI for `rho_k` lies below `1.0` and the population-null orientation score `z_pop` has an entire 95% CI below zero.

H1 and H2 are allowed to hold simultaneously: a physical architecture can be practically rank-typical while remaining detectably non-Haar in orientation.

### H3: RY-RZ-CZ one-body structural exception

For `RY-RZ-CZ-line`, persistence of the one-body exception is confirmed only if the entire 95% CI for `rho_1` lies below `0.90`.

### H4: RY-RZ-CZ two-body practical rank typicality

For `RY-RZ-CZ-line`, the two-body rank law is confirmed only if the entire 95% CI for `rho_2` lies inside `[0.90,1.10]`. A systematic negative bias is reported separately if the entire CI also lies below `1.0` and the `z_pop` CI is below zero.

### H5: U(1) symmetry-induced positive alignment

For `U1-RZ-XY-line`, symmetry enhancement is confirmed for a readout order only if the entire 95% CI for `rho_k` lies above `1.10` and the entire 95% CI for `z_pop` lies above zero.

The magnitude of the U(1) enhancement is reported without introducing a post-outcome numerical threshold.

## Population-null orientation diagnostic

For each circuit,

`z_pop = (rho_phys - 1) / sigma_rho`,

where `sigma_rho` uses the exact real Haar/Grassmann rank-matched projector variance with the archived pairwise U-statistic estimate of `Tr(C^2)`.

The normalized bridge ratio `|z_pop|/sqrt(r d_eff)` is reported descriptively only. It is not a separate primary hypothesis because it is algebraically coupled to `rho-1` through `sigma_rho`.

## Validity gates

Scientific decisions are made only if:

- the rigorous technical validator passes;
- every scheduled family has 12 independent fixed circuits;
- dense tangent regularity is at least 99%;
- all population-purity estimates used in `z_pop` lie in the admissible PSD interval `[1/N,1]`;
- the relevant family-level `rho_k` cell passes the profile precision flag (`max_relative_ci_halfwidth=0.20`).

A failed scientific prediction is retained as a valid negative result. A failed technical/precision gate is reported as insufficient evidence rather than converted into support by changing thresholds or rerunning with a different seed.

## Secondary outputs

The run reports actual retention, `d_eff`, pairwise purity, `F_full/F_Q`, U(1)-minus-family-balanced-generic contrasts, and the standard numerical audit. These are secondary for this confirmation and do not alter the primary decision rules above.

## Provenance

The profile, this document, evaluator code, workflow, and commit SHA must be merged to `main` before the trigger that starts the run. The run head SHA is the frozen preregistration point. All shard raw CSVs and aggregate analysis tables will be archived after completion.
