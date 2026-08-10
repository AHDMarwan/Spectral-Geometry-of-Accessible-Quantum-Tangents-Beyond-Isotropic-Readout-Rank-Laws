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

## Claim control

- [x] No claim that the random-projector expectation `r/N` is a new theorem.
- [x] No claim that rank typicality implies isotropy.
- [x] No claim that the tested physical circuits converge to Haar orientation.
- [x] No supervised barren-plateau or task-loss scaling claim is made from the directional gradient/SNR experiment.
- [x] U(1) is a structured case study, not the novelty pillar.
- [x] No hydrodynamic mechanism or asymptotic exponent is claimed.
- [x] Closest prior art on Hamming-weight-preserving trainability, DLA/adjoint structure, low-bodyness concentration, fixed-charge slice geometry, random-measurement Fisher geometry, and readout-visible equivariant coherence is acknowledged.

## Figures

- [x] PennyLane circuit schematics are generated from the same gate-order definitions used by the simulator.
- [x] Circuit gate parameters are hidden in publication drawings; only gate names are shown.
- [x] Production data figures use enlarged, repositioned, or shared legends to avoid covering data.
- [x] U(1) scaling figure reports bootstrap intervals and both finite-size fits.
- [x] Symmetry-breaking figure includes the visual rank baseline with an explicit caveat that it is not a sector-Haar null.
- [ ] Final canonical PDF should still be inspected page-by-page after each production build for clipping, legend collisions, caption wrapping, and two-column readability.

## Final blockers before submission

1. Inspect the newest canonical `paper/prx/spectral_geometry_prx.pdf` visually after the final bot build.
2. Confirm there are no undefined citations, missing figure files, overfull boxes that visibly clip text, or stale figures.
3. Confirm the title, abstract, conclusion, and cover letter use the same conservative novelty framing.
4. Freeze the submission package only after the final PDF visual inspection passes.
