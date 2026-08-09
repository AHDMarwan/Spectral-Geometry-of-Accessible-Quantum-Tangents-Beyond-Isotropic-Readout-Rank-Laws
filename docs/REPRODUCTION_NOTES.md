# Reproduction notes and provenance

The repository was rebuilt from three research notebooks supplied with the manuscript draft. Their exact JSON files are retained under `legacy/` for provenance; the production code in `src/aqt/` is the version intended for reproducible runs.

A specific scheduling inconsistency was found in the confirmatory notebook: the configuration declares `u1_confirm_instances = 12`, but the main schedule iterates only over the generic `INSTANCES = 6` value for every family. The later dataframe filter allows U(1) instance indices below 12, but a fresh execution of that notebook does not create indices 6--11. The manuscript, however, states that twelve U(1) circuits per size were used.

The `reproduce_paper` profile therefore implements the protocol stated in the manuscript explicitly: six instances for each of the three generic families and twelve for U(1), at n=6,8,10, d=6n, with 48 tangent directions. The analysis writes `paper_reproduction_comparison.csv`. It does not fail the workflow when the rerun differs from the manuscript; any discrepancy is evidence to investigate, not something to hide.

The expanded PRA profiles use new master seeds and are kept separate from the reproduction profile. This prevents accidental tuning on the original random realization.
