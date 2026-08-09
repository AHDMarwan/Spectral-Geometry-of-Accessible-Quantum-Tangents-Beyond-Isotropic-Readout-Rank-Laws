import json

import pandas as pd

from aqt.v3_orientation_confirmatory import evaluate


def test_v3_decision_rules(tmp_path):
    rank = pd.DataFrame(
        [
            {"n": 20, "k": 1, "group": "SU2-HaarU4-brickwork", "mean_enhancement": 0.94, "ci95_low": 0.92, "ci95_high": 0.96},
            {"n": 20, "k": 2, "group": "SU2-HaarU4-brickwork", "mean_enhancement": 0.96, "ci95_low": 0.95, "ci95_high": 0.97},
            {"n": 20, "k": 1, "group": "RY-RZ-CZ-line", "mean_enhancement": 0.87, "ci95_low": 0.85, "ci95_high": 0.89},
            {"n": 20, "k": 2, "group": "RY-RZ-CZ-line", "mean_enhancement": 0.93, "ci95_low": 0.92, "ci95_high": 0.94},
        ]
    )
    family_rows = []
    for fam in ["SU2-HaarU4-brickwork", "RY-RZ-CZ-line", "U1-RZ-XY-line"]:
        for k in [1, 2]:
            family_rows.append({"family": fam, "n": 20, "k": k, "metric": "enhancement", "inference_ready": True})
    family = pd.DataFrame(family_rows)
    bridge_rows = []
    for fam, rho1, rho2, z1, z2 in [
        ("SU2-HaarU4-brickwork", 0.94, 0.96, -8.0, -12.0),
        ("RY-RZ-CZ-line", 0.87, 0.93, -10.0, -14.0),
        ("U1-RZ-XY-line", 1000.0, 200.0, 1000.0, 700.0),
    ]:
        for k, rho, z in [(1, rho1, z1), (2, rho2, z2)]:
            bridge_rows.extend(
                [
                    {"family": fam, "n": 20, "k": k, "metric": "enhancement", "mean": rho, "ci95_low": rho * 0.98, "ci95_high": rho * 1.02},
                    {"family": fam, "n": 20, "k": k, "metric": "population_orientation_z", "mean": z, "ci95_low": z - 1.0, "ci95_high": z + 1.0},
                ]
            )
    bridge = pd.DataFrame(bridge_rows)

    rank_path = tmp_path / "rank.csv"
    family_path = tmp_path / "family.csv"
    bridge_path = tmp_path / "bridge.csv"
    bridge_manifest_path = tmp_path / "bridge_manifest.json"
    rank.to_csv(rank_path, index=False)
    family.to_csv(family_path, index=False)
    bridge.to_csv(bridge_path, index=False)
    bridge_manifest_path.write_text(json.dumps({"invalid_population_purity_estimator_rows": 0}))

    out = evaluate(rank_path, family_path, bridge_path, bridge_manifest_path, tmp_path / "out")
    decisions = pd.read_csv(out / "confirmatory_decisions.csv")
    assert len(decisions) == 9
    assert set(decisions.decision_status) == {"confirmed"}
