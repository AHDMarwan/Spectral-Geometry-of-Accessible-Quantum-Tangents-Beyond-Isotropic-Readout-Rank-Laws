from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


HAAR = "SU2-HaarU4-brickwork"
RY = "RY-RZ-CZ-line"
U1 = "U1-RZ-XY-line"
EQ_LOW = 0.90
EQ_HIGH = 1.10


def _one(frame: pd.DataFrame, **where) -> pd.Series:
    mask = pd.Series(True, index=frame.index)
    for key, value in where.items():
        mask &= frame[key] == value
    rows = frame[mask]
    if len(rows) != 1:
        raise ValueError(f"expected one row for {where}, found {len(rows)}")
    return rows.iloc[0]


def _family_ready(family_summary: pd.DataFrame, family: str, k: int) -> bool:
    row = _one(family_summary, family=family, n=20, k=k, metric="enhancement")
    return bool(row["inference_ready"])


def _z_row(bridge_summary: pd.DataFrame, family: str, k: int) -> pd.Series:
    return _one(bridge_summary, family=family, n=20, k=k, metric="population_orientation_z")


def _rho_bridge_row(bridge_summary: pd.DataFrame, family: str, k: int) -> pd.Series:
    return _one(bridge_summary, family=family, n=20, k=k, metric="enhancement")


def _rank_row(rank_equiv: pd.DataFrame, family: str, k: int) -> pd.Series:
    return _one(rank_equiv, n=20, k=k, group=family)


def _decision_row(
    hypothesis: str,
    family: str,
    k: int,
    ready: bool,
    supported: bool,
    rule: str,
    rho_mean: float,
    rho_lo: float,
    rho_hi: float,
    z_mean: float | None = None,
    z_lo: float | None = None,
    z_hi: float | None = None,
) -> dict:
    status = "confirmed" if ready and supported else "not_confirmed" if ready else "insufficient_precision"
    return {
        "hypothesis": hypothesis,
        "family": family,
        "n": 20,
        "k": k,
        "decision_status": status,
        "ready": ready,
        "rule": rule,
        "rho_mean": rho_mean,
        "rho_ci95_low": rho_lo,
        "rho_ci95_high": rho_hi,
        "z_pop_mean": z_mean,
        "z_pop_ci95_low": z_lo,
        "z_pop_ci95_high": z_hi,
    }


def evaluate(
    rank_equivalence_path: str | Path,
    family_summary_path: str | Path,
    bridge_summary_path: str | Path,
    bridge_manifest_path: str | Path,
    output_dir: str | Path,
) -> Path:
    rank = pd.read_csv(rank_equivalence_path)
    family = pd.read_csv(family_summary_path)
    bridge = pd.read_csv(bridge_summary_path)
    manifest = json.loads(Path(bridge_manifest_path).read_text(encoding="utf-8"))
    purity_valid = int(manifest.get("invalid_population_purity_estimator_rows", -1)) == 0

    rows: list[dict] = []

    for k in (1, 2):
        rr = _rank_row(rank, HAAR, k)
        zr = _z_row(bridge, HAAR, k)
        ready = _family_ready(family, HAAR, k) and purity_valid
        rho_lo, rho_hi = float(rr.ci95_low), float(rr.ci95_high)
        rows.append(_decision_row(
            f"H1_Haar_rank_typical_k{k}", HAAR, k, ready,
            rho_lo >= EQ_LOW and rho_hi <= EQ_HIGH,
            "entire rho 95% CI inside [0.90,1.10]",
            float(rr.mean_enhancement), rho_lo, rho_hi,
            float(zr["mean"]), float(zr.ci95_low), float(zr.ci95_high),
        ))
        rows.append(_decision_row(
            f"H2_Haar_negative_bias_k{k}", HAAR, k, ready,
            rho_hi < 1.0 and float(zr.ci95_high) < 0.0,
            "entire rho 95% CI below 1 and entire z_pop 95% CI below 0",
            float(rr.mean_enhancement), rho_lo, rho_hi,
            float(zr["mean"]), float(zr.ci95_low), float(zr.ci95_high),
        ))

    rr1 = _rank_row(rank, RY, 1)
    zr1 = _z_row(bridge, RY, 1)
    ready1 = _family_ready(family, RY, 1) and purity_valid
    rows.append(_decision_row(
        "H3_RY_k1_structural_exception", RY, 1, ready1,
        float(rr1.ci95_high) < EQ_LOW,
        "entire rho_1 95% CI below 0.90",
        float(rr1.mean_enhancement), float(rr1.ci95_low), float(rr1.ci95_high),
        float(zr1["mean"]), float(zr1.ci95_low), float(zr1.ci95_high),
    ))

    rr2 = _rank_row(rank, RY, 2)
    zr2 = _z_row(bridge, RY, 2)
    ready2 = _family_ready(family, RY, 2) and purity_valid
    rows.append(_decision_row(
        "H4_RY_k2_rank_typical", RY, 2, ready2,
        float(rr2.ci95_low) >= EQ_LOW and float(rr2.ci95_high) <= EQ_HIGH,
        "entire rho_2 95% CI inside [0.90,1.10]",
        float(rr2.mean_enhancement), float(rr2.ci95_low), float(rr2.ci95_high),
        float(zr2["mean"]), float(zr2.ci95_low), float(zr2.ci95_high),
    ))
    rows.append(_decision_row(
        "H4b_RY_k2_negative_bias", RY, 2, ready2,
        float(rr2.ci95_high) < 1.0 and float(zr2.ci95_high) < 0.0,
        "entire rho_2 95% CI below 1 and entire z_pop 95% CI below 0",
        float(rr2.mean_enhancement), float(rr2.ci95_low), float(rr2.ci95_high),
        float(zr2["mean"]), float(zr2.ci95_low), float(zr2.ci95_high),
    ))

    for k in (1, 2):
        rr = _rho_bridge_row(bridge, U1, k)
        zr = _z_row(bridge, U1, k)
        ready = _family_ready(family, U1, k) and purity_valid
        rho_lo, rho_hi = float(rr.ci95_low), float(rr.ci95_high)
        rows.append(_decision_row(
            f"H5_U1_positive_alignment_k{k}", U1, k, ready,
            rho_lo > EQ_HIGH and float(zr.ci95_low) > 0.0,
            "entire rho 95% CI above 1.10 and entire z_pop 95% CI above 0",
            float(rr["mean"]), rho_lo, rho_hi,
            float(zr["mean"]), float(zr.ci95_low), float(zr.ci95_high),
        ))

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    decisions = pd.DataFrame(rows)
    decisions.to_csv(out / "confirmatory_decisions.csv", index=False)
    summary = {
        "profile": "v3_n20_orientation_confirmatory",
        "decision_rules_frozen_before_outcomes": True,
        "equivalence_band": [EQ_LOW, EQ_HIGH],
        "population_purity_rows_valid": purity_valid,
        "confirmed": int((decisions.decision_status == "confirmed").sum()),
        "not_confirmed": int((decisions.decision_status == "not_confirmed").sum()),
        "insufficient_precision": int((decisions.decision_status == "insufficient_precision").sum()),
        "note": "A not_confirmed prediction is retained as a scientific negative result. The normalized bridge ratio is secondary because it is algebraically coupled to rho.",
    }
    (out / "confirmatory_manifest.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate frozen v3 n20 orientation-confirmatory decision rules")
    parser.add_argument("--rank-equivalence", required=True)
    parser.add_argument("--family-summary", required=True)
    parser.add_argument("--bridge-summary", required=True)
    parser.add_argument("--bridge-manifest", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    evaluate(args.rank_equivalence, args.family_summary, args.bridge_summary, args.bridge_manifest, args.output)


if __name__ == "__main__":
    main()
