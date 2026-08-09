# Measurement-Accessible Quantum Tangent Geometry

**Rank Typicality Without Isotropy**

This repository contains the theory, frozen numerical protocols, data products, figures, and manuscript for:

**Marwan Ait Haddou, _Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy_ (2026).**

- [Manuscript PDF](paper/prx/spectral_geometry_prx.pdf)
- [LaTeX source](paper/prx/spectral_geometry_prx.tex)
- [Rigorous-v2 protocol](docs/RIGOROUS_PROTOCOL_V2.md)
- [Author ORCID](https://orcid.org/0009-0008-1734-1721)

## The question

Variational quantum circuits are trained through measurements. A circuit may have a large and highly structured tangent space, but an optimizer only sees the part of that geometry that is visible through the chosen readout.

For a trace-one tangent-score covariance `C` in an `N`-dimensional centered score space and a rank-`r` readout projector `P`, the retained tangent information is

```text
Tr(P C).
```

The rank-only reference is `r/N`. We therefore study

```text
rho = Tr(P C) / (r/N).
```

The project asks:

1. When is a physical low-weight readout close to the rank-only reference?
2. Does `rho ≈ 1` require an isotropic tangent covariance?
3. How do architecture and symmetry change the overlap between tangent information and the readout?
4. If a physical readout captures little information, is that information absent, or merely oriented outside the measured subspace?

## What we did

The work combines an analytic random-orientation result with frozen finite-size numerical tests.

### Random-orientation theory

For a fixed covariance `C` and an independent Haar/Grassmann rank-`r` real projector `P`, the rank-normalized overlap obeys

```text
E[rho] = 1,

Var(rho)
= 2 (N-r) (N Tr(C^2)-1)
  / [r (N-1)(N+2)]
<= 2 / (r d_eff),
```

with

```text
d_eff = 1 / Tr(C^2).
```

The concentration scale is therefore controlled by `r d_eff`. It does not require `C` to approach the isotropic covariance `I/N`.

For full computational-basis score space and a fixed-weight `k` readout,

```text
r_k(n) = sum_{j=1}^k binom(n,j),
```

so the random-orientation model gives rank-normalized overlap approaching one while the retained fraction itself is only of order `n^k / 2^n` for fixed `k`.

### Frozen numerical campaign

The main experiment suite is `rigorous-v2`. Seeds, inference rules, the independent statistical unit, convergence checks, and the positive equivalence criterion were fixed before the corresponding outcomes were inspected.

The campaign includes:

- several nonconserving variational-circuit families;
- a half-filled `U(1)`-symmetric family;
- one- and two-body diagonal readouts;
- circuit-level bootstrap confidence intervals with equal weighting across generic ansatz families;
- nested tangent counts `M = 32, 64, 128, 256`;
- explicit Haar/Grassmann orientation calibration;
- measurement-basis and tangent-direction robustness tests;
- dedicated spectral runs with empirical eigenvalue profiles, Ky-Fan bounds, and cross-fitted rank-matched subspaces;
- family-balanced finite-size tests through `n = 16` and a targeted Haar-`U(4)` stress test at `n = 18`.

The finite-size simulations are not used as an asymptotic proof for the physical circuit ensembles.

## What we found

### Generic circuits are practically rank-typical without becoming isotropic

For the family-balanced generic ensemble, one- and two-body readouts remain within the prespecified practical rank-equivalence band through the tested family-balanced sizes. The targeted Haar-`U(4)` stress test at `n = 18` also remains in that band, with approximately

```text
rho_1 = 0.929
rho_2 = 0.958.
```

At the same time, the tangent covariance becomes increasingly anisotropic: `N Tr(C^2)` grows while `d_eff/N` decreases.

So practical rank typicality and global isotropy are different statements.

### Architecture produces systematic departures from the rank reference

The `RY-RZ-CZ` family develops a persistent one-body deficit. At the larger tested sizes, `rho_1` remains below the prespecified `0.90` equivalence boundary.

The data establish an architecture-dependent orientation bias. They do not, by themselves, identify a unique microscopic gate-level cause.

### Symmetry can strongly align tangent information with simple observables

The half-filled `U(1)` family occupies a different regime. Its low-weight readouts retain far more tangent information than the corresponding rank-only reference. At `n = 18`, the measured retained fractions are approximately

```text
one-body: 0.215
two-body: 0.401.
```

For the symmetry-reduced `U(1)` rows, the analysis uses the actual archived score dimension and readout rank. The full-support binomial rank formula is not applied to those rows.

### The spectral calculation shows where inaccessible information can reside

For generic circuits, the physical low-weight readout can retain much less tangent mass than a rank-matched leading spectral subspace. Cross-fitted spectral subspaces also outperform the physical low-weight observables.

This means that a small accessible fraction does not necessarily imply that tangent information disappeared. It can still be present in the state-space geometry but oriented away from the chosen measurement span.

For the `U(1)` family, the gap between the physical readout and the leading rank-matched spectral directions is much smaller, consistent with symmetry-induced alignment.

## Main conclusion

A compact summary of the results is:

```text
readout rank sets the baseline;
tangent spectrum and relative orientation set the deviation from that baseline.
```

For QML, the practical implication is that state-space geometry and measurement-accessible geometry should be treated separately. A measurement interface can be an information bottleneck even when substantial tangent structure remains in the quantum state. This motivates ansatz-readout co-design rather than evaluating an ansatz independently of the observables used to train or read it out.

This work does **not** claim a barren-plateau theorem for a supervised loss. In particular, no asymptotic scaling law for `Var(partial_theta L)` is inferred from the tangent-score calculations.

## Repository map

```text
paper/prx/                         manuscript, appendices, vector figures, source package
src/aqt/                           experiment and analysis code
profiles/                          frozen experiment profiles
docs/RIGOROUS_PROTOCOL_V2.md       confirmatory protocol and inference rules
results/rigorous-v2_primary/       primary family-balanced campaign
results/rigorous-v2_large_n/       n=14,16 finite-size extension
results/rigorous-v2_n18/           targeted n=18 stress test
results/exploratory_asymptotic_bridge/
                                   post-hoc population-orientation bridge diagnostics
.github/workflows/                 reproducible CI and experiment workflows
```

## Reproducing the local checks

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

The GitHub Actions workflows reproduce the manuscript build and the frozen numerical pipelines. Scientific outcomes do not cause CI failure; CI gates technical validity, provenance, normalization, and other prespecified invariants.

## Statistical and reporting policy

The fixed circuit instance is the independent statistical unit. Confidence intervals are bootstrapped over circuits. Generic aggregates weight ansatz families equally rather than weighting by circuit count.

Positive rank-law claims use the prespecified equivalence band

```text
rho in [0.90, 1.10]
```

and require the full 95% confidence interval to lie inside the band.

No scheduled cell is removed because it weakens a claim. Post-outcome analyses are labeled exploratory, and the tested finite sizes are not presented as proofs of physical asymptotic behavior.

## Citation

If you use the manuscript, theory, figures, numerical data, or code from this repository, please cite the work below. Until a journal DOI or archival preprint identifier is assigned, use the repository URL.

```bibtex
@misc{AitHaddou2026MeasurementAccessible,
  author       = {Marwan Ait Haddou},
  title        = {Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy},
  year         = {2026},
  howpublished = {Manuscript and reproducibility repository},
  url          = {https://github.com/AHDMarwan/Spectral-Geometry-of-Accessible-Quantum-Tangents-Beyond-Isotropic-Readout-Rank-Laws},
  note         = {ORCID: 0009-0008-1734-1721}
}
```

GitHub also reads [`CITATION.cff`](CITATION.cff), so the repository's **Cite this repository** interface provides the same preferred citation.

## Author

**Marwan Ait Haddou** — Independent Researcher  
ORCID: [0009-0008-1734-1721](https://orcid.org/0009-0008-1734-1721)
