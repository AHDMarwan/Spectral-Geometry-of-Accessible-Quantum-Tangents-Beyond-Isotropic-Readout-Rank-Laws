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
- Remains descriptive and keyword-rich; contains no formula.

## Stage 1 — Abstract

### Source sentence 1
`A fixed quantum measurement can expose substantially more tangent information than a restricted observable readout retains.`

### Revision
`Variational quantum circuits are accessed through measurements, but learning pipelines often retain only a restricted set of observables or classical features.`

### Reason
Opens with the experimental/learning interface rather than an abstract contrast. The VQC setting is named immediately.

### Source sentence 2
`We study this second restriction directly.`

### Revision
`Readout dimension alone does not determine how much measurement-induced tangent information survives this restriction.`

### Reason
Removes first person, as required by AQT abstract style, and replaces a procedural sentence with the scientific question.

### Source covariance/rank/equation block
The source defines `C`, `P`, `R`, `rho`, and includes the full Grassmann variance equation in the abstract.

### Revision
`A normalized covariance of tangent scores separates readout rank, spectral concentration, and readout orientation, while random rank-matched subspaces define a rank-only reference.`

### Reason
Keeps the conceptual decomposition while removing a long displayed equation from the abstract. The exact formula remains appropriate for the theory section.

### Source generic-circuit result
Family-balanced low-weight readouts remain near the rank reference through `n=16` despite strong anisotropy.

### Revision
`Across five generic circuit families, one- and two-body diagonal readouts remain near this reference through 16 qubits although the tangent covariance becomes strongly anisotropic.`

### Reason
States the sample class and physical readout in plain language. Avoids vague evaluative wording.

### Source equal-rank result
At Haar-`U(4)`, `n=12`, cross-fitted alignment gives 9.584x gradient-energy and 3.111x finite-shot SNR gain relative to the physical one-body readout.

### Revision
`In an equal-rank comparison for Haar-U(4) circuits at 12 qubits, a cross-fitted aligned readout increases the mean directional gradient-energy proxy by a factor of 9.584 and the finite-shot signal-to-noise ratio by a factor of 3.111 relative to the physical one-body readout; a random rank-matched subspace remains near the reference.`

### Reason
Preserves the strongest controlled quantitative result and specifies the comparator. No broader optimization claim is added.

### Source U(1) result and caveat block
The source presents a half-filled U(1)-conserving counter-regime and then lists several negative claims about barren plateaus and hydrodynamics.

### Revision
`A half-filled U(1)-conserving family shows the complementary regime, where low-weight Z readouts are already aligned with leading tangent directions.`

### Reason
Retains the observation and removes defensive caveat density from the abstract. The mechanistic limitations belong in the main text.

### Source closing sentence
`The results isolate readout orientation as a degree of freedom that is invisible to rank alone but directly controls how much measured tangent information remains usable after readout restriction.`

### Revision
`Readout orientation therefore controls measurement-accessible tangent information independently of readout rank and can materially alter finite-shot directional signal.`

### Reason
Uses a direct, testable conclusion. Avoids promotional language and the common rhetorical template `invisible to X but controls Y`.

## Stage 1 — Keywords

Proposed keywords:
- variational quantum circuits
- quantum information geometry
- quantum measurements
- readout design
- Fisher information
- quantum machine learning

These will be re-audited after the Introduction and reference positioning are finalized.

## Style checks applied

- AQT: abstract <= 200 words; present tense; impersonal style; no references.
- Avoid generic significance claims (`crucial`, `key`, `highlights`, `underscores`, `broader landscape`).
- Avoid repeated `not X but Y` and `not only X but also Y` constructions.
- Avoid decorative rule-of-three phrasing unless the three items are scientifically defined quantities.
- Prefer concrete nouns, measured quantities, named comparators, and direct verbs.
- Preserve necessary caveats, but place them where they delimit the claim rather than repeating them in every section.

## Next stage

Introduction, paragraphs 1--2: problem framing and literature boundary.
