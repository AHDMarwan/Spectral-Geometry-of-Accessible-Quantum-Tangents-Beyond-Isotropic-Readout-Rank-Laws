# Advanced Quantum Technologies (AQT) Revision Checklist

Target journal: Advanced Quantum Technologies (Wiley)
Target article type: Research Article
Working source: `paper/manuscript/spectral_geometry_rewrite.tex`
Working branch: `aqt-submission`

This checklist is the control document for the AQT-specific rewrite. The scientific claims must remain traceable to the existing manuscript, data, scripts, and cited literature. The AQT version should sharpen significance and accessibility without inflating claims.

## 0. Non-negotiable scientific boundary

- [ ] Keep the three-paper program separated: isotropic readout-rank laws = prior/theoretical baseline; this paper = spectral orientation beyond isotropy; AQNG = later algorithmic optimization paper.
- [ ] Do not re-derive or present the isotropic Beta/rank laws as a new contribution here.
- [ ] State clearly that the Grassmann mean/variance identities are standard null-model machinery, not the novelty.
- [ ] Make the novelty explicit: at fixed measurement and fixed readout rank, accessibility depends on the orientation of the readout relative to the spectrum/eigenspaces of the measurement-induced tangent covariance.
- [ ] Preserve the distinction between measurement-accessible tangent geometry and supervised-loss trainability.
- [ ] Do not claim a barren-plateau theorem.
- [ ] Do not claim that U(1) symmetry generically improves trainability.
- [ ] Do not claim hydrodynamics as the established mechanism for the U(1) observations.
- [ ] Do not describe finite-size fits as asymptotic laws unless an actual theorem supports that statement.

## 1. AQT journal-format requirements

Based on the current Wiley AQT Author Guidelines:

- [ ] Use American English throughout.
- [ ] Treat the manuscript as a Research Article.
- [ ] Aim for the typical AQT Research Article envelope of roughly 3000–8000 words in total; length can exceed this only when scientifically justified.
- [ ] Aim for roughly 3–8 main-text display items (figures/schemes/tables); move secondary diagnostics to Supporting Information where this improves the narrative.
- [ ] Title must be descriptive and keyword-rich, not catchy; avoid mathematical formulae in the title.
- [ ] Title capitalization must follow AQT guidance.
- [ ] Provide complete author name(s), affiliation(s), and corresponding-author information.
- [ ] Confirm that the corresponding-author email satisfies Wiley/AQT requirements before submission.
- [ ] Add 3–7 keywords.
- [ ] Abstract <= 200 words.
- [ ] Rewrite abstract in present tense and impersonal style; avoid first-person `we`.
- [ ] Define every abbreviation at first abstract use.
- [ ] No references in the abstract.
- [ ] Main manuscript order should follow AQT convention: Title; Authors; Affiliations; Keywords; Abstract; Main Text; Methods/Experimental Section where appropriate; Acknowledgements; References; required statements; ToC material as required.
- [ ] Use numbered references in order of citation for the final AQT-formatted version; one literature citation per numbered reference.
- [ ] Use the full word `Figure` in manuscript prose rather than abbreviating it.
- [ ] Ensure every figure/table is cited in numerical order.
- [ ] Ensure figure captions are self-contained and define symbols/abbreviations needed to interpret the figure.
- [ ] Prefer vector PDF/EPS/PS for plots/line art; ensure bitmap graphics meet >=300 dpi and adequate pixel dimensions.
- [ ] Prepare Supporting Information as a separate, self-contained file where possible.
- [ ] Add Data Availability Statement.
- [ ] Add Funding Statement.
- [ ] Add Conflict of Interest statement.
- [ ] Add other ethics/integrity statements only where applicable.
- [ ] Prepare a 50–60 word third-person Table-of-Contents text for a general audience.
- [ ] Prepare an original ToC graphic at either 55 mm x 50 mm or 110 mm x 20 mm.
- [ ] Confirm ORCID and author metadata before submission.

## 2. Editorial positioning for AQT

- [ ] Rewrite the first paragraph so a broad quantum-technology reader understands the practical problem before the formalism.
- [ ] Explain why a restricted readout is an experimentally relevant information bottleneck after a measurement record has already been obtained.
- [ ] Put the main technological message early: readout rank alone does not determine usable tangent information.
- [ ] Present spectral orientation as a design degree of freedom of the measurement/readout interface.
- [ ] Explain the relevance to variational quantum circuits, measurement design, feature extraction, and finite-shot operation without overstating immediate hardware deployment.
- [ ] Make the relationship to the isotropic readout-rank paper explicit in one concise paragraph: that paper supplies the isotropic baseline; this paper studies what controls accessibility when isotropy is absent.
- [ ] Keep the AQNG/optimization story out of this manuscript except, at most, as a future direction; do not dilute this paper's independent contribution.
- [ ] Ensure the introduction ends with a compact list/prose statement of concrete contributions, not only a slogan.

## 3. Title

- [ ] Audit current title: `Measurement-Accessible Quantum Tangent Geometry: Rank Baselines and Spectral Orientation`.
- [ ] Check whether `Rank Baselines` overemphasizes standard/null-model machinery relative to the actual novelty.
- [ ] Consider AQT-facing alternatives that foreground measurement accessibility and spectral orientation while remaining descriptive.
- [ ] Final title must not imply that rank laws themselves are newly derived in this manuscript.

## 4. Abstract — line-by-line rewrite

- [ ] Reduce to <=200 words.
- [ ] Remove first-person constructions (`We study`, `We use`, `We treat`).
- [ ] Remove the displayed variance equation from the abstract unless essential; AQT abstract should prioritize problem, method, principal quantitative result, and significance.
- [ ] Introduce the fixed-measurement/fixed-rank question in the first 1–2 sentences.
- [ ] State the central object `R = Tr(PC)` compactly only if it improves clarity for a broad readership.
- [ ] Explicitly label random orientation as a rank-only null/reference, not a physical-circuit model.
- [ ] Keep the strongest equal-rank quantitative result: Haar-U(4), n=12, 9.584x gradient-energy and 3.111x finite-shot SNR relative to physical one-body readout.
- [ ] Keep the U(1) result as the structured contrast, but compress caveats.
- [ ] End on the positive contribution: spectral orientation controls usable measured tangent information beyond rank.
- [ ] Avoid defensive language density in the abstract.

## 5. Introduction — line-by-line rewrite

- [ ] Paragraph 1: lead with the experimental measurement/readout interface, then connect to QFI/QGT/natural-gradient geometry.
- [ ] Paragraph 2: compress adjacent barren-plateau/controllability/symmetry literature; keep only literature needed to delimit the question.
- [ ] Paragraph 3: define the fixed-measurement, fixed-rank problem in plain language before equations.
- [ ] Paragraph 4: distinguish prior isotropic readout-rank result from the present beyond-isotropy contribution.
- [ ] Avoid calling standard Grassmann identities a contribution.
- [ ] Explain `d_eff` physically as spectral participation/effective tangent dimension.
- [ ] Recast the four numerical results as a coherent evidence chain: rank-typical but anisotropic -> architecture-dependent orientation -> equal-rank aligned intervention -> finite-shot consequence.
- [ ] Present U(1) as a structured counter-regime, not an appended exception.
- [ ] Replace repeated negative caveats with one precise scope paragraph near the end of the Introduction.
- [ ] End Introduction with 3–4 explicit contributions and the AQT-relevant significance.

## 6. Theory / Measurement-accessible tangent geometry

- [ ] Verify every definition against the numerical implementation.
- [ ] Explain the score-vector construction sufficiently for a reader outside information geometry.
- [ ] Clarify what ensemble the expectation defining `C` is taken over.
- [ ] Keep `Tr C = 1` normalization explicit and consistent throughout.
- [ ] Explain `d_eff = 1/Tr(C^2)` as a spectral concentration diagnostic.
- [ ] Explain why a retained observable family maps to a projector in centered score space.
- [ ] Emphasize the operational identity `R = E ||P u_v||^2 = Tr(PC)`.
- [ ] Check terminology: distinguish `measurement record`, `readout`, `feature span`, `score space`, and `observable subspace` consistently.

## 7. Rank baseline / random orientation

- [ ] Cite standard Grassmann/projector-moment sources directly.
- [ ] State explicitly that `E[R]=r/N` is a null/reference under randomized relative orientation.
- [ ] Do not imply that generic finite-depth circuits are Haar-oriented.
- [ ] Keep exact variance formula if it is used quantitatively later; otherwise consider moving derivation details to Supporting Information.
- [ ] Retain the bound `Var(rho) <= 2/(r d_eff)` because it supports the key conceptual point that rank-typicality does not imply isotropy.
- [ ] Explain the distinction between large `r d_eff` and `d_eff/N -> 1` in prose.
- [ ] Keep fixed-weight Pauli rank scaling as context/baseline, but avoid duplicating the isotropic-rank paper's main theorem.

## 8. Spectral orientation section

- [ ] Make this the conceptual center of the paper.
- [ ] State the Ky Fan optimum as standard matrix analysis and cite it.
- [ ] Define aligned, random rank-matched, and physical readouts before showing results.
- [ ] Explain why equal rank isolates orientation from dimension.
- [ ] Explain cross-fitting before presenting aligned-readout gains.
- [ ] State what is learned on calibration tangents and what is evaluated on held-out tangents.
- [ ] Make clear that learning the aligned subspace has a calibration cost that is not included in the fixed evaluation-shot comparison.

## 9. Numerical protocol / Methods

- [ ] Consolidate circuit definitions, tangent sampling, system sizes, depth choices, seeds, sample counts, and support restrictions into a reproducible Methods section or Supporting Information.
- [ ] Keep the circuit instance as the statistical unit where that is the actual analysis unit.
- [ ] State bootstrap procedure and confidence-interval construction precisely.
- [ ] State family balancing/weighting precisely for aggregate results.
- [ ] State cross-fit calibration/evaluation sample sizes.
- [ ] State finite-shot estimator and shot budget.
- [ ] State how zero/near-zero probabilities and score regularization are handled.
- [ ] State exact computational-basis support used in the U(1) sector and how rank is corrected on that support.
- [ ] Confirm all reported numbers can be regenerated from repository artifacts.

## 10. Generic-circuit results

- [ ] Lead with the surprising point: physical one-/two-body readouts can be near the rank baseline while `C` is strongly anisotropic.
- [ ] Report `d_eff/N` or normalized purity alongside `rho` so readers cannot equate rank-typicality with isotropy.
- [ ] Keep architecture-resolved results that demonstrate deviations on both sides of the baseline.
- [ ] Avoid language suggesting convergence to Haar orientation unless directly established.
- [ ] Audit every scaling phrase (`decays`, `grows`, `asymptotic`, `exponential`) against what the finite-size data actually establish.

## 11. Equal-rank intervention / operational bridge

- [ ] Give this result high visual and narrative priority.
- [ ] Explicitly list what is held fixed: circuit, measurement record, readout rank, evaluation tangents, and evaluation shot budget.
- [ ] Compare physical vs random rank-matched vs cross-fitted aligned readouts.
- [ ] Keep the n=12 9.584x gradient-energy and 3.111x SNR gains prominently reported, with uncertainty/statistical context where available.
- [ ] Explain the directional gradient-energy proxy and finite-shot SNR in operational terms.
- [ ] State clearly that these are diagnostics, not a complete supervised-training benchmark.
- [ ] Discuss calibration cost as a limitation/future resource-accounting question.

## 12. U(1)-conserving case study

- [ ] Explain why the correct null must use the fixed-charge support and actual centered Gram rank.
- [ ] Show that physical low-weight readouts are strongly aligned relative to the sector-corrected random null.
- [ ] Keep finite-size language precise.
- [ ] Separate observation from mechanism: the data establish strong alignment; they do not uniquely establish hydrodynamic causation.
- [ ] Avoid generic claims about symmetry and barren plateaus.
- [ ] Use the U(1) result to reinforce the central thesis: outside isotropy, orientation matters and can be favorable or unfavorable.

## 13. Discussion

- [ ] Organize around positive conclusions before limitations.
- [ ] Distinguish three concepts cleanly: rank baseline, covariance spectrum, readout orientation.
- [ ] State when rank is informative and when it is insufficient.
- [ ] Discuss design implications: measurement/readout co-design, symmetry-adapted features, learned readout subspaces, and finite-shot resource allocation.
- [ ] Do not turn the discussion into the AQNG paper; optimization can be named as a next step only.
- [ ] Consolidate limitations into a compact subsection/paragraph: fixed computational-basis measurement, diagonal/linear readout framework, local tangent/Fisher character, calibration cost, finite-size numerics, no supervised-loss theorem.
- [ ] Avoid repeating the same caveat in Abstract, Introduction, Results, and Conclusion.

## 14. Conclusion

- [ ] Keep concise and forward-looking.
- [ ] First sentence: answer the scientific question directly.
- [ ] Second: state the strongest controlled evidence.
- [ ] Third: state the U(1) counter-regime.
- [ ] Final sentence: identify readout orientation as a quantum-technology design variable at the measurement/classical interface.
- [ ] Do not introduce new claims or literature.

## 15. Figures and tables for AQT

- [ ] Audit main-text display count against the typical 3–8 AQT range.
- [ ] Figure 1 should communicate the entire framework to a broad quantum-technology reader without requiring the main text.
- [ ] Give the equal-rank intervention a main-text figure.
- [ ] Keep a compact generic anisotropy/rank-typicality figure.
- [ ] Keep a compact U(1) structured-contrast figure.
- [ ] Move secondary scaling fits, robustness sweeps, and extended architecture breakdowns to Supporting Information when possible.
- [ ] Use lower-case panel labels consistently.
- [ ] Check fonts/line weights at final single-/double-column dimensions.
- [ ] Ensure legends do not obscure data and remain readable after typesetting.
- [ ] Ensure color choices remain interpretable in grayscale/color-vision-deficiency contexts.

## 16. References and literature positioning

- [ ] Verify every citation supports the exact adjacent claim.
- [ ] Update literature search before submission, especially measurement-induced Fisher geometry, variational quantum trainability, observable/readout locality, symmetry/conservation, random measurements, and quantum natural-gradient context.
- [ ] Cite the isotropic readout-rank paper transparently as prior/companion work if it is public/submitted as allowed by journal policy.
- [ ] Inform the editor about related submitted/in-press manuscripts that bear on this submission, as required by AQT/Wiley policy.
- [ ] Avoid self-citation being used as the sole support for standard results.
- [ ] Ensure bibliography metadata and DOIs are complete where available.

## 17. Reproducibility / integrity

- [ ] Confirm repository commit/tag corresponding exactly to the submitted manuscript.
- [ ] Freeze analysis outputs used for every main-text number.
- [ ] Maintain a result-to-file/script provenance table.
- [ ] Ensure all random seeds/profiles needed for reproduction are archived.
- [ ] Ensure data availability wording points to a stable archival record when available (e.g., Zenodo), not only a mutable branch.
- [ ] Check that no figure is manually altered in a way that changes scientific content.

## 18. AQT submission package

- [ ] AQT main manuscript source/PDF.
- [ ] Separate Supporting Information file.
- [ ] ToC text (50–60 words, third person, general audience).
- [ ] ToC graphic in an accepted size.
- [ ] Cover letter tailored to AQT and its interdisciplinary readership.
- [ ] Data Availability Statement.
- [ ] Funding Statement.
- [ ] Conflict of Interest statement.
- [ ] ORCID and author metadata.
- [ ] Highest-resolution/vector figure files.
- [ ] Any applicable Wiley Data Reporting Checklist.
- [ ] Disclosure of related manuscripts/preprints where required.

## 19. Line-by-line revision protocol

For every paragraph of `spectral_geometry_rewrite.tex`:

- [ ] CLAIM — What single scientific claim is this paragraph making?
- [ ] SUPPORT — Is that claim directly supported by a theorem, citation, or reported dataset?
- [ ] NOVELTY — Is standard background clearly separated from this paper's contribution?
- [ ] SCOPE — Is the wording no stronger than the evidence?
- [ ] AQT — Is the relevance understandable to an interdisciplinary quantum-technology reader?
- [ ] PRECISION — Are measurement, readout, rank, spectrum, orientation, and trainability used consistently?
- [ ] ECONOMY — Can defensive/repetitive text be removed without losing scientific safeguards?
- [ ] CITATION — Does every literature-dependent claim have the right reference?
- [ ] TRANSITION — Does the paragraph logically motivate the next one?
- [ ] STYLE — American English, direct syntax, no unnecessary jargon, no first-person in abstract.

## 20. Final pre-submission gate

- [ ] Abstract <=200 words and compliant with AQT style.
- [ ] 3–7 keywords present.
- [ ] Main scientific contribution is distinguishable from the isotropic-rank paper in <30 seconds of reading title + abstract + first page.
- [ ] AQNG contribution is not prematurely absorbed into this manuscript.
- [ ] Every quantitative headline has a reproducible source.
- [ ] No unsupported asymptotic or causal claims.
- [ ] Main article stands alone without Supporting Information.
- [ ] Figures are publication quality.
- [ ] All required statements and submission metadata are present.
- [ ] Cover letter explicitly explains significance beyond specialists.
- [ ] Final PDF receives a visual/equation/reference preflight before submission.

## Official guide used

Advanced Quantum Technologies, Wiley, Author Guidelines: https://advanced.onlinelibrary.wiley.com/hub/journal/25119044/author-guidelines
