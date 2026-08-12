# AQT Revision Status

Branch: `aqt-submission`
Target: *Advanced Quantum Technologies* Research Article

## Editorial/scientific rewrite completed

- [x] AQT-specific title and six keywords.
- [x] Abstract rewritten to <=200 words, impersonal present tense, no references or displayed equation.
- [x] Introduction fully rewritten for a quantum-technology readership.
- [x] Gross & Rieser (arXiv:2602.18377) added as explicit closest related work; broad novelty claims about subspace visibility/projector geometry removed.
- [x] Separate isotropic rank-law paper positioned as the isotropic baseline rather than duplicated here.
- [x] AQNG kept outside the contribution of this manuscript; current status recorded as an unsubmitted manuscript in preparation.
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
- [x] Cover letter finalized for current metadata and related-work status.
- [x] AI-use disclosure updated, including assistance with the schematic graphical ToC; no AI-generated or AI-altered research data/results.
- [x] Data Availability draft prepared pending the final Zenodo DOI.
- [x] 55-word Table-of-Contents text prepared.
- [x] Original 110 mm x 20 mm graphical-ToC schematic prepared in SVG plus a reproducible Python generator.
- [x] Integrated free-format LaTeX manuscript assembled at `paper/aqt/aqt_spectral_geometry.tex`.
- [x] AQT-specific GitHub Actions build added and previously compiled successfully with checks for undefined citations and cross-references.

## Author metadata confirmed

- [x] Affiliation: `Independent Researcher`.
- [x] Corresponding email: `aithaddou.marwan@outlook.com`.
- [x] Conflict of Interest: `The author declares no conflict of interest.`
- [x] Funding: `The author received no specific funding for this work.`
- [x] AQNG status: manuscript in preparation only; not submitted and not posted as a preprint.

## Reproducibility release preparation

- [x] `.zenodo.json` added at repository root with AQT-specific metadata.
- [x] `CITATION.cff` updated to version `0.2.0` and the AQT-facing title.
- [x] Frozen release-candidate branch created: `aqt-release-v0.2.0`.
- [ ] Create the GitHub **Release** from the frozen AQT release-candidate commit and assign tag `v0.2.0`.
- [ ] Ensure this GitHub repository is enabled in the author's Zenodo GitHub integration.
- [ ] Wait for Zenodo to ingest the GitHub release and mint the version DOI.
- [ ] Replace the pending sentence in the Data Availability Statement with that DOI.

The GitHub connector available in this editing session can create branches and repository files but does not expose GitHub Release/tag publication or authenticated Zenodo deposition actions. Those final publication clicks therefore remain an author-side action.

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
- `AQT_SUBMISSION_METADATA.tex` — final author declarations plus pending DOI.
- `AQT_TOC_GRAPHIC.svg` — graphical ToC source at the required wide aspect ratio.
- `make_aqt_toc_graphic.py` — reproducible PNG/SVG generator.
- `AQT_REVISION_CHECKLIST.md` — journal/scientific checklist.
- `AQT_WRITING_STYLE_GUIDE.md` — prose audit.
- `AQT_LINE_BY_LINE_LOG.md` — editorial rationale and change log.

## Remaining final-pass items

1. Publish GitHub release/tag `v0.2.0` and obtain the Zenodo version DOI.
2. Insert DOI into Data Availability and cover-letter reproducibility sentence if desired.
3. Re-run AQT CI after the final DOI insertion.
4. Run final PDF visual preflight and word/display-item count.
5. Assemble the Supporting Information as a separate final file.
6. Export the graphical ToC to the exact file format preferred at upload (the 110 mm x 20 mm PNG preview is 1300 px wide; the SVG source is preserved).
7. Create the final submission-ready source/PDF/SI package.
