# Independent reproduction status

Before relying on the GitHub Actions campaign, the rebuilt implementation was checked locally against the manuscript protocol using the exact RNG convention recovered from the supplied confirmatory notebook: each fixed circuit uses `stable_seed(job_id)`; the same NumPy generator draws the parameter vector first and the Gaussian tangent directions second; fixed Haar-U(4) architecture gates use `stable_seed(job_id + "|arch")`.

The full unit suite currently contains 18 tests and passes locally. It includes an independent explicit full-matrix small-n simulator, analytic-versus-finite-difference tangent checks, state normalization/horizontality, Fisher contraction, U(1) support conservation, support-correct readout ranks, isotropic spectral moments, the Haar random-subspace rank law, readout-noise normalization, and the empirical covariance deviation bound.

`independent_reproduction_n6_n8.csv` records the local rerun for n=6 and n=8. All reported point estimates are recovered to the rounding precision of the manuscript table. This was a reproduction check, not a fitted calculation: no parameters were tuned to reduce those differences.

The n=10 cell and the expanded robustness profiles are intentionally delegated to the sharded GitHub Actions workflow because they exceed the short local execution budget available during the repository rebuild. The workflow always writes discrepancies; scientific disagreement does not cause a CI failure or result deletion.
