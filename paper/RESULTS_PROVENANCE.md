# Rigorous-v2 primary Results provenance

This directory contains the paper-ready Results text derived only from the frozen `rigorous-v2` primary campaign.

- GitHub Actions run: `31313459321`
- Profile: `profiles/v2_primary.json`
- Frozen head commit executed by the workflow: `60064d92739ccff423e085fc8a5f8c6489e764e6`
- Consolidated artifact: `rigorous-v2_primary-analysis`
- Artifact id: `9038174847`
- Artifact SHA-256 digest reported by GitHub Actions: `1045b04856dd9a4893cae91a2ea969ce89a3da86f91e301c9c18dc923da06d46`
- Scientific-results source file: `paper/RESULTS_RIGOROUS_V2.tex`

## Technical validation

The artifact's `technical_validation.json` reported `valid: true`. All scheduled jobs and all scheduled prefix/readout rows were present. The numerical-validity maxima were:

- state-norm error: `2.520206265899105e-14`
- horizontal-overlap maximum: `4.507682478015467e-15`
- probability-sum error: `2.5091040356528535e-14`
- probability-tangent zero-sum error: `1.8041124150158796e-16`
- maximum `F_full - F_Q`: `-0.0430811468556428`
- minimum empirical covariance/projector-bound slack: `0.1608014711186547`

No scientific-sign or magnitude criterion is part of this technical validity gate.

## Files used from the consolidated artifact

The Results section was written from the following prespecified outputs:

- `pooled_summary.csv`
- `family_summary.csv`
- `rank_law_equivalence.csv`
- `u1_vs_generic_contrasts.csv`
- `anisotropy_normalized.csv`
- `leave_one_family_out.csv`
- `technical_validation.json`

Legacy reproduction tables and pre-rigorous-v2 numerical outcomes were not used.

## Interpretation boundary

The primary run uses `M=128` tangent directions per fixed circuit. Under the frozen preregistration, the strongest convergence-sensitive wording remains conditional on the separate `v2_convergence` campaign with nested `M=32,64,128,256`. The current Results section therefore reports the primary estimates and their circuit-level uncertainty without claiming an asymptotic law or an already-verified tangent-sample convergence statement.
