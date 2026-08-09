from __future__ import annotations

import argparse
import glob
import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from .core import (
    FAMILIES,
    parameter_layers,
    rotate_measurement_basis,
    sample_parameter_directions,
    simulate_vqc_tangent_batch,
    stable_seed,
)
from .metrics import (
    apply_independent_bitflip_channel,
    covariance_spectrum,
    direct_readout_retention,
    probability_tangent_batch,
    random_rank_subspace_null,
    repeated_crossfit_kyfan,
    normalized_visible_scores_from_pdp,
    pairwise_purity_and_deff,
    third_spectral_moment,
)
from .stats import bootstrap_mean_ci


GENERIC = [f for f in FAMILIES if f != "U1-RZ-XY-line"]
PRIMARY_METRICS = (
    "enhancement",
    "actual_retention",
    "deff_pairwise",
    "pairwise_purity",
    "sample_covariance_purity",
    "trC3_u_stat",
    "Ffull_over_FQ_mean",
    "haar_alignment_z",
    "physical_minus_rank_baseline",
)


def load_profile(path: str | Path) -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {
        "name",
        "master_seed",
        "families",
        "n_values",
        "depth_factors",
        "instances",
        "tangents",
        "readout_orders",
    }
    missing = sorted(required - set(cfg))
    if missing:
        raise ValueError(f"profile missing keys: {missing}")
    if cfg.get("rng_scheme", "independent_streams") != "independent_streams":
        raise ValueError("rigorous-v2 requires independent RNG streams")
    if int(cfg["tangents"]) < 8:
        raise ValueError("at least eight tangent directions are required")
    prefixes = cfg.get("tangent_prefixes", [cfg["tangents"]])
    prefixes = sorted({int(x) for x in prefixes})
    if not prefixes or prefixes[-1] != int(cfg["tangents"]):
        raise ValueError("tangent_prefixes must contain the full tangent count")
    if prefixes[0] < 8 or prefixes[-1] > int(cfg["tangents"]):
        raise ValueError("invalid tangent_prefixes")
    cfg["tangent_prefixes"] = prefixes
    return cfg


def _family_instances(cfg: dict, family: str) -> int:
    value = cfg["instances"]
    if isinstance(value, int):
        return int(value)
    return int(value.get(family, value.get("default", 1)))


def build_schedule(cfg: dict) -> list[dict]:
    schedule = []
    for family in cfg["families"]:
        if family not in FAMILIES:
            raise ValueError(f"unknown family {family!r}")
        for n in cfg["n_values"]:
            n = int(n)
            for fac in cfg["depth_factors"]:
                depth = max(1, int(round(float(fac) * n)))
                for instance in range(_family_instances(cfg, family)):
                    for sampler in cfg.get("direction_samplers", ["gaussian"]):
                        for basis in cfg.get("measurement_bases", ["Z"]):
                            for eta in cfg.get("bitflip_rates", [0.0]):
                                schedule.append(
                                    {
                                        "family": family,
                                        "n": n,
                                        "depth": depth,
                                        "depth_factor": float(fac),
                                        "instance": int(instance),
                                        "direction_sampler": str(sampler),
                                        "measurement_basis": str(basis),
                                        "bitflip_rate": float(eta),
                                        "tangents": int(cfg["tangents"]),
                                    }
                                )
    return schedule


def _ids(job: dict) -> tuple[str, str]:
    circuit_id = (
        f"{job['family']}|n{job['n']}|d{job['depth']}|i{job['instance']}"
    )
    job_id = (
        f"{circuit_id}|dir={job['direction_sampler']}"
        f"|basis={job['measurement_basis']}|eta={job['bitflip_rate']:.6g}"
    )
    return circuit_id, job_id


def _draw_circuit(cfg: dict, job: dict):
    circuit_id, _ = _ids(job)
    _, pcount = parameter_layers(job["n"], job["depth"], job["family"])
    rng_theta = np.random.default_rng(
        stable_seed(circuit_id + "|theta", int(cfg["master_seed"]))
    )
    theta = rng_theta.uniform(-np.pi, np.pi, size=pcount)
    rng_dir = np.random.default_rng(
        stable_seed(
            circuit_id + "|directions|" + job["direction_sampler"],
            int(cfg["master_seed"]),
        )
    )
    directions = sample_parameter_directions(
        rng_dir, job["tangents"], pcount, job["direction_sampler"]
    )
    arch_seed = stable_seed(circuit_id + "|architecture", int(cfg["master_seed"]))
    basis_seed = stable_seed(circuit_id + "|measurement-basis", int(cfg["master_seed"]))
    return pcount, theta, directions, arch_seed, basis_seed


def _simulate_visible_scores_batched(cfg: dict, job: dict) -> dict:
    """Exact statevector simulation with memory-bounded tangent batches.

    Batching changes only memory use. Each direction is propagated analytically with
    the same circuit parameters and architecture seed. The circuit state is
    recomputed for each batch and checked for consistency.
    """
    pcount, theta, directions, arch_seed, basis_seed = _draw_circuit(cfg, job)
    batch_size = max(1, int(cfg.get("simulation_batch_size", job["tangents"])))
    p_floor = float(cfg.get("probability_floor", 1e-13))

    p_ref = None
    support_ref = None
    psi_ref = None
    U_parts = []
    regular_indices = []
    ffull_regular = []
    fq_regular = []
    diagnostics = {
        "state_norm_error": 0.0,
        "horizontal_overlap_max": 0.0,
        "probability_sum_error": 0.0,
        "probability_tangent_sum_max": 0.0,
        "fisher_violation_max": -np.inf,
    }

    for start in range(0, job["tangents"], batch_size):
        stop = min(job["tangents"], start + batch_size)
        psi, phis, _ = simulate_vqc_tangent_batch(
            job["n"],
            job["depth"],
            job["family"],
            theta,
            directions[start:stop],
            arch_seed,
        )
        psi, phis = rotate_measurement_basis(
            psi, phis, job["n"], job["measurement_basis"], basis_seed
        )
        p, dp = probability_tangent_batch(psi, phis)
        fq = 4.0 * np.sum(np.abs(phis) ** 2, axis=1).real
        if job["bitflip_rate"]:
            p, dp = apply_independent_bitflip_channel(
                p, dp, job["n"], job["bitflip_rate"]
            )
        info = normalized_visible_scores_from_pdp(
            p, dp, fq, probability_floor=p_floor
        )

        if p_ref is None:
            p_ref = info["p"].copy()
            support_ref = info["support"].copy()
            psi_ref = psi.copy()
        else:
            if not np.allclose(p_ref, info["p"], rtol=0.0, atol=5e-13):
                raise RuntimeError("probabilities changed across tangent batches")
            if not np.array_equal(support_ref, info["support"]):
                raise RuntimeError("numerical support changed across tangent batches")
            if not np.allclose(psi_ref, psi, rtol=0.0, atol=5e-13):
                raise RuntimeError("statevector changed across tangent batches")

        reg_local = np.flatnonzero(info["regular"])
        regular_indices.extend((start + reg_local).tolist())
        if len(reg_local):
            U_parts.append(info["U"])
            ffull_regular.append(info["Ffull"][info["regular"]])
            fq_regular.append(info["FQ"][info["regular"]])

        diagnostics["state_norm_error"] = max(
            diagnostics["state_norm_error"],
            float(abs(np.vdot(psi, psi).real - 1.0)),
        )
        diagnostics["horizontal_overlap_max"] = max(
            diagnostics["horizontal_overlap_max"],
            float(np.max(np.abs(phis @ np.conjugate(psi)))) if len(phis) else 0.0,
        )
        diagnostics["probability_sum_error"] = max(
            diagnostics["probability_sum_error"], float(abs(np.sum(p) - 1.0))
        )
        diagnostics["probability_tangent_sum_max"] = max(
            diagnostics["probability_tangent_sum_max"],
            float(np.max(np.abs(np.sum(dp, axis=1)))) if len(dp) else 0.0,
        )
        diagnostics["fisher_violation_max"] = max(
            diagnostics["fisher_violation_max"],
            float(np.max(info["Ffull"] - info["FQ"])) if len(info["FQ"]) else -np.inf,
        )

    if not U_parts:
        raise RuntimeError("no regular tangent directions")
    U = np.vstack(U_parts)
    ffull = np.concatenate(ffull_regular)
    fq = np.concatenate(fq_regular)
    regular_indices = np.asarray(regular_indices, dtype=int)

    return {
        "pcount": pcount,
        "p": p_ref,
        "support": support_ref,
        "p_support": p_ref[support_ref],
        "support_indices": np.flatnonzero(support_ref),
        "U": U,
        "regular_indices": regular_indices,
        "Ffull_regular": ffull,
        "FQ_regular": fq,
        **diagnostics,
    }


def _haar_rank_null_moments(rank: int, nscore: int, purity: float) -> tuple[float, float]:
    """Exact first two Haar-Grassmann moments of Tr(P C) for real score space."""
    if nscore <= 1 or rank < 0 or rank > nscore:
        return np.nan, np.nan
    mean = rank / nscore
    if rank == 0 or rank == nscore:
        return float(mean), 0.0
    excess = max(0.0, nscore * float(purity) - 1.0)
    var = (
        2.0
        * rank
        * (nscore - rank)
        * excess
        / (nscore**2 * (nscore - 1) * (nscore + 2))
    )
    return float(mean), float(math.sqrt(max(0.0, var)))


def _prefix_view(bundle: dict, m_use: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    take = bundle["regular_indices"] < int(m_use)
    return (
        bundle["U"][take],
        bundle["Ffull_regular"][take],
        bundle["FQ_regular"][take],
    )


def _job_rows(cfg: dict, job: dict, bundle: dict, m_use: int):
    circuit_id, job_id = _ids(job)
    U, ffull, fq = _prefix_view(bundle, m_use)
    min_fraction = float(cfg.get("min_regular_fraction", 0.99))
    required = max(8, int(math.ceil(min_fraction * m_use)))
    if len(U) < required:
        raise RuntimeError(
            f"{job_id}: only {len(U)}/{m_use} regular tangents; required {required}"
        )

    purity, deff = pairwise_purity_and_deff(U)
    gram = U @ U.T
    sample_cov_purity = float(np.sum(gram * gram) / (len(U) ** 2))
    trc3 = third_spectral_moment(U)
    support_idx = bundle["support_indices"]
    nscore = len(support_idx) - 1
    readout_orders = [int(k) for k in cfg["readout_orders"] if int(k) < job["n"]]
    svd_tol = float(cfg.get("svd_tolerance", 1e-10))
    spectral_cfg = cfg.get("spectral", {})
    max_prefix = int(cfg["tangents"])
    do_spectrum = bool(spectral_cfg.get("enabled", False)) and m_use == max_prefix
    eig = covariance_spectrum(U) if do_spectrum else np.array([])
    ranks = []
    diag = {}
    for k in readout_orders:
        ret, rank, baseline = direct_readout_retention(
            U, bundle["p_support"], support_idx, job["n"], k, svd_tol
        )
        diag[k] = (ret, rank, baseline)
        ranks.append(rank)
    cv = (
        repeated_crossfit_kyfan(
            U,
            sorted(set(ranks)),
            stable_seed(job_id + f"|crossfit|M{m_use}", int(cfg["master_seed"])),
            repeats=int(spectral_cfg.get("crossfit_repeats", 50)),
        )
        if do_spectrum
        else {}
    )

    rows = []
    for k, (ret, rank, baseline) in diag.items():
        null_mean, null_std = _haar_rank_null_moments(
            rank, nscore, sample_cov_purity
        )
        delta = ret - baseline
        z = delta / null_std if null_std > 0 else np.nan
        theorem_rhs_sample = math.sqrt(
            max(0.0, rank * (1.0 - rank / nscore))
            * max(0.0, sample_cov_purity - 1.0 / nscore)
        ) if nscore > 0 else np.nan
        theorem_rhs_u_stat = math.sqrt(
            max(0.0, rank * (1.0 - rank / nscore))
            * max(0.0, purity - 1.0 / nscore)
        ) if nscore > 0 else np.nan
        rows.append(
            {
                "profile": cfg["name"],
                "analysis_role": cfg.get("analysis_role", "unspecified"),
                "job_id": job_id,
                "circuit_id": circuit_id,
                **job,
                "tangent_count_used": int(m_use),
                "parameter_count": int(bundle["pcount"]),
                "regular_tangents": int(len(U)),
                "regular_fraction": float(len(U) / m_use),
                "support_size": int(len(support_idx)),
                "score_dimension": int(nscore),
                "FQ_mean": float(np.mean(fq)),
                "Ffull_mean": float(np.mean(ffull)),
                "Ffull_over_FQ_mean": float(np.mean(ffull / fq)),
                "pairwise_purity": float(purity),
                "sample_covariance_purity": float(sample_cov_purity),
                "deff_pairwise": float(deff),
                "trC3_u_stat": float(trc3),
                "renyi3_dimension_diag": float(trc3 ** -0.5) if trc3 > 0 else np.nan,
                "k": int(k),
                "readout_rank": int(rank),
                "actual_retention": float(ret),
                "rank_baseline": float(baseline),
                "enhancement": float(ret / baseline) if baseline > 0 else np.nan,
                "physical_minus_rank_baseline": float(delta),
                "haar_null_mean": float(null_mean),
                "haar_null_std": float(null_std),
                "haar_alignment_z": float(z),
                "theorem_rhs_sample": float(theorem_rhs_sample),
                "theorem_bound_slack_sample": float(
                    theorem_rhs_sample - abs(delta)
                )
                if np.isfinite(theorem_rhs_sample)
                else np.nan,
                "theorem_rhs_u_stat": float(theorem_rhs_u_stat),
                "theorem_bound_slack_u_stat": float(
                    theorem_rhs_u_stat - abs(delta)
                )
                if np.isfinite(theorem_rhs_u_stat)
                else np.nan,
                "crossfit_kyfan": float(cv.get(rank, np.nan)),
                "sample_lambda_max": float(eig[0]) if len(eig) else np.nan,
                "sample_spectrum_rank": int(len(eig)),
                "state_norm_error": float(bundle["state_norm_error"]),
                "horizontal_overlap_max": float(bundle["horizontal_overlap_max"]),
                "probability_sum_error": float(bundle["probability_sum_error"]),
                "probability_tangent_sum_max": float(
                    bundle["probability_tangent_sum_max"]
                ),
                "fisher_violation_max": float(bundle["fisher_violation_max"]),
                "min_circuits_for_inference": int(
                    cfg.get("min_circuits_for_inference", 10)
                ),
                "max_relative_ci_halfwidth": float(
                    cfg.get("max_relative_ci_halfwidth", 0.20)
                ),
            }
        )
    return rows, eig, diag, U


def run_profile(
    profile_path: str | Path,
    output_dir: str | Path,
    shard_index: int = 0,
    num_shards: int = 1,
) -> Path:
    cfg = load_profile(profile_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "profile.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")

    schedule = build_schedule(cfg)
    selected = [job for i, job in enumerate(schedule) if i % num_shards == shard_index]
    raw_path = out / "raw.csv"
    spectrum_path = out / "spectrum.csv"
    null_path = out / "random_readout_null.csv"

    for job in selected:
        bundle = _simulate_visible_scores_batched(cfg, job)
        for m_use in cfg["tangent_prefixes"]:
            rows, eig, diag, U = _job_rows(cfg, job, bundle, m_use)
            pd.DataFrame(rows).to_csv(
                raw_path, mode="a", header=not raw_path.exists(), index=False
            )

            if len(eig):
                circuit_id, job_id = _ids(job)
                top_eigs = int(cfg.get("spectral", {}).get("top_eigenvalues", len(eig)))
                pd.DataFrame(
                    [
                        {
                            "profile": cfg["name"],
                            "job_id": job_id,
                            "circuit_id": circuit_id,
                            "tangent_count_used": int(m_use),
                            "eigen_index": j + 1,
                            "eigenvalue": float(x),
                        }
                        for j, x in enumerate(eig[:top_eigs])
                    ]
                ).to_csv(
                    spectrum_path,
                    mode="a",
                    header=not spectrum_path.exists(),
                    index=False,
                )

            null_cfg = cfg.get("random_readout_null", {})
            draws = int(null_cfg.get("draws", 0))
            run_null = (
                draws > 0
                and m_use == int(cfg["tangents"])
                and job["measurement_basis"].upper() == "Z"
                and job["bitflip_rate"] == 0.0
            )
            if run_null:
                circuit_id, job_id = _ids(job)
                sqrtp = np.sqrt(bundle["p_support"])
                null_rows = []
                for k, (ret, rank, baseline) in diag.items():
                    sims = random_rank_subspace_null(
                        U,
                        sqrtp,
                        rank,
                        draws,
                        stable_seed(
                            job_id + f"|rank-null|k{k}", int(cfg["master_seed"])
                        ),
                    )
                    null_rows.append(
                        {
                            "profile": cfg["name"],
                            "job_id": job_id,
                            "circuit_id": circuit_id,
                            "family": job["family"],
                            "n": job["n"],
                            "depth_factor": job["depth_factor"],
                            "k": int(k),
                            "tangent_count_used": int(m_use),
                            "physical_retention": float(ret),
                            "rank_baseline": float(baseline),
                            "null_mean": float(np.mean(sims)),
                            "null_std": float(np.std(sims, ddof=1)),
                            "null_q025": float(np.quantile(sims, 0.025)),
                            "null_q975": float(np.quantile(sims, 0.975)),
                            "empirical_upper_p": float(
                                (1.0 + np.sum(sims >= ret)) / (len(sims) + 1.0)
                            ),
                            "null_draws": int(len(sims)),
                        }
                    )
                pd.DataFrame(null_rows).to_csv(
                    null_path,
                    mode="a",
                    header=not null_path.exists(),
                    index=False,
                )

    if not raw_path.exists():
        pd.DataFrame().to_csv(raw_path, index=False)
    return raw_path


def _load_csvs(patterns: list[str]) -> pd.DataFrame:
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
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def _balanced_family_bootstrap(
    frame: pd.DataFrame,
    metric: str,
    seed: int,
    n_resamples: int = 10000,
    confidence: float = 0.95,
):
    groups = []
    for _, g in frame.groupby("family"):
        x = g[metric].to_numpy(float)
        x = x[np.isfinite(x)]
        if len(x):
            groups.append(x)
    if not groups:
        return np.nan, np.nan, np.nan
    observed = float(np.mean([np.mean(x) for x in groups]))
    rng = np.random.default_rng(seed)
    values = np.empty(n_resamples)
    for b in range(n_resamples):
        values[b] = np.mean(
            [np.mean(rng.choice(x, size=len(x), replace=True)) for x in groups]
        )
    alpha = (1.0 - confidence) / 2.0
    return (
        observed,
        float(np.quantile(values, alpha)),
        float(np.quantile(values, 1.0 - alpha)),
    )


def _jackknife_max_shift(values) -> float:
    x = np.asarray(values, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return np.nan
    full = np.mean(x)
    total = np.sum(x)
    loo = (total - x) / (len(x) - 1)
    return float(np.max(np.abs(loo - full)))


def _relative_halfwidth(mean: float, lo: float, hi: float) -> float:
    if not np.isfinite(mean) or not np.isfinite(lo) or not np.isfinite(hi):
        return np.nan
    denom = max(abs(mean), 1e-15)
    return float((hi - lo) / (2.0 * denom))


def analyze(
    raw_patterns: list[str],
    output_dir: str | Path,
    spectrum_patterns: list[str] | None = None,
    null_patterns: list[str] | None = None,
    master_seed: int = 77124000,
) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    df = _load_csvs(raw_patterns)
    if df.empty:
        raise FileNotFoundError("no nonempty rigorous-v2 raw CSV files found")
    df.to_csv(out / "merged_raw.csv", index=False)

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
        "k",
    ]
    rows = []
    for gkey, g in df.groupby(keys, dropna=False):
        meta = dict(zip(keys, gkey))
        min_circuits = int(g["min_circuits_for_inference"].max())
        max_rel = float(g["max_relative_ci_halfwidth"].min())
        for metric in PRIMARY_METRICS:
            if metric not in g:
                continue
            seed = stable_seed(
                "v2|family|" + "|".join(map(str, gkey)) + "|" + metric,
                master_seed,
            )
            mean, lo, hi = bootstrap_mean_ci(
                g[metric], seed, n_resamples=10000, confidence=0.95
            )
            circuits = int(g["circuit_id"].nunique())
            rel = _relative_halfwidth(mean, lo, hi)
            rows.append(
                {
                    **meta,
                    "metric": metric,
                    "mean": mean,
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "circuits": circuits,
                    "relative_ci95_halfwidth": rel,
                    "jackknife_max_shift": _jackknife_max_shift(g[metric]),
                    "passes_min_circuits": circuits >= min_circuits,
                    "passes_precision_flag": bool(np.isfinite(rel) and rel <= max_rel),
                    "inference_ready": bool(
                        circuits >= min_circuits
                        and np.isfinite(rel)
                        and rel <= max_rel
                    ),
                }
            )
    family_summary = pd.DataFrame(rows)
    family_summary.to_csv(out / "family_summary.csv", index=False)

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
    pooled_rows = []
    loo_rows = []
    for ckey, g0 in df.groupby(cond, dropna=False):
        meta = dict(zip(cond, ckey))
        generic = g0[g0["family"] != "U1-RZ-XY-line"]
        for metric in PRIMARY_METRICS:
            if metric not in g0:
                continue
            if len(generic):
                seed = stable_seed(
                    "v2|generic-balanced|" + "|".join(map(str, ckey)) + "|" + metric,
                    master_seed,
                )
                mean, lo, hi = _balanced_family_bootstrap(generic, metric, seed)
                pooled_rows.append(
                    {
                        **meta,
                        "group": "generic_family_balanced",
                        "metric": metric,
                        "mean": mean,
                        "ci95_low": lo,
                        "ci95_high": hi,
                        "families": int(generic["family"].nunique()),
                        "circuits": int(generic["circuit_id"].nunique()),
                        "estimator": "equal weight per ansatz family; circuit bootstrap within family",
                    }
                )
                full_mean = mean
                if generic["family"].nunique() >= 3:
                    for omitted in sorted(generic["family"].unique()):
                        keep = generic[generic["family"] != omitted]
                        family_means = [
                            gg[metric].replace([np.inf, -np.inf], np.nan).dropna().mean()
                            for _, gg in keep.groupby("family")
                        ]
                        omit_mean = float(np.nanmean(family_means))
                        loo_rows.append(
                            {
                                **meta,
                                "metric": metric,
                                "omitted_family": omitted,
                                "remaining_families": int(keep["family"].nunique()),
                                "full_family_balanced_mean": full_mean,
                                "leave_one_family_out_mean": omit_mean,
                                "absolute_shift": float(omit_mean - full_mean),
                            }
                        )
            u1 = g0[g0["family"] == "U1-RZ-XY-line"]
            if len(u1):
                seed = stable_seed(
                    "v2|u1|" + "|".join(map(str, ckey)) + "|" + metric,
                    master_seed,
                )
                mean, lo, hi = bootstrap_mean_ci(
                    u1[metric], seed, n_resamples=10000, confidence=0.95
                )
                pooled_rows.append(
                    {
                        **meta,
                        "group": "U1",
                        "metric": metric,
                        "mean": mean,
                        "ci95_low": lo,
                        "ci95_high": hi,
                        "families": 1,
                        "circuits": int(u1["circuit_id"].nunique()),
                        "estimator": "circuit bootstrap",
                    }
                )
    pd.DataFrame(pooled_rows).to_csv(out / "pooled_summary.csv", index=False)
    pd.DataFrame(loo_rows).to_csv(out / "leave_one_family_out.csv", index=False)

    conv_rows = []
    base_keys = [
        "profile",
        "family",
        "n",
        "depth_factor",
        "instance",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "k",
    ]
    if df["tangent_count_used"].nunique() > 1:
        for bkey, g in df.groupby(base_keys, dropna=False):
            max_m = int(g["tangent_count_used"].max())
            gmax = g[g["tangent_count_used"] == max_m]
            if len(gmax) != 1:
                continue
            ref = gmax.iloc[0]
            for _, row in g.iterrows():
                for metric in (
                    "enhancement",
                    "actual_retention",
                    "deff_pairwise",
                    "pairwise_purity",
                    "Ffull_over_FQ_mean",
                ):
                    denom = max(abs(float(ref[metric])), 1e-15)
                    conv_rows.append(
                        {
                            **dict(zip(base_keys, bkey)),
                            "tangent_count_used": int(row["tangent_count_used"]),
                            "reference_tangent_count": max_m,
                            "metric": metric,
                            "value": float(row[metric]),
                            "reference_value": float(ref[metric]),
                            "relative_difference": float(
                                (row[metric] - ref[metric]) / denom
                            ),
                        }
                    )
    conv = pd.DataFrame(conv_rows)
    conv.to_csv(out / "tangent_convergence_by_circuit.csv", index=False)
    if len(conv):
        conv_summary = (
            conv.groupby(
                [
                    "profile",
                    "family",
                    "n",
                    "depth_factor",
                    "tangent_count_used",
                    "reference_tangent_count",
                    "metric",
                ],
                dropna=False,
            )["relative_difference"]
            .agg(
                circuits="count",
                median_abs=lambda x: float(np.median(np.abs(x))),
                q95_abs=lambda x: float(np.quantile(np.abs(x), 0.95)),
                max_abs=lambda x: float(np.max(np.abs(x))),
            )
            .reset_index()
        )
        conv_summary.to_csv(out / "tangent_convergence_summary.csv", index=False)

    orientation_rows = []
    for gkey, g in df.groupby(keys, dropna=False):
        meta = dict(zip(keys, gkey))
        seed = stable_seed(
            "v2|orientation|" + "|".join(map(str, gkey)), master_seed
        )
        mean, lo, hi = bootstrap_mean_ci(
            g["physical_minus_rank_baseline"],
            seed,
            n_resamples=10000,
            confidence=0.95,
        )
        orientation_rows.append(
            {
                **meta,
                "mean_physical_minus_rank_baseline": mean,
                "ci95_low": lo,
                "ci95_high": hi,
                "circuits": int(g["circuit_id"].nunique()),
                "fraction_positive": float(
                    np.mean(g["physical_minus_rank_baseline"] > 0)
                ),
                "median_haar_z": float(np.nanmedian(g["haar_alignment_z"])),
            }
        )
    pd.DataFrame(orientation_rows).to_csv(out / "orientation_summary.csv", index=False)

    if spectrum_patterns:
        spectrum = _load_csvs(spectrum_patterns)
        if len(spectrum):
            spec_rows = []
            spectra = {}
            for (job_id, m), g in spectrum.groupby(
                ["job_id", "tangent_count_used"], dropna=False
            ):
                eig = g.sort_values("eigen_index")["eigenvalue"].to_numpy(float)
                spectra[(job_id, int(m))] = eig
            max_per_job = df.groupby("job_id")["tangent_count_used"].transform("max")
            full_rows = df[df["tangent_count_used"] == max_per_job]
            for _, row in full_rows.iterrows():
                eig = spectra.get((row["job_id"], int(row["tangent_count_used"])))
                if eig is None or not len(eig):
                    continue
                r = int(row["readout_rank"])
                ky = float(np.sum(eig[: min(r, len(eig))]))
                spec_rows.append(
                    {
                        "profile": row["profile"],
                        "job_id": row["job_id"],
                        "circuit_id": row["circuit_id"],
                        "family": row["family"],
                        "n": int(row["n"]),
                        "k": int(row["k"]),
                        "tangent_count_used": int(row["tangent_count_used"]),
                        "physical_retention": float(row["actual_retention"]),
                        "sample_kyfan": ky,
                        "sample_kyfan_minus_physical": float(
                            ky - row["actual_retention"]
                        ),
                        "crossfit_kyfan": float(row["crossfit_kyfan"]),
                        "sample_purity": float(np.sum(eig * eig)),
                        "sample_trC3": float(np.sum(eig * eig * eig)),
                    }
                )
            pd.DataFrame(spec_rows).to_csv(
                out / "spectral_diagnostics.csv", index=False
            )

    if null_patterns:
        null = _load_csvs(null_patterns)
        if len(null):
            null.to_csv(out / "merged_random_readout_null.csv", index=False)

    audit_cols = [
        "profile",
        "analysis_role",
        "job_id",
        "circuit_id",
        "family",
        "n",
        "depth_factor",
        "tangent_count_used",
        "k",
        "regular_fraction",
        "state_norm_error",
        "horizontal_overlap_max",
        "probability_sum_error",
        "probability_tangent_sum_max",
        "fisher_violation_max",
        "theorem_bound_slack_sample",
    ]
    df[audit_cols].to_csv(out / "numerical_audit.csv", index=False)
    return out


def validate(
    profile_path: str | Path,
    raw_patterns: list[str],
    output_path: str | Path,
) -> bool:
    cfg = load_profile(profile_path)
    df = _load_csvs(raw_patterns)
    report = {
        "profile": cfg["name"],
        "technical_validity_only": True,
        "scientific_outcomes_are_not_pass_fail_criteria": True,
        "checks": {},
    }
    if df.empty:
        report["checks"]["nonempty"] = False
        Path(output_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
        return False

    schedule = build_schedule(cfg)
    expected_jobs = {_ids(j)[1] for j in schedule}
    observed_jobs = set(df["job_id"].unique())
    report["checks"]["all_scheduled_jobs_present"] = expected_jobs <= observed_jobs
    report["missing_jobs"] = sorted(expected_jobs - observed_jobs)

    expected_rows = set()
    for job in schedule:
        _, job_id = _ids(job)
        for m_use in cfg["tangent_prefixes"]:
            for k in cfg["readout_orders"]:
                if int(k) < int(job["n"]):
                    expected_rows.add((job_id, int(m_use), int(k)))
    observed_rows = {
        (str(r.job_id), int(r.tangent_count_used), int(r.k))
        for r in df[["job_id", "tangent_count_used", "k"]].itertuples(index=False)
    }
    report["checks"]["all_scheduled_prefix_readout_rows_present"] = (
        expected_rows <= observed_rows
    )
    report["missing_prefix_readout_rows"] = [
        list(x) for x in sorted(expected_rows - observed_rows)
    ]

    tol = cfg.get("numerical_tolerances", {})
    checks = {
        "regular_fraction": float(df["regular_fraction"].min())
        >= float(cfg.get("min_regular_fraction", 0.99)),
        "state_norm": float(df["state_norm_error"].max())
        <= float(tol.get("state_norm_error", 5e-12)),
        "horizontal_tangent": float(df["horizontal_overlap_max"].max())
        <= float(tol.get("horizontal_overlap_max", 5e-10)),
        "probability_normalization": float(df["probability_sum_error"].max())
        <= float(tol.get("probability_sum_error", 5e-12)),
        "probability_tangent_zero_sum": float(df["probability_tangent_sum_max"].max())
        <= float(tol.get("probability_tangent_sum_max", 1e-9)),
        "classical_fisher_leq_quantum_fisher": float(df["fisher_violation_max"].max())
        <= float(tol.get("fisher_violation_max", 1e-9)),
        "sample_covariance_projector_bound": float(
            df["theorem_bound_slack_sample"].min()
        ) >= -float(tol.get("projector_bound_slack", 2e-9)),
        "finite_primary_metrics": bool(
            np.isfinite(
                df[
                    [
                        "actual_retention",
                        "enhancement",
                        "pairwise_purity",
                        "deff_pairwise",
                        "Ffull_over_FQ_mean",
                    ]
                ].to_numpy(float)
            ).all()
        ),
    }
    report["checks"].update(checks)
    ok = bool(all(report["checks"].values()))
    report["valid"] = ok
    report["maxima"] = {
        "state_norm_error": float(df["state_norm_error"].max()),
        "horizontal_overlap_max": float(df["horizontal_overlap_max"].max()),
        "probability_sum_error": float(df["probability_sum_error"].max()),
        "probability_tangent_sum_max": float(
            df["probability_tangent_sum_max"].max()
        ),
        "fisher_violation_max": float(df["fisher_violation_max"].max()),
        "minimum_projector_bound_slack_sample": float(
            df["theorem_bound_slack_sample"].min()
        ),
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(report, indent=2), encoding="utf-8")
    return ok


def main() -> None:
    p = argparse.ArgumentParser(
        prog="python -m aqt.rigorous",
        description="Outcome-blind rigorous-v2 experiment engine",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("--profile", required=True)
    r.add_argument("--output", required=True)
    r.add_argument("--shard-index", type=int, default=0)
    r.add_argument("--num-shards", type=int, default=1)

    a = sub.add_parser("analyze")
    a.add_argument("--raw", action="append", required=True)
    a.add_argument("--spectrum", action="append")
    a.add_argument("--null", action="append")
    a.add_argument("--output", required=True)
    a.add_argument("--master-seed", type=int, default=77124000)

    v = sub.add_parser("validate")
    v.add_argument("--profile", required=True)
    v.add_argument("--raw", action="append", required=True)
    v.add_argument("--output", required=True)

    args = p.parse_args()
    if args.cmd == "run":
        run_profile(args.profile, args.output, args.shard_index, args.num_shards)
    elif args.cmd == "analyze":
        analyze(args.raw, args.output, args.spectrum, args.null, args.master_seed)
    else:
        ok = validate(args.profile, args.raw, args.output)
        if not ok:
            sys.exit(2)


if __name__ == "__main__":
    main()
