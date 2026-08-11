# Final scientific consistency QA

This checklist is the last production pass before treating the manuscript as submission-ready.

## Theory and equations

- [x] `R = Tr(PC)` is presented as the paper's measurement-accessible tangent-mass definition in this VQC setting, not as a generally new projector identity.
- [x] The Grassmann mean `E Tr(PC)=r/N` is framed as a standard random-subspace baseline and cited to Grassmann/Weingarten prior art.
- [x] The variance formula is attributed to standard Grassmann projector moments; the manuscript interpretation in terms of `d_eff` is separated from priority claims.
- [x] `d_eff = 1/Tr(C^2)` is used as a participation-ratio/effective-dimension diagnostic, not as a new definition of effective rank in the literature.
- [x] The Ky Fan optimum is explicitly cited as standard spectral optimization.
- [x] Fixed-weight rank formulas are combinatorial identities and are not presented as literature novelty.

## Numerical provenance

- [x] Circuit instance, not tangent direction, is the independent statistical unit.
- [x] Circuit-level bootstrap is cited to Efron and described consistently.
- [x] Frozen profiles, source code, aggregate tables, shard outputs, and paper-facing summaries are cited to `AitHaddou2026MeasurementAccessible`.
- [x] Main numerical result paragraphs are individually tied to `AitHaddou2026MeasurementAccessible`, so the repository is the provenance reference for reported values.
- [x] The final U(1) n=18 values use 20 independent circuit instances.
- [x] Power-vs-exponential comparison is described as finite-size model discrimination only.
- [x] The symmetry-breaking experiment is labeled a pilot/sensitivity control, not a mechanism-identification result.
- [x] The half-filled-sector random-orientation null is included as a geometric control and is not presented as a mechanism-identification result.
- [x] Cross-fit calibration data are explicitly accounted for as a separate resource from the fixed evaluation shot budget.

## Claim control

- [x] No claim that the random-projector expectation `r/N` is a new theorem.
- [x] No claim that rank typicality implies isotropy.
- [x] No claim that the tested physical circuits converge to Haar orientation.
- [x] No supervised barren-plateau or task-loss scaling claim is made from the directional gradient/SNR experiment.
- [x] U(1) is a structured case study, not the novelty pillar.
- [x] No hydrodynamic mechanism or asymptotic exponent is claimed.
- [x] Closest prior art on Hamming-weight-preserving trainability, DLA/adjoint structure, low-bodyness concentration, fixed-charge slice geometry, random-measurement Fisher geometry, and readout-visible equivariant coherence is acknowledged.
- [x] The abstract states the frozen equal-rank operational result once and uses the same conservative novelty framing as the conclusion and PRA cover letter.

## Figures and PDF production

- [x] PennyLane circuit schematics are generated from the same gate-order definitions used by the simulator.
- [x] Circuit gate parameters are hidden in publication drawings; only gate names are shown.
- [x] Production data figures use enlarged, repositioned, or shared legends to avoid covering data.
- [x] U(1) scaling figure reports bootstrap intervals and both finite-size fits; its `alpha`/`Delta AICc` annotations render on separate lines.
- [x] Symmetry-breaking figure includes the visual rank baseline with an explicit caveat that it is not a sector-Haar null.
- [x] The fixed-charge sector-null figure renders cleanly and makes the same-sector null comparison explicit.
- [x] Automated canonical-PDF preflight passes: 15 pages, 71 embedded fonts, 48 px minimum raster ink margin at 120 dpi, no nearly blank pages, no outer-boundary ink contact, and zero LaTeX overfull-box warnings.
- [x] The exact canonical 15-page PDF was exposed through the read-only visual-QA artifact workflow and inspected at 180 dpi. The full 15-page contact sheet and key pages (title/abstract, numerical strategy/resource accounting, sector-null figure, U(1) scaling/symmetry-control page, and final reference page) show no clipping, legend collisions, broken annotation text, or caption overflow.
- [x] The sparse final reference page is an intentional continuation of the bibliography, not a blank-page production error.

## Submission package status

- [x] `paper/manuscript/spectral_geometry.pdf` is the canonical PRA-targeted manuscript.
- [x] `paper/manuscript/spectral_geometry_submission_package.zip` is generated only after the hardened production workflow re-applies PRA-v2 invariants and passes the PDF preflight.
- [x] `paper/manuscript/PRA_COVER_LETTER.txt` uses the same conservative novelty framing and documented limitations as the manuscript.
- [x] The production workflow is hardened so legacy manuscript-generation steps cannot silently reintroduce pre-v2 prose or remove the sector-null/resource-accounting controls.
- [x] The canonical-PDF visual-QA artifact workflow provides the exact current PDF for future page-by-page inspection without rebuilding it.

## Final status

**Submission-ready from the repository/production-QA side.**

Remaining actions are external submission actions only (journal portal metadata/upload and any author-side declarations required by the submission form). No scientific or production blocker remains in the repository at this checkpoint.
