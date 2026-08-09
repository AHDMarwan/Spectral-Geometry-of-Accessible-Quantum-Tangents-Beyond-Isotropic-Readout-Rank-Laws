# Experiment design: falsification first

The numerical suite is designed to test the theory, not to manufacture agreement with it. A workflow is considered technically successful when the simulation and analysis complete and the numerical invariants pass. Scientific disagreement with the manuscript is **never** converted into a CI failure.

## Experimental unit and inference

A fixed random circuit instance is the independent experimental unit. Tangent directions sampled within one fixed circuit are repeated measurements of its local tangent ensemble and are never counted as independent circuits in confidence intervals. This avoids pseudoreplication.

For a fixed circuit, normalized visible scores are

\[
 u_v(z)=\frac{\dot p_v(z)}{\sqrt{p(z)F_{\rm full}(v)}}.
\]

The physical readout retention is computed as the squared projection onto the weighted, centered Pauli-Z feature span. The support and the numerical rank are recomputed for every circuit and measurement condition by SVD; the U(1) sector is therefore support-corrected rather than compared with the full Boolean cube.

## Estimators

`pairwise_purity` is the distinct-pair U-statistic for \(\mathrm{Tr}(C^2)\), hence unbiased for that second spectral moment. `deff_pairwise=1/pairwise_purity` is explicitly labeled a diagnostic because the reciprocal is not unbiased.

The suite also estimates \(\mathrm{Tr}(C^3)\) with the distinct-triple U-statistic

\[
\widehat{\mathrm{Tr}(C^3)}=
\frac{\operatorname{tr}(G^3)-3\sum_{ij}G_{ij}^2+2M}{M(M-1)(M-2)},
\]

where \(G_{ij}=u_i\cdot u_j\). This addresses the limitation of diagnosing anisotropy from a second moment alone.

Sample covariance eigenvalues are reported only as finite-sample spectra. Rank-r optimal recovery is additionally estimated out of sample with repeated train/test splits (`crossfit_kyfan`) to reduce the optimistic bias of an in-sample Ky Fan sum.

## Prespecified experiment families

1. **`reproduce_paper`** — exact protocol target for the manuscript: n=6,8,10, d=6n, 6 circuits for each generic family, 12 U(1) circuits, 48 Gaussian tangent directions. Results are compared with the reported table, but disagreement is reported rather than suppressed.
2. **`pra_core`** — larger independent replication with n=6,8,10,12; five nonconserving architectures plus U(1); more circuit seeds and tangent directions; second and third spectral moments; cross-fitted spectral recovery.
3. **`pra_depth`** — depth sweep d/n=0.5,1,2,4,6,8. This directly tests whether near-rank behavior is a deep-circuit phenomenon rather than an artifact of choosing d=6n.
4. **`pra_spectrum`** — high-M local spectral runs for n=8,10. This is the main check of compressibility beyond `d_eff`.
5. **`pra_orientation`** — at fixed measured covariance, compares the physical low-weight readout with Haar-random rank-matched score subspaces. This directly tests the relative-orientation statement behind the rank law.
6. **`pra_basis`** — repeats selected experiments in Z, X, Y, and independent random local measurement bases. This probes how much of the observed U(1) alignment is tied to the computational basis, as the theory predicts it may be.
7. **`pra_noise`** — exact independent readout bit-flip channels at eta=0,0.01,0.03,0.05. Because this is an exact stochastic channel on probabilities and probability tangents, it tests measurement noise without introducing a biased finite-shot Fisher estimator.
8. **`pra_directions`** — Gaussian, Rademacher, and coordinate parameter-direction ensembles. The goal is to test dependence on how the local tangent ensemble is sampled.
9. **`pra_large_n`** — selected n=12,14 runs for the Haar-U(4) generic family and U(1), intended as a finite-size extension only. No asymptotic exponent is inferred from these sizes alone.

## Negative and exact controls

The test suite compares the fast tensor simulator with a separate small-n explicit full-matrix implementation. It checks analytic probability tangents against centered finite differences, QFI contraction, horizontality, state norm, U(1) support conservation, expected readout ranks, gate unitarity, and the exact isotropic Beta projector law.

The relative-orientation experiment samples random rank-r projectors in the centered score space while holding the observed covariance fixed. Under the theorem, their mean retention must approach r/N for any fixed covariance. The physical projector can then be placed against that null distribution without assuming global isotropy.

## Statistical reporting

All main intervals are nonparametric bootstrap intervals over circuit instances. Generic pooled intervals are stratified by ansatz in the PRA analyses so that one architecture cannot dominate the resampling distribution. U(1)/generic effect ratios resample the two groups independently at the circuit level.

The repository reports all scheduled cells. There is no selection based on whether a cell supports the manuscript. Master seeds for the expanded PRA profiles differ from the reproduction seed to separate replication from reuse of the original random realization.

## What is deliberately not claimed

Finite-size runs do not establish asymptotic exponents. Cross-fitted finite-sample spectra do not reconstruct eigenvalues below the resolution set by the number of tangent samples. Exact Fisher-information simulations do not by themselves establish finite-shot optimizer performance. Those distinctions should remain explicit in the manuscript even if all numerical checks agree with the theory.
