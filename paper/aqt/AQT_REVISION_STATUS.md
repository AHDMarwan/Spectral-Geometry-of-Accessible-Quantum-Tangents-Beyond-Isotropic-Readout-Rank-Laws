# AQT Revision Status

Branch: `aqt-submission`
Target: *Advanced Quantum Technologies* Research Article

## Editorial/scientific rewrite completed

- [x] AQT-specific title and six keywords.
- [x] Abstract rewritten to 175 words, impersonal present tense, no references or displayed equation.
- [x] Introduction fully rewritten for a quantum-technology readership.
- [x] Gross & Rieser (arXiv:2602.18377) added as explicit closest related work; broad novelty claims about subspace visibility/projector geometry removed.
- [x] Separate isotropic rank-law paper positioned as the isotropic baseline rather than duplicated here.
- [x] AQNG kept outside the contribution of this manuscript.
- [x] Main theory rewritten around Fisher-normalized VQC parameter tangents, covariance spectrum, readout rank, and spectral orientation.
- [x] Standard Grassmann moments and Ky Fan optimization identified as reference tools rather than novelty claims.
- [x] Numerical protocol consolidated, including circuit-instance statistical unit, bootstrap, cross-fitting, finite-shot budget, and calibration-cost qualification.
- [x] Generic-circuit results rewritten around near-rank retention coexisting with strong anisotropy.
- [x] Equal-rank physical/random/cross-fitted comparison given central narrative priority.
- [x] Haar-U(4), n=12 headline values retained: 9.584x directional gradient-energy proxy and 3.111x finite-shot SNR.
- [x] U(1) result rewritten around a fixed-charge sector-corrected orientation null.
- [x] Full-record Fisher control retained to locate the generic/U(1) separation at the readout stage.
- [x] Discussion and Conclusion rewritten to remove repeated defensive prose and generic significance language.
- [x] Five-figure main-text plan prepared; secondary diagnostics assigned to Supporting Information.
- [x] AQT-facing references assembled in first-citation order, including Gross & Rieser.
- [x] Cover-letter draft prepared with related-manuscript disclosure language.
- [x] Detailed AI-use disclosure drafted in line with Wiley policy.
- [x] Data Availability draft and 55-word Table-of-Contents text prepared.
- [x] Integrated free-format LaTeX manuscript assembled at `paper/aqt/aqt_spectral_geometry.tex`.
- [x] AQT-specific GitHub Actions build added.
- [x] CI compilation completed successfully for the integrated AQT manuscript with checks for undefined citations and cross-references.

## Files that constitute the AQT working package

- `aqt_spectral_geometry.tex` — integrated manuscript draft.
- `AQT_TITLE_ABSTRACT.tex` — front-matter working copy.
- `AQT_INTRODUCTION_DRAFT.tex` — rewritten Introduction.
- `AQT_MAIN_TEXT_REWRITE.tex` — rewritten theory, methods, results, Discussion, Conclusion.
- `AQT_MAIN_FIGURES.tex` — recommended five main figures and captions.
- `AQT_REFERENCES.tex` — AQT-facing reference list.
- `AQT_SUPPORTING_INFORMATION_PLAN.md` — main/SI split.
- `AQT_RELATED_WORK_AUDIT.md` — novelty boundary versus Gross & Rieser.
- `AQT_COVER_LETTER_DRAFT.txt` — journal-specific cover letter.
- `AQT_SUBMISSION_METADATA.tex` — disclosure, data statement, ToC text, and unresolved metadata.
- `AQT_REVISION_CHECKLIST.md` — journal/scientific checklist.
- `AQT_WRITING_STYLE_GUIDE.md` — prose audit.
- `AQT_LINE_BY_LINE_LOG.md` — editorial rationale and change log.

## Author-confirmation blockers before submission

These fields cannot be inferred or invented from the manuscript:

1. Complete affiliation wording for the title page.
2. Institutional/company corresponding-author email requested by the AQT author guidance.
3. Funding statement.
4. Conflict-of-interest statement.
5. Status of the AQNG manuscript: if submitted, in press, or planned for imminent submission, it should be disclosed to the editor as related work.
6. Submission-specific archival release/DOI or frozen tag for the numerical record.
7. Original Table-of-Contents graphic.

## Final technical pass after author metadata is supplied

- Replace all `TO CONFIRM` placeholders.
- Freeze the final data/code release and update Data Availability.
- Insert final ToC graphic.
- Re-run CI compilation and PDF visual preflight.
- Check word count and main-text display count on the final assembled version.
- Verify every reference against the final numbered citation order.
- Create the submission-ready source/PDF/SI package.

No scientific claim should be strengthened during this final pass unless a theorem, cited source, or archived result directly supports the change.
