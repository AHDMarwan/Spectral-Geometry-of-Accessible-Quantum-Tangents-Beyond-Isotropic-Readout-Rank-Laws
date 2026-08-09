# Claim-to-test matrix

| Claim or theoretical object | Primary numerical test | Failure mode that would count against the claim |
|---|---|---|
| Measurement/readout accessibility is a contraction | Finite-difference checks; every regular tangent satisfies F_full <= F_Q | Persistent violations beyond numerical tolerance |
| Rank law is a relative-orientation statement | `pra_orientation`: Haar-random rank-matched score subspaces at fixed C | Random-subspace mean systematically differs from r/N |
| Physical generic low-weight readouts become rank-typical when deep | `pra_core` + `pra_depth`, separately by architecture | Stable order-one deviation from rho=1 at large depth across generic families |
| U(1) tangent geometry remains preferentially low-weight aligned in the computational basis | `pra_core`, `pra_orientation` | U(1) physical readout sits within ordinary random-orientation fluctuations or enhancement does not grow over tested sizes |
| Spectral concentration and readout alignment are different notions | `pra_spectrum`: pairwise purity, Tr(C^3), cross-fitted Ky Fan, physical retention | Physical retention cannot be separated from spectral compressibility, or generic covariance becomes indistinguishable from flat within estimator resolution |
| Isotropic corollary gives Beta rank-projector law | `aqt controls` and `test_isotropic_law.py` | Distributional/moment disagreement beyond Monte Carlo error |
| Support correction is essential in the U(1) sector | rank tests and per-circuit SVD on actual support | Numerical rank disagrees with support constraints or results rely on full-cube rank |
| Main phenomenon is not a single-ansatz accident | five generic nonconserving families in `pra_core` | One or more generic architectures show persistent U(1)-like enhancement |
| Tangent-ensemble choice is not silently determining the result | `pra_directions` | Qualitative conclusion reverses across Gaussian/Rademacher/coordinate ensembles |
| Measurement architecture matters as predicted by the framework | `pra_basis`, `pra_noise` | Results remain claimed universal despite strong basis/channel dependence |
