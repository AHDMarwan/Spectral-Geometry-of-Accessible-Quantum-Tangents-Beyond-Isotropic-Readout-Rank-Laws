# Measurement-Accessible Quantum Tangent Geometry

**Rank Baselines and Spectral Orientation**

This repository contains the theory, frozen numerical protocols, archived results, figures, appendices, and production manuscript for:

**Marwan Ait Haddou, _Measurement-Accessible Quantum Tangent Geometry: Rank Baselines and Spectral Orientation_ (2026).**

- [Production manuscript PDF](paper/prx/spectral_geometry_prx.pdf)
- [LaTeX source](paper/prx/spectral_geometry_prx.tex)
- [Submission package](paper/prx/spectral_geometry_prx_submission_package.zip)
- [Rigorous-v2 protocol](docs/RIGOROUS_PROTOCOL_V2.md)
- [Citation/equation audit](paper/prx/CITATION_EQUATION_AUDIT.md)
- [Figure visual-QA checklist](paper/prx/FIGURE_VISUAL_QA_CHECKLIST.md)
- [Author ORCID](https://orcid.org/0009-0008-1734-1721)

## Core question

A fixed quantum measurement induces a classical score geometry. A restricted readout keeps only part of that already-measured information.

For a trace-one tangent-score covariance `C` in an `N`-dimensional centered score space and a rank-`r` readout projector `P`, the retained normalized tangent mass is

```text
R(P,C) = Tr(P C).
```

The rank-only random-orientation reference is `r/N`, so we define

```text
rho(P,C) = Tr(P C) / (r/N).
```

The central distinction of the paper is:

```text
rank fixes the baseline;
spectral orientation controls the actual accessible tangent information.
```

The project asks:

1. When is a physical low-weight readout close to the rank-only random-orientation reference?
2. Can `rho ≈ 1` coexist with a strongly anisotropic tangent covariance?
3. How much can equal-rank readouts differ when only their orientation changes?
4. Does an orientation advantage survive an operational fixed-shot comparison?
5. Why is the half-filled `U(1)` family structurally different from generic nonconserving families?

## Theory

For fixed `C` and a Haar-uniform rank-`r` projector on the real Grassmann manifold,

```text
E[rho] = 1,

Var(rho)
= 2 (N-r) (N Tr(C^2)-1)
  / [r (N-1)(N+2)]
<= 2 / (r d_eff),
```

where

```text
d_eff = 1 / Tr(C^2).
```

The concentration scale is controlled by `r d_eff`. Therefore rank-typical overlap does **not** require the covariance to approach the isotropic form `I/N`.

For full computational-basis support, cumulative diagonal Pauli-`Z` readout through weight `k` has rank

```text
r_k(n) = sum_{j=1}^k binom(n,j),
```

and the rank-only retained fraction is of order `n^k / 2^n` for fixed `k`.

The random-subspace identity itself is standard Grassmann geometry. The contribution of this project is the rank-controlled organization of measurement-induced VQC tangent scores, spectral orientation, equal-rank controls, and fixed-shot operational consequences.

## Main numerical results

### 1. Generic circuits can be rank-typical while remaining strongly anisotropic

Family-balanced one- and two-body readouts stay close to the rank reference over the tested generic sizes through `n = 16`. A targeted Haar-`U(4)` stress point at `n = 18` gives approximately

```text
rho_1 = 0.929   [0.910, 0.950]
rho_2 = 0.958   [0.952, 0.966]
```

At the same time the normalized covariance becomes strongly anisotropic. For the generic/Haar sequence,

```text
N Tr(C^2) ≈ 1.35  at n=6
N Tr(C^2) ≈ 6.17  at n=12
N Tr(C^2) ≈ 49.84 at n=16
N Tr(C^2) ≈ 146.8 at the Haar n=18 stress point
```

while `d_eff/N` falls sharply. This is the finite-size evidence behind the statement that **rank typicality is not isotropy**.

### 2. Architecture produces systematic orientation effects

Not every circuit family is close to the rank baseline. The `RY-RZ-CZ` family develops a persistent one-body deficit, while structured families can lie far above the rank reference.

The paper does not claim that finite-depth physical circuits converge to Haar orientation.

### 3. Equal rank does not imply equal accessibility

At fixed rank, physical low-weight, random-rank, cross-fitted aligned, and same-sample Ky-Fan subspaces can retain very different tangent mass.

Representative one-body retained masses include:

```text
Haar-U(4), n=12
physical      ≈ 2.71e-3
cross-fitted  ≈ 3.06e-2
Ky-Fan        ≈ 9.15e-2

U(1), n=12
physical      ≈ 0.292
cross-fitted  ≈ 0.375
Ky-Fan        ≈ 0.444
```

The same-sample Ky-Fan quantity is used only as an optimistic spectral benchmark. The cross-fitted subspace is learned on independent tangents and evaluated out of sample.

### 4. Orientation has an operational consequence at fixed rank and shot budget

The operational bridge keeps the **same circuit, computational-basis measurement, readout rank, and shot budget** and changes only the retained score-space orientation.

For Haar-`U(4)` circuits, aligned-to-physical directional gradient-energy gains are approximately

```text
n=8   2.96x
n=10  4.64x
n=12  9.58x
```

with finite-shot SNR gains approximately

```text
n=8   1.73x
n=10  2.13x
n=12  3.11x
```

Random equal-rank controls remain near the rank baseline. The `U(1)` family shows only modest additional gain because its physical low-weight readout is already comparatively well aligned.

These are controlled directional diagnostics, not a supervised barren-plateau theorem.

### 5. Half-filled `U(1)` circuits form a structured case study

For the half-filled `U(1)` family,

```text
N = binom(n, n/2) - 1
r_1 = n - 1
r_{<=2} = binom(n,2) - 1
```

The physical low-weight readout is strongly enhanced relative to the corresponding random-orientation rank scale. At `n = 18`, the physical retained fractions are approximately

```text
one-body: 0.215
two-body: 0.401
```

Cross-fitted overlap between the leading rank-`r_1` tangent subspace and cumulative low-weight Walsh spans remains substantial through `n = 18`:

```text
A_1(n=18)    = 0.283586  [0.277044, 0.290865]
A_{<=2}(n=18)= 0.463538  [0.457425, 0.469591]
```

Finite-size model comparison over `n = 8,...,18` favors a power model over a simple exponential model for both observables,

```text
A_1     ~ n^(-0.822)
A_{<=2} ~ n^(-0.704)
```

but the manuscript treats this strictly as **finite-size model discrimination**, not as an asymptotic scaling theorem or a hydrodynamic exponent.

### 6. Symmetry-breaking sensitivity control

A small verified pilot keeps the trainable parameter count fixed and inserts nontrainable perturbations after circuit layers:

```text
preserve_Z : RZ(epsilon * alpha)
break_X    : RX(epsilon * alpha)
```

At `n = 8`, a representative one-body alignment changes from roughly

```text
unperturbed       A_1 ≈ 0.517
preserve_Z, eps=.3    ≈ 0.481
break_X,    eps=.3    ≈ 0.0295
```

The control demonstrates sensitivity to charge breaking. It does not by itself identify the microscopic mechanism behind the `U(1)` alignment.

### 7. Readout-noise robustness

For Haar-`U(4)`, `n = 12`, the aligned-to-physical directional gradient-energy gain remains above unity under the tested bit-flip readout noise:

```text
clean  9.584
1%     6.919
3%     4.491
5%     3.127
```

The aligned subspace is re-estimated after noise is applied, so this is **not** a claim that one fixed optimized observable is itself noise-robust.

## Full-record Fisher information versus restricted accessibility

The computational-basis record itself retains a broadly comparable fraction of QFI across the tested generic/Haar and `U(1)` families, approximately `0.49` versus `0.47–0.48`, even though low-weight accessibility can differ by orders of magnitude.

This separates two questions:

```text
How informative is the full measurement record?
How much of that measured tangent geometry does the chosen readout retain?
```

The paper studies the second question.

## Appendices

The production manuscript includes a comprehensive appendix without changing the main narrative. It contains:

- score-space construction and Fisher normalization;
- a full derivation of the Grassmann first and second projector moments used for the variance formula;
- fixed-weight and fixed-charge readout-rank bookkeeping;
- cross-fitting, Ky-Fan, bootstrap, and statistical-unit details;
- operational gradient-energy and finite-shot signal definitions;
- additional effective-dimension and orientation diagnostics;
- readout-noise robustness plots;
- finite-size `U(1)` fit diagnostics;
- individual PennyLane circuit schematics and reproducibility conventions.

The main text contains only short pointers where a full derivation or protocol is deferred to the appendix.

## Frozen numerical and reporting policy

The fixed circuit instance is the independent statistical unit. Confidence intervals are bootstrapped over circuits, not over tangent vectors drawn from the same circuit. Generic aggregates weight ansatz families equally rather than weighting by circuit count.

Positive rank-law statements use the prespecified practical equivalence band

```text
rho in [0.90, 1.10]
```

and require the full 95% confidence interval to lie inside the band.

The tested finite sizes are not presented as proofs of asymptotic physical behavior. No scheduled cell is removed because it weakens a claim, and post-outcome analyses are identified as exploratory or diagnostic where appropriate.

## Repository map

```text
paper/prx/                         production manuscript, appendices, figures, source package
paper/prx/data/                    paper-facing archived tables
paper/prx/figure_scripts/          deterministic publication and appendix figure generation
src/aqt/                           experiment and analysis code
profiles/                          frozen experiment profiles
docs/RIGOROUS_PROTOCOL_V2.md       confirmatory protocol and inference rules
results/rigorous-v2_primary/       primary family-balanced campaign
results/rigorous-v2_large_n/       n=14,16 finite-size extension
results/rigorous-v2_n18/           targeted n=18 generic/Haar stress test
results/u1_alignment_scaling_v1/   half-filled U(1) alignment scaling through n=18
.github/workflows/                 manuscript production and numerical workflows
```

## Paper-production workflow

The manuscript production workflow regenerates publication figures, appendix figures, PennyLane circuit diagrams, compiles the manuscript, checks citations and appendix cross-references, validates author/ORCID formatting, and promotes the resulting rewrite to the canonical PDF/source files.

The workflow also checks that figure legends are rendered below plots rather than over the data.

## Reproducing local checks

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

The GitHub Actions workflows reproduce the manuscript build and frozen numerical pipelines. Scientific outcomes do not determine CI success; CI gates technical validity, provenance, normalization, manuscript consistency, and other prespecified invariants.

## Relation to the preceding isotropic-rank manuscript

This paper is a direct continuation of an earlier manuscript:

**Marwan Ait Haddou, _Readout-Rank Laws for Isotropic Quantum Tangents_ (2026), submitted to arXiv; identifier pending.**

The earlier work derives exact rank laws under joint state-tangent isotropy. The present paper starts where that assumption stops being sufficient: it keeps the measurement fixed, allows an arbitrary anisotropic tangent covariance, and studies the spectral orientation of equal-rank readout subspaces.

In short:

```text
Paper I: under isotropy, rank is enough.
Paper II: beyond isotropy, rank is the baseline and orientation determines the deviation.
```

## Citation

If you use the manuscript, theory, figures, numerical data, or code from this repository, please cite:

```bibtex
@misc{AitHaddou2026MeasurementAccessible,
  author       = {Marwan Ait Haddou},
  title        = {Measurement-Accessible Quantum Tangent Geometry: Rank Baselines and Spectral Orientation},
  year         = {2026},
  howpublished = {Manuscript and reproducibility repository},
  url          = {https://github.com/AHDMarwan/Spectral-Geometry-of-Accessible-Quantum-Tangents-Beyond-Isotropic-Readout-Rank-Laws}
}
```

Until an archival preprint identifier or journal DOI is available, the repository URL is the stable public reference.

GitHub also reads [`CITATION.cff`](CITATION.cff) through the repository's **Cite this repository** interface.

## Author

**Marwan Ait Haddou** — Independent Researcher  
[ORCID](https://orcid.org/0009-0008-1734-1721) · [Email](mailto:aithaddou.marwan@outlook.com)
