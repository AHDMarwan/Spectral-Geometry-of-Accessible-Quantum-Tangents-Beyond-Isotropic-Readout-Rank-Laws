from __future__ import annotations

"""
Next high-value experiments for measurement-accessible tangent geometry.

1) Robustness sweep:
   same circuit / same rank comparison under readout bit-flip noise and
   finite-shot budgets.

2) Symmetry-alignment mechanism:
   quantify how much of the cross-fitted leading tangent subspace lies inside
   cumulative low-weight Walsh readout spans.

All statistical aggregation is at the circuit-instance level.
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
from .trainability_bridge import (
    _build_readout_bases,
    _evaluate_basis,
    _family_instances,
    _paired_bootstrap_ratio,
    _prepare_fd_pairs,
    _simulate_visible_bundle,
    load_profile,
)


METHODS = ("physical", "aligned_crossfit", "random_rank")


def _depth(cfg: dict, n: int) -> int:
    return max(1, int(round(float(cfg["depth_factor"]) * int(n))))


def _result_row_base(
    cfg: dict,
    bundle: dict,
    family: str,
    n: int,
    depth: int,
    instance: int,
    method: str,
    rank: int,
) -> dict:
    return {
        "profile": cfg["name"],
        "circuit_id": bundle["circuit_id"],
        "family": family,
        "n": int(n),
        "depth": int(depth),
        "depth_factor": float(cfg["depth_factor"]),
        "instance": int(instance),
        "method": method,
        "parameter_count": int(bundle["pcount"]),
        "score_dimension": int(len(bundle["p_support"]) - 1),
        "readout_order": int(cfg["readout_order"]),
        "readout_rank": int(rank),
        "align_regular_tangents": int(len(bundle["U_train"])),
        "eval_regular_tangents": int(len(bundle["U_eval"])),
        "Ffull_eval_mean": float(np.mean(bundle["Ffull_eval"])),
        "FQ_eval_mean": float(np.mean(bundle["FQ_eval"])),
        "Ffull_over_FQ_eval_mean": float(
            np.mean(bundle["Ffull_eval"] / bundle["FQ_eval"])
        ),
        "fd_epsilon": float(cfg["fd_epsilon"]),
    }


def run_robustness_cell(
    profile: str | Path,
    family: str,
    n: int,
    bitflip_rate: float,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    n = int(n)
    eta = float(bitflip_rate)
    cfg["families"] = [family]
    cfg["n_values"] = [n]
    cfg["bitflip_rate"] = eta

    shot_budgets = [int(x) for x in cfg.get("shot_budgets", [cfg["shots"]])]
    depth = _depth(cfg, n)
    rows: list[dict] = []

    for instance in range(_family_instances(cfg, family)):
        bundle = _simulate_visible_bundle(cfg, family, n, depth, instance)
        bases, rank = _build_readout_bases(
            cfg, bundle, family, n, depth, instance
        )
        fd_pairs = _prepare_fd_pairs(cfg, bundle, family, n, depth)

        for method, q in bases.items():
            for shots in shot_budgets:
                cfg_shot = dict(cfg)
                cfg_shot["shots"] = int(shots)
                metrics = _evaluate_basis(cfg_shot, bundle, q, rank, fd_pairs)
                rows.append(
                    {
                        **_result_row_base(
                            cfg,
                            bundle,
                            family,
                            n,
                            depth,
                            instance,
                            method,
                            rank,
                        ),
                        "bitflip_rate": eta,
                        "shots": int(shots),
                        "fd_directions": int(len(fd_pairs)),
                        **metrics,
                    }
                )

        print(
            f"[robustness] {bundle['circuit_id']} eta={eta:.4g} "
            f"rank={rank} support={len(bundle['p_support'])} done",
            flush=True,
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw = pd.DataFrame(rows)
    raw.to_csv(outdir / "raw.csv", index=False)
    (outdir / "cell.json").write_text(
        json.dumps(
            {
                "profile": cfg["name"],
                "family": family,
                "n": n,
                "bitflip_rate": eta,
                "circuits": int(raw["circuit_id"].nunique()),
                "rows": int(len(raw)),
                "shot_budgets": shot_budgets,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return raw


def _baseline_zero_noise_rows(
    cfg: dict,
    baseline_raw: str | Path,
) -> pd.DataFrame:
    base = pd.read_csv(baseline_raw)
    required = {
        "circuit_id",
        "family",
        "n",
        "method",
        "shots",
        "finite_difference_snr_mean",
        "linearized_fd_snr",
    }
    missing = sorted(required - set(base.columns))
    if missing:
        raise ValueError(f"baseline raw missing columns: {missing}")

    source_shots = int(base["shots"].iloc[0])
    if not np.all(base["shots"].to_numpy(int) == source_shots):
        raise ValueError("baseline raw contains multiple source shot budgets")

    pieces = []
    for shots in [int(x) for x in cfg["shot_budgets"]]:
        frame = base.copy()
        scale = math.sqrt(shots / source_shots)
        frame["profile"] = cfg["name"]
        frame["bitflip_rate"] = 0.0
        frame["shots"] = int(shots)
        frame["finite_difference_snr_mean"] *= scale
        frame["finite_difference_snr_median"] *= scale
        frame["linearized_fd_snr"] *= scale
        pieces.append(frame)
    return pd.concat(pieces, ignore_index=True)


def _bootstrap_group_summary(
    raw: pd.DataFrame,
    cfg: dict,
    group_cols: list[str],
    metrics: list[str],
    label: str,
) -> pd.DataFrame:
    rows = []
    for keys, frame in raw.groupby(group_cols, sort=True):
        if not isinstance(keys, tuple):
            keys = (keys,)
        keydict = dict(zip(group_cols, keys))
        for metric in metrics:
            mean, lo, hi = bootstrap_mean_ci(
                frame[metric].to_numpy(float),
                seed=stable_seed(
                    label
                    + "|"
                    + "|".join(f"{k}={keydict[k]}" for k in group_cols)
                    + f"|{metric}",
                    int(cfg["master_seed"]),
                ),
                n_resamples=int(cfg["bootstrap_resamples"]),
            )
            rows.append(
                {
                    **keydict,
                    "metric": metric,
                    "mean": mean,
                    "ci_low": lo,
                    "ci_high": hi,
                    "circuits": int(frame["circuit_id"].nunique()),
                }
            )
    return pd.DataFrame(rows)


def _robustness_paired_gains(raw: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    metrics = [
        ("actual_retention", "aligned_crossfit", "physical", "aligned_over_physical"),
        (
            "expected_scalar_directional_grad2",
            "aligned_crossfit",
            "physical",
            "aligned_over_physical",
        ),
        (
            "finite_difference_snr_mean",
            "aligned_crossfit",
            "physical",
            "aligned_over_physical",
        ),
        (
            "linearized_shots_for_snr1",
            "physical",
            "aligned_crossfit",
            "physical_over_aligned",
        ),
        ("actual_retention", "random_rank", "physical", "random_over_physical"),
        (
            "expected_scalar_directional_grad2",
            "random_rank",
            "physical",
            "random_over_physical",
        ),
        (
            "finite_difference_snr_mean",
            "random_rank",
            "physical",
            "random_over_physical",
        ),
    ]
    rows = []
    group_cols = ["family", "n", "bitflip_rate", "shots"]

    for keys, frame in raw.groupby(group_cols, sort=True):
        family, n, eta, shots = keys
        for metric, numerator_method, denominator_method, contrast in metrics:
            pivot = frame.pivot(
                index="circuit_id", columns="method", values=metric
            )
            if numerator_method not in pivot or denominator_method not in pivot:
                continue
            ratio, lo, hi = _paired_bootstrap_ratio(
                pivot[numerator_method].to_numpy(float),
                pivot[denominator_method].to_numpy(float),
                stable_seed(
                    f"robust-gain|{family}|n{n}|eta{eta}|shots{shots}|"
                    f"{metric}|{contrast}",
                    int(cfg["master_seed"]),
                ),
                int(cfg["bootstrap_resamples"]),
            )
            rows.append(
                {
                    "family": family,
                    "n": int(n),
                    "bitflip_rate": float(eta),
                    "shots": int(shots),
                    "metric": metric,
                    "contrast": contrast,
                    "ratio_of_means": ratio,
                    "ci_low": lo,
                    "ci_high": hi,
                    "paired_circuits": int(len(pivot)),
                }
            )
    return pd.DataFrame(rows)


def _noise_degradation(raw: pd.DataFrame, cfg: dict) -> pd.DataFrame:
    metrics = [
        "actual_retention",
        "expected_scalar_directional_grad2",
        "finite_difference_snr_mean",
    ]
    rows = []
    for (family, n, shots, method), frame in raw.groupby(
        ["family", "n", "shots", "method"], sort=True
    ):
        for metric in metrics:
            pivot = frame.pivot(
                index="circuit_id", columns="bitflip_rate", values=metric
            )
            if 0.0 not in pivot:
                continue
            for eta in sorted(x for x in pivot.columns if float(x) > 0):
                ratio, lo, hi = _paired_bootstrap_ratio(
                    pivot[eta].to_numpy(float),
                    pivot[0.0].to_numpy(float),
                    stable_seed(
                        f"noise-degradation|{family}|n{n}|shots{shots}|"
                        f"{method}|{metric}|eta{eta}",
                        int(cfg["master_seed"]),
                    ),
                    int(cfg["bootstrap_resamples"]),
                )
                rows.append(
                    {
                        "family": family,
                        "n": int(n),
                        "shots": int(shots),
                        "method": method,
                        "metric": metric,
                        "bitflip_rate": float(eta),
                        "noisy_over_clean": ratio,
                        "ci_low": lo,
                        "ci_high": hi,
                        "paired_circuits": int(len(pivot)),
                    }
                )
    return pd.DataFrame(rows)


def aggregate_robustness(
    profile: str | Path,
    input_dir: str | Path,
    baseline_raw: str | Path,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    paths = sorted(Path(input_dir).rglob("raw.csv"))
    if not paths:
        raise FileNotFoundError(f"no robustness raw.csv files under {input_dir}")

    noisy = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    clean = _baseline_zero_noise_rows(cfg, baseline_raw)
    raw = pd.concat([clean, noisy], ignore_index=True)

    raw = raw.drop_duplicates(
        subset=["circuit_id", "method", "bitflip_rate", "shots"], keep="last"
    )
    raw = raw.sort_values(
        ["family", "n", "bitflip_rate", "shots", "instance", "method"],
        kind="stable",
    ).reset_index(drop=True)

    expected_etas = sorted(float(x) for x in cfg["bitflip_rates"])
    expected_shots = sorted(int(x) for x in cfg["shot_budgets"])
    expected_circuits = sum(
        _family_instances(cfg, family) * len(cfg["n_values"])
        for family in cfg["families"]
    )
    if raw["circuit_id"].nunique() != expected_circuits:
        raise RuntimeError(
            f"robustness aggregate has {raw['circuit_id'].nunique()} circuits; "
            f"expected {expected_circuits}"
        )

    for eta in expected_etas:
        for shots in expected_shots:
            cell = raw[
                np.isclose(raw["bitflip_rate"].to_numpy(float), eta)
                & (raw["shots"].to_numpy(int) == shots)
            ]
            if cell["circuit_id"].nunique() != expected_circuits:
                raise RuntimeError(
                    f"incomplete robustness cell eta={eta}, shots={shots}: "
                    f"{cell['circuit_id'].nunique()}/{expected_circuits} circuits"
                )
            if len(cell) != expected_circuits * len(METHODS):
                raise RuntimeError(
                    f"incomplete robustness rows eta={eta}, shots={shots}: "
                    f"{len(cell)}/{expected_circuits * len(METHODS)}"
                )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(outdir / "raw.csv", index=False)

    summary = _bootstrap_group_summary(
        raw,
        cfg,
        ["family", "n", "bitflip_rate", "shots", "method"],
        [
            "actual_retention",
            "rho",
            "expected_scalar_directional_grad2",
            "estimated_parameter_gradient_norm2",
            "finite_difference_snr_mean",
            "linearized_shots_for_snr1",
        ],
        "robustness-summary",
    )
    summary.to_csv(outdir / "summary.csv", index=False)

    gains = _robustness_paired_gains(raw, cfg)
    gains.to_csv(outdir / "paired_gains.csv", index=False)

    degradation = _noise_degradation(raw, cfg)
    degradation.to_csv(outdir / "noise_degradation.csv", index=False)

    _plot_robustness(gains, outdir)

    manifest = {
        "profile": cfg,
        "noisy_cell_files": [str(p) for p in paths],
        "baseline_raw": str(baseline_raw),
        "circuits": int(raw["circuit_id"].nunique()),
        "rows": int(len(raw)),
        "bitflip_rates": expected_etas,
        "shot_budgets": expected_shots,
        "scope": (
            "noise-aware readout geometry under an exact independent classical "
            "bit-flip channel; aligned subspace is re-estimated at each noise level"
        ),
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    _write_robustness_summary(gains, outdir)
    return raw


def _plot_robustness(gains: pd.DataFrame, outdir: Path) -> None:
    import matplotlib.pyplot as plt

    metrics = [
        (
            "expected_scalar_directional_grad2",
            "Aligned / physical gradient-signal gain under readout noise",
            "Gain ratio of means",
            "gradient_gain_vs_bitflip.png",
        ),
        (
            "finite_difference_snr_mean",
            "Aligned / physical finite-shot SNR gain under readout noise",
            "Gain ratio of means",
            "snr_gain_vs_bitflip.png",
        ),
    ]
    for metric, title, ylabel, filename in metrics:
        d = gains[
            (gains["metric"] == metric)
            & (gains["contrast"] == "aligned_over_physical")
            & (gains["shots"] == gains["shots"].max())
        ]
        plt.figure(figsize=(8.0, 5.2))
        for (family, n), g in d.groupby(["family", "n"], sort=True):
            g = g.sort_values("bitflip_rate")
            yerr = np.vstack(
                [
                    g["ratio_of_means"] - g["ci_low"],
                    g["ci_high"] - g["ratio_of_means"],
                ]
            )
            plt.errorbar(
                100.0 * g["bitflip_rate"],
                g["ratio_of_means"],
                yerr=yerr,
                marker="o",
                capsize=3,
                label=f"{family}, n={n}",
            )
        plt.axhline(1.0, linestyle="--", linewidth=1)
        plt.xlabel("Independent readout bit-flip rate (%)")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.legend(fontsize=8)
        plt.tight_layout()
        plt.savefig(outdir / filename, dpi=200, bbox_inches="tight")
        plt.close()


def _write_robustness_summary(gains: pd.DataFrame, outdir: Path) -> None:
    d = gains[
        (gains["metric"] == "expected_scalar_directional_grad2")
        & (gains["contrast"] == "aligned_over_physical")
        & (gains["shots"] == gains["shots"].max())
    ].sort_values(["family", "n", "bitflip_rate"])

    lines = [
        "# Trainability-bridge robustness summary",
        "",
        "Primary contrast: cross-fitted tangent-aligned / physical readout, same circuit and rank.",
        "",
        "| family | n | bit-flip rate | gradient-signal gain | 95% CI |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, r in d.iterrows():
        lines.append(
            f"| {r['family']} | {int(r['n'])} | {100*r['bitflip_rate']:.1f}% | "
            f"{r['ratio_of_means']:.3f}x | "
            f"[{r['ci_low']:.3f}, {r['ci_high']:.3f}] |"
        )
    lines += [
        "",
        "Interpretation: the aligned subspace is re-estimated after the specified classical readout-noise channel, so this is a noise-aware geometry test.",
    ]
    (outdir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_mechanism_cell(
    profile: str | Path,
    family: str,
    n: int,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    n = int(n)
    cfg["families"] = [family]
    cfg["n_values"] = [n]
    cfg["bitflip_rate"] = float(cfg.get("bitflip_rate", 0.0))
    depth = _depth(cfg, n)
    max_order = int(cfg.get("max_walsh_order", 4))

    rows: list[dict] = []
    for instance in range(_family_instances(cfg, family)):
        bundle = _simulate_visible_bundle(cfg, family, n, depth, instance)
        bases, r1 = _build_readout_bases(
            cfg, bundle, family, n, depth, instance
        )
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

            cumulative_ret = float(
                np.mean(np.sum((U_eval @ qk) ** 2, axis=1))
            )

            cross = q_align.T @ qk
            s = np.linalg.svd(cross, compute_uv=False)
            overlap = float(np.sum(s * s) / r1)
            worst_cos2 = float(np.min(s * s)) if len(s) >= r1 else 0.0

            rows.append(
                {
                    "profile": cfg["name"],
                    "circuit_id": bundle["circuit_id"],
                    "family": family,
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
                    "incremental_aligned_subspace_overlap": float(
                        overlap - prev_overlap
                    ),
                    "worst_aligned_principal_cos2": worst_cos2,
                }
            )

            prev_ret = cumulative_ret
            prev_overlap = overlap
            prev_rank = rank_k

        print(
            f"[mechanism] {bundle['circuit_id']} r1={r1} "
            f"support={len(bundle['p_support'])} done",
            flush=True,
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw = pd.DataFrame(rows)
    raw.to_csv(outdir / "raw.csv", index=False)
    (outdir / "cell.json").write_text(
        json.dumps(
            {
                "profile": cfg["name"],
                "family": family,
                "n": n,
                "circuits": int(raw["circuit_id"].nunique()),
                "orders": sorted(raw["walsh_order"].unique().tolist()),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return raw


def aggregate_mechanism(
    profile: str | Path,
    input_dir: str | Path,
    output: str | Path,
) -> pd.DataFrame:
    cfg = load_profile(profile)
    paths = sorted(Path(input_dir).rglob("raw.csv"))
    if not paths:
        raise FileNotFoundError(f"no mechanism raw.csv files under {input_dir}")

    raw = pd.concat([pd.read_csv(p) for p in paths], ignore_index=True)
    raw = raw.drop_duplicates(
        subset=["circuit_id", "walsh_order"], keep="last"
    )
    raw = raw.sort_values(
        ["family", "n", "instance", "walsh_order"], kind="stable"
    ).reset_index(drop=True)

    expected_circuits = sum(
        _family_instances(cfg, family) * len(cfg["n_values"])
        for family in cfg["families"]
    )
    if raw["circuit_id"].nunique() != expected_circuits:
        raise RuntimeError(
            f"mechanism aggregate has {raw['circuit_id'].nunique()} circuits; "
            f"expected {expected_circuits}"
        )

    outdir = Path(output)
    outdir.mkdir(parents=True, exist_ok=True)
    raw.to_csv(outdir / "raw.csv", index=False)

    summary = _bootstrap_group_summary(
        raw,
        cfg,
        ["family", "n", "walsh_order"],
        [
            "cumulative_tangent_retention",
            "incremental_tangent_retention",
            "cumulative_aligned_subspace_overlap",
            "incremental_aligned_subspace_overlap",
            "worst_aligned_principal_cos2",
            "aligned_eval_retention",
        ],
        "mechanism-summary",
    )
    summary.to_csv(outdir / "summary.csv", index=False)

    _plot_mechanism(summary, outdir)
    _write_mechanism_summary(summary, outdir)

    manifest = {
        "profile": cfg,
        "cell_files": [str(p) for p in paths],
        "circuits": int(raw["circuit_id"].nunique()),
        "rows": int(len(raw)),
        "mechanism_statistic": (
            "Tr(Q_align^T P_{<=k} Q_align) / r1, evaluated with a cross-fitted "
            "rank-r1 aligned subspace"
        ),
    }
    (outdir / "manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )
    return raw


def _plot_mechanism(summary: pd.DataFrame, outdir: Path) -> None:
    import matplotlib.pyplot as plt

    d = summary[
        summary["metric"] == "cumulative_aligned_subspace_overlap"
    ]
    max_n = int(d["n"].max())
    dn = d[d["n"] == max_n].sort_values(["family", "walsh_order"])

    plt.figure(figsize=(7.5, 5.0))
    for family, g in dn.groupby("family", sort=True):
        yerr = np.vstack(
            [g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]]
        )
        plt.errorbar(
            g["walsh_order"],
            g["mean"],
            yerr=yerr,
            marker="o",
            capsize=3,
            label=family,
        )
    plt.xlabel("Cumulative Walsh weight k")
    plt.ylabel("Fraction of aligned rank-r1 subspace inside weight <= k")
    plt.title(f"Low-weight localization of leading tangent subspace (n={max_n})")
    plt.ylim(-0.02, 1.02)
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        outdir / "aligned_subspace_low_weight_overlap.png",
        dpi=200,
        bbox_inches="tight",
    )
    plt.close()

    d1 = d[d["walsh_order"] == 1].sort_values(["family", "n"])
    plt.figure(figsize=(7.5, 5.0))
    for family, g in d1.groupby("family", sort=True):
        yerr = np.vstack(
            [g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]]
        )
        plt.errorbar(
            g["n"],
            g["mean"],
            yerr=yerr,
            marker="o",
            capsize=3,
            label=family,
        )
    plt.xlabel("Number of qubits n")
    plt.ylabel("Aligned subspace captured by one-body Walsh span")
    plt.title("One-body localization of the cross-fitted leading tangent subspace")
    plt.ylim(-0.02, 1.02)
    plt.legend()
    plt.tight_layout()
    plt.savefig(
        outdir / "one_body_aligned_overlap_vs_n.png",
        dpi=200,
        bbox_inches="tight",
    )
    plt.close()


def _write_mechanism_summary(summary: pd.DataFrame, outdir: Path) -> None:
    d = summary[
        summary["metric"] == "cumulative_aligned_subspace_overlap"
    ].sort_values(["family", "n", "walsh_order"])

    lines = [
        "# Symmetry-alignment mechanism summary",
        "",
        "Statistic: fraction of the cross-fitted leading rank-r1 tangent subspace contained in the cumulative Walsh readout span of weight <= k.",
        "",
        "| family | n | k | aligned-subspace fraction | 95% CI |",
        "|---|---:|---:|---:|---:|",
    ]
    for _, r in d.iterrows():
        lines.append(
            f"| {r['family']} | {int(r['n'])} | {int(r['walsh_order'])} | "
            f"{r['mean']:.4f} | [{r['ci_low']:.4f}, {r['ci_high']:.4f}] |"
        )
    (outdir / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("robustness-cell")
    r.add_argument("--profile", required=True)
    r.add_argument("--family", required=True)
    r.add_argument("--n", type=int, required=True)
    r.add_argument("--bitflip-rate", type=float, required=True)
    r.add_argument("--output", required=True)

    ra = sub.add_parser("robustness-aggregate")
    ra.add_argument("--profile", required=True)
    ra.add_argument("--input-dir", required=True)
    ra.add_argument("--baseline-raw", required=True)
    ra.add_argument("--output", required=True)

    m = sub.add_parser("mechanism-cell")
    m.add_argument("--profile", required=True)
    m.add_argument("--family", required=True)
    m.add_argument("--n", type=int, required=True)
    m.add_argument("--output", required=True)

    ma = sub.add_parser("mechanism-aggregate")
    ma.add_argument("--profile", required=True)
    ma.add_argument("--input-dir", required=True)
    ma.add_argument("--output", required=True)

    args = parser.parse_args()
    if args.cmd == "robustness-cell":
        run_robustness_cell(
            args.profile,
            args.family,
            args.n,
            args.bitflip_rate,
            args.output,
        )
    elif args.cmd == "robustness-aggregate":
        aggregate_robustness(
            args.profile,
            args.input_dir,
            args.baseline_raw,
            args.output,
        )
    elif args.cmd == "mechanism-cell":
        run_mechanism_cell(args.profile, args.family, args.n, args.output)
    else:
        aggregate_mechanism(args.profile, args.input_dir, args.output)


if __name__ == "__main__":
    main()
