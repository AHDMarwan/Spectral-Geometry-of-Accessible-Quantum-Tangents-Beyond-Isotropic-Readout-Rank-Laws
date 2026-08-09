from __future__ import annotations

import glob
import json
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
    covariance_spectrum,
    direct_readout_retention,
    normalized_visible_scores,
    pairwise_purity_and_deff,
    random_rank_subspace_null,
    repeated_crossfit_kyfan,
    third_spectral_moment,
)
from .stats import bootstrap_mean_ci, bootstrap_ratio_ci, stratified_bootstrap_mean_ci


def load_profile(path: str | Path) -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ["name", "master_seed", "families", "n_values", "depth_factors", "tangents"]
    missing = [x for x in required if x not in cfg]
    if missing:
        raise ValueError(f"profile missing keys: {missing}")
    return cfg


def _family_instances(cfg: dict, family: str) -> int:
    value = cfg.get("instances", 1)
    if isinstance(value, int):
        return value
    if family in value:
        return int(value[family])
    return int(value.get("default", 1))


def build_schedule(cfg: dict) -> list[dict]:
    schedule = []
    bases = cfg.get("measurement_bases", ["Z"])
    noises = cfg.get("bitflip_rates", [0.0])
    samplers = cfg.get("direction_samplers", ["gaussian"])
    for family in cfg["families"]:
        if family not in FAMILIES:
            raise ValueError(f"unknown family {family}")
        for n in cfg["n_values"]:
            for fac in cfg["depth_factors"]:
                depth = max(1, int(round(float(fac) * int(n))))
                for instance in range(_family_instances(cfg, family)):
                    for sampler in samplers:
                        for basis in bases:
                            for eta in noises:
                                schedule.append(
                                    {
                                        "family": family,
                                        "n": int(n),
                                        "depth": depth,
                                        "depth_factor": float(fac),
                                        "instance": instance,
                                        "direction_sampler": sampler,
                                        "measurement_basis": basis,
                                        "bitflip_rate": float(eta),
                                        "tangents": int(cfg["tangents"]),
                                    }
                                )
    return schedule


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
    readout_orders = [int(k) for k in cfg.get("readout_orders", [1, 2])]
    p_floor = float(cfg.get("probability_floor", 1e-13))
    svd_tol = float(cfg.get("svd_tolerance", 1e-10))
    spectral = cfg.get("spectral", {})
    do_spectrum = bool(spectral.get("enabled", False))
    top_eigs = int(spectral.get("top_eigenvalues", 64))
    cv_repeats = int(spectral.get("crossfit_repeats", 20))
    null_cfg = cfg.get("random_readout_null", {})
    null_draws = int(null_cfg.get("draws", 0))

    for job in selected:
        family, n, depth, instance = job["family"], job["n"], job["depth"], job["instance"]
        circuit_id = f"{family}|n{n}|d{depth}|i{instance}"
        job_id = (
            f"{circuit_id}|dir={job['direction_sampler']}|basis={job['measurement_basis']}"
            f"|eta={job['bitflip_rate']:.6g}"
        )
        rng_theta = np.random.default_rng(stable_seed(circuit_id + "|theta", cfg["master_seed"]))
        _, pcount = parameter_layers(n, depth, family)
        theta = rng_theta.uniform(-np.pi, np.pi, size=pcount)
        rng_dir = np.random.default_rng(
            stable_seed(circuit_id + "|dir|" + job["direction_sampler"], cfg["master_seed"])
        )
        directions = sample_parameter_directions(
            rng_dir, job["tangents"], pcount, job["direction_sampler"]
        )
        psi, phis, _ = simulate_vqc_tangent_batch(
            n,
            depth,
            family,
            theta,
            directions,
            stable_seed(circuit_id + "|arch", cfg["master_seed"]),
        )
        psi_m, phis_m = rotate_measurement_basis(
            psi,
            phis,
            n,
            job["measurement_basis"],
            stable_seed(circuit_id + "|basis", cfg["master_seed"]),
        )
        info = normalized_visible_scores(
            psi_m,
            phis_m,
            probability_floor=p_floor,
            bitflip_rate=job["bitflip_rate"],
        )
        U = info["U"]
        if len(U) < max(6, job["tangents"] // 2):
            raise RuntimeError(f"too few regular tangents in {job_id}: {len(U)}/{job['tangents']}")
        purity, deff = pairwise_purity_and_deff(U)
        trc3 = third_spectral_moment(U)
        support_idx = np.flatnonzero(info["support"])
        ffull = info["Ffull"][info["regular"]]
        fq = info["FQ"][info["regular"]]
        ranks = []
        diag = {}
        for k in [k for k in readout_orders if k < n]:
            ret, rank, baseline = direct_readout_retention(
                U, info["p_support"], support_idx, n, k, svd_tol
            )
            diag[k] = (ret, rank, baseline)
            ranks.append(rank)
        cv = (
            repeated_crossfit_kyfan(
                U,
                sorted(set(ranks)),
                stable_seed(job_id + "|cv", cfg["master_seed"]),
                repeats=cv_repeats,
            )
            if do_spectrum
            else {}
        )
        eig = covariance_spectrum(U) if do_spectrum else np.array([])

        rows = []
        for k, (ret, rank, baseline) in diag.items():
            rows.append(
                {
                    "profile": cfg["name"],
                    "job_id": job_id,
                    "circuit_id": circuit_id,
                    **job,
                    "parameter_count": pcount,
                    "regular_tangents": len(U),
                    "support_size": len(support_idx),
                    "score_dimension": len(support_idx) - 1,
                    "FQ_mean": float(np.mean(fq)),
                    "Ffull_mean": float(np.mean(ffull)),
                    "Ffull_over_FQ_mean": float(np.mean(ffull / fq)),
                    "pairwise_purity": purity,
                    "deff_pairwise": deff,
                    "trC3_u_stat": trc3,
                    "renyi3_dimension_diag": float(trc3 ** -0.5) if trc3 > 0 else np.nan,
                    "k": k,
                    "readout_rank": rank,
                    "actual_retention": ret,
                    "rank_baseline": baseline,
                    "enhancement": ret / baseline if baseline > 0 else np.nan,
                    "crossfit_kyfan": cv.get(rank, np.nan),
                    "sample_lambda_max": float(eig[0]) if len(eig) else np.nan,
                    "sample_spectrum_rank": len(eig) if do_spectrum else 0,
                }
            )
        pd.DataFrame(rows).to_csv(raw_path, mode="a", header=not raw_path.exists(), index=False)

        if do_spectrum:
            pd.DataFrame(
                [
                    {
                        "profile": cfg["name"],
                        "job_id": job_id,
                        "circuit_id": circuit_id,
                        "eigen_index": j + 1,
                        "eigenvalue": float(x),
                    }
                    for j, x in enumerate(eig[:top_eigs])
                ]
            ).to_csv(spectrum_path, mode="a", header=not spectrum_path.exists(), index=False)

        if null_draws > 0 and job["measurement_basis"].upper() == "Z" and job["bitflip_rate"] == 0:
            null_rows = []
            sqrtp = np.sqrt(info["p_support"])
            for k, (ret, rank, baseline) in diag.items():
                draws = random_rank_subspace_null(
                    U,
                    sqrtp,
                    rank,
                    null_draws,
                    stable_seed(job_id + f"|null|k{k}", cfg["master_seed"]),
                )
                p_upper = (1.0 + np.sum(draws >= ret)) / (len(draws) + 1.0)
                null_rows.append(
                    {
                        "profile": cfg["name"],
                        "job_id": job_id,
                        "circuit_id": circuit_id,
                        "k": k,
                        "readout_rank": rank,
                        "physical_retention": ret,
                        "rank_baseline": baseline,
                        "null_mean": float(draws.mean()),
                        "null_std": float(draws.std(ddof=1)),
                        "null_q025": float(np.quantile(draws, 0.025)),
                        "null_q975": float(np.quantile(draws, 0.975)),
                        "empirical_upper_p": float(p_upper),
                        "null_draws": len(draws),
                    }
                )
            pd.DataFrame(null_rows).to_csv(null_path, mode="a", header=not null_path.exists(), index=False)
    if not raw_path.exists():
        pd.DataFrame().to_csv(raw_path, index=False)
    return raw_path


def _load_many_csv(patterns: list[str]) -> pd.DataFrame:
    paths = []
    for pat in patterns:
        paths.extend(glob.glob(pat, recursive=True))
    paths = sorted(set(paths))
    frames = []
    for p in paths:
        try:
            df = pd.read_csv(p)
        except pd.errors.EmptyDataError:
            continue
        if len(df):
            frames.append(df)
    if not frames:
        raise FileNotFoundError(f"no nonempty CSVs matched {patterns}")
    return pd.concat(frames, ignore_index=True).drop_duplicates()


def analyze(patterns: list[str], output_dir: str | Path, master_seed: int = 20260809):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    df = _load_many_csv(patterns)
    df.to_csv(out / "merged_raw.csv", index=False)
    keys = [
        "profile",
        "family",
        "n",
        "depth_factor",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "k",
    ]
    metrics = [
        "enhancement",
        "actual_retention",
        "deff_pairwise",
        "pairwise_purity",
        "trC3_u_stat",
        "Ffull_over_FQ_mean",
        "crossfit_kyfan",
    ]
    rows = []
    for group_key, g in df.groupby(keys, dropna=False):
        meta = dict(zip(keys, group_key))
        for metric in metrics:
            if metric not in g:
                continue
            seed = stable_seed("agg|" + "|".join(map(str, group_key)) + "|" + metric, master_seed)
            mean, lo, hi = bootstrap_mean_ci(g[metric], seed)
            rows.append(
                {
                    **meta,
                    "metric": metric,
                    "mean": mean,
                    "ci95_low": lo,
                    "ci95_high": hi,
                    "circuits": g["circuit_id"].nunique(),
                }
            )
    pd.DataFrame(rows).to_csv(out / "family_summary.csv", index=False)

    pooled_rows = []
    cond_keys = [
        "profile",
        "n",
        "depth_factor",
        "direction_sampler",
        "measurement_basis",
        "bitflip_rate",
        "k",
    ]
    for ckey, g0 in df.groupby(cond_keys, dropna=False):
        meta = dict(zip(cond_keys, ckey))
        for label, g in [
            ("generic_pooled", g0[g0.family != "U1-RZ-XY-line"]),
            ("U1", g0[g0.family == "U1-RZ-XY-line"]),
        ]:
            if len(g) == 0:
                continue
            for metric in metrics:
                if metric not in g:
                    continue
                seed = stable_seed("pool|" + label + "|" + "|".join(map(str, ckey)) + "|" + metric, master_seed)
                if label == "generic_pooled" and g.family.nunique() > 1:
                    mean, lo, hi = stratified_bootstrap_mean_ci(g, metric, "family", seed)
                    method = "family-stratified circuit bootstrap"
                else:
                    mean, lo, hi = bootstrap_mean_ci(g[metric], seed)
                    method = "circuit bootstrap"
                pooled_rows.append(
                    {
                        **meta,
                        "group": label,
                        "metric": metric,
                        "mean": mean,
                        "ci95_low": lo,
                        "ci95_high": hi,
                        "circuits": g.circuit_id.nunique(),
                        "bootstrap_method": method,
                    }
                )
    pd.DataFrame(pooled_rows).to_csv(out / "pooled_summary.csv", index=False)

    ratio_rows = []
    for ckey, g0 in df.groupby(cond_keys, dropna=False):
        meta = dict(zip(cond_keys, ckey))
        gu = g0[g0.family == "U1-RZ-XY-line"]
        gg = g0[g0.family != "U1-RZ-XY-line"]
        if len(gu) < 2 or len(gg) < 2:
            continue
        for metric in ["actual_retention", "enhancement", "deff_pairwise"]:
            seed = stable_seed("ratio|" + "|".join(map(str, ckey)) + "|" + metric, master_seed)
            ratio, lo, hi = bootstrap_ratio_ci(gu[metric], gg[metric], seed)
            ratio_rows.append(
                {**meta, "metric": metric, "U1_over_generic": ratio, "ci95_low": lo, "ci95_high": hi}
            )
    pd.DataFrame(ratio_rows).to_csv(out / "u1_generic_ratios.csv", index=False)

    expected = {
        (6, "generic_pooled"): {"enhancement_k1": 0.958, "enhancement_k2": 0.993, "deff": 46.1, "F": 0.4885},
        (6, "U1"): {"enhancement_k1": 2.077, "enhancement_k2": 1.186, "deff": 9.52, "F": 0.4744},
        (8, "generic_pooled"): {"enhancement_k1": 0.931, "enhancement_k2": 0.973, "deff": 136.1, "F": 0.4897},
        (8, "U1"): {"enhancement_k1": 4.224, "enhancement_k2": 1.895, "deff": 16.97, "F": 0.4785},
        (10, "generic_pooled"): {"enhancement_k1": 0.926, "enhancement_k2": 0.964, "deff": 351.6, "F": 0.4919},
        (10, "U1"): {"enhancement_k1": 9.824, "enhancement_k2": 3.607, "deff": 27.49, "F": 0.4700},
    }
    rep = df[(df.profile == "reproduce_paper") & (df.direction_sampler == "gaussian") & (df.measurement_basis == "Z") & (df.bitflip_rate == 0.0)]
    compare_rows = []
    if len(rep):
        for (n, label), tgt in expected.items():
            sub = rep[rep.n == n]
            sub = sub[sub.family == "U1-RZ-XY-line"] if label == "U1" else sub[sub.family != "U1-RZ-XY-line"]
            if len(sub) == 0:
                continue
            vals = {
                "enhancement_k1": sub[sub.k == 1].enhancement.mean(),
                "enhancement_k2": sub[sub.k == 2].enhancement.mean(),
                "deff": sub[sub.k == 1].deff_pairwise.mean(),
                "F": sub[sub.k == 1].Ffull_over_FQ_mean.mean(),
            }
            for metric, target in tgt.items():
                observed = float(vals[metric])
                compare_rows.append(
                    {"n": n, "group": label, "metric": metric, "reported": target, "rerun": observed, "difference": observed - target}
                )
    pd.DataFrame(compare_rows).to_csv(out / "paper_reproduction_comparison.csv", index=False)
    return out
