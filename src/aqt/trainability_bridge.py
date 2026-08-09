from __future__ import annotations

"""
Cross-fitted trainability bridge for Measurement-Accessible Quantum Tangent Geometry.

Controlled comparison on the SAME circuit instance, SAME computational-basis
measurement record, SAME readout rank, and SAME shot budget:

    physical low-weight readout
    vs.
    cross-fitted tangent-aligned rank-matched readout
    vs.
    Haar-random rank-matched readout.

The aligned subspace is learned only from an independent set of tangent directions.
All reported accessibility / gradient quantities are evaluated on held-out tangents.

Main outputs per circuit and method
-----------------------------------
actual_retention
    E_v ||P u_v||^2 for normalized visible tangent scores u_v.

rho
    actual_retention / (rank / centered_score_dimension).

raw_gradient_energy
    E_v [ F_full(v) ||P u_v||^2 ].
    This equals the summed squared directional derivatives of an orthonormal,
    whitened set of readout coordinates.

expected_scalar_directional_grad2
    raw_gradient_energy / rank.
    This is the variance of the directional derivative when the scalar linear
    readout is drawn isotropically inside the rank-r readout span.

estimated_parameter_gradient_norm2
    parameter_count * expected_scalar_directional_grad2.
    For isotropic unit parameter directions v,
    E_v[(v . grad L)^2] = ||grad L||^2 / parameter_count.

finite_difference_snr
    Exact finite-difference signal divided by the analytic multinomial shot-noise
    standard deviation for the same number of shots at theta +/- epsilon v.
    No Monte-Carlo shot sampling is needed.

Important scope
---------------
This is a controlled linear-readout bridge, not a supervised-learning benchmark.
It directly tests whether the geometry predicts local loss-gradient strength and
finite-shot resolvability. A later experiment can add data encoding, labels,
nonlinear heads, and end-to-end training.
"""

import argparse
import json
import math
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
    normalized_visible_scores_from_pdp,
    probability_tangent_batch,
    walsh_readout_basis,
)
from .stats import bootstrap_mean_ci


METHODS = ("physical", "aligned_crossfit", "random_rank")


def load_profile(path: str | Path) -> dict:
    cfg = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {
        "name",
        "master_seed",
        "families",
        "n_values",
        "depth_factor",
        "instances",
        "align_tangents",
        "eval_tangents",
        "readout_order",
        "shots",
        "fd_epsilon",
        "fd_directions",
    }
    missing = sorted(required - set(cfg))
    if missing:
        raise ValueError(f"profile missing keys: {missing}")

    for family in cfg["families"]:
        if family not in FAMILIES:
            raise ValueError(f"unknown circuit family: {family!r}")

    if int(cfg["align_tangents"]) < 8 or int(cfg["eval_tangents"]) < 8:
        raise ValueError("need at least 8 alignment and 8 evaluation tangents")
    if int(cfg["readout_order"]) < 1:
        raise ValueError("readout_order must be >= 1")
    if int(cfg["shots"]) < 1:
        raise ValueError("shots must be positive")
    if float(cfg["fd_epsilon"]) <= 0:
        raise ValueError("fd_epsilon must be positive")
    if int(cfg["fd_directions"]) < 0:
        raise ValueError("fd_directions must be non-negative")

    cfg.setdefault("direction_sampler", "gaussian")
    cfg.setdefault("measurement_basis", "Z")
    cfg.setdefault("bitflip_rate", 0.0)
    cfg.setdefault("simulation_batch_size", 32)
    cfg.setdefault("probability_floor", 1e-13)
    cfg.setdefault("svd_tolerance", 1e-10)
    cfg.setdefault("bootstrap_resamples", 10000)
    cfg.setdefault("min_regular_fraction", 0.95)
    return cfg


def _family_instances(cfg: dict, family: str) -> int:
    value = cfg["instances"]
    if isinstance(value, int):
        return int(value)
    return int(value.get(family, value.get("default", 1)))


def _circuit_id(family: str, n: int, depth: int, instance: int) -> str:
    return f"{family}|n{n}|d{depth}|i{instance}"


def _draw_circuit_and_directions(
    cfg: dict,
    family: str,
    n: int,
    depth: int,
    instance: int,
):
    circuit_id = _circuit_id(family, n, depth, instance)
    _, pcount = parameter_layers(n, depth, family)

    rng_theta = np.random.default_rng(
        stable_seed(circuit_id + "|theta", int(cfg["master_seed"]))
    )
    theta = rng_theta.uniform(-np.pi, np.pi, size=pcount)

    total = int(cfg["align_tangents"]) + int(cfg["eval_tangents"])
    rng_dir = np.random.default_rng(
        stable_seed(
            circuit_id + "|bridge-directions|" + str(cfg["direction_sampler"]),
            int(cfg["master_seed"]),
        )
    )
    directions = sample_parameter_directions(
        rng_dir,
        total,
        pcount,
        str(cfg["direction_sampler"]),
    )

    arch_seed = stable_seed(
        circuit_id + "|architecture", int(cfg["master_seed"])
    )
    basis_seed = stable_seed(
        circuit_id + "|measurement-basis", int(cfg["master_seed"])
    )
    return circuit_id, pcount, theta, directions, arch_seed, basis_seed


def _simulate_visible_bundle(
    cfg: dict,
    family: str,
    n: int,
    depth: int,
    instance: int,
) -> dict:
    (
        circuit_id,
        pcount,
        theta,
        directions,
        arch_seed,
        basis_seed,
    ) = _draw_circuit_and_directions(cfg, family, n, depth, instance)

    batch_size = max(1, int(cfg["simulation_batch_size"]))
    p_floor = float(cfg["probability_floor"])

    p_ref = None
    support_ref = None
    psi_ref = None

    U_parts: list[np.ndarray] = []
    ffull_parts: list[np.ndarray] = []
    fq_parts: list[np.ndarray] = []
    regular_indices: list[int] = []

    total = len(directions)

    for start in range(0, total, batch_size):
        stop = min(total, start + batch_size)

        psi, phis, _ = simulate_vqc_tangent_batch(
            n=n,
            depth=depth,
            family=family,
            theta=theta,
            directions=directions[start:stop],
            architecture_seed=arch_seed,
        )
        psi, phis = rotate_measurement_basis(
            psi,
            phis,
            n,
            str(cfg["measurement_basis"]),
            basis_seed,
        )

        p, dp = probability_tangent_batch(psi, phis)
        fq = 4.0 * np.sum(np.abs(phis) ** 2, axis=1).real

        eta = float(cfg["bitflip_rate"])
        if eta:
            p, dp = apply_independent_bitflip_channel(p, dp, n, eta)

        info = normalized_visible_scores_from_pdp(
            p,
            dp,
            fq,
            probability_floor=p_floor,
        )

        if p_ref is None:
            p_ref = info["p"].copy()
            support_ref = info["support"].copy()
            psi_ref = psi.copy()
        else:
            if not np.allclose(p_ref, info["p"], rtol=0.0, atol=5e-13):
                raise RuntimeError(f"{circuit_id}: probabilities changed across batches")
            if not np.array_equal(support_ref, info["support"]):
                raise RuntimeError(f"{circuit_id}: support changed across batches")
            if not np.allclose(psi_ref, psi, rtol=0.0, atol=5e-13):
                raise RuntimeError(f"{circuit_id}: state changed across batches")

        reg_local = np.flatnonzero(info["regular"])
        if len(reg_local):
            regular_indices.extend((start + reg_local).tolist())
            U_parts.append(info["U"])
            ffull_parts.append(info["Ffull"][info["regular"]])
            fq_parts.append(info["FQ"][info["regular"]])

    if not U_parts:
        raise RuntimeError(f"{circuit_id}: no regular tangent directions")

    U = np.vstack(U_parts)
    ffull = np.concatenate(ffull_parts)
    fq = np.concatenate(fq_parts)
    regular_indices_arr = np.asarray(regular_indices, dtype=int)

    align_count = int(cfg["align_tangents"])
    train_mask = regular_indices_arr < align_count
    eval_mask = regular_indices_arr >= align_count

    min_fraction = float(cfg["min_regular_fraction"])
    min_train = math.ceil(min_fraction * int(cfg["align_tangents"]))
    min_eval = math.ceil(min_fraction * int(cfg["eval_tangents"]))

    if int(train_mask.sum()) < min_train:
        raise RuntimeError(
            f"{circuit_id}: only {train_mask.sum()} regular alignment tangents; "
            f"required >= {min_train}"
        )
    if int(eval_mask.sum()) < min_eval:
        raise RuntimeError(
            f"{circuit_id}: only {eval_mask.sum()} regular evaluation tangents; "
            f"required >= {min_eval}"
        )

    support_indices = np.flatnonzero(support_ref)

    return {
        "circuit_id": circuit_id,
        "pcount": pcount,
        "theta": theta,
        "directions": directions,
        "arch_seed": arch_seed,
        "basis_seed": basis_seed,
        "p": p_ref,
        "support": support_ref,
        "support_indices": support_indices,
        "p_support": p_ref[support_ref],
        "U_train": U[train_mask],
        "Ffull_train": ffull[train_mask],
        "U_eval": U[eval_mask],
        "Ffull_eval": ffull[eval_mask],
        "FQ_eval": fq[eval_mask],
        "eval_global_indices": regular_indices_arr[eval_mask],
    }


def _centered_orthonormalize(
    q: np.ndarray,
    sqrt_p: np.ndarray,
    rank: int,
) -> np.ndarray:
    w = sqrt_p / np.linalg.norm(sqrt_p)
    q = q - w[:, None] * (w @ q)[None, :]
    q, _ = np.linalg.qr(q, mode="reduced")
    q = q[:, :rank]

    if q.shape[1] != rank:
        raise RuntimeError("could not construct requested centered rank")
    if np.linalg.norm(q.T @ q - np.eye(rank)) > 1e-8:
        raise RuntimeError("readout basis lost orthonormality")
    if np.linalg.norm(w @ q) > 1e-8:
        raise RuntimeError("readout basis is not centered")
    return q


def _build_readout_bases(
    cfg: dict,
    bundle: dict,
    family: str,
    n: int,
    depth: int,
    instance: int,
) -> tuple[dict[str, np.ndarray], int]:
    q_phys, rank, _ = walsh_readout_basis(
        bundle["p_support"],
        bundle["support_indices"],
        n,
        int(cfg["readout_order"]),
        float(cfg["svd_tolerance"]),
    )
    if rank < 1:
        raise RuntimeError(f"{bundle['circuit_id']}: physical readout rank is zero")

    sqrt_p = np.sqrt(bundle["p_support"])
    q_phys = _centered_orthonormalize(q_phys, sqrt_p, rank)

    # Cross-fit: learn the leading score-space directions from independent tangents.
    U_train = bundle["U_train"]
    if U_train.shape[0] < rank:
        raise RuntimeError(
            f"{bundle['circuit_id']}: alignment sample has {U_train.shape[0]} rows "
            f"but physical rank is {rank}"
        )
    _, _, vh = np.linalg.svd(U_train, full_matrices=False)
    if vh.shape[0] < rank:
        raise RuntimeError(
            f"{bundle['circuit_id']}: SVD supplies only {vh.shape[0]} directions "
            f"for requested rank {rank}"
        )
    q_align = _centered_orthonormalize(vh[:rank].T, sqrt_p, rank)

    rng = np.random.default_rng(
        stable_seed(
            bundle["circuit_id"] + "|random-rank-readout",
            int(cfg["master_seed"]),
        )
    )
    a = rng.normal(size=(len(sqrt_p), rank))
    q_rand = _centered_orthonormalize(a, sqrt_p, rank)

    return {
        "physical": q_phys,
        "aligned_crossfit": q_align,
        "random_rank": q_rand,
    }, rank


def _probability_at(
    cfg: dict,
    bundle: dict,
    family: str,
    n: int,
    depth: int,
    theta: np.ndarray,
) -> np.ndarray:
    zero_direction = np.zeros((1, bundle["pcount"]), dtype=float)
    psi, phis, _ = simulate_vqc_tangent_batch(
        n=n,
        depth=depth,
        family=family,
        theta=theta,
        directions=zero_direction,
        architecture_seed=bundle["arch_seed"],
    )
    psi, _ = rotate_measurement_basis(
        psi,
        phis,
        n,
        str(cfg["measurement_basis"]),
        bundle["basis_seed"],
    )
    p = np.abs(psi) ** 2

    eta = float(cfg["bitflip_rate"])
    if eta:
        dummy = np.zeros((1, len(p)), dtype=float)
        p, _ = apply_independent_bitflip_channel(p, dummy, n, eta)
    return p


def _prepare_fd_pairs(
    cfg: dict,
    bundle: dict,
    family: str,
    n: int,
    depth: int,
) -> list[dict]:
    requested = min(int(cfg["fd_directions"]), len(bundle["U_eval"]))
    if requested == 0:
        return []

    rng = np.random.default_rng(
        stable_seed(
            bundle["circuit_id"] + "|fd-heldout-selection",
            int(cfg["master_seed"]),
        )
    )
    chosen = np.sort(rng.choice(len(bundle["U_eval"]), size=requested, replace=False))
    eps = float(cfg["fd_epsilon"])

    pairs = []
    for local_idx in chosen:
        global_idx = int(bundle["eval_global_indices"][local_idx])
        v = bundle["directions"][global_idx]

        p_plus = _probability_at(
            cfg, bundle, family, n, depth, bundle["theta"] + eps * v
        )
        p_minus = _probability_at(
            cfg, bundle, family, n, depth, bundle["theta"] - eps * v
        )

        pairs.append(
            {
                "local_eval_index": int(local_idx),
                "global_direction_index": global_idx,
                "p_plus": p_plus,
                "p_minus": p_minus,
            }
        )
    return pairs


def _fd_metrics_for_basis(
    cfg: dict,
    bundle: dict,
    q: np.ndarray,
    fd_pairs: list[dict],
) -> dict:
    if not fd_pairs:
        return {
            "finite_difference_snr_mean": np.nan,
            "finite_difference_snr_median": np.nan,
            "finite_difference_grad2_mean": np.nan,
            "finite_difference_relative_error_mean": np.nan,
        }

    support_idx = bundle["support_indices"]
    p0 = bundle["p_support"]
    rank = q.shape[1]
    eps = float(cfg["fd_epsilon"])
    shots = int(cfg["shots"])

    # Whitened feature functions. At theta_0:
    # E_p[f] = 0 and Cov_p(f) = I_r.
    features = q / np.sqrt(p0)[:, None]

    snrs = []
    grad2s = []
    rel_errors = []

    for item in fd_pairs:
        j = int(item["local_eval_index"])
        pp = item["p_plus"][support_idx]
        pm = item["p_minus"][support_idx]

        # If support leaks under the finite step, the fixed-support feature map is
        # no longer exact. This should not occur for the current frozen Z-readout
        # families at the chosen small epsilon.
        outside = np.ones_like(bundle["p"], dtype=bool)
        outside[support_idx] = False
        leak = float(
            item["p_plus"][outside].sum() + item["p_minus"][outside].sum()
        )
        if leak > 1e-9:
            raise RuntimeError(
                f"{bundle['circuit_id']}: finite-step probability leaked outside "
                f"the base support by {leak:.3e}"
            )

        mu_plus = pp @ features
        mu_minus = pm @ features
        fd_derivative = (mu_plus - mu_minus) / (2.0 * eps)

        # Multinomial shot-noise variance of each feature coordinate.
        var_plus = pp @ (features * features) - mu_plus * mu_plus
        var_minus = pm @ (features * features) - mu_minus * mu_minus
        var_plus = np.clip(var_plus, 0.0, None)
        var_minus = np.clip(var_minus, 0.0, None)

        derivative_noise_trace = float(
            (var_plus.sum() + var_minus.sum())
            / (4.0 * eps * eps * shots)
        )
        signal2 = float(np.dot(fd_derivative, fd_derivative))
        snr = (
            math.sqrt(signal2 / derivative_noise_trace)
            if derivative_noise_trace > 0
            else np.inf
        )

        # Analytic directional derivative from the tangent simulation.
        analytic = (
            math.sqrt(float(bundle["Ffull_eval"][j]))
            * (bundle["U_eval"][j] @ q)
        )
        denom = max(float(np.linalg.norm(analytic)), 1e-14)
        rel_error = float(np.linalg.norm(fd_derivative - analytic) / denom)

        snrs.append(snr)
        grad2s.append(signal2 / rank)
        rel_errors.append(rel_error)

    return {
        "finite_difference_snr_mean": float(np.mean(snrs)),
        "finite_difference_snr_median": float(np.median(snrs)),
        "finite_difference_grad2_mean": float(np.mean(grad2s)),
        "finite_difference_relative_error_mean": float(np.mean(rel_errors)),
    }


def _evaluate_basis(
    cfg: dict,
    bundle: dict,
    q: np.ndarray,
    rank: int,
    fd_pairs: list[dict],
) -> dict:
    U = bundle["U_eval"]
    ffull = bundle["Ffull_eval"]

    coeff = U @ q
    projection_mass = np.sum(coeff * coeff, axis=1)

    actual_retention = float(np.mean(projection_mass))
    nscore = len(bundle["p_support"]) - 1
    rank_baseline = rank / nscore
    rho = actual_retention / rank_baseline

    # Raw local derivative energy of r whitened readout coordinates.
    per_direction_gradient_energy = ffull * projection_mass
    raw_gradient_energy = float(np.mean(per_direction_gradient_energy))

    # Average over an isotropic scalar linear objective a in R^r, ||a||=1:
    # E_a[(d/dt a^T mu(theta+t v))^2] = gradient_energy / r.
    expected_scalar_directional_grad2 = raw_gradient_energy / rank
    estimated_parameter_gradient_norm2 = (
        bundle["pcount"] * expected_scalar_directional_grad2
    )

    eps = float(cfg["fd_epsilon"])
    shots = int(cfg["shots"])

    # Localized prediction using Cov_p(f)=I_r at theta_0.
    linearized_fd_snr = math.sqrt(
        max(0.0, 2.0 * eps * eps * shots * expected_scalar_directional_grad2)
    )
    shots_for_snr1 = (
        1.0 / (2.0 * eps * eps * expected_scalar_directional_grad2)
        if expected_scalar_directional_grad2 > 0
        else np.inf
    )

    return {
        "actual_retention": actual_retention,
        "rank_baseline": float(rank_baseline),
        "rho": float(rho),
        "raw_gradient_energy": raw_gradient_energy,
        "expected_scalar_directional_grad2": float(
            expected_scalar_directional_grad2
        ),
        "estimated_parameter_gradient_norm2": float(
            estimated_parameter_gradient_norm2
        ),
        "linearized_fd_snr": float(linearized_fd_snr),
        "linearized_shots_for_snr1": float(shots_for_snr1),
        **_fd_metrics_for_basis(cfg, bundle, q, fd_pairs),
    }


def run_profile(profile: str | Path, output: str | Path) -> pd.DataFrame:
    cfg = load_profile(profile)
    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)

    rows = []

    for family in cfg["families"]:
        for n_raw in cfg["n_values"]:
            n = int(n_raw)
            depth = max(1, int(round(float(cfg["depth_factor"]) * n)))

            for instance in range(_family_instances(cfg, family)):
                bundle = _simulate_visible_bundle(
                    cfg, family, n, depth, instance
                )
                bases, rank = _build_readout_bases(
                    cfg, bundle, family, n, depth, instance
                )
                fd_pairs = _prepare_fd_pairs(
                    cfg, bundle, family, n, depth
                )

                for method, q in bases.items():
                    metrics = _evaluate_basis(
                        cfg, bundle, q, rank, fd_pairs
                    )
                    rows.append(
                        {
                            "profile": cfg["name"],
                            "circuit_id": bundle["circuit_id"],
                            "family": family,
                            "n": n,
                            "depth": depth,
                            "depth_factor": float(cfg["depth_factor"]),
                            "instance": int(instance),
                            "method": method,
                            "parameter_count": int(bundle["pcount"]),
                            "score_dimension": int(
                                len(bundle["p_support"]) - 1
                            ),
                            "readout_order": int(cfg["readout_order"]),
                            "readout_rank": int(rank),
                            "align_regular_tangents": int(
                                len(bundle["U_train"])
                            ),
                            "eval_regular_tangents": int(
                                len(bundle["U_eval"])
                            ),
                            "Ffull_eval_mean": float(
                                np.mean(bundle["Ffull_eval"])
                            ),
                            "FQ_eval_mean": float(
                                np.mean(bundle["FQ_eval"])
                            ),
                            "Ffull_over_FQ_eval_mean": float(
                                np.mean(
                                    bundle["Ffull_eval"]
                                    / bundle["FQ_eval"]
                                )
                            ),
                            "shots": int(cfg["shots"]),
                            "fd_epsilon": float(cfg["fd_epsilon"]),
                            "fd_directions": int(len(fd_pairs)),
                            **metrics,
                        }
                    )

                print(
                    f"[bridge] {bundle['circuit_id']} "
                    f"rank={rank} support={len(bundle['p_support'])} done",
                    flush=True,
                )

    raw = pd.DataFrame(rows)
    raw.to_csv(outdir / "raw.csv", index=False)

    summary = summarize(raw, cfg)
    summary.to_csv(outdir / "summary.csv", index=False)

    gains = paired_gains(raw, cfg)
    gains.to_csv(outdir / "paired_gains.csv", index=False)

    manifest = {
        "profile": cfg,
        "outputs": [
            "raw.csv",
            "summary.csv",
            "paired_gains.csv",
        ],
        "interpretation": {
            "primary_bridge_metric": "expected_scalar_directional_grad2",
            "primary_operational_metric": "finite_difference_snr_mean",
            "primary_contrast": "aligned_crossfit / physical on the same circuit",
            "warning": (
                "This is a controlled local linear-readout trainability bridge, "
                "not a supervised barren-plateau claim."
            ),
        },
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )

    return raw


def summarize(raw: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    metrics = [
        "actual_retention",
        "rho",
        "expected_scalar_directional_grad2",
        "estimated_parameter_gradient_norm2",
        "linearized_fd_snr",
        "finite_difference_snr_mean",
        "finite_difference_grad2_mean",
        "finite_difference_relative_error_mean",
    ]
    rows = []

    for (family, n, method), frame in raw.groupby(
        ["family", "n", "method"], sort=True
    ):
        for metric in metrics:
            mean, lo, hi = bootstrap_mean_ci(
                frame[metric].to_numpy(float),
                seed=stable_seed(
                    f"bridge-summary|{family}|n{n}|{method}|{metric}",
                    int(cfg["master_seed"]),
                ),
                n_resamples=int(cfg["bootstrap_resamples"]),
            )
            rows.append(
                {
                    "family": family,
                    "n": int(n),
                    "method": method,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                    "circuits": int(len(frame)),
                }
            )
    return pd.DataFrame(rows)


def _paired_bootstrap_ratio(
    numerator: np.ndarray,
    denominator: np.ndarray,
    seed: int,
    n_resamples: int,
) -> tuple[float, float, float]:
    a = np.asarray(numerator, float)
    b = np.asarray(denominator, float)
    mask = np.isfinite(a) & np.isfinite(b) & (b > 0)
    a, b = a[mask], b[mask]
    if len(a) == 0:
        return np.nan, np.nan, np.nan
    observed = float(a.mean() / b.mean())
    if len(a) == 1:
        return observed, np.nan, np.nan

    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(a), size=(n_resamples, len(a)))
    ratio = a[idx].mean(axis=1) / b[idx].mean(axis=1)
    return (
        observed,
        float(np.quantile(ratio, 0.025)),
        float(np.quantile(ratio, 0.975)),
    )


def paired_gains(raw: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    metrics = [
        "actual_retention",
        "expected_scalar_directional_grad2",
        "finite_difference_snr_mean",
    ]
    rows = []

    for (family, n), frame in raw.groupby(["family", "n"], sort=True):
        for metric in metrics:
            p = frame.pivot(
                index="circuit_id",
                columns="method",
                values=metric,
            )
            if "physical" not in p or "aligned_crossfit" not in p:
                continue

            ratio, lo, hi = _paired_bootstrap_ratio(
                p["aligned_crossfit"].to_numpy(float),
                p["physical"].to_numpy(float),
                stable_seed(
                    f"bridge-gain|{family}|n{n}|{metric}",
                    int(cfg["master_seed"]),
                ),
                int(cfg["bootstrap_resamples"]),
            )
            rows.append(
                {
                    "family": family,
                    "n": int(n),
                    "metric": metric,
                    "contrast": "aligned_crossfit_over_physical",
                    "ratio_of_means": ratio,
                    "ci_low": lo,
                    "ci_high": hi,
                    "paired_circuits": int(len(p)),
                }
            )

            if "random_rank" in p:
                ratio, lo, hi = _paired_bootstrap_ratio(
                    p["random_rank"].to_numpy(float),
                    p["physical"].to_numpy(float),
                    stable_seed(
                        f"bridge-gain-random|{family}|n{n}|{metric}",
                        int(cfg["master_seed"]),
                    ),
                    int(cfg["bootstrap_resamples"]),
                )
                rows.append(
                    {
                        "family": family,
                        "n": int(n),
                        "metric": metric,
                        "contrast": "random_rank_over_physical",
                        "ratio_of_means": ratio,
                        "ci_low": lo,
                        "ci_high": hi,
                        "paired_circuits": int(len(p)),
                    }
                )

    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Cross-fitted same-rank trainability bridge: physical vs "
            "tangent-aligned vs random readout."
        )
    )
    parser.add_argument("--profile", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    run_profile(args.profile, args.output)


if __name__ == "__main__":
    main()
