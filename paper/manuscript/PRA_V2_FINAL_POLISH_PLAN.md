# PRA v2 final polish plan

This pass is intentionally non-outcome-changing. It addresses presentation and production robustness only.

## Changes

- Remove duplicated novelty language from the abstract and report the already-frozen n=12 operational gains once.
- State in the main numerical-strategy section that cross-fit calibration data are a separate resource from the fixed evaluation shot budget.
- Add an explicit in-text reference to the half-filled-sector random-orientation control figure.
- Add automated PDF rendering/font/boundary preflight while retaining the requirement for final human visual inspection.
- Make the PRA-v2 automation persist on `main` and future `agent/pra-v2-*` maintenance branches.

## Scientific invariants

- No raw data, frozen profiles, bootstrap seeds, equivalence thresholds, circuit counts, or numerical outcomes are changed.
- The U(1) sector-null audit remains a geometric random-orientation control, not a mechanism-identification test.
- The operational comparison remains a fixed-evaluation-resource diagnostic, not an end-to-end supervised trainability theorem.
