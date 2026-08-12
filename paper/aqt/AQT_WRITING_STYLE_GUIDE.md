# AQT Scientific Prose Style Guide

Target manuscript: `paper/manuscript/spectral_geometry_rewrite.tex`
Working branch: `aqt-submission`

This document supplements `AQT_REVISION_CHECKLIST.md`. It combines the formal requirements of the Advanced Quantum Technologies author guide with editorial heuristics drawn from Wikipedia's *Signs of AI writing* advice page. The Wikipedia page is descriptive rather than prescriptive and is not an authorship detector. Its useful role here is narrower: identify prose habits that can make technical writing generic, inflated, repetitive, or mechanically patterned.

Sources:
- AQT Author Guidelines: https://advanced.onlinelibrary.wiley.com/hub/journal/25119044/author-guidelines
- Wikipedia, Signs of AI writing: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing

## 1. Governing principle

Scientific content comes first. Do not rewrite a technically precise sentence merely to avoid a word or syntactic pattern. The goal is to make every sentence specific to this paper, proportional to the evidence, and easy for a quantum-technology reader to parse.

A sentence should normally do one identifiable job: state a result, define an object, delimit a claim, connect to prior work, or explain a physical implication. Avoid sentences whose main function is rhetorical emphasis.

## 2. Prefer specific claims over generic significance language

Avoid stock significance phrases unless the manuscript supplies a concrete reason for them. In particular, do not rely on phrases such as:

- `plays a crucial/key/pivotal role`
- `underscores the importance of`
- `highlights the significance of`
- `represents a major shift`
- `provides valuable insights`
- `opens new avenues`
- `in the broader landscape of`
- `serves as a testament to`

Replace them with the actual scientific statement.

Weak:
`These results highlight the crucial role of spectral orientation in quantum learning.`

Preferred:
`At fixed measurement and readout rank, changing only the retained score subspace changes the retained tangent mass and finite-shot directional signal.`

## 3. Control high-frequency generic vocabulary

Words identified as common in formulaic AI prose are not forbidden. They should appear only when they are the most precise term. Audit repeated use of words such as `highlight`, `emphasize`, `enhance`, `robust`, `crucial`, `key`, `pivotal`, `interplay`, `landscape`, `valuable`, `showcase`, and `underscore`.

For this manuscript, prefer domain-specific verbs:

- `retains`, `projects`, `bounds`, `concentrates`, `deviates`, `aligns`, `suppresses`, `resolves`, `estimates`, `conditions`, `scales`, `fits`, `increases`, `decreases`, `matches`, `exceeds`.

Do not replace a precise technical word merely for lexical variety. Repetition of a defined term such as `readout`, `score space`, `retention`, or `orientation` is preferable to changing terminology for style.

## 4. Avoid canned contrast constructions

Use `not X but Y`, `not only X but also Y`, and `rather than` only when the contrast is logically necessary. Repeated negative parallelism makes prose sound argumentative and can obscure the positive claim.

Weak:
`The effect is not merely geometric, but also operational.`

Preferred:
`The same orientation dependence appears in the finite-shot directional-signal diagnostics.`

Weak:
`This is not an isotropy statement; rather, it is an orientation statement.`

Preferred:
`Near-baseline retention coexists with a strongly anisotropic tangent covariance, so the observation concerns relative orientation rather than isotropy.`

## 5. Do not manufacture triples

Avoid routinely packaging ideas into groups of three for rhythm. Use the number of items required by the science.

If the paper genuinely has three distinct quantities—rank, covariance spectrum, and readout orientation—retain that three-part decomposition because it is substantive. Do not add a third adjective, consequence, or future direction merely to complete a rhetorical pattern.

## 6. Limit em dashes and parenthetical punchlines

Use em dashes sparingly. In technical prose, commas, parentheses, colons, or separate sentences are often clearer.

Weak:
`The aligned subspace—learned on independent tangents—retains substantially more mass.`

Preferred when the qualification matters:
`The aligned subspace is learned on an independent tangent set and then evaluated on held-out tangents. It retains substantially more mass.`

Keep en dashes where they are typographically correct in compound technical terms such as `rank-matched`, `finite-shot`, or ranges where the journal style requires them.

## 7. Avoid vague attribution

Do not write `experts argue`, `several studies show`, `it is widely known`, or similar phrases unless the cited literature actually establishes a broad consensus.

Prefer named, traceable claims:

`Randomized-measurement studies derive Haar-averaged relations between the CFIM and QFIM [ref].`

not

`Recent studies have highlighted the importance of randomized measurements.`

Every literature-dependent sentence should be supportable by the cited reference immediately adjacent to it.

## 8. Avoid superficial significance clauses

Be suspicious of sentence-final participial clauses that add generic interpretation without new information, for example:

`..., highlighting the importance of readout design.`
`..., demonstrating the broader relevance of the framework.`
`..., offering valuable insight into trainability.`

Either state the implication precisely in a new sentence or delete it.

## 9. Use ordinary copular syntax when it is clearest

Do not avoid `is`, `are`, `has`, or `shows` merely to sound sophisticated.

Preferred:
`The rank-only reference is r/N.`
`The covariance is strongly anisotropic at n=16.`
`The U(1) readout is already aligned with leading tangent directions.`

Avoid inflated alternatives such as `constitutes`, `serves as`, or `stands as` when a basic verb is more accurate.

## 10. Do not over-polish terminology

Technical terms should remain stable. Do not rotate among near-synonyms such as `readout subspace`, `feature manifold`, `observable sector`, and `measurement projection` unless they denote different objects.

Maintain a controlled vocabulary:

- `measurement record`: the full classical outcome record produced by the fixed quantum measurement.
- `score space`: the centered Fisher-normalized space in which tangent scores are represented.
- `readout subspace`: the retained linear span inside score space.
- `readout rank`: the dimension of that retained subspace.
- `tangent covariance C`: covariance of normalized measurement-induced tangent scores.
- `retained tangent mass R`: `Tr(PC)`.
- `rank-normalized retention rho`: `R/(r/N)`.
- `spectral orientation`: relative orientation between the readout projector and eigenspaces of C.

## 11. Paragraph structure

Avoid paragraphs that read like mini-outlines or repeated summaries. Each paragraph should normally follow:

1. scientific point or question;
2. necessary definition/evidence;
3. direct consequence.

Do not add a generic concluding sentence if the consequence is already clear.

Paragraph openings should vary naturally because the logic varies, not because synonyms have been mechanically substituted. Avoid repeated templates such as `Importantly,`, `Notably,`, `Crucially,`, `Furthermore,`, and `Taken together,`.

## 12. Introductions and conclusions

### Introduction

Do not inflate the field-level importance before stating the problem. Start from the concrete measurement/readout mismatch. Move from the practical interface to the geometric question, then delimit prior work.

Avoid broad claims such as `Quantum computing is rapidly transforming...` or `Variational quantum algorithms have emerged as a promising paradigm...` unless a specific argument requires them.

### Conclusion

Do not end with a generic list of `challenges and future opportunities`. Conclude with the result established by the paper and one technically motivated next question if needed.

Avoid `Taken together, these findings...` unless the sentence adds content not already stated.

## 13. Abstract-specific rules

In addition to AQT's formal abstract requirements:

- No generic field-opening sentence.
- No rhetorical claims of importance.
- No literature review.
- No displayed equation unless indispensable.
- Prefer exact quantities over adjectives such as `substantial`, `significant`, or `dramatic` when numbers are available.
- Keep one main narrative: fixed measurement and rank -> orientation dependence -> controlled equal-rank result -> structured U(1) contrast -> conclusion.
- Avoid a cluster of caveats. State the scope once and precisely.

## 14. Evidence-calibrated adjectives

Use adjectives only when their meaning is quantitatively supported.

- `strongly anisotropic`: accompany with `N Tr(C^2)` or `d_eff/N`.
- `large gain`: give the gain factor.
- `near the rank baseline`: give rho and uncertainty/range where practical.
- `strongly aligned`: give overlap relative to the sector-corrected null.
- `finite-size`: use explicitly for fits and trends that are not asymptotic theorems.

Avoid `remarkable`, `striking`, `dramatic`, `compelling`, `powerful`, and `unprecedented` unless there is an exceptional editorial reason.

## 15. Sentence-level revision test

For every sentence, ask:

- Does it contain a claim specific to this manuscript?
- Is every adjective justified by data or mathematics?
- Could a simpler verb state the same fact more accurately?
- Is a contrast construction logically necessary?
- Is an `-ing` clause adding information or just emphasis?
- Is the attribution specific and cited?
- Does the sentence use the established technical vocabulary?
- Can it be shortened without losing a condition, assumption, or quantitative result?

## 16. Human editorial pass

The Wikipedia advice page explicitly cautions that its signs are probabilistic and that both human judgment and AI detectors can be unreliable. Do not optimize the manuscript for an AI-detection score. The final pass should instead check whether the prose is scientifically accountable: every sentence should be explainable in terms of the underlying result, citation, design choice, or limitation.

Before submission, read the manuscript aloud or line-edit it on paper/PDF. Flag sentences that sound smoother than they are informative. Replace generic fluency with specific content.

## 17. Final style gate

- [ ] No inflated significance language where a concrete result can be stated.
- [ ] No dense cluster of generic AI-associated vocabulary.
- [ ] No repeated `not X but Y` or `not only X but also Y` constructions.
- [ ] No artificial rule-of-three phrasing.
- [ ] Em dashes are rare and justified.
- [ ] No vague authorities (`experts`, `studies`, `researchers`) without specific support.
- [ ] No sentence-final generic `-ing` significance clause.
- [ ] No synonym rotation for defined technical objects.
- [ ] No generic field-opening paragraph.
- [ ] No outline-like future-prospects conclusion.
- [ ] Quantitative statements replace promotional adjectives wherever possible.
- [ ] Limitations are stated once at the point where they affect interpretation.
- [ ] The manuscript reads as a technical argument, not as a sequence of polished summaries.
