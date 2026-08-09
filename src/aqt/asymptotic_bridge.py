from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .core import stable_seed
from .stats import bootstrap_mean_ci


BOOTSTRAP_RESAMPLES = 10_000
ANALYSIS_STATUS = "exploratory_post_hoc"


def haar_rank_law_variance_rho(
    score_dimension: int,
    readout_rank: int,
    purity: float,
) -> float:
    """Exact Haar/Grassmann variance of rho = Tr(PC)/(r/N).

    Here C is positive semidefinite with Tr(C)=1, P is an independent
    Haar-random real rank-r projector in N dimensions, and
    purity=Tr(C^2).  The formula is conditional on C.
    """
    N = int(score_dimension)
    r = int(readout_rank)
    q = float(purity)
    if N < 2:
        raise ValueError("score_dimension must be at least 2")
    if not 1 <= r < N:
        raise ValueError("readout_rank must satisfy 1 <= r < score_dimension")
    if not np.isfinite(q):
        return float("nan")
    tol = 64.0 * np.finfo(float).eps
    if q < 1.0 / N - tol or q > 1.0 + tol:
        return float("nan")
    q = min(1.0, max(1.0 / N, q))
    value = 2.0 * (N - r) * (N * q - 1.0) / (r * (N - 1) * (N + 2))
    return float(max(0.0, value))


def haar_rank_law_variance_bound(
    readout_rank: int,
    purity: float,
) -> float:
    """Upper bound 2/(r d_eff) = 2 Tr(C^2)/r for Var(rho)."""
    r = int(readout_rank)
    q = float(purity)
    if r < 1:
        raise ValueError("readout_rank must be positive")
    if not np.isfinite(q) or q < 0.0:
        return float("nan")
    return float(2.0 * q / r)


def low_weight_readout_rank(n: int, k: int) -> int:
    """Rank of nonconstant diagonal Z strings of weight at most k."""
    from math import comb

    n = int(n)
    k = int(k)
    if n < 1 or not 1 <= k <= n:
        raise ValueError("require n >= 1 and 1 <= k <= n")
    return int(sum(comb(n, j) for j in range(1, k + 1)))


def add_population_bridge_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Add population-purity orientation-null diagnostics to circuit rows.

    The pairwise U-statistic is used as an estimator of Tr(C^2).  Rows whose
    estimator lies outside the population PSD interval [1/N, 1] are retained
    but their population-null sigma/z diagnostics are marked NaN rather than
    clipped into an apparently valid scientific result.
    """
    required = {
        "profile",
        "circuit_id",
        "family",
        "n",
        "k",
        "score_dimension",
        "readout_rank",
        "enhancement",
        "pairwise_purity",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    out = frame.copy()
    N = out["score_dimension"].to_numpy(int)
    r = out["readout_rank"].to_numpy(int)
    purity = out["pairwise_purity"].to_numpy(float)
    rho = out["enhancement"].to_numpy(float)

    sigma2 = np.full(len(out), np.nan, dtype=float)
    bound = np.full(len(out), np.nan, dtype=float)
    valid = np.zeros(len(out), dtype=bool)
    for i, (Ni, ri, qi) in enumerate(zip(N, r, purity)):
        sigma2[i] = haar_rank_law_variance_rho(Ni, ri, qi)
        bound[i] = haar_rank_law_variance_bound(ri, qi)
        valid[i] = np.isfinite(sigma2[i])

    sigma = np.sqrt(sigma2)
    z = np.full(len(out), np.nan, dtype=float)
    nonzero = valid & (sigma > 0.0) & np.isfinite(rho)
    z[nonzero] = (rho[nonzero] - 1.0) / sigma[nonzero]
    exact_iso = valid & (sigma == 0.0) & np.isfinite(rho) & np.isclose(rho, 1.0)
    z[exact_iso] = 0.0

    deff = np.full(len(out), np.nan, dtype=float)
    positive = np.isfinite(purity) & (purity > 0.0)
    deff[positive] = 1.0 / purity[positive]
    r_times_deff = r.astype(float) * deff

    out["analysis_status"] = ANALYSIS_STATUS
    out["population_purity_estimate_valid"] = valid
    out["deff_from_pairwise_purity"] = deff
    out["r_times_deff"] = r_times_deff
    out["haar_population_var_rho"] = sigma2
    out["haar_population_sd_rho"] = sigma
    out["haar_population_var_bound"] = bound
    out["population_orientation_z"] = z
    out["abs_population_orientation_z"] = np.abs(z)
    out["orientation_growth_ratio"] = np.abs(z) / np.sqrt(r_times_deff)
    out["chebyshev_bound_abs_rho_minus_1_ge_0p1"] = np.minimum(
        1.0, sigma2 / 0.01
    )
    return out


def _load(paths: Iterable[str | Path]) -> pd.DataFrame:
    frames = []
    for path in paths:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(p)
        f = pd.read_csv(p)
        if len(f):
            f = f.copy()
            f["source_path"] = p.as_posix()
            frames.append(f)
    if not frames:
        raise ValueError("no nonempty input tables")
    df = pd.concat(frames, ignore_index=True)
    dedup = [
        c
        for c in (
            "profile",
            "circuit_id",
            "direction_sampler",
            "measurement_basis",
            "bitflip_rate",
            "tangent_count_used",
            "k",
        )
        if c in df.columns
    ]
    return df.drop_duplicates(subset=dedup, keep="first")


def summarize_bridge(frame: pd.DataFrame, master_seed: int = 77124000) -> pd.DataFrame:
    metrics = (
        "enhancement",
        "actual_retention",
        "deff_from_pairwise_purity",
        "r_times_deff",
        "haar_population_sd_rho",
        "population_orientation_z",
        "orientation_growth_ratio",
    )
    group_cols = ["family", "n", "k"]
    rows: list[dict] = []
    for key, group in frame.groupby(group_cols, dropna=False):
        meta = dict(zip(group_cols, key))
        circuits = int(group["circuit_id"].nunique())
        for metric in metrics:
            x = pd.to_numeric(group[metric], errors="coerce")
            x = x[np.isfinite(x)]
            if len(x) == 0:
                continue
            seed = stable_seed(
                "exploratory-asymptotic-bridge|"
                + "|".join(map(str, key))
                + "|"
                + metric,
                master_seed,
            )
            mean, lo, hi = bootstrap_mean_ci(
                x,
                seed,
                n_resamples=BOOTSTRAP_RESAMPLES,
                confidence=0.95,
            )
            rows.append(
                {
                    **meta,
                    "analysis_status": ANALYSIS_STATUS,
                    "metric": metric,
                    "mean": mean,
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "circuits": circuits,
                }
            )
    return pd.DataFrame(rows)


def build_bridge(
    raw_paths: Iterable[str | Path],
    output_dir: str | Path,
    master_seed: int = 77124000,
) -> Path:
    raw_paths = [Path(p) for p in raw_paths]
    df = _load(raw_paths)
    bridge = add_population_bridge_columns(df)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    keep = [
        c
        for c in (
            "analysis_status",
            "source_path",
            "profile",
            "analysis_role",
            "circuit_id",
            "family",
            "n",
            "depth_factor",
            "direction_sampler",
            "measurement_basis",
            "tangent_count_used",
            "k",
            "score_dimension",
            "readout_rank",
            "enhancement",
            "actual_retention",
            "pairwise_purity",
            "population_purity_estimate_valid",
            "deff_from_pairwise_purity",
            "r_times_deff",
            "haar_population_var_rho",
            "haar_population_sd_rho",
            "haar_population_var_bound",
            "population_orientation_z",
            "abs_population_orientation_z",
            "orientation_growth_ratio",
            "chebyshev_bound_abs_rho_minus_1_ge_0p1",
        )
        if c in bridge.columns
    ]
    per_circuit = bridge[keep].sort_values(["n", "family", "k", "circuit_id"])
    per_circuit.to_csv(out / "per_circuit.csv", index=False)
    summary = summarize_bridge(bridge, master_seed=master_seed)
    summary.to_csv(out / "summary.csv", index=False)

    expected_rank = per_circuit.apply(
        lambda row: low_weight_readout_rank(int(row["n"]), int(row["k"])), axis=1
    )
    rank_consistent = bool(
        np.all(expected_rank.to_numpy(int) == per_circuit["readout_rank"].to_numpy(int))
    )
    invalid_purity_rows = int((~per_circuit["population_purity_estimate_valid"]).sum())
    manifest = {
        "analysis_status": ANALYSIS_STATUS,
        "scientific_role": "post-hoc bridge between the prespecified finite-size campaign and the random-orientation asymptotic theorem; not primary confirmatory inference",
        "new_quantum_simulations": False,
        "source_tables": [p.as_posix() for p in raw_paths],
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "independent_unit": "fixed circuit instance",
        "purity_estimator": "pairwise U-statistic already stored as pairwise_purity",
        "population_null": "real Haar/Grassmann rank-matched projector conditional on C",
        "rank_columns_consistent_with_fixed_weight_formula": rank_consistent,
        "invalid_population_purity_estimator_rows": invalid_purity_rows,
        "formulae": {
            "rho": "Tr(P C)/(r/N)",
            "variance": "2(N-r)(N Tr(C^2)-1)/(r(N-1)(N+2))",
            "variance_bound": "Var(rho) <= 2 Tr(C^2)/r = 2/(r d_eff)",
            "orientation_z": "(rho_physical-1)/sqrt(Var_Haar(rho)|C)",
        },
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exploratory post-hoc asymptotic bridge from archived rigorous-v2 raw tables"
    )
    parser.add_argument("--raw", action="append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--master-seed", type=int, default=77124000)
    args = parser.parse_args()
    build_bridge(args.raw, args.output, master_seed=args.master_seed)


if __name__ == "__main__":
    main()
