from __future__ import annotations

import argparse
import glob
from pathlib import Path

import numpy as np
import pandas as pd

from .core import stable_seed
from .stats import bootstrap_mean_ci, bootstrap_ratio_ci


def _load(pattern: str) -> pd.DataFrame:
    frames = []
    for path in sorted(glob.glob(pattern, recursive=True)):
        try:
            df = pd.read_csv(path)
        except (pd.errors.EmptyDataError, FileNotFoundError):
            continue
        if len(df):
            frames.append(df)
    return pd.concat(frames, ignore_index=True).drop_duplicates() if frames else pd.DataFrame()


def paper_reproduction(raw: pd.DataFrame, out: Path) -> None:
    if raw.empty or "profile" not in raw or not (raw.profile == "reproduce_paper").any():
        return
    rep = raw[
        (raw.profile == "reproduce_paper")
        & (raw.direction_sampler == "gaussian")
        & (raw.measurement_basis == "Z")
        & (raw.bitflip_rate == 0.0)
    ]
    reported = {
        (6, "generic_pooled"): {
            "enhancement_k1": (0.958, 0.919, 0.999),
            "enhancement_k2": (0.993, 0.974, 1.012),
            "deff": (46.1, 43.7, 48.5),
            "F": (0.4885, 0.4848, 0.4927),
        },
        (6, "U1"): {
            "enhancement_k1": (2.077, 2.013, 2.142),
            "enhancement_k2": (1.186, 1.168, 1.204),
            "deff": (9.52, 9.19, 9.82),
            "F": (0.4744, 0.4579, 0.4909),
        },
        (8, "generic_pooled"): {
            "enhancement_k1": (0.931, 0.893, 0.972),
            "enhancement_k2": (0.973, 0.960, 0.984),
            "deff": (136.1, 124.3, 148.3),
            "F": (0.4897, 0.4851, 0.4941),
        },
        (8, "U1"): {
            "enhancement_k1": (4.224, 4.091, 4.356),
            "enhancement_k2": (1.895, 1.866, 1.927),
            "deff": (16.97, 16.30, 17.74),
            "F": (0.4785, 0.4692, 0.4883),
        },
        (10, "generic_pooled"): {
            "enhancement_k1": (0.926, 0.896, 0.956),
            "enhancement_k2": (0.964, 0.953, 0.976),
            "deff": (351.6, 302.2, 403.4),
            "F": (0.4919, 0.4896, 0.4940),
        },
        (10, "U1"): {
            "enhancement_k1": (9.824, 9.547, 10.124),
            "enhancement_k2": (3.607, 3.553, 3.654),
            "deff": (27.49, 26.89, 28.06),
            "F": (0.4700, 0.4641, 0.4751),
        },
    }
    rows = []
    for (n, group), targets in reported.items():
        cell = rep[rep.n == n]
        cell = cell[cell.family == "U1-RZ-XY-line"] if group == "U1" else cell[cell.family != "U1-RZ-XY-line"]
        if cell.empty:
            continue
        seed_group = "u1" if group == "U1" else "generic"
        specs = {
            "enhancement_k1": (cell[cell.k == 1].enhancement, 1, "enhancement"),
            "enhancement_k2": (cell[cell.k == 2].enhancement, 2, "enhancement"),
            "deff": (cell[cell.k == 1].deff_pairwise, 1, "deff_pairwise"),
            "F": (cell[cell.k == 1].Ffull_over_FQ_mean, 1, "Ffull_over_FQ_mean"),
        }
        for metric, (values, k, notebook_metric) in specs.items():
            target, target_lo, target_hi = targets[metric]
            if len(values) < 2:
                continue
            seed = stable_seed(f"boot|{seed_group}|{n}|{k}|{notebook_metric}", 20260809)
            value, lo, hi = bootstrap_mean_ci(values, seed)
            rows.append({
                "n": n, "group": group, "metric": metric,
                "reported": target, "reported_ci95_low": target_lo, "reported_ci95_high": target_hi,
                "rerun": value, "rerun_ci95_low": lo, "rerun_ci95_high": hi,
                "difference": value - target,
            })
    pd.DataFrame(rows).to_csv(out / "paper_reproduction_with_ci.csv", index=False)

    ratio_targets = {(10, 1): (38.9, 37.3, 40.7), (10, 2): (12.20, 11.98, 12.41)}
    ratios = []
    for (n, k), (target, target_lo, target_hi) in ratio_targets.items():
        g = rep[(rep.n == n) & (rep.k == k)]
        a = g[g.family == "U1-RZ-XY-line"].actual_retention
        b = g[g.family != "U1-RZ-XY-line"].actual_retention
        if len(a) < 2 or len(b) < 2:
            continue
        value, lo, hi = bootstrap_ratio_ci(a, b, stable_seed(f"paper|retention-ratio|n{n}|k{k}", 20260809))
        ratios.append({
            "n": n, "k": k,
            "reported_ratio": target, "reported_ci95_low": target_lo, "reported_ci95_high": target_hi,
            "rerun_ratio": value, "rerun_ci95_low": lo, "rerun_ci95_high": hi,
            "difference": value - target,
        })
    pd.DataFrame(ratios).to_csv(out / "paper_retention_ratio_comparison.csv", index=False)


def spectral_diagnostics(raw: pd.DataFrame, spectrum: pd.DataFrame, out: Path) -> None:
    if raw.empty or spectrum.empty:
        return
    spectra = {}
    for job_id, g in spectrum.groupby("job_id"):
        eig = g.sort_values("eigen_index").eigenvalue.to_numpy(float)
        eig = eig[np.isfinite(eig) & (eig >= 0)]
        spectra[job_id] = eig
    rows = []
    for _, row in raw.iterrows():
        eig = spectra.get(row.job_id)
        if eig is None or len(eig) == 0:
            continue
        rank = int(row.readout_rank)
        nscore = int(row.score_dimension)
        retention = float(row.actual_retention)
        baseline = float(row.rank_baseline)
        sample_kyfan = float(np.sum(eig[: min(rank, len(eig))])) if rank > 0 else 0.0
        sample_purity = float(np.sum(eig * eig))
        rhs = float(np.sqrt(max(0.0, rank * (1 - rank / nscore)) * max(0.0, sample_purity - 1 / nscore))) if nscore > 0 else np.nan
        rows.append({
            "profile": row.profile, "job_id": row.job_id, "circuit_id": row.circuit_id,
            "family": row.family, "n": row.n, "depth_factor": row.depth_factor, "k": row.k,
            "readout_rank": rank, "score_dimension": nscore,
            "physical_retention": retention, "rank_baseline": baseline,
            "sample_kyfan": sample_kyfan,
            "physical_over_sample_kyfan": retention / sample_kyfan if sample_kyfan > 0 else np.nan,
            "sample_covariance_purity": sample_purity,
            "theorem9_rhs_sample": rhs,
            "theorem9_slack_sample": rhs - abs(retention - baseline) if np.isfinite(rhs) else np.nan,
            "kyfan_slack_sample": sample_kyfan - retention,
        })
    pd.DataFrame(rows).to_csv(out / "spectral_theorem_diagnostics.csv", index=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--spectrum", required=False)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    raw = _load(args.raw)
    spectrum = _load(args.spectrum) if args.spectrum else pd.DataFrame()
    paper_reproduction(raw, out)
    spectral_diagnostics(raw, spectrum, out)


if __name__ == "__main__":
    main()
