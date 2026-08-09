from __future__ import annotations

import argparse
import glob
from pathlib import Path

import numpy as np
import pandas as pd

from .core import stable_seed
from .rigorous_inference import family_balanced_bootstrap
from .stats import bootstrap_mean_ci


BOOTSTRAP_RESAMPLES = 10000


def _load(patterns: list[str]) -> pd.DataFrame:
    paths = []
    for pattern in patterns:
        paths.extend(glob.glob(pattern, recursive=True))
    frames = []
    for path in sorted(set(paths)):
        try:
            frame = pd.read_csv(path)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            continue
        if len(frame):
            frames.append(frame)
    if not frames:
        raise FileNotFoundError("no nonempty raw CSV files matched")
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def analyze_visibility(
    raw_patterns: list[str],
    output_dir: str | Path,
    master_seed: int = 77124000,
) -> Path:
    raw = _load(raw_patterns)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # regular_fraction is a property of a fixed circuit/tangent ensemble and is
    # duplicated over readout orders. Collapse those duplicates before inference.
    cols = [
        "profile",
        "analysis_role",
        "job_id",
        "circuit_id",
        "family",
        "n",
        "depth_factor",
        "instance",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "tangent_count_used",
        "regular_tangents",
        "regular_fraction",
    ]
    df = raw[cols].drop_duplicates(
        subset=["profile", "job_id", "tangent_count_used"]
    )
    df.to_csv(out / "visibility_by_circuit.csv", index=False)

    keys = [
        "profile",
        "analysis_role",
        "family",
        "n",
        "depth_factor",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "tangent_count_used",
    ]
    rows = []
    for gkey, g in df.groupby(keys, dropna=False):
        meta = dict(zip(keys, gkey))
        seed = stable_seed(
            "v2|visibility|family|" + "|".join(map(str, gkey)), master_seed
        )
        mean, lo, hi = bootstrap_mean_ci(
            g["regular_fraction"],
            seed,
            n_resamples=BOOTSTRAP_RESAMPLES,
            confidence=0.95,
        )
        rows.append(
            {
                **meta,
                "mean_regular_fraction": mean,
                "ci95_low": lo,
                "ci95_high": hi,
                "median_regular_fraction": float(np.median(g["regular_fraction"])),
                "minimum_regular_fraction": float(np.min(g["regular_fraction"])),
                "circuits": int(g["circuit_id"].nunique()),
            }
        )
    pd.DataFrame(rows).to_csv(out / "visibility_by_family.csv", index=False)

    cond = [
        "profile",
        "analysis_role",
        "n",
        "depth_factor",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "tangent_count_used",
    ]
    pooled = []
    for ckey, g0 in df.groupby(cond, dropna=False):
        meta = dict(zip(cond, ckey))
        generic = g0[g0["family"] != "U1-RZ-XY-line"]
        if len(generic):
            seed = stable_seed(
                "v2|visibility|generic|" + "|".join(map(str, ckey)), master_seed
            )
            mean, lo, hi = family_balanced_bootstrap(
                generic,
                "regular_fraction",
                seed,
                n_resamples=BOOTSTRAP_RESAMPLES,
            )
            pooled.append(
                {
                    **meta,
                    "group": "generic_family_balanced",
                    "mean_regular_fraction": mean,
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "families": int(generic["family"].nunique()),
                    "circuits": int(generic["circuit_id"].nunique()),
                }
            )
        u1 = g0[g0["family"] == "U1-RZ-XY-line"]
        if len(u1):
            seed = stable_seed(
                "v2|visibility|u1|" + "|".join(map(str, ckey)), master_seed
            )
            mean, lo, hi = bootstrap_mean_ci(
                u1["regular_fraction"],
                seed,
                n_resamples=BOOTSTRAP_RESAMPLES,
                confidence=0.95,
            )
            pooled.append(
                {
                    **meta,
                    "group": "U1",
                    "mean_regular_fraction": mean,
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "families": 1,
                    "circuits": int(u1["circuit_id"].nunique()),
                }
            )
    pd.DataFrame(pooled).to_csv(out / "visibility_summary.csv", index=False)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visible-tangent fraction analysis for rigorous-v2"
    )
    parser.add_argument("--raw", action="append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--master-seed", type=int, default=77124000)
    args = parser.parse_args()
    analyze_visibility(args.raw, args.output, args.master_seed)


if __name__ == "__main__":
    main()
