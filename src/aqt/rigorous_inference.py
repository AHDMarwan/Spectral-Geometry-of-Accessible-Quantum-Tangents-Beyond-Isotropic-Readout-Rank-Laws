from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .core import stable_seed
from .stats import bootstrap_mean_ci


RANK_LAW_EQUIVALENCE_MARGIN = 0.10
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


def _family_arrays(frame: pd.DataFrame, metric: str) -> list[np.ndarray]:
    groups = []
    for _, g in frame.groupby("family"):
        x = g[metric].to_numpy(float)
        x = x[np.isfinite(x)]
        if len(x):
            groups.append(x)
    return groups


def family_balanced_bootstrap(
    frame: pd.DataFrame,
    metric: str,
    seed: int,
    n_resamples: int = BOOTSTRAP_RESAMPLES,
):
    groups = _family_arrays(frame, metric)
    if not groups:
        return np.nan, np.nan, np.nan
    observed = float(np.mean([np.mean(x) for x in groups]))
    rng = np.random.default_rng(seed)
    samples = np.empty(n_resamples)
    for b in range(n_resamples):
        samples[b] = np.mean(
            [np.mean(rng.choice(x, size=len(x), replace=True)) for x in groups]
        )
    return (
        observed,
        float(np.quantile(samples, 0.025)),
        float(np.quantile(samples, 0.975)),
    )


def u1_minus_generic_bootstrap(
    u1: pd.DataFrame,
    generic: pd.DataFrame,
    metric: str,
    seed: int,
    n_resamples: int = BOOTSTRAP_RESAMPLES,
):
    u = u1[metric].to_numpy(float)
    u = u[np.isfinite(u)]
    groups = _family_arrays(generic, metric)
    if len(u) < 2 or not groups:
        return np.nan, np.nan, np.nan
    observed = float(np.mean(u) - np.mean([np.mean(x) for x in groups]))
    rng = np.random.default_rng(seed)
    samples = np.empty(n_resamples)
    for b in range(n_resamples):
        u_mean = np.mean(rng.choice(u, size=len(u), replace=True))
        g_mean = np.mean(
            [np.mean(rng.choice(x, size=len(x), replace=True)) for x in groups]
        )
        samples[b] = u_mean - g_mean
    return (
        observed,
        float(np.quantile(samples, 0.025)),
        float(np.quantile(samples, 0.975)),
    )


def analyze_inference(
    raw_patterns: list[str],
    profile_path: str | Path,
    output_dir: str | Path,
    master_seed: int = 77124000,
) -> Path:
    df = _load(raw_patterns)
    cfg = json.loads(Path(profile_path).read_text(encoding="utf-8"))
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    margin = float(cfg.get("rank_law_equivalence_margin", RANK_LAW_EQUIVALENCE_MARGIN))
    cond = [
        "profile",
        "analysis_role",
        "n",
        "depth_factor",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "tangent_count_used",
        "k",
    ]

    equivalence_rows = []
    contrast_rows = []
    anisotropy_rows = []

    for ckey, g0 in df.groupby(cond, dropna=False):
        meta = dict(zip(cond, ckey))
        generic = g0[g0["family"] != "U1-RZ-XY-line"]
        u1 = g0[g0["family"] == "U1-RZ-XY-line"]

        if len(generic):
            seed = stable_seed(
                "v2|rank-equivalence|" + "|".join(map(str, ckey)), master_seed
            )
            mean, lo, hi = family_balanced_bootstrap(generic, "enhancement", seed)
            equivalence_rows.append(
                {
                    **meta,
                    "group": "generic_family_balanced",
                    "mean_enhancement": mean,
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "equivalence_margin": margin,
                    "equivalence_low": 1.0 - margin,
                    "equivalence_high": 1.0 + margin,
                    "ci_entirely_inside_equivalence_band": bool(
                        np.isfinite(lo)
                        and np.isfinite(hi)
                        and lo >= 1.0 - margin
                        and hi <= 1.0 + margin
                    ),
                    "families": int(generic["family"].nunique()),
                    "circuits": int(generic["circuit_id"].nunique()),
                }
            )

            for family, gf in generic.groupby("family"):
                seed = stable_seed(
                    "v2|rank-equivalence|"
                    + "|".join(map(str, ckey))
                    + "|"
                    + family,
                    master_seed,
                )
                mean_f, lo_f, hi_f = bootstrap_mean_ci(
                    gf["enhancement"],
                    seed,
                    n_resamples=BOOTSTRAP_RESAMPLES,
                    confidence=0.95,
                )
                equivalence_rows.append(
                    {
                        **meta,
                        "group": family,
                        "mean_enhancement": mean_f,
                        "ci95_low": lo_f,
                        "ci95_high": hi_f,
                        "equivalence_margin": margin,
                        "equivalence_low": 1.0 - margin,
                        "equivalence_high": 1.0 + margin,
                        "ci_entirely_inside_equivalence_band": bool(
                            np.isfinite(lo_f)
                            and np.isfinite(hi_f)
                            and lo_f >= 1.0 - margin
                            and hi_f <= 1.0 + margin
                        ),
                        "families": 1,
                        "circuits": int(gf["circuit_id"].nunique()),
                    }
                )

        if len(generic) and len(u1):
            for metric in (
                "enhancement",
                "actual_retention",
                "deff_pairwise",
                "pairwise_purity",
                "Ffull_over_FQ_mean",
                "physical_minus_rank_baseline",
            ):
                seed = stable_seed(
                    "v2|u1-minus-generic|"
                    + "|".join(map(str, ckey))
                    + "|"
                    + metric,
                    master_seed,
                )
                diff, lo, hi = u1_minus_generic_bootstrap(
                    u1, generic, metric, seed
                )
                contrast_rows.append(
                    {
                        **meta,
                        "metric": metric,
                        "contrast": "U1 minus equal-weight generic-family mean",
                        "difference": diff,
                        "ci95_low": lo,
                        "ci95_high": hi,
                        "ci_excludes_zero": bool(
                            np.isfinite(lo)
                            and np.isfinite(hi)
                            and (lo > 0.0 or hi < 0.0)
                        ),
                        "direction_if_excludes_zero": (
                            "positive" if lo > 0.0 else "negative" if hi < 0.0 else "none"
                        ),
                    }
                )

        for label, group in [
            ("generic_family_balanced", generic),
            ("U1", u1),
        ]:
            if len(group) == 0:
                continue
            derived = group.copy()
            derived["N_times_pairwise_purity"] = (
                derived["score_dimension"] * derived["pairwise_purity"]
            )
            derived["deff_over_N"] = (
                derived["deff_pairwise"] / derived["score_dimension"]
            )
            for metric in ("N_times_pairwise_purity", "deff_over_N"):
                seed = stable_seed(
                    "v2|anisotropy|"
                    + label
                    + "|"
                    + "|".join(map(str, ckey))
                    + "|"
                    + metric,
                    master_seed,
                )
                if label == "generic_family_balanced":
                    mean, lo, hi = family_balanced_bootstrap(derived, metric, seed)
                else:
                    mean, lo, hi = bootstrap_mean_ci(
                        derived[metric],
                        seed,
                        n_resamples=BOOTSTRAP_RESAMPLES,
                        confidence=0.95,
                    )
                anisotropy_rows.append(
                    {
                        **meta,
                        "group": label,
                        "metric": metric,
                        "mean": mean,
                        "ci95_low": lo,
                        "ci95_high": hi,
                        "isotropic_reference": 1.0,
                    }
                )

    pd.DataFrame(equivalence_rows).to_csv(
        out / "rank_law_equivalence.csv", index=False
    )
    pd.DataFrame(contrast_rows).to_csv(
        out / "u1_vs_generic_contrasts.csv", index=False
    )
    pd.DataFrame(anisotropy_rows).to_csv(
        out / "anisotropy_normalized.csv", index=False
    )

    policy = {
        "profile": cfg["name"],
        "outcome_blind": True,
        "rank_law_equivalence_margin": margin,
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "independent_unit": "fixed circuit instance",
        "generic_estimator": "equal weight per ansatz family, circuit bootstrap within family",
        "interpretation": {
            "generic_rank_law": "positive only when the 95% CI is entirely inside the prespecified equivalence band; failure is inconclusive or evidence against equivalence, not evidence for equivalence",
            "u1_vs_generic": "report the full contrast CI; do not select metrics by whether the CI excludes zero",
            "anisotropy": "N*Tr(C^2)=1 and d_eff/N=1 are isotropic references; full spectral-shape claims require v2_spectrum",
            "large_n": "finite-size evidence only; never described as asymptotic proof",
        },
    }
    (out / "inference_policy.json").write_text(
        json.dumps(policy, indent=2), encoding="utf-8"
    )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prespecified inference tables for rigorous-v2"
    )
    parser.add_argument("--raw", action="append", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--master-seed", type=int, default=77124000)
    args = parser.parse_args()
    analyze_inference(args.raw, args.profile, args.output, args.master_seed)


if __name__ == "__main__":
    main()
