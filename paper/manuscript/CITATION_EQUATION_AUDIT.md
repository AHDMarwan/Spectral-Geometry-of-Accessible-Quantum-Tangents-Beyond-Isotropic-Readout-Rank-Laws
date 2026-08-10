# Citation and equation audit — production rewrite

Date: 2026-08-10

Scope: `paper/manuscript/spectral_geometry_rewrite.tex` on branch `paper-rewrite-rank-orientation`.

Principle used in this audit:

- A **definition introduced in this paper** does not require a priority citation, but nearby prose must distinguish it from established ingredients.
- A **standard theorem/identity** requires a source and must not be framed as original.
- A **paper-derived numerical value** should point to the corresponding figure/table/result archive, not to external literature.
- A **mechanistic interpretation** requires either direct evidence in this paper or explicit presentation as an unresolved hypothesis supported by prior literature.
- The hostile novelty audits are treated only as search leads. Bibliographic claims are accepted here only after checking a primary or publisher source.

## A. Equation-by-equation audit

| Manuscript object | Status | Required action/source |
|---|---|---|
| `p_theta(x)` as the outcome distribution of a fixed measurement | standard setup | Cite Braunstein–Caves (1994) or a standard quantum-estimation reference when connecting probability derivatives to Fisher information. |
| normalized score vector `u_v` | paper-specific representation | Definition used here; no priority claim. Methods must specify the exact normalization and regularity/probability-floor convention. |
| `C = E_v[u_v u_v^T]`, `C >= 0`, `Tr C = 1` | definition + immediate algebra | No external priority claim. Explain that this is a covariance/second-moment construction over normalized measurement-score tangents. |
| `d_eff = 1/Tr(C^2)` | standard participation-ratio/effective-rank form | Present as a standard participation-ratio style effective dimension, not as a new definition of effective dimension in general. A generic effective-rank/participation-ratio citation may be added, though the formula is elementary. |
| `N Tr(C^2) = N/d_eff` | algebraic identity | No citation needed beyond the definition. |
| `r = Tr P` for an orthogonal projector | standard linear algebra | No citation needed. |
| `E_v ||P u_v||^2 = Tr(PC)` | direct derivation from the paper's definitions | Derive explicitly, as currently done. Do **not** claim the abstract trace-overlap functional itself is novel. Cite Fernandez et al. (TMLR 2025 / arXiv:2504.14701) in the surrounding prior-art paragraph as a classical use of Grassmannian subspace overlap. |
| `E_P P = (r/N) I` under Haar/Grassmann orientation | standard invariant-integration identity | Cite Collins–Matsumoto (2017) / Bendokat–Zimmermann–Absil (2024), and Fernandez et al. (2025) as a directly relevant overlap baseline in classical ML. |
| `E_P Tr(PC) = r/N` and `E rho = 1` | standard consequence | Must be called a **rank-only random-orientation reference**, not a new theorem. Cite the sources above. |
| exact `Var_P(rho | C)` formula | standard Grassmann second moment specialized to this covariance | Keep the derivation in an appendix, but cite invariant-integration/Grassmann projector moments. Phrase as “using standard Grassmann projector moments, we obtain…”. |
| `Var(rho) <= 2/(r d_eff)` | paper's elementary corollary of the exact moment | Derive in text/appendix. No separate external priority claim. |
| Chebyshev tail bound | standard probability inequality | Cite Chebyshev only if desired; not necessary in a physics manuscript if derivation is one line, but do not call it a new concentration theorem. Prefer “Chebyshev consequence” rather than “concentration theorem”. |
| `N_n = 2^n - 1` for the centered full computational-basis score space | combinatorial dimension | No citation needed; explicitly state the full-support assumption. |
| `r_k = sum_{j=1}^k binom(n,j)` for diagonal Z strings through weight k | combinatorial/Pauli-Walsh basis fact | No citation strictly required; methods should state independence/rank is evaluated numerically in symmetry-reduced support. |
| `E R_k = r_k/(2^n-1) = O(n^k/2^n)` | consequence of the random-orientation null | Cite the Grassmann baseline where introduced and repeat that this is not a physical-Haar-convergence claim. |
| `max_rank(P)=r Tr(PC) = sum_{j<=r} lambda_j(C)` | Ky Fan variational principle | Cite Ky Fan (PNAS 1949). Explicitly state this optimization theorem is standard. |
| cross-fitted leading subspace | paper-specific estimator/protocol | No external theorem required. Explain independence of alignment and evaluation tangent sets to avoid same-sample optimism. |
| full-record CFI bounded by QFI | standard quantum-estimation inequality | Cite Braunstein–Caves (1994). |
| gradient-energy and finite-shot SNR formulas | paper-specific operational bridge built from standard multinomial sampling | Derive fully in Methods/Appendix. Cite standard multinomial/Fisher facts only where needed. Do not call the resulting quantity a supervised-loss barren-plateau metric. |
| `A_k = Tr(P_{<=k} P_top)/r_1` | paper-specific diagnostic | Definition here. Relate it explicitly to general subspace-overlap/Grassmann metrics (Fernandez et al. 2025) and do not claim subspace overlap itself is new. |
| finite-size power/exponential fits | empirical model comparison | Cite no physical law. Report AICc/LOOCV as model-selection diagnostics and state they are not asymptotic theorems or hydrodynamic exponents. |

## B. Claim-by-claim citation audit

### 1. Measurement contraction and state-space versus accessible geometry

**Claim:** QFI/QGT characterize state sensitivity before a measurement is fixed; a fixed measurement yields a classical Fisher geometry, and restrictions to observables/features can reduce accessible information.

**Sources already in the manuscript:**

- S. L. Braunstein and C. M. Caves, Phys. Rev. Lett. 72, 3439 (1994), DOI 10.1103/PhysRevLett.72.3439.
- M. Hotta and M. Ozawa, Phys. Rev. A 70, 022327 (2004), DOI 10.1103/PhysRevA.70.022327.
- X.-M. Lu, S. Luo, and C. H. Oh, Phys. Rev. A 86, 022342 (2012), DOI 10.1103/PhysRevA.86.022342.

**Status:** supported. Keep these citations close to the claim.

### 2. Random measurements as a neighboring but distinct problem

**Claim:** Recent work averages the **measurement basis itself** and obtains an average CFIM related to the QFIM, with variance/concentration results.

**Verified source:**

- Jianfeng Lu and Kecen Sha, “Quantum Fisher information matrix via its classical counterpart from random measurements,” arXiv:2509.08196 (2025; current arXiv version in 2026). The paper states for pure states that Haar averaging over measurement bases gives `E_U F^U = Q/2`, and develops variance and concentration bounds.

**Required distinction in our paper:** Lu–Sha randomize the full quantum measurement basis. We keep the quantum measurement fixed and use random orientation only as a null model for a rank-restricted readout subspace **inside the induced classical score space**.

### 3. `Tr(PC)` / Grassmann overlap is not abstractly novel

**Claim:** A trace overlap between projectors/subspaces, together with a chance-level random overlap baseline, exists outside quantum tangent geometry.

**Verified source:**

- Andres Fernandez, Frank Schneider, Maren Mahsereci, Philipp Hennig, “Connecting Parameter Magnitudes and Hessian Eigenspaces at Scale using Sketched Methods,” TMLR (2025), arXiv:2504.14701. The paper explicitly develops Grassmannian overlap between parameter masks and Hessian eigenspaces and compares it with chance-level overlap.

**Required wording:** Our contribution is the VQC measurement-score application and controlled fixed-rank operational comparison, not invention of Grassmannian overlap or the `r/N` identity.

### 4. Observable locality / trainability is established prior art

**Claim:** Observable locality and circuit structure can strongly affect gradient concentration/trainability.

**Sources:**

- M. Cerezo et al., Nat. Commun. 12, 1791 (2021), DOI 10.1038/s41467-021-21728-w.
- A. Uvarov and J. Biamonte, J. Phys. A 54, 245301 (2021), DOI 10.1088/1751-8121/abfac7.
- M. Larocca et al., Quantum 6, 824 (2022), DOI 10.22331/q-2022-09-29-824.
- Enrico Fontana et al., “Characterizing barren plateaus in quantum ansätze with the adjoint representation,” Nat. Commun. 15, 7171 (2024), DOI 10.1038/s41467-024-49910-w.
- Michael Ragone et al., “A Lie algebraic theory of barren plateaus for deep parameterized quantum circuits,” Nat. Commun. 15, 7172 (2024), DOI 10.1038/s41467-024-49909-3.

**Required wording:** Do not claim that “which observable is measured matters for trainability” is new. The fixed-rank orientation-controlled diagnostic and its finite-shot consequence are the narrower contribution.

### 5. Hamming-weight/U(1)-preserving circuit trainability is established prior art

**Verified source:**

- Léo Monbroussou, Eliott Z. Mamon, Jonas Landman, Alex B. Grilo, Romain Kukla, Elham Kashefi, “Trainability and Expressivity of Hamming-Weight Preserving Quantum Circuits for Machine Learning,” Quantum 9, 1745 (2025), DOI 10.22331/q-2025-05-15-1745, arXiv:2309.15547. It analyzes controllability/QFIM rank and gradient-variance bounds in fixed-Hamming-weight subspaces.

**Required wording:** Our U(1) result is a structured case study of low-weight tangent orientation, not a first demonstration that Hamming-weight-preserving circuits have distinct trainability properties.

### 6. Symmetric low-dimensional trainable subspaces and classical simulability

**Verified source:**

- M. Cerezo et al., “Does provable absence of barren plateaus imply classical simulability? Or, why we need to rethink variational quantum computing,” arXiv:2312.09121; published Nature Communications 16, 7907 (2025).

**Required wording:** Use only for the broad point that trainability-protecting structure can confine the model to smaller subspaces and has implications beyond a bare “symmetry helps” narrative.

### 7. Closest U(1)-equivariant/readout-visible trainability prior art

**Verified source:**

- Hassan Ugail and Newton Howard, “A Coherence Law for Trainability in Noisy Equivariant Quantum Neural Networks,” arXiv:2606.30688 (2026). The paper studies U(1)-equivariant brickwork circuits, a sector-restricted readout/light-cone structure, and a **readout-visible aligned coherence rate** under noise.

**Required wording:** This is the closest phenomenon-level neighbor. Our paper must explicitly say that the mathematics and setting differ: their functional is a noise/coherence Rayleigh-quotient-type diagnostic for gradient decay, whereas ours is the noiseless measurement-score covariance overlap `Tr(PC)` plus equal-rank physical/random/aligned comparisons. Therefore the U(1) phenomenon itself is not a novelty pillar.

### 8. Generic structural restriction can concentrate information in low-bodyness observables

**Verified source:**

- Pablo Bermejo, Paolo Braccia, Manuel S. Rudolph, Zoë Holmes, Lukasz Cincio, M. Cerezo, “Quantum Convolutional Neural Networks are Effectively Classically Simulable,” PRX Quantum 7, 020304 (2026), DOI 10.1103/8qt9-72ts, arXiv:2408.12739. The published abstract states that randomly initialized QCNNs can operate only on information encoded in low-bodyness measurements of the input states.

**Required wording:** Do not present “structured architecture -> low-weight information concentration” as a new phenomenon class. Our circuit family, metric, and equal-rank orientation control are different.

### 9. U(1) operator hydrodynamics is a plausible mechanism, not an established explanation of our statistic

**Sources to cite in Discussion/Outlook:**

- V. Khemani, A. Vishwanath, and D. A. Huse, Phys. Rev. X 8, 031057 (2018).
- T. Rakovszky, F. Pollmann, and C. W. von Keyserlingk, Phys. Rev. X 8, 031058 (2018).

**Required wording:** These works establish slow/diffusive structures associated with conserved densities in U(1)-conserving random circuits, but they do not study our VQC tangent-score covariance or `A_k`. Hydrodynamics remains a candidate mechanism for a future project, not a causal conclusion of this paper.

### 10. Fixed-charge/slice harmonic geometry is another unresolved null mechanism

**Source lead requiring final bibliographic insertion:**

- Yuval Filmus, “An orthogonal basis for functions over a slice of the Boolean hypercube,” Electron. J. Combin. 23(1), P1.23 (2016), plus related harmonic-analysis-on-slices literature.

**Required wording:** At half filling, the outcome support is a fixed-Hamming-weight slice. Low-degree harmonic/Johnson structure can create low-weight organization independent of the circuit dynamics. Mention this as an alternative structural explanation; do not equate the physical probability-weighted projector in our calculation with the uniform Johnson projector unless justified.

### 11. QFI spectral orientation in another application is only conceptual overlap

**Verified source:**

- Justice Owusu Agyemang, Jerry John Kponyo, Elliot Amponsah, Godfred Manu Addo Boakye, “Optimal Quantum Differential Privacy via Fisher Information Spectral Analysis,” arXiv:2605.24166 (2026).

**Status:** optional citation. It is an emerging preprint in a different application; it may be cited in a “related spectral viewpoint” sentence, but it is not needed to support any core derivation.

## C. Numerical claims and required internal evidence links

These are manuscript claims that need **result-archive/figure provenance**, not external citations.

1. Generic one-/two-body rank typicality through `n=16` and targeted Haar-U4 stress point at `n=18` -> cite/point to archived rigorous-v2 tables and Fig. 7.
2. Strong covariance anisotropy (`N Tr(C^2)` growth and `d_eff/N` decrease) -> archived anisotropy table and Fig. 7.
3. RY-RZ-CZ one-body deficit -> family-resolved archive and Fig. 8.
4. Haar-U4 same-rank physical vs cross-fit vs same-sample Ky Fan retention -> spectral profile and Fig. 9.
5. Fixed-rank gradient-energy and finite-shot SNR gains -> `results/trainability_bridge_v1` (or final consolidated path) and Fig. 10.
6. Noise robustness -> `results/trainability_bridge_robustness_v1` and Fig. 11, with the explicit caveat that the aligned subspace is re-estimated after noise.
7. U(1) alignment scaling through `n=18` -> `results/u1_alignment_scaling_v1`. Final values: `A_1(18)=0.283586 [0.277044,0.290865]`, `A_{<=2}(18)=0.463538 [0.457425,0.469591]`, 20 circuit instances.
8. U(1) finite-size model discrimination -> `results/u1_alignment_scaling_v1/fits.csv` / `SUMMARY.md`. Main-window exponents: one-body `alpha=0.8223 [0.7694,0.8735]`, weight<=2 `alpha=0.7041 [0.6798,0.7281]`; positive `Delta AICc(exp-power)` favors power over exponential in the tested range. Explicitly not asymptotic.
9. Symmetry-breaking pilot -> must be re-verified directly from archived raw CSV before production insertion. Until verified, mark as pilot and avoid causal wording.

## D. Manuscript wording changes mandated by the audit

### Replace/avoid

- “We prove a new random-orientation theorem …”
- “The `r/N` law is a new rank law …”
- “U(1) symmetry creates the observed low-weight alignment …”
- “The observed finite-size power law demonstrates diffusion/hydrodynamics …”
- “This shows U(1) circuits are more trainable …”
- “The top-r subspace optimality is new …”
- “Low-weight information concentration in structured circuits is a new phenomenon …”

### Preferred language

- “Using standard Grassmann projector moments, we use `r/N` as a rank-only random-orientation reference.”
- “Our contribution is the rank-controlled application to a fixed measurement-induced VQC tangent-score geometry and the equal-rank operational comparison.”
- “Rank typicality is compatible with strong anisotropy because the random-orientation width depends on `r d_eff`, not on `d_eff/N` approaching one.”
- “The U(1) data provide a structured case study; several mechanisms from symmetry, fixed-charge geometry, readout compatibility, and operator hydrodynamics remain plausible.”
- “The finite-size data favor a power-law fit over an exponential fit on the tested sizes; no asymptotic exponent is claimed.”

## E. References that must be added to the production bibliography

Mandatory new references beyond the original manuscript bibliography:

1. Fernandez, Schneider, Mahsereci, Hennig — TMLR 2025 / arXiv:2504.14701.
2. Lu and Sha — arXiv:2509.08196.
3. Fontana et al. — Nat. Commun. 15, 7171 (2024), DOI 10.1038/s41467-024-49910-w.
4. Ragone et al. — Nat. Commun. 15, 7172 (2024), DOI 10.1038/s41467-024-49909-3.
5. Monbroussou et al. — Quantum 9, 1745 (2025), DOI 10.22331/q-2025-05-15-1745.
6. Cerezo et al. — Nat. Commun. 16, 7907 (2025) / arXiv:2312.09121.
7. Ugail and Howard — arXiv:2606.30688.
8. Bermejo et al. — PRX Quantum 7, 020304 (2026), DOI 10.1103/8qt9-72ts.
9. Khemani, Vishwanath, Huse — PRX 8, 031057 (2018).
10. Rakovszky, Pollmann, von Keyserlingk — PRX 8, 031058 (2018).
11. Filmus — Electron. J. Combin. 23(1), P1.23 (2016) (verify DOI/URL before final bibliography freeze).

Optional/emerging:

12. Agyemang et al. — arXiv:2605.24166, only if a spectral-viewpoint comparison is retained.

## F. Audit conclusion

The rewrite can be made citation-complete without weakening the central result. The bibliography must make three things explicit to a referee:

1. Grassmann overlap and the `r/N` mean are known mathematics.
2. Observable/symmetry-dependent trainability and low-bodyness structure are known physical phenomena.
3. The paper's narrower contribution is the fixed-measurement, fixed-rank tangent-score accessibility framework, together with controlled equal-rank physical/random/cross-fit comparisons and their finite-shot operational consequences.
