import pandas as pd

from aqt.rigorous_inference import (
    family_balanced_bootstrap,
    u1_minus_generic_bootstrap,
)
from aqt.rigorous_paired import _paired_contrasts


def test_family_balanced_estimator_does_not_weight_by_circuit_count():
    frame = pd.DataFrame(
        {
            "family": ["A", "A", "A", "B"],
            "metric": [1.0, 1.0, 1.0, 3.0],
        }
    )
    mean, lo, hi = family_balanced_bootstrap(frame, "metric", 123, 2000)
    assert mean == 2.0
    assert lo <= mean <= hi


def test_u1_minus_generic_uses_family_balanced_generic_reference():
    generic = pd.DataFrame(
        {
            "family": ["A", "A", "A", "B", "B"],
            "metric": [1.0, 1.0, 1.0, 3.0, 3.0],
        }
    )
    u1 = pd.DataFrame({"family": ["U1", "U1"], "metric": [4.0, 4.0]})
    diff, lo, hi = u1_minus_generic_bootstrap(u1, generic, "metric", 456, 2000)
    assert diff == 2.0
    assert lo <= diff <= hi


def test_basis_robustness_is_paired_within_circuit(tmp_path):
    rows = []
    for instance in range(5):
        for basis, shift in [("Z", 0.0), ("X", 0.2)]:
            rows.append(
                {
                    "profile": "v2_basis",
                    "family": "A",
                    "n": 8,
                    "depth_factor": 6.0,
                    "instance": instance,
                    "direction_sampler": "gaussian",
                    "measurement_basis": basis,
                    "bitflip_rate": 0.0,
                    "tangent_count_used": 128,
                    "k": 1,
                    "enhancement": 1.0 + shift,
                    "actual_retention": 0.1 + shift,
                    "deff_pairwise": 10.0 + shift,
                    "pairwise_purity": 0.1 + shift,
                    "Ffull_over_FQ_mean": 0.5 + shift,
                    "physical_minus_rank_baseline": 0.01 + shift,
                }
            )
    frame = pd.DataFrame(rows)
    output = tmp_path / "paired.csv"
    _paired_contrasts(frame, "measurement_basis", "Z", output, 789)
    result = pd.read_csv(output)
    row = result[(result.metric == "enhancement") & (result.comparison == "X")].iloc[0]
    assert abs(row.mean_paired_difference - 0.2) < 1e-12
    assert row.paired_circuits == 5
