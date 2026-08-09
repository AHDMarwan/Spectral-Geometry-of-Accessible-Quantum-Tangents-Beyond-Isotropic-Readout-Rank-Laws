# Rigorous v2 protocol: outcome-blind numerical study

## 1. Reset and scientific objective

This protocol supersedes the earlier exploratory/confirmatory numerical campaign for the purpose of new inference. No previously observed numerical value, confidence interval, trend, plot, or effect size is used to choose a seed, remove a circuit, set a success threshold, select an ansatz, or tune an analysis choice in rigorous-v2.

The objective is falsification-oriented: determine which finite-size statements about accessible quantum tangent geometry are supported by new independent simulations, and state explicitly where the evidence is insufficient or contradictory.

The legacy reproduction code and outputs remain in the repository for provenance, but rigorous-v2 profiles use new master seeds and a separate engine (`src/aqt/rigorous.py`). Legacy results are not inputs to rigorous-v2 analysis.

## 2. Independent experimental unit

A fixed circuit instance is the independent experimental unit. Tangent directions sampled inside one fixed circuit are repeated local probes and are never counted as independent circuits. All uncertainty intervals used for scientific inference are therefore bootstrapped over circuit instances.

For pooled generic statements, ansatz families receive equal weight. The analysis resamples circuits within each ansatz family and then averages family means. This prevents a family with more circuit instances from dominating a generic conclusion.

The analysis also reports leave-one-family-out estimates. A generic claim must survive this sensitivity analysis; a contrary architecture is reported as a contrary architecture rather than hidden by pooling.

## 3. Prespecified primary quantities

The primary finite-size quantities are:

- physical readout retention `Tr(P_k C)` for one- and two-body computational-basis readouts;
- rank-law enhancement `rho_k = Tr(P_k C)/(r_k/N)`;
- the pairwise U-statistic estimator of `Tr(C^2)` and its reciprocal diagnostic `d_eff`;
- `F_full/F_Q`;
- physical-minus-rank-baseline alignment `Tr(P_k C) - r_k/N`.

`d_eff` is treated only as a second-moment diagnostic. Claims about the shape of the spectrum require the dedicated spectral campaign.

## 4. Rank-law statement is an equivalence claim

A generic circuit is not declared rank-typical merely because a test fails to reject `rho_k=1`. The prespecified practical equivalence band is

`0.90 <= rho_k <= 1.10`.

`src/aqt/rigorous_inference.py` writes `rank_law_equivalence.csv`. A positive rank-law equivalence statement requires the entire circuit-level 95% confidence interval to lie inside this band. Results outside the band, or confidence intervals too wide to fit inside it, are reported as non-equivalent or inconclusive respectively.

This 10% equivalence margin is fixed before rigorous-v2 outcomes are inspected.

## 5. Main campaign

`v2_primary` is the main family-robust finite-size experiment.

- sizes: `n = 6, 8, 10, 12`;
- depth: `d = 6n`;
- five nonconserving ansatz families plus the half-filled U(1) family;
- 16 independent circuits per nonconserving family and 20 U(1) circuits per size;
- 128 normalized Gaussian parameter directions per fixed circuit;
- one- and two-body readouts;
- no spectral reconstruction and no post-hoc exclusion.

A family/size cell is flagged as inference-ready only when it contains at least 12 independent circuits and the circuit-level 95% confidence interval satisfies the prespecified precision diagnostic in the profile. A scientifically negative result is still a valid result.

## 6. Tangent-sample convergence

`v2_convergence` draws 256 directions once and analyzes the nested prefixes `M = 32, 64, 128, 256`. The smaller-M data are prefixes of the same direction draw, not separately resampled datasets.

Before a result based on `M <= 128` is used as a strong conclusion, the convergence tables must show that increasing M does not materially change the corresponding endpoint. The prespecified practical targets are:

- `rho_k`, physical retention, and `F_full/F_Q`: 95th percentile absolute relative change no larger than 5% when compared with `M=256`;
- `d_eff` and `Tr(C^2)`: 95th percentile absolute relative change no larger than 10%.

Failure of these targets does not invalidate the theory; it means that more tangent directions are required before that endpoint can support a precise conclusion.

## 7. Depth dependence

`v2_depth` tests `d/n = 0.5, 1, 2, 4, 6, 8` at `n = 8, 12` for three distinct nonconserving architectures and U(1). This separates a deep-circuit statement from an accidental choice of one depth.

Any claim of deep generic rank-typicality must be phrased as a depth-dependent observation if the approach to the rank law is not stable across this sweep.

## 8. Dedicated spectral experiment

`v2_spectrum` uses 512 tangent directions at `n = 8, 10, 12` and stores the entire nonzero empirical spectrum available from those directions. It additionally reports:

- the pairwise U-statistic for `Tr(C^2)`;
- the distinct-triple U-statistic for `Tr(C^3)`;
- the empirical covariance spectrum;
- the empirical Ky Fan rank-r optimum;
- repeated train/test cross-fitted rank-r recovery.

Spectral claims are made from this campaign, not inferred from `d_eff` alone. The high-n campaigns are not used to assert a full spectral shape when the number of sampled tangent directions is too small to resolve it.

## 9. Physical alignment versus random orientation

For a rank-r Haar-random real projector `P` in an N-dimensional centered score space and fixed empirical covariance `C` with `Tr(C)=1`, rigorous-v2 records the exact first two orientation-null moments

`E[Tr(PC)] = r/N`,

`Var[Tr(PC)] = 2 r (N-r) (N Tr(C^2)-1) / [N^2 (N-1)(N+2)]`.

The engine uses empirical covariance purity for this conditional orientation diagnostic and reports a standardized physical-readout alignment score. It also checks the deterministic projector/covariance deviation bound using the empirical covariance.

`v2_orientation` is a focused calibration study at moderate sizes. It uses 500 explicit rank-matched random subspaces on a smaller set of independent circuits to verify that the analytic orientation-null moments behave correctly on actual circuit covariances. Individual Monte Carlo p-values are diagnostic and are not used as a multiple-testing fishing mechanism.

## 10. U(1)-versus-generic contrasts

The prespecified inference module writes `u1_vs_generic_contrasts.csv`. The generic side of each contrast is the equal-weight mean of generic ansatz-family means, with circuits bootstrapped within families. U(1) circuits are bootstrapped independently.

All listed primary contrasts are retained. Metrics are not selected for publication according to whether their confidence interval excludes zero.

## 11. Global anisotropy diagnostics

The inference module reports dimension-normalized second-moment quantities:

- `N * Tr(C^2)`, whose isotropic reference is 1;
- `d_eff/N`, whose isotropic reference is 1.

These are second-moment diagnostics only. A statement about the full spectrum requires `v2_spectrum`.

## 12. Measurement and tangent-ensemble scope

`v2_basis` repeats the same fixed-circuit logic in Z, X, Y, and independently seeded random-local measurement bases. A basis-dependent phenomenon must be stated as basis-dependent.

`v2_directions` compares Gaussian, Rademacher, and coordinate parameter-direction ensembles. A qualitative reversal across direction ensembles prevents an ensemble-independent claim.

## 13. Large-n extension

`v2_large_n` extends selected architecture families to `n = 14, 16` with 12 nonconserving and 16 U(1) circuit instances and 96 tangent directions. These cells are used only when their precision flags and the tangent-convergence study support the relevant endpoint.

`v2_n18` is a targeted `n=18` stress test using a generic Haar-U4 brickwork family and U(1). It is not promoted to a primary conclusion merely because the simulation completes.

`v2_n20_optional` is deliberately labeled optional. It may be cited as evidence only if technical validation passes, the minimum circuit count is met, and the relevant tangent estimator has already shown adequate convergence. A completed but imprecise `n=20` experiment is reported as imprecise rather than used to strengthen a claim.

No result up to `n=20` is described as an asymptotic proof.

## 14. Technical validity gates

The GitHub Actions workflow fails only for technical invalidity, never because a scientific effect has the wrong sign or magnitude. The validation step checks:

- every prescheduled job, tangent prefix, and readout order is present;
- at least 99% of requested tangents are regular in every reported cell;
- state normalization;
- horizontal tangent orthogonality;
- probability normalization;
- zero-sum probability tangents;
- `F_full <= F_Q` within numerical tolerance;
- the empirical covariance/projector deviation bound;
- finiteness of the primary numerical quantities.

If a technical check fails, the cause is fixed and the same prespecified seed/cell is rerun. The failing result is not silently removed.

## 15. Memory-bounded exact simulation

The rigorous-v2 engine supports `simulation_batch_size`. Tangent directions are propagated in deterministic batches to reduce peak memory. This is not a stochastic approximation: the circuit, parameter vector, architecture seed, and direction vectors are unchanged. The statevector is recomputed for each tangent batch and checked for numerical identity across batches.

Unit tests compare batched and unbatched propagation directly on small systems.

## 16. Reporting policy

All paper tables should report circuit-level point estimates, 95% confidence intervals, number of independent circuits, number of tangent directions, and the relevant quality flags. Family-specific results appear alongside any family-balanced generic aggregate.

All scheduled cells are retained in the raw artifacts. No cell is dropped because it weakens a narrative. Any analysis invented after inspecting rigorous-v2 outcomes is labeled exploratory and is not merged into the prespecified primary analysis.

A release used for a manuscript should archive the exact Git commit, profile JSON files, raw shard outputs, merged tables, numerical-validation report, inference-policy file, environment manifests, and figures under a persistent DOI.
