# AQT Line-by-Line Revision Log

Working source: `paper/manuscript/spectral_geometry_rewrite.tex`
Target: *Advanced Quantum Technologies*
Branch: `aqt-submission`

This log records substantive editorial changes. Scientific claims and numerical values are changed only when the source manuscript, archived results, or cited literature supports the change.

## Stage 1 — Title

### Source
`Measurement-Accessible Quantum Tangent Geometry: Rank Baselines and Spectral Orientation`

### AQT draft
`Spectral Orientation of Measurement-Accessible Quantum Tangent Geometry in Variational Quantum Circuits`

### Reason
- Moves the paper-specific contribution, spectral orientation, to the beginning.
- Removes `Rank Baselines` from the title because the random-rank baseline is supporting/null-model machinery rather than the novelty claim.
- Adds `Variational Quantum Circuits` to identify the physical/computational setting for an interdisciplinary AQT reader.
- Remains descriptive and keyword-rich and contains no formula.

## Stage 1 — Abstract

### Source opening
`A fixed quantum measurement can expose substantially more tangent information than a restricted observable readout retains. We study this second restriction directly.`

### Final AQT opening
`After a fixed measurement of a trainable variational quantum circuit, readout subspaces of the same dimension can retain different amounts of parameter-tangent information.`

### Reason
- Removes first person.
- Specifies that the tangent is a trainable-circuit parameter tangent rather than a generic feature tangent.
- Frames the scientific question at fixed measurement and fixed readout dimension.
- Avoids claiming that subspace visibility itself is new.

### Source covariance/rank/equation block
The source defines `C`, `P`, `R`, `rho`, and includes the full Grassmann variance equation in the abstract.

### Final AQT treatment
`This dependence is resolved by the covariance spectrum of Fisher-normalized measurement scores and by the orientation of the retained readout subspace within that score space. Random rank-matched subspaces provide a rank-only reference.`

### Reason
The abstract keeps the object and null model without presenting standard Grassmann mathematics as the headline contribution.

### Generic-circuit result
The source reports near-rank one-/two-body retention through `n=16` despite strong covariance anisotropy. The AQT abstract retains this result in plain language and names the five generic circuit families collectively.

### Equal-rank result
The AQT abstract retains the strongest controlled result: Haar-`U(4)`, 12 qubits, `9.584x` directional gradient-energy proxy and `3.111x` finite-shot SNR relative to the physical one-body readout at identical rank.

### U(1) result
The AQT abstract retains the structured contrast but removes the long caveat list. Mechanism limits are stated in the Introduction and Discussion.

### Abstract compliance
- 175 words.
- Present tense.
- Impersonal style.
- No references.
- No displayed equation.
- No unsupported optimization or barren-plateau claim.

## Stage 1 — Keywords

- variational quantum circuits
- quantum information geometry
- quantum measurements
- readout design
- Fisher information
- quantum machine learning

Six keywords satisfy the AQT 3–7 keyword requirement.

## Stage 2 — Introduction

### Paragraph 1
Changed the opening from a state-space-first discussion to the experimental sequence:
`parameterized state -> fixed measurement -> measured outcome geometry -> restricted readout`.

Reason: AQT has an interdisciplinary quantum-technology readership. The readout bottleneck is easier to understand when the physical interface is stated before the formalism.

### Paragraph 2 — Gross & Rieser boundary
Added explicit discussion of Gross and Rieser, arXiv:2602.18377.

Their problem is described as Pauli-feature decodability in QELMs/QRCs, with an effective PTM row space and a local-injectivity condition on the tangent space of the classical input feature map. The present paper is distinguished by the object being projected: Fisher-normalized derivatives with respect to trainable VQC parameters after a fixed measurement.

Reason: after Gross & Rieser, the paper must not claim novelty for `readout subspace visibility` or projector geometry in general.

### Paragraph 3 — central definitions
Moved `C`, `P`, `R=Tr(PC)`, and `rho` into one compact paragraph. The denominator `r/N` is explicitly called a random-relative-orientation reference rather than a physical-circuit model.

### Paragraph 4 — relation to isotropic-rank paper
The prior isotropic paper is described as a boundary case that supplies exact rank laws under joint state–tangent isotropy. The present paper is positioned as the non-isotropic extension in which the covariance spectrum and relative orientation become necessary.

The standard Grassmann variance result is retained only as null-width machinery. `d_eff` is explained as spectral concentration rather than introduced as a formal statistic without interpretation.

### Paragraph 5 — evidence chain
The previous numbered/rhetorical four-part list is rewritten as one evidence chain:
near-rank generic retention -> strong anisotropy -> architecture-specific deviations -> equal-rank spectral intervention -> finite-shot consequence.

### Paragraph 6 — U(1)
The U(1) result is presented as a structured regime rather than an exception appended after the generic case. Mechanistic possibilities are named, but no hydrodynamic or generic trainability claim is made.

### Paragraph 7 — contribution statement
The contribution is stated positively and specifically:
- covariance-resolved parameter-tangent geometry after a fixed measurement;
- equal-rank physical/random/cross-fitted controls;
- fixed-charge sector-corrected structured comparison;
- finite-shot directional-signal test.

Standard Grassmann and Ky Fan results are explicitly excluded from the novelty claim.

## Stage 3 — Main theory and methods

### Score geometry
Kept the Fisher-normalized score definition and `C = E[u_v u_v^T]`. Added a direct explanation that normalization separates tangent direction from the overall classical Fisher scale.

### Readout projector
Kept the operational identity `R = E||P u_v||^2 = Tr(PC)`. The prose now states exactly what changes when `P` changes: the retained classical subspace, not the state family or the quantum measurement.

### Gross-Rieser distinction repeated once in theory
Added one concise sentence distinguishing the PTM Pauli-feature object from the present parameter-tangent score covariance. No repeated literature discussion elsewhere in the section.

### Rank reference
Compressed fixed-weight rank scaling to context. The exact isotropic Beta/rank-law derivations are assigned to the separate isotropic-rank paper and Supporting Information where needed for bookkeeping.

### Same-rank controls
Ky Fan is identified as a standard upper benchmark. Cross-fitting is explained before any aligned-readout result, and calibration tangents are explicitly separated from held-out evaluation tangents.

### Numerical protocol
Consolidated the circuit families, statistical unit, bootstrap procedure, cross-fit sample counts, and fixed-shot evaluation model into one Methods-style section. Calibration cost is stated as a separate resource rather than hidden inside the fixed evaluation-shot comparison.

## Stage 4 — Results

### Generic circuits
The result is stated as `near-rank retention with strong anisotropy`, not as convergence to Haar orientation. The `d_eff/N` values and normalized purity are retained to prevent `rho approximately 1` from being misread as isotropy.

### Equal-rank intervention
The physical, random, cross-fitted aligned, and Ky Fan objects are assigned distinct roles. The `R_phys = 2.71e-3` and `R_xfit = 3.06e-2` values at Haar-`U(4)`, `n=12`, remain central.

### Finite-shot section
Kept the `9.584x` gradient-energy and `3.111x` SNR headline at `n=12`. The text lists what is held fixed and states that these are directional diagnostics rather than supervised-loss gradient variances.

### U(1)
The main result uses a fixed-charge sector-corrected null. The `811x` and `148x` enhancements over the sector null at `n=18` remain in the main article. Detailed finite-size model fits and the symmetry-breaking figure are assigned to Supporting Information, while the numerical sensitivity result remains available in the main text.

### Full-record control
Kept the `F_full/F_Q approximately 0.49` generic and `0.47–0.48` U(1) comparison because it rules out the interpretation that the structured circuit simply preserves much more information at the measurement stage.

## Stage 5 — Discussion and Conclusion

### Discussion
Reorganized around the controlled equal-rank result, then related work, the structured U(1) regime, limitations, and design implications. Removed repeated defensive wording and the slogan-like `three-part separation` opening.

The Gross-Rieser comparison is stated fairly: their work also treats covariance-sensitive predictability, so the manuscript does not claim that they `ignore covariance`. The distinction is the object and stage of the pipeline.

### Conclusion
Reduced to one compact paragraph. It answers the fixed-measurement/fixed-rank question directly, states the generic and U(1) regimes, and ends with the design implication at the quantum-measurement/classical-processing interface.

## Stage 6 — AQT packaging

Created:
- `AQT_MAIN_TEXT_REWRITE.tex`
- `AQT_MAIN_FIGURES.tex`
- `AQT_REFERENCES.tex`
- `AQT_SUPPORTING_INFORMATION_PLAN.md`
- `AQT_RELATED_WORK_AUDIT.md`
- `AQT_SUBMISSION_METADATA.tex`
- `AQT_COVER_LETTER_DRAFT.txt`
- integrated draft `aqt_spectral_geometry.tex`

Recommended main-text display count: five figures. Circuit schematics, detailed null derivations, finite-size fit panels, noise sweeps, and extended robustness diagnostics are assigned to Supporting Information.

## Remaining author-confirmation items

These are not editorial judgments and cannot be filled from the research files without author confirmation:

1. complete AQT affiliation wording;
2. institutional/company corresponding-author email requested by the journal;
3. funding statement;
4. conflict-of-interest statement;
5. whether the AQNG manuscript is already submitted, in press, or planned for imminent submission and therefore needs explicit cover-letter disclosure;
6. final archival DOI/tag for the submitted numerical record;
7. original non-AI-generated ToC graphic.

## Style checks applied throughout

- American English.
- Direct syntax and concrete subjects.
- No generic significance fillers such as `crucial`, `key`, `highlights`, or `underscores` unless scientifically necessary.
- Avoid repeated `not X, but Y` and `not only X, but also Y` templates.
- Avoid decorative three-item lists unless the items are genuinely defined scientific quantities.
- Avoid repeated em-dash constructions.
- Prefer named comparators, measured quantities, and exact scope conditions.
- Keep limitations where they delimit a claim instead of repeating them in Abstract, Introduction, Results, Discussion, and Conclusion.
