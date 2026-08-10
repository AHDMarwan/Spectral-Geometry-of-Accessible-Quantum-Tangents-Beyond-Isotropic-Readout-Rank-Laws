# Research and Manuscript Development Track

This file records how the project evolved: what was attempted, what worked, what failed, which hypotheses survived, which ideas were abandoned, and why the present paper has the scope it does.

It is intentionally more candid than the manuscript. The paper presents the final scientific argument; this file preserves the development history and the negative results that shaped it.

Last updated: 2026-08-10.

---

## 1. Starting point: isotropic readout-rank laws

The project grew out of an earlier manuscript, **Readout-Rank Laws for Isotropic Quantum Tangents**.

That earlier work established a two-stage information hierarchy

\[
F_Q \longrightarrow F_{\rm full} \longrightarrow I_{\mathcal A},
\]

and, under a joint Haar/isotropic state--tangent model, exact finite-size laws for the fraction of information surviving the measurement and readout restrictions. In particular, the isotropic readout fraction has mean \(r/N\), and fixed-weight readout therefore retains only a polynomial-over-exponential fraction of the full score space.

The important limitation was already visible there: the rank law is exact only after sufficient isotropization. The half-filled \(U(1)\) family was a strong violation of the support-corrected isotropic prediction, indicating that **orientation** remained important.

That observation became the seed of the present project.

### What survived from the first paper

- The score-space viewpoint.
- The readout projector interpretation.
- The rank fraction \(r/N\) as the correct dimension-only baseline.
- The distinction between full-record Fisher information and restricted readout accessibility.
- The observation that \(U(1)\) circuits can strongly violate an isotropic rank prediction.

### What had to be changed

The new paper could not simply repeat the isotropic law. The central question became:

> If the measurement is fixed and the readout rank is fixed, what determines the actual fraction of tangent information retained when the tangent covariance is anisotropic?

This changed the project from an isotropic-rank paper into a **spectral-orientation paper**.

---

## 2. Core reformulation: covariance plus readout projector

The present framework was built around a normalized tangent-score covariance

\[
C\succeq0,\qquad \operatorname{Tr} C=1,
\]

and a rank-\(r\) readout projector \(P\).

The retained tangent mass is

\[
R(P,C)=\operatorname{Tr}(PC),
\]

and the rank-normalized quantity is

\[
\rho(P,C)=\frac{\operatorname{Tr}(PC)}{r/N}.
\]

This formulation separated three ingredients that had previously been conflated:

1. **rank** fixes the mean random-orientation accessibility scale;
2. the **spectrum of \(C\)** controls the width of random-orientation fluctuations;
3. the **relative orientation of \(P\)** and the eigenspaces of \(C\) determines the actual retained mass.

The working slogan became:

> **Rank fixes the baseline; spectral orientation controls actual accessible tangent information.**

This eventually became the organizing principle of the paper.

---

## 3. Theoretical result that worked

For a fixed trace-one covariance \(C\) and a Haar/Grassmann random rank-\(r\) projector,

\[
\mathbb E\rho=1,
\]

and

\[
\operatorname{Var}(\rho)
=
\frac{2(N-r)\left[N\operatorname{Tr}(C^2)-1\right]}
{r(N-1)(N+2)}.
\]

With

\[
d_{\rm eff}=\frac1{\operatorname{Tr}(C^2)},
\]

this yields

\[
\operatorname{Var}(\rho)\le \frac{2}{r d_{\rm eff}}.
\]

### What this clarified

A covariance does **not** have to become isotropic for \(\rho\) to concentrate near one. It is enough for the product \(r d_{\rm eff}\) to be large.

This was the key conceptual separation:

> **rank typicality is not isotropy.**

The numerical campaign was then redesigned to test exactly that statement.

### What is not claimed as new

The Grassmann expectation \(r/N\), projector moments, and Ky Fan optimality are standard mathematics. The novelty claim is not the identity itself. The contribution is the way these tools are organized around fixed-measurement VQC tangent scores, together with physical, random, and aligned equal-rank controls and an operational fixed-shot comparison.

---

## 4. Generic-circuit campaign: the first major success

A family-balanced campaign was run on several nonconserving variational circuit architectures using computational-basis measurement and low-weight diagonal \(Z\) readout.

The main result was that one- and two-body readouts remained close to the random rank reference through the tested sizes, even while the tangent covariance became strongly anisotropic.

Representative generic/Haar results included:

- one-body \(\rho\) near the rank baseline;
- two-body \(\rho\) even closer to the rank baseline;
- a targeted Haar-\(U(4)\) stress point at \(n=18\):
  - \(\rho_1\approx0.929\),
  - \(\rho_2\approx0.958\).

At the same time the normalized purity grew strongly and the effective spectral fraction fell substantially. For example, the generic/Haar data showed a large increase in

\[
N\operatorname{Tr}(C^2)
\]

and a strong decrease in

\[
\frac{d_{\rm eff}}{N}.
\]

### What succeeded scientifically

This was the cleanest evidence that a physical low-weight readout can be rank-typical **without** the tangent covariance becoming globally isotropic.

### Important qualification

We do **not** claim that physical finite-depth circuits converge to Haar-random orientation. The numerical statement is finite-size and operational: the tested generic low-weight readouts happen to lie near the rank baseline even though the covariance is far from isotropic.

---

## 5. Architecture dependence: rank alone was not enough

The generic aggregate concealed real family structure.

The clearest example was the **RY--RZ--CZ** family, which developed a systematic one-body deficit relative to the rank-only baseline.

This mattered because it showed that the near-unity generic aggregate was not a universal law of physical circuits. Architecture can create a persistent orientation bias even at fixed readout rank.

### What we learned

A family average can be rank-typical while individual architectures are not. Therefore:

- rank is a baseline, not a prediction for every ansatz;
- architecture-specific orientation must be measured, not assumed;
- the paper should not sell a universal "all generic circuits become random" story.

That stronger story was explicitly abandoned.

---

## 6. The decisive equal-rank experiment

A major weakness of a rank-only discussion is that low physical retention could be misread as "the tangent information is absent."

To test this, we compared subspaces of **exactly the same rank**:

1. the physical low-weight readout;
2. a random rank-matched subspace;
3. a cross-fitted leading tangent subspace;
4. the same-sample Ky Fan optimum as an optimistic upper benchmark.

This produced one of the strongest results in the project.

For Haar-like generic circuits, a leading tangent subspace of the same rank retained far more mass than the physical low-weight observables. A representative \(n=12\) Haar comparison was approximately:

- physical one-body retention: \(2.71\times10^{-3}\),
- cross-fitted aligned retention: \(3.06\times10^{-2}\),
- same-sample Ky Fan benchmark: \(9.15\times10^{-2}\).

### Why this result mattered

It showed that low physical accessibility can be an **orientation mismatch**, not a lack of tangent information at that rank.

The random-rank control was also essential: random equal-rank subspaces stayed near the rank baseline, so the gain was not caused merely by changing the basis representation.

### What changed in the paper after this result

The paper stopped being mainly about "rank typicality without isotropy" and became more explicitly about **spectral orientation at fixed rank**.

This motivated the final title:

> **Measurement-Accessible Quantum Tangent Geometry: Rank Baselines and Spectral Orientation**

---

## 7. Operational bridge: from geometry to gradient signal

A purely geometric overlap could still be criticized as abstract. The next step was therefore to test whether orientation mattered for an operational quantity at fixed resources.

A controlled comparison was implemented with:

- the same circuit;
- the same computational-basis measurement record;
- the same readout rank;
- the same shot budget;
- only the readout orientation changed.

The compared readouts were physical, random-rank, and cross-fitted aligned subspaces.

The diagnostics included:

- actual retained tangent mass;
- raw directional Fisher/gradient energy;
- expected scalar directional gradient squared;
- an estimated parameter-gradient norm proxy;
- finite-shot SNR under multinomial measurement noise.

### Main success

For Haar-like circuits the aligned readout produced large gains over the physical low-weight readout. Representative aligned/physical gradient-energy gains were approximately:

- \(n=8\): 2.96,
- \(n=10\): 4.64,
- \(n=12\): 9.58.

The corresponding finite-shot SNR gains were approximately:

- \(n=8\): 1.73,
- \(n=10\): 2.13,
- \(n=12\): 3.11.

Random rank-matched controls remained close to the physical generic baseline.

### Interpretation that survived

Readout orientation is an **operational control knob at fixed rank and fixed measurement budget**.

### Claim that was deliberately rejected

This is **not** a supervised barren-plateau theorem. No labels, loss function, encoding distribution, classical head, or training trajectory are included in this diagnostic. The paper therefore does not claim a theorem about \(\operatorname{Var}(\partial_\theta L)\) for arbitrary supervised learning.

---

## 8. Noise robustness: useful but limited

A bit-flip readout-noise study was added to test whether the aligned-readout advantage disappears immediately under simple noise.

For Haar \(n=12\), the aligned/physical directional gradient-energy gain decreased with noise but remained above unity through the tested range:

- clean: about 9.58,
- 1%: about 6.92,
- 3%: about 4.49,
- 5%: about 3.13.

The \(U(1)\) gains remained much smaller, consistent with the physical low-weight readout already being comparatively aligned.

### Important limitation

The aligned subspace was **re-estimated after noise was applied**. Therefore this experiment does **not** establish robustness of one fixed optimized observable under changing noise. It only shows that useful aligned directions remain recoverable in the noisy score geometry.

That caveat is retained explicitly in the paper and appendix.

---

## 9. The half-filled \(U(1)\) case study

The \(U(1)\) family was initially tempting as a potential main novelty pillar because it strongly violated the isotropic rank law.

The physical one-body and two-body retained fractions remained very large compared with their random-orientation rank baselines. At \(n=18\), representative retained fractions were approximately:

- one-body: 0.215,
- two-body: 0.401.

The same-rank aligned advantage was much smaller than in Haar-like circuits, suggesting that the physical low-weight readout was already close to important tangent directions.

To quantify this, a cross-fitted alignment statistic was introduced:

\[
A_k=\frac1{r_1}\operatorname{Tr}(P_{\le k}P_{\rm top}),
\]

where \(P_{\rm top}\) is the leading rank-\(r_1\) tangent subspace learned on independent tangents.

### Large-size result

The \(U(1)\) scaling campaign was extended through \(n=18\), with 20 independent circuit instances at the largest point.

At \(n=18\):

- \(A_1\approx0.2836\),
- \(A_{\le2}\approx0.4635\).

These are vastly larger than random-subspace overlap scales.

### Finite-size fits

Over \(n=8,10,12,14,16,18\), the data were compared with power and exponential forms.

The full-window fits favored a power model by AICc for both one-body and cumulative-through-two overlap. Representative power exponents were approximately:

- \(A_1\sim n^{-0.82}\),
- \(A_{\le2}\sim n^{-0.70}\).

### What we do not claim

These fits are **finite-size model discrimination only**. We do not claim:

- an asymptotic scaling theorem;
- a universal hydrodynamic exponent;
- a diffusion law;
- that \(U(1)\) symmetry generically guarantees trainability.

This restraint became important after exploring several possible mechanism stories.

---

## 10. Mechanism hunt: several attractive stories that did not close

The \(U(1)\) result raised the natural question: **why** is low-weight readout so strongly aligned?

Several explanations were discussed and investigated conceptually:

### 10.1 Readout--charge compatibility

Because the physical readout uses low-weight diagonal \(Z\) observables and the ansatz conserves total \(Z\)-charge, one possibility is that simple charge observables are naturally aligned with the tangent structure.

This is plausible, but the existing data do not isolate it from other fixed-charge geometric effects.

### 10.2 Harmonic geometry on the fixed-weight slice

The half-filled computational basis is a Boolean slice, and low-degree functions on that slice have a structured harmonic decomposition.

This provides mathematical context for why low-weight diagonal features may behave differently from the full hypercube, but it does not by itself identify the dynamical origin of the observed leading tangent subspace.

### 10.3 Dynamical Lie algebra / controllability

Symmetry-restricted controllability and dynamical Lie-algebra results offer another explanation: the tangent space may live in a much more structured accessible algebra than generic circuits.

Again, the current experiments do not isolate this mechanism quantitatively.

### 10.4 Hydrodynamic slow modes / diffusion

Conserved-density hydrodynamics was an especially tempting explanation because local charge modes can remain slow and low-weight-visible.

However, the current finite-size overlap data are not enough to infer a hydrodynamic exponent or prove that diffusion controls the measured alignment.

This line was therefore **not promoted into a mechanism claim**.

### Decision

The \(U(1)\) result remains a **structured case study**, not the novelty pillar of the paper.

The mechanism question is deferred to a separate future project where locality, conservation, random fixed-charge baselines, depth scaling, and controllability can be varied independently.

---

## 11. Symmetry-breaking pilot: the most useful mechanism control

A small intervention study was run at \(n=8\) with the same trainable \(U(1)\) architecture and fixed nontrainable perturbations inserted after layers:

- `preserve_Z`: fixed \(R_Z(\epsilon\alpha)\), preserving charge;
- `break_X`: fixed \(R_X(\epsilon\alpha)\), breaking charge.

The trainable parameter count was held fixed.

Representative one-body alignment values were:

- unperturbed: \(A_1\approx0.517\),
- \(\epsilon=0.3\), symmetry-preserving: \(A_1\approx0.481\),
- \(\epsilon=0.3\), symmetry-breaking: \(A_1\approx0.0295\).

The physical one-body retained fraction similarly collapsed under symmetry breaking.

### What this established

The strong low-weight alignment is **sensitive to breaking the conserved charge structure**.

### What this did not establish

This control does not identify which of the following is the actual mechanism:

- readout--charge compatibility;
- fixed-charge harmonic geometry;
- dynamical Lie algebra / controllability;
- hydrodynamic slow modes;
- another symmetry-induced structural effect.

Therefore the pilot is used as a sensitivity control only.

---

## 12. Full-record Fisher comparison

Another possible explanation for the \(U(1)\) behavior was that the computational-basis measurement simply captures much more total Fisher information in the symmetric circuits.

That explanation did not hold.

Across generic/Haar and \(U(1)\) families, the full computational-basis Fisher fraction remained of comparable order, roughly around one-half of the QFI in the tested setups, even while the low-weight retained fractions differed by orders of magnitude.

### Conclusion

The dramatic difference is not primarily a difference in total measurement information. It is a difference in **where that information lies inside the measured score space**.

This strengthened the spectral-orientation interpretation.

---

## 13. Prior-art audit and novelty correction

A substantial effort went into checking whether the central mathematics or physical message had already appeared elsewhere.

The audit forced several useful corrections.

### Things that are known and must not be oversold

- \(\mathbb E\operatorname{Tr}(PC)=r/N\) is a standard random-subspace identity.
- "rank typicality does not imply isotropy" is a generic projection-geometric fact, not a new theorem by itself.
- Ky Fan top-\(r\) optimality is standard.
- Score compression, estimating functions, Godambe geometry, and MOPED-like ideas are classical ancestors.
- Observable-dependent trainability and locality effects are established in the VQA literature.
- Symmetry-aware trainability, fixed-Hamming-weight circuits, dynamical Lie algebras, and conserved-density dynamics have substantial prior literature.

### Closest conceptual pressure points

- Random-measurement work relating average CFIM to QFIM: distinct because it randomizes the full measurement basis, whereas this paper fixes the measurement and varies readout orientation inside its score space.
- Classical subspace-overlap work using \(\operatorname{Tr}(PC)\)-type metrics and chance-level dimension baselines.
- Recent equivariant/noisy QNN work that is qualitatively close to the \(U(1)\) story.

### Final novelty framing

The defensible novelty statement became:

> We introduce a rank-controlled framework for measurement-accessible VQC tangent geometry, use the known random-subspace baseline to isolate spectral orientation, and show that orientation has large physical and finite-shot consequences at fixed readout rank.

The strongest reviewer objection anticipated is that the paper is "routine projection linear algebra repackaging known measurement-dependent Fisher accessibility."

The strongest answer is the controlled experiment:

> same circuit + same measurement + same rank + same shot budget, changing only the readout orientation, produces substantially different retained tangent mass, directional signal, and finite-shot SNR.

---

## 14. Approaches that were considered and deliberately abandoned

Several directions were discussed but removed from the current paper because they either did not close scientifically or would have made the story too diffuse.

### 14.1 "Solve the physical origin of the \(U(1)\) alignment in this paper"

Abandoned.

Reason: existing experiments cannot distinguish among charge-readout compatibility, slice harmonic geometry, controllability, and hydrodynamic mechanisms.

### 14.2 Infer an asymptotic power law or hydrodynamic exponent from \(n\le18\)

Abandoned.

Reason: finite-size model preference is not an asymptotic theorem. The data support descriptive model discrimination only.

### 14.3 Sector-Haar or random fixed-charge baselines as a new campaign

Deferred.

Reason: scientifically useful for mechanism identification, but it would launch a new project rather than finish the current one.

### 14.4 Fourier-mode / diffusion-resolved analysis

Deferred.

Reason: this would require a dedicated conserved-mode study, depth scaling, and larger-size diagnostics to support a hydrodynamic claim.

### 14.5 Push to \(n=20\) simply to extend the plot

Abandoned for the current paper.

Reason: the \(n=18\) point already materially strengthened the finite-size case; another expensive point would not resolve the mechanism or turn the fit into an asymptotic theorem.

### 14.6 Turn the operational diagnostic into a supervised barren-plateau paper

Rejected.

Reason: task-level trainability additionally depends on encoding, labels, loss, classical head, optimization trajectory, and parameterization. The present geometry is upstream of those choices.

### 14.7 Merge accessible quantum natural gradient into the current manuscript

Rejected.

Reason: accessible QNG is a natural application of the geometry, but it is a separate task-level research question and would blur the current paper's conceptual focus.

---

## 15. Production and manuscript failures

The scientific work was not the only source of failure. The manuscript-production pipeline also went through several iterations.

### 15.1 Compiling the wrong manuscript source

An early production workflow compiled the older canonical `spectral_geometry_prx.tex` rather than the rewritten source.

Fix: the workflow was changed to compile the rewrite and then promote it to the canonical manuscript.

### 15.2 Git push/rebase failure

The production job failed with unstaged changes during rebase.

Fix: reset the working tree before the rebase/push step.

### 15.3 Non-idempotent editorial patch scripts

Some source-rewrite scripts assumed exact text anchors that disappeared after the first pass.

Fix: add rerun-safe/idempotency handling and restore the complete canonical manuscript before applying production edits.

### 15.4 Figure legends repeatedly broke

Several visual passes produced unacceptable results:

- legends overlapping plot titles;
- duplicate legends;
- legends disappearing entirely;
- legends placed inside data regions instead of below the plot;
- a cleanup script accidentally stripped the helper responsible for re-adding legends.

The final policy is explicit:

> plot -> shared legend -> caption

with no in-panel legends for the affected multi-panel figures.

CI checks were added to prevent the legend helper from being silently stripped again.

### 15.5 Boxed prose that should not have been boxed

A central prose statement was initially rendered inside a box, contrary to the intended visual style.

Fix: normalize it to plain centered emphasis and add a check preventing the boxed form from returning.

### 15.6 ORCID rendering

Numeric ORCID prose appeared in places where only a clickable green icon was desired.

Fix:

- author header uses `orcidlink` icon only;
- acknowledgment for Mohamed Bennai uses a clickable ORCID icon only;
- CI rejects visible numeric ORCID prose in those locations.

### 15.7 Appendix initially did not appear in the canonical PDF

The appendix scripts and workflow were present, but the visible canonical PDF came from an earlier production build.

Fix: trigger a clean rebuild with checks that require `\\appendix`, appendix labels, appendix figures, and resolved cross-references before promotion.

These production failures are documented here because they explain why the current workflow contains many defensive sanity checks.

---

## 16. Manuscript evolution

The manuscript changed substantially during the project.

### Early framing

**Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy**

The main emphasis was the surprising coexistence of rank-typical low-weight readout with a strongly anisotropic covariance.

### Intermediate framing

The equal-rank spectral experiment showed that orientation was more than a technical caveat: it controlled large differences in retained information at fixed rank.

The operational SNR/gradient experiment then showed that the same distinction mattered at fixed measurement resources.

### Current framing

**Measurement-Accessible Quantum Tangent Geometry: Rank Baselines and Spectral Orientation**

The present paper is organized as:

1. fixed-measurement score geometry;
2. random-orientation rank baseline and spectral null width;
3. generic rank-typical but anisotropic numerics;
4. architecture-dependent deviations;
5. equal-rank physical/random/aligned/Ky-Fan comparison;
6. operational fixed-shot consequence;
7. structured half-filled \(U(1)\) case study through \(n=18\);
8. symmetry-breaking sensitivity control;
9. discussion and limitations;
10. appendices with full derivations, protocols, and supporting diagnostics.

The first isotropic-rank manuscript is now cited explicitly as the predecessor: Paper I gives exact isotropic rank laws; Paper II removes isotropy and resolves the role of spectral orientation.

---

## 17. What we consider established by the current project

Within the tested framework and finite-size regimes, the project supports the following conclusions.

### Established analytically

- The rank-only random-relative-orientation mean is \(r/N\).
- The fluctuation width depends on the covariance purity/effective dimension.
- Large \(r d_{\rm eff}\) can yield rank-typical overlap even when \(d_{\rm eff}/N\ll1\).
- At fixed rank, the leading eigenspace of \(C\) is the spectral optimum by Ky Fan.

### Established numerically

- Generic low-weight readouts can be close to the rank baseline while the tangent covariance is strongly anisotropic.
- Architecture-specific deviations from the baseline exist.
- Equal-rank subspaces can retain very different tangent mass.
- Cross-fitted aligned readouts can substantially outperform physical low-weight readouts in generic Haar-like circuits.
- The orientation advantage changes gradient-energy and finite-shot SNR at fixed circuit, measurement, rank, and shots.
- Half-filled \(U(1)\) circuits form a structured regime where low-weight diagonal readout is already strongly aligned with leading tangent directions.
- That alignment persists through the tested range up to \(n=18\).
- Breaking the conserved charge in a small pilot strongly suppresses the low-weight alignment.
- Comparable full-record Fisher fractions can coexist with very different restricted readout accessibility.

---

## 18. What remains unresolved

The following questions are intentionally left open.

1. What microscopic mechanism controls the \(U(1)\) low-weight alignment?
2. How does the alignment scale asymptotically with system size and depth?
3. What is the correct fixed-charge random baseline for separating symmetry geometry from dynamical structure?
4. How do locality and conservation independently affect tangent orientation?
5. Which experimentally realizable observables best approximate the aligned score subspace?
6. How should one learn or adapt readout orientation under finite shots without overfitting?
7. How much of the accessible geometry is actually used by a task-specific supervised loss?
8. Can the framework be converted into a practical measurement-accessible natural-gradient method?

These questions motivate separate follow-up projects rather than extensions of the present manuscript.

---

## 19. Separate future project: Accessible Quantum Natural Gradient

A distinct repository was started for **Accessible Quantum Natural Gradient**.

The question there is not whether a readout subspace retains tangent mass, but what minimal measurement-accessible geometry is sufficient for useful natural-gradient optimization.

This is deliberately kept separate from the present paper because it introduces task-level optimization and algorithm design beyond the current fixed-measurement geometry.

---

## 20. Current status

As of 2026-08-10:

- the core theory is stable;
- the generic and \(U(1)\) numerical campaigns are complete for the present scope;
- the \(n=18\) \(U(1)\) scaling point has been completed;
- the equal-rank operational bridge is integrated;
- the noise robustness study is integrated with its caveat;
- the symmetry-breaking pilot is integrated as a sensitivity control;
- the manuscript has been reframed around rank baselines and spectral orientation;
- the earlier isotropic-rank paper is cited as the direct predecessor;
- the appendices collect full derivations, protocol details, additional diagnostics, noise, fit diagnostics, and circuit conventions;
- the repository README and production workflow reflect the current paper structure;
- no new large simulation campaign is currently required for this manuscript.

The intended scope is now deliberately narrow enough to defend:

> fixed measurement, fixed readout rank, anisotropic tangent covariance, and the physical consequences of relative spectral orientation.

---

## 21. Short project summary

The project began with a rank law under isotropy. The first important surprise was that generic circuits could look rank-typical even when their tangent covariance was strongly anisotropic. The next decisive result was that equal-rank subspaces could retain dramatically different tangent mass, proving that orientation was not a minor correction to rank. The operational fixed-shot experiment then showed that this orientation difference changes usable directional signal and SNR. The half-filled \(U(1)\) family provided the opposite structured regime, where physical low-weight observables are already strongly aligned. Attempts to turn that observation into a complete mechanism story did not close, so the paper was deliberately narrowed: the structured \(U(1)\) behavior is evidence for the framework, not the framework's claimed universal explanation.

The final scientific message is therefore simpler and more defensible than several intermediate versions:

> **Rank tells us how many score directions are kept. The tangent spectrum and the orientation of the retained subspace tell us how much useful measured tangent information those directions actually contain.**
