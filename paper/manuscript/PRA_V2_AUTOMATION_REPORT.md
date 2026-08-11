# PRA v2 automation report

Status: all technical, manuscript, and automated PDF-preflight gates passed in this job.

## Added referee-facing controls

- Half-filled-sector random-orientation null for A_k.
- n=18 one-body observed/null ratio: 811.0x.
- n=18 weight-through-two observed/null ratio: 148.3x.
- Cross-fit resource accounting: 128 fit tangents, 128 held-out evaluation tangents, 10000 evaluation shots, 8 finite-difference directions.
- Abstract novelty framing now reports the frozen n=12 operational gains once, without repetition.
- REVTeX target is PRA.

## Interpretation guardrails

The sector-null control is geometric and does not identify the U(1) mechanism. The fixed-shot comparison isolates evaluation-time orientation effects; calibration cost for learning the aligned projector remains separate. Automated PDF preflight does not replace final human visual inspection.
