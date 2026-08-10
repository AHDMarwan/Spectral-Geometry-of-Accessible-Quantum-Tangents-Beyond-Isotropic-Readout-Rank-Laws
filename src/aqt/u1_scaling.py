from __future__ import annotations

"""High-n U(1) scaling extension for the tangent-alignment mechanism.

This module extends the existing U(1) mechanism experiment to n=14,16,18,
keeps the frozen depth d=6n and 128/128 cross-fit tangent split, and combines
those cells with the archived n=8,10,12 U(1) data.  The primary statistic is

    A_k(n) = Tr(Q_align^T P_{<=k} Q_align) / r_1,

with k=1,2.  We compare finite-size power-law and exponential fits in log space.
The output is evidence for scaling discrimination, not an asymptotic theorem.
"""

import argparse
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

from .core import stable_seed
from .metrics import walsh_readout_basis
from .stats import bootstrap_mean_ci
from .trainability_bridge import _build_readout_bases, _simulate_visible_bundle, load_profile


FAMILY = "U1-RZ-XY-line"
PRIMARY_METRIC = "cumulative_aligned_subspace_overlap"
SUMMARY_METRICS = [
    "cumulative_aligned_subspace_overlap",
    "cumulative_tangent_retention",
    "worst_aligned_principal_cos2",
    "aligned_eval_retention",
]


def _depth(cfg: dict, n: int) -> int:
    return max(1, int(round(float(cfg["depth_factor"]) * int(n))))


def run_chunk(
    profile: str | Path,
    n: int,
    instance_start: int,
    instance_stop: int,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    n = int(n)
    instance_start = int(instance_start)
    instance_stop = int(instance_stop)

    if cfg["families"] != [FAMILY]:
        raise ValueError(f"scaling profile must contain only {FAMILY!r}")
    if n not in [int(x) for x in cfg["n_values"]]:
        raise ValueError(f"n={n} is not in profile n_values")

    total_instances = int(cfg["instances"])
    if not (0 <= instance_start < instance_stop <= total_instances):
        raise ValueError(
            f"need 0 <= start < stop <= {total_instances}; got "
            f"{instance_start}, {instance_stop}"
        )

    cfg = dict(cfg)
    cfg["families"] = [FAMILY]
    cfg["n_values"] = [n]
    cfg["bitflip_rate"] = 0.0
    depth = _depth(cfg, n)
    max_order = int(cfg.get("max_walsh_order", 2))

    rows: list[dict] = []
    for instance in range(instance_start, instance_stop):
        bundle = _simulate_visible_bundle(cfg, FAMILY, n, depth, instance)
        bases, r1 = _build_readout_bases(cfg, bundle, FAMILY, n, depth, instance)
        q_align = bases["aligned_crossfit"]
        U_eval = bundle["U_eval"]
        aligned_ret = float(np.mean(np.sum((U_eval @ q_align) ** 2, axis=1)))

        prev_ret = 0.0
        prev_overlap = 0.0
        prev_rank = 0

        for order in range(1, min(max_order, n - 1) + 1):
            qk, rank_k, _ = walsh_readout_basis(
                bundle["p_support"],
                bundle["support_indices"],
                n,
                order,
                float(cfg["svd_tolerance"]),
            )
            if rank_k < 1:
                continue

            cumulative_ret = float(np.mean(np.sum((U_eval @ qk) ** 2, axis=1)))
            cross = q_align.T @ qk
            s = np.linalg.svd(cross, compute_uv=False)
            overlap = float(np.sum(s * s) / r1)
            worst_cos2 = float(np.min(s * s)) if len(s) >= r1 else 0.0

            rows.append(
                {
                    "profile": cfg["name"],
                    "circuit_id": bundle["circuit_id"],
                    "family": FAMILY,
                    "n": n,
                    "depth": depth,
                    "instance": int(instance),
                    "score_dimension": int(len(bundle["p_support"]) - 1),
                    "one_body_rank": int(r1),
                    "walsh_order": int(order),
                    "cumulative_rank": int(rank_k),
                    "incremental_rank": int(rank_k - prev_rank),
                    "aligned_eval_retention": aligned_ret,
                    "cumulative_tangent_retention": cumulative_ret,
                    "incremental_tangent_retention": float(cumulative_ret - prev_ret),
                    "cumulative_aligned_subspace_overlap": overlap,
                    "incremental_aligned_subspace_overlap": float(overlap - prev_overlap),
                    "worst_aligned_principal_cos2": worst_cos2,
                }
            )
            prev_ret = cumulative_ret
            prev_overlap = overlap
            prev_rank = rank_k

        print(
            f"[u1-scaling] n={n} instance={instance} d={depth} "
            f"r1={r1} support={len(bundle['p_support'])} done",
            flush=True,
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw = pd.DataFrame(rows)
    raw.to_csv(outdir / "raw.csv", index=False)
    (outdir / "chunk.json").write_text(
        json.dumps(
            {
                "profile": cfg["name"],
                "family": FAMILY,
                "n": n,
                "depth": depth,
                "instance_start": instance_start,
                "instance_stop": instance_stop,
                "circuits": int(raw["circuit_id"].nunique()),
                "rows": int(len(raw)),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return raw


def _summary(combined: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    rows: list[dict] = []
    for (n, order), frame in combined.groupby(["n", "walsh_order"], sort=True):
        for metric in SUMMARY_METRICS:
            mean, lo, hi = bootstrap_mean_ci(
                frame[metric].to_numpy(float),
                seed=stable_seed(
                    f"u1-scaling-summary|n{n}|k{order}|{metric}",
                    int(cfg["master_seed"]),
                ),
                n_resamples=int(cfg["bootstrap_resamples"]),
            )
            rows.append(
                {
                    "family": FAMILY,
                    "n": int(n),
                    "walsh_order": int(order),
                    "metric": metric,
                    "mean": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                    "circuits": int(frame["circuit_id"].nunique()),
                }
            )
    return pd.DataFrame(rows)


def _line_fit(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, float]:
    logy = np.log(np.asarray(y, float))
    x = np.asarray(x, float)
    slope, intercept = np.polyfit(x, logy, 1)
    residual = logy - (intercept + slope * x)
    rss = float(np.sum(residual * residual))
    nobs = len(x)
    kpar = 2
    rss_safe = max(rss, 1e-300)
    aic = nobs * math.log(rss_safe / nobs) + 2 * kpar
    if nobs > kpar + 1:
        aicc = aic + (2 * kpar * (kpar + 1)) / (nobs - kpar - 1)
    else:
        aicc = math.inf
    return float(slope), float(intercept), rss, float(aicc)


def _loocv_mse(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, float)
    logy = np.log(np.asarray(y, float))
    errors = []
    for i in range(len(x)):
        mask = np.ones(len(x), dtype=bool)
        mask[i] = False
        slope, intercept = np.polyfit(x[mask], logy[mask], 1)
        pred = intercept + slope * x[i]
        errors.append((logy[i] - pred) ** 2)
    return float(np.mean(errors))


def _fit_models_for_window(
    raw: pd.DataFrame,
    cfg: dict,
    order: int,
    n_min: int,
    label: str,
) -> dict:
    d = raw[(raw["walsh_order"] == int(order)) & (raw["n"] >= int(n_min))]
    groups = {
        int(n): g[PRIMARY_METRIC].to_numpy(float)
        for n, g in d.groupby("n", sort=True)
    }
    nvals = np.array(sorted(groups), dtype=float)
    means = np.array([np.mean(groups[int(n)]) for n in nvals], dtype=float)
    if len(nvals) < 4:
        raise RuntimeError(f"fit window {label} has fewer than four n values")
    if np.any(means <= 0):
        raise RuntimeError("overlap means must be positive for log-space fits")

    p_slope, p_intercept, p_rss, p_aicc = _line_fit(np.log(nvals), means)
    e_slope, e_intercept, e_rss, e_aicc = _line_fit(nvals, means)
    p_loocv = _loocv_mse(np.log(nvals), means)
    e_loocv = _loocv_mse(nvals, means)

    B = int(cfg["bootstrap_resamples"])
    rng = np.random.default_rng(
        stable_seed(f"u1-scaling-fit|k{order}|{label}", int(cfg["master_seed"]))
    )
    alpha_bs = np.empty(B, dtype=float)
    b_bs = np.empty(B, dtype=float)
    delta_aicc_bs = np.empty(B, dtype=float)

    for b in range(B):
        boot_means = []
        for n in nvals.astype(int):
            values = groups[int(n)]
            idx = rng.integers(0, len(values), size=len(values))
            boot_means.append(float(np.mean(values[idx])))
        boot_means = np.asarray(boot_means, float)
        ps, _, _, pa = _line_fit(np.log(nvals), boot_means)
        es, _, _, ea = _line_fit(nvals, boot_means)
        alpha_bs[b] = -ps
        b_bs[b] = -es
        delta_aicc_bs[b] = ea - pa

    delta = e_aicc - p_aicc
    return {
        "walsh_order": int(order),
        "window": label,
        "n_min": int(nvals.min()),
        "n_max": int(nvals.max()),
        "n_points": int(len(nvals)),
        "power_prefactor": float(math.exp(p_intercept)),
        "power_alpha": float(-p_slope),
        "power_alpha_ci_low": float(np.quantile(alpha_bs, 0.025)),
        "power_alpha_ci_high": float(np.quantile(alpha_bs, 0.975)),
        "power_log_rss": p_rss,
        "power_aicc": p_aicc,
        "power_loocv_log_mse": p_loocv,
        "exp_prefactor": float(math.exp(e_intercept)),
        "exp_rate_b": float(-e_slope),
        "exp_rate_b_ci_low": float(np.quantile(b_bs, 0.025)),
        "exp_rate_b_ci_high": float(np.quantile(b_bs, 0.975)),
        "exp_log_rss": e_rss,
        "exp_aicc": e_aicc,
        "exp_loocv_log_mse": e_loocv,
        "delta_aicc_exp_minus_power": float(delta),
        "delta_aicc_ci_low": float(np.quantile(delta_aicc_bs, 0.025)),
        "delta_aicc_ci_high": float(np.quantile(delta_aicc_bs, 0.975)),
        "bootstrap_fraction_power_lower_aicc": float(np.mean(delta_aicc_bs > 0)),
    }


def _fits(combined: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    rows = []
    for order in (1, 2):
        rows.append(_fit_models_for_window(combined, cfg, order, 8, "n8_to_n18"))
        rows.append(_fit_models_for_window(combined, cfg, order, 12, "tail_n12_to_n18"))
    return pd.DataFrame(rows)


def _plot(summary: pd.DataFrame, fits: pd.DataFrame, outdir: Path) -> None:
    import matplotlib.pyplot as plt

    d = summary[summary["metric"] == PRIMARY_METRIC].sort_values(
        ["walsh_order", "n"]
    )

    plt.figure(figsize=(7.5, 5.0))
    for order, g in d.groupby("walsh_order", sort=True):
        yerr = np.vstack([g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]])
        plt.errorbar(
            g["n"], g["mean"], yerr=yerr, marker="o", capsize=3, label=f"k <= {order}"
        )
    plt.xlabel("Number of qubits n")
    plt.ylabel("Aligned-subspace fraction")
    plt.title("U(1) low-weight localization of the leading tangent subspace")
    plt.yscale("log")
    plt.xticks(sorted(d["n"].unique()))
    plt.legend()
    plt.tight_layout()
    plt.savefig(outdir / "u1_aligned_overlap_vs_n_log.png", dpi=200, bbox_inches="tight")
    plt.close()

    for order in (1, 2):
        g = d[d["walsh_order"] == order].sort_values("n")
        fit = fits[(fits["walsh_order"] == order) & (fits["window"] == "n8_to_n18")].iloc[0]
        x = np.linspace(float(g["n"].min()), float(g["n"].max()), 200)
        power = fit["power_prefactor"] * x ** (-fit["power_alpha"])
        expo = fit["exp_prefactor"] * np.exp(-fit["exp_rate_b"] * x)

        plt.figure(figsize=(7.5, 5.0))
        yerr = np.vstack([g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]])
        plt.errorbar(g["n"], g["mean"], yerr=yerr, marker="o", capsize=3, label="data")
        plt.plot(x, power, label=f"power: n^(-{fit['power_alpha']:.2f})")
        plt.plot(x, expo, label=f"exp: exp(-{fit['exp_rate_b']:.3f} n)")
        plt.yscale("log")
        plt.xlabel("Number of qubits n")
        plt.ylabel("Aligned-subspace fraction")
        plt.title(f"U(1) scaling-model comparison, weight <= {order}")
        plt.xticks(sorted(g["n"].unique()))
        plt.legend()
        plt.tight_layout()
        plt.savefig(outdir / f"u1_model_comparison_k{order}.png", dpi=200, bbox_inches="tight")
        plt.close()


def _write_summary(summary: pd.DataFrame, fits: pd.DataFrame, outdir: Path) -> None:
    d = summary[summary["metric"] == PRIMARY_METRIC].sort_values(
        ["walsh_order", "n"]
    )
    lines = [
        "# U(1) alignment scaling extension",
        "",
        "Primary statistic: fraction of the cross-fitted leading rank-r1 tangent subspace inside the cumulative Walsh span of weight <= k.",
        "",
        "The n=8,10,12 cells are archived data from `u1_alignment_mechanism_v1`; n=14,16,18 are new runs with the same d=6n and 128/128 cross-fit tangent protocol.",
        "",
        "| n | k | aligned-subspace fraction | 95% bootstrap CI | circuits |",
        "|---:|---:|---:|---:|---:|",
    ]
    for _, r in d.iterrows():
        lines.append(
            f"| {int(r['n'])} | {int(r['walsh_order'])} | {r['mean']:.6f} | "
            f"[{r['ci_low']:.6f}, {r['ci_high']:.6f}] | {int(r['circuits'])} |"
        )

    lines += [
        "",
        "## Finite-size scaling discrimination",
        "",
        "Both candidate models have two fitted parameters and are fit in log-overlap space. Positive Delta AICc = AICc(exp) - AICc(power) favors the power law. LOOCV is also reported in `fits.csv`.",
        "",
        "| k | window | power alpha | 95% CI | exp rate b | 95% CI | Delta AICc (exp-power) | bootstrap P(power AICc lower) |",
        "|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for _, r in fits.sort_values(["walsh_order", "n_min"]).iterrows():
        lines.append(
            f"| {int(r['walsh_order'])} | {r['window']} | {r['power_alpha']:.4f} | "
            f"[{r['power_alpha_ci_low']:.4f}, {r['power_alpha_ci_high']:.4f}] | "
            f"{r['exp_rate_b']:.5f} | [{r['exp_rate_b_ci_low']:.5f}, {r['exp_rate_b_ci_high']:.5f}] | "
            f"{r['delta_aicc_exp_minus_power']:.3f} | "
            f"{r['bootstrap_fraction_power_lower_aicc']:.3f} |"
        )

    lines += [
        "",
        "Interpretation rule: this experiment can support finite-size polynomial-vs-exponential scaling evidence. It does not by itself prove an asymptotic lower bound or a hydrodynamic theorem.",
    ]
    (outdir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def aggregate(
    profile: str | Path,
    input_dir: str | Path,
    low_n_raw: str | Path,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    paths = sorted(Path(input_dir).rglob("raw.csv"))
    if not paths:
        raise FileNotFoundError(f"no high-n raw.csv files under {input_dir}")

    high = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    high = high.drop_duplicates(["circuit_id", "walsh_order"], keep="last")
    expected_high_circuits = int(cfg["instances"]) * len(cfg["n_values"])
    if high["circuit_id"].nunique() != expected_high_circuits:
        raise RuntimeError(
            f"high-n aggregate has {high['circuit_id'].nunique()} circuits; "
            f"expected {expected_high_circuits}"
        )
    expected_orders = set(range(1, int(cfg.get("max_walsh_order", 2)) + 1))
    for cid, frame in high.groupby("circuit_id"):
        if set(frame["walsh_order"].astype(int)) != expected_orders:
            raise RuntimeError(f"missing Walsh order for {cid}")

    low = pd.read_csv(low_n_raw)
    low = low[
        (low["family"] == FAMILY)
        & (low["n"].isin([8, 10, 12]))
        & (low["walsh_order"].isin(sorted(expected_orders)))
    ].copy()
    if low["circuit_id"].nunique() != 60:
        raise RuntimeError(
            f"expected 60 archived U1 low-n circuits, found {low['circuit_id'].nunique()}"
        )

    combined = pd.concat([low, high], ignore_index=True)
    combined = combined.drop_duplicates(["circuit_id", "walsh_order"], keep="last")
    combined = combined.sort_values(["n", "instance", "walsh_order"], kind="stable")

    expected_all_circuits = 60 + expected_high_circuits
    if combined["circuit_id"].nunique() != expected_all_circuits:
        raise RuntimeError(
            f"combined data have {combined['circuit_id'].nunique()} circuits; "
            f"expected {expected_all_circuits}"
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    high.to_csv(outdir / "raw_high_n.csv", index=False)
    combined.to_csv(outdir / "raw_combined_n8_n18.csv", index=False)

    summary = _summary(combined, cfg)
    summary.to_csv(outdir / "summary.csv", index=False)
    fits = _fits(combined, cfg)
    fits.to_csv(outdir / "fits.csv", index=False)
    _plot(summary, fits, outdir)
    _write_summary(summary, fits, outdir)

    manifest = {
        "profile": cfg,
        "high_n_cell_files": [str(p) for p in paths],
        "archived_low_n_raw": str(low_n_raw),
        "new_n_values": [int(x) for x in cfg["n_values"]],
        "combined_n_values": sorted(combined["n"].astype(int).unique().tolist()),
        "new_circuits": int(high["circuit_id"].nunique()),
        "combined_circuits": int(combined["circuit_id"].nunique()),
        "primary_metric": PRIMARY_METRIC,
        "fit_models": ["a*n^(-alpha)", "a*exp(-b*n)"],
        "fit_scope": "finite-size model discrimination; not an asymptotic proof",
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return combined


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run-chunk")
    run.add_argument("--profile", required=True)
    run.add_argument("--n", type=int, required=True)
    run.add_argument("--instance-start", type=int, required=True)
    run.add_argument("--instance-stop", type=int, required=True)
    run.add_argument("--output", required=True)

    agg = sub.add_parser("aggregate")
    agg.add_argument("--profile", required=True)
    agg.add_argument("--input-dir", required=True)
    agg.add_argument("--low-n-raw", required=True)
    agg.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.cmd == "run-chunk":
        run_chunk(
            args.profile,
            args.n,
            args.instance_start,
            args.instance_stop,
            args.output,
        )
    else:
        aggregate(args.profile, args.input_dir, args.low_n_raw, args.output)


if __name__ == "__main__":
    main()
