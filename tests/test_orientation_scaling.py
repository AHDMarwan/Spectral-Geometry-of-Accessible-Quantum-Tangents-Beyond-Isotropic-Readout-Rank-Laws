import numpy as np
import pandas as pd

from aqt.orientation_scaling import fit_scaling, summarize_cells


def _synthetic_frame():
    rows = []
    for family, g_by_n, rho_by_n in [
        ("SU2-HaarU4-brickwork", {6: 0.12, 10: 0.08, 14: 0.05}, {6: 0.96, 10: 0.97, 14: 0.98}),
        ("RY-RZ-CZ-line", {6: 0.10, 10: 0.09, 14: 0.09}, {6: 0.94, 10: 0.89, 14: 0.87}),
        ("U1-RZ-XY-line", {6: 2.0, 10: 10.0, 14: 40.0}, {6: 2.0, 10: 10.0, 14: 40.0}),
    ]:
        for n, g in g_by_n.items():
            for instance in range(6):
                rows.append(
                    {
                        "family": family,
                        "n": n,
                        "k": 1,
                        "circuit_id": f"{family}|n{n}|i{instance}",
                        "enhancement": rho_by_n[n] + 0.001 * (instance - 2.5),
                        "orientation_growth_ratio": g * (1.0 + 0.01 * (instance - 2.5)),
                        "population_orientation_z": 1.0,
                        "r_times_deff": 100.0 * n,
                    }
                )
    return pd.DataFrame(rows)


def test_cell_summary_preserves_circuit_unit():
    out = summarize_cells(_synthetic_frame(), master_seed=1)
    row = out[
        (out.family == "SU2-HaarU4-brickwork")
        & (out.n == 14)
        & (out.k == 1)
        & (out.metric == "orientation_growth_ratio")
    ].iloc[0]
    assert row.circuits == 6
    assert row.ci95_low <= row["mean"] <= row.ci95_high


def test_scaling_screen_separates_three_patterns():
    fits = fit_scaling(_synthetic_frame(), master_seed=2)
    haar = fits[fits.family == "SU2-HaarU4-brickwork"].iloc[0]
    ry = fits[fits.family == "RY-RZ-CZ-line"].iloc[0]
    u1 = fits[fits.family == "U1-RZ-XY-line"].iloc[0]
    assert haar.finite_size_trend == "decreasing"
    assert haar.screening_label == "rank_typical_at_largest_n"
    assert ry.screening_label == "structured_rank_law_deviation_at_largest_n"
    assert u1.finite_size_trend == "increasing"
    assert u1.screening_label == "symmetry_aligned_outside_random_orientation_scale"
    assert np.isfinite(haar.plateau_intercept_c)
