from __future__ import annotations

import argparse
import glob
from pathlib import Path

import numpy as np
import pandas as pd

from .core import stable_seed
from .stats import bootstrap_mean_ci


METRICS = (
    "enhancement",
    "actual_retention",
    "deff_pairwise",
    "pairwise_purity",
    "Ffull_over_FQ_mean",
    "physical_minus_rank_baseline",
)


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


def _paired_contrasts(
    df: pd.DataFrame,
    factor: str,
    reference: str,
    output_path: Path,
    master_seed: int,
):
    levels = [str(x) for x in sorted(df[factor].astype(str).unique())]
    if reference not in levels or len(levels) < 2:
        pd.DataFrame().to_csv(output_path, index=False)
        return

    if factor == "measurement_basis":
        match = [
            "profile",
            "family",
            "n",
            "depth_factor",
            "instance",
            "direction_sampler",
            "bitflip_rate",
            "tangent_count_used",
            "k",
        ]
    elif factor == "direction_sampler":
        match = [
            "profile",
            "family",
            "n",
            "depth_factor",
            "instance",
            "measurement_basis",
            "bitflip_rate",
            "tangent_count_used",
            "k",
        ]
    else:
        raise ValueError(f"unsupported paired factor {factor}")

    rows = []
    ref = df[df[factor].astype(str) == reference]
    for level in levels:
        if level == reference:
            continue
        other = df[df[factor].astype(str) == level]
        paired = ref.merge(
            other,
            on=match,
            suffixes=("_ref", "_other"),
            how="inner",
            validate="one_to_one",
        )
        if paired.empty:
            continue
        group_keys = [
            "profile",
            "family",
            "n",
            "depth_factor",
            "tangent_count_used",
            "k",
        ]
        for gkey, g in paired.groupby(group_keys, dropna=False):
            meta = dict(zip(group_keys, gkey))
            for metric in METRICS:
                delta = g[f"{metric}_other"].to_numpy(float) - g[
                    f"{metric}_ref"
                ].to_numpy(float)
                seed = stable_seed(
                    "v2|paired|"
                    + factor
                    + "|"
                    + reference
                    + "|"
                    + level
                    + "|"
                    + "|".join(map(str, gkey))
                    + "|"
                    + metric,
                    master_seed,
                )
                mean, lo, hi = bootstrap_mean_ci(
                    delta,
                    seed,
                    n_resamples=10000,
                    confidence=0.95,
                )
                rows.append(
                    {
                        **meta,
                        "factor": factor,
                        "reference": reference,
                        "comparison": level,
                        "metric": metric,
                        "paired_circuits": int(len(g)),
                        "mean_paired_difference": mean,
                        "ci95_low": lo,
                        "ci95_high": hi,
                        "fraction_positive_differences": float(np.mean(delta > 0)),
                    }
                )
    pd.DataFrame(rows).to_csv(output_path, index=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Within-circuit paired robustness contrasts for rigorous-v2"
    )
    parser.add_argument("--raw", action="append", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--master-seed", type=int, default=77124000)
    args = parser.parse_args()
    df = _load(args.raw)
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    _paired_contrasts(
        df,
        "measurement_basis",
        "Z",
        out / "paired_measurement_basis_contrasts.csv",
        args.master_seed,
    )
    _paired_contrasts(
        df,
        "direction_sampler",
        "gaussian",
        out / "paired_direction_sampler_contrasts.csv",
        args.master_seed,
    )


if __name__ == "__main__":
    main()
