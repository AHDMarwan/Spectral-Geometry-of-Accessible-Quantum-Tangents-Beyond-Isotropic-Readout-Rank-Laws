from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .core import stable_seed


BOOTSTRAP_RESAMPLES = 10_000
EQUIVALENCE_LOW = 0.90
EQUIVALENCE_HIGH = 1.10
ANALYSIS_STATUS = "exploratory_post_hoc"


def _bootstrap_cell_mean(values: np.ndarray, rng: np.random.Generator) -> float:
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return float("nan")
    return float(np.mean(rng.choice(values, size=len(values), replace=True)))


def _fit_loglog(n: np.ndarray, g: np.ndarray) -> tuple[float, float, float]:
    mask = np.isfinite(n) & np.isfinite(g) & (n > 0) & (g > 0)
    x = np.log(n[mask])
    y = np.log(g[mask])
    if len(x) < 3:
        return float("nan"), float("nan"), float("nan")
    slope, intercept = np.polyfit(x, y, 1)
    fitted = intercept + slope * x
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(slope), float(intercept), float(r2)


def _fit_plateau_inv_n(n: np.ndarray, y: np.ndarray) -> tuple[float, float, float]:
    mask = np.isfinite(n) & np.isfinite(y) & (n > 0)
    x = 1.0 / n[mask]
    y = y[mask]
    if len(x) < 3:
        return float("nan"), float("nan"), float("nan")
    X = np.column_stack([np.ones(len(x)), x])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    plateau, slope_inv_n = coef
    fitted = X @ coef
    ss_res = float(np.sum((y - fitted) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return float(plateau), float(slope_inv_n), float(r2)


def _screening_label(rho_last: float, g_last: float) -> str:
    if np.isfinite(g_last) and g_last > 1.0:
        return "symmetry_aligned_outside_subcritical_bridge_scale"
    if np.isfinite(rho_last) and EQUIVALENCE_LOW <= rho_last <= EQUIVALENCE_HIGH:
        return "rank_typical_at_largest_n"
    return "structured_rank_law_deviation_at_largest_n"


def summarize_cells(frame: pd.DataFrame, master_seed: int = 77124000) -> pd.DataFrame:
    required = {
        "family",
        "n",
        "k",
        "circuit_id",
        "enhancement",
        "orientation_growth_ratio",
        "population_orientation_z",
        "r_times_deff",
        "haar_population_sd_rho",
    }
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    work = frame.copy()
    work["null_scale_factor"] = (
        pd.to_numeric(work["haar_population_sd_rho"], errors="coerce")
        * np.sqrt(pd.to_numeric(work["r_times_deff"], errors="coerce"))
    )
    work["abs_rho_minus_one"] = np.abs(
        pd.to_numeric(work["enhancement"], errors="coerce") - 1.0
    )

    rows: list[dict] = []
    metrics = [
        "enhancement",
        "abs_rho_minus_one",
        "orientation_growth_ratio",
        "population_orientation_z",
        "r_times_deff",
        "null_scale_factor",
    ]
    for (family, n, k), group in work.groupby(["family", "n", "k"], dropna=False):
        meta = {
            "family": family,
            "n": int(n),
            "k": int(k),
            "analysis_status": ANALYSIS_STATUS,
            "circuits": int(group["circuit_id"].nunique()),
        }
        for metric in metrics:
            values = pd.to_numeric(group[metric], errors="coerce").to_numpy(float)
            values = values[np.isfinite(values)]
            if len(values) == 0:
                continue
            seed = stable_seed(
                f"orientation-scaling|cell|{family}|{n}|{k}|{metric}", master_seed
            )
            rng = np.random.default_rng(seed)
            boots = np.empty(BOOTSTRAP_RESAMPLES, dtype=float)
            for b in range(BOOTSTRAP_RESAMPLES):
                boots[b] = _bootstrap_cell_mean(values, rng)
            rows.append(
                {
                    **meta,
                    "metric": metric,
                    "mean": float(np.mean(values)),
                    "ci95_low": float(np.quantile(boots, 0.025)),
                    "ci95_high": float(np.quantile(boots, 0.975)),
                }
            )
    return pd.DataFrame(rows)


def fit_scaling(frame: pd.DataFrame, master_seed: int = 77124000) -> pd.DataFrame:
    rows: list[dict] = []
    for (family, k), group0 in frame.groupby(["family", "k"], dropna=False):
        by_n = []
        for n, group in sorted(group0.groupby("n"), key=lambda item: item[0]):
            g = pd.to_numeric(group["orientation_growth_ratio"], errors="coerce").to_numpy(float)
            rho = pd.to_numeric(group["enhancement"], errors="coerce").to_numpy(float)
            g = g[np.isfinite(g)]
            rho = rho[np.isfinite(rho)]
            if len(g) and len(rho):
                by_n.append((int(n), g, rho))
        if len(by_n) < 3:
            continue

        nvals = np.array([x[0] for x in by_n], dtype=float)
        gmeans = np.array([np.mean(x[1]) for x in by_n], dtype=float)
        rhomeans = np.array([np.mean(x[2]) for x in by_n], dtype=float)
        log_slope, log_intercept, log_r2 = _fit_loglog(nvals, gmeans)
        g_plateau, g_inv_slope, g_plateau_r2 = _fit_plateau_inv_n(nvals, gmeans)
        rho_plateau, rho_inv_slope, rho_plateau_r2 = _fit_plateau_inv_n(nvals, rhomeans)

        seed = stable_seed(f"orientation-scaling|fit|{family}|{k}", master_seed)
        rng = np.random.default_rng(seed)
        boot_log_slope = np.full(BOOTSTRAP_RESAMPLES, np.nan)
        boot_g_plateau = np.full(BOOTSTRAP_RESAMPLES, np.nan)
        boot_rho_plateau = np.full(BOOTSTRAP_RESAMPLES, np.nan)
        for b in range(BOOTSTRAP_RESAMPLES):
            gb = np.array([_bootstrap_cell_mean(x[1], rng) for x in by_n], dtype=float)
            rb = np.array([_bootstrap_cell_mean(x[2], rng) for x in by_n], dtype=float)
            boot_log_slope[b] = _fit_loglog(nvals, gb)[0]
            boot_g_plateau[b] = _fit_plateau_inv_n(nvals, gb)[0]
            boot_rho_plateau[b] = _fit_plateau_inv_n(nvals, rb)[0]

        finite_slope = boot_log_slope[np.isfinite(boot_log_slope)]
        finite_g_plateau = boot_g_plateau[np.isfinite(boot_g_plateau)]
        finite_rho_plateau = boot_rho_plateau[np.isfinite(boot_rho_plateau)]
        slope_lo = float(np.quantile(finite_slope, 0.025))
        slope_hi = float(np.quantile(finite_slope, 0.975))
        g_plateau_lo = float(np.quantile(finite_g_plateau, 0.025))
        g_plateau_hi = float(np.quantile(finite_g_plateau, 0.975))
        rho_plateau_lo = float(np.quantile(finite_rho_plateau, 0.025))
        rho_plateau_hi = float(np.quantile(finite_rho_plateau, 0.975))
        if slope_hi < 0:
            trend = "decreasing"
        elif slope_lo > 0:
            trend = "increasing"
        else:
            trend = "unresolved"

        rho_last = float(rhomeans[-1])
        g_last = float(gmeans[-1])
        rows.append(
            {
                "family": family,
                "k": int(k),
                "analysis_status": ANALYSIS_STATUS,
                "n_points": int(len(nvals)),
                "n_min": int(nvals[0]),
                "n_max": int(nvals[-1]),
                "g_first": float(gmeans[0]),
                "g_last": g_last,
                "g_last_over_first": float(g_last / gmeans[0]),
                "rho_first": float(rhomeans[0]),
                "rho_last": rho_last,
                "rho_bias_last": float(rho_last - 1.0),
                "loglog_slope_g": log_slope,
                "loglog_slope_g_ci95_low": slope_lo,
                "loglog_slope_g_ci95_high": slope_hi,
                "loglog_r2_g": log_r2,
                "power_decay_exponent_g": float(-log_slope),
                "g_plateau_intercept": g_plateau,
                "g_plateau_intercept_ci95_low": g_plateau_lo,
                "g_plateau_intercept_ci95_high": g_plateau_hi,
                "g_plateau_inv_n_slope": g_inv_slope,
                "g_plateau_r2": g_plateau_r2,
                "rho_plateau_intercept": rho_plateau,
                "rho_plateau_intercept_ci95_low": rho_plateau_lo,
                "rho_plateau_intercept_ci95_high": rho_plateau_hi,
                "rho_plateau_inv_n_slope": rho_inv_slope,
                "rho_plateau_r2": rho_plateau_r2,
                "finite_size_trend_g": trend,
                "screening_label": _screening_label(rho_last, g_last),
                "screening_rule": "descriptive only: g_last>1 marks a supercritical bridge ratio; otherwise the frozen rho equivalence band [0.90,1.10] distinguishes practical rank typicality from a structured deviation",
            }
        )
    return pd.DataFrame(rows)


def make_figures(cell_summary: pd.DataFrame, output_dir: Path) -> None:
    focus = ["SU2-HaarU4-brickwork", "RY-RZ-CZ-line", "U1-RZ-XY-line"]
    labels = {
        "SU2-HaarU4-brickwork": "Haar-U4 brickwork",
        "RY-RZ-CZ-line": "RY-RZ-CZ line",
        "U1-RZ-XY-line": "U(1) RZ-XY line",
    }

    for metric, filename, ylabel, logy in [
        ("orientation_growth_ratio", "orientation_growth_scaling.pdf", r"$|z_{\rm pop}|/\sqrt{r d_{\rm eff}}$", True),
        ("enhancement", "rank_enhancement_scaling.pdf", r"$\rho_k$", True),
    ]:
        fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.2), sharey=False)
        sub = cell_summary[cell_summary["metric"] == metric]
        for ax, k in zip(axes, [1, 2]):
            for family in focus:
                g = sub[(sub["family"] == family) & (sub["k"] == k)].sort_values("n")
                if len(g) == 0:
                    continue
                y = g["mean"].to_numpy(float)
                lo = g["ci95_low"].to_numpy(float)
                hi = g["ci95_high"].to_numpy(float)
                ax.errorbar(
                    g["n"].to_numpy(float),
                    y,
                    yerr=np.vstack([y - lo, hi - y]),
                    marker="o",
                    capsize=2,
                    label=labels.get(family, family),
                )
            if metric == "orientation_growth_ratio":
                ax.axhline(1.0, linestyle="--", linewidth=1.0)
            else:
                ax.axhspan(EQUIVALENCE_LOW, EQUIVALENCE_HIGH, alpha=0.12)
                ax.axhline(1.0, linestyle="--", linewidth=1.0)
            if logy:
                ax.set_yscale("log")
            ax.set_xlabel("qubits n")
            ax.set_ylabel(ylabel)
            ax.set_title(f"k={k}")
            ax.grid(True, alpha=0.2)
        axes[0].legend(fontsize=8)
        fig.tight_layout()
        fig.savefig(output_dir / filename, bbox_inches="tight")
        plt.close(fig)


def build_scaling_analysis(
    per_circuit_path: str | Path,
    output_dir: str | Path,
    master_seed: int = 77124000,
) -> Path:
    frame = pd.read_csv(per_circuit_path)
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    cell = summarize_cells(frame, master_seed=master_seed)
    fits = fit_scaling(frame, master_seed=master_seed)
    cell.to_csv(out / "cell_summary.csv", index=False)
    fits.to_csv(out / "scaling_fits.csv", index=False)
    make_figures(cell, out)
    manifest = {
        "analysis_status": ANALYSIS_STATUS,
        "source": str(per_circuit_path),
        "bootstrap_resamples": BOOTSTRAP_RESAMPLES,
        "independent_unit": "fixed circuit instance, resampled within each n cell",
        "fit_diagnostics": {
            "loglog_g": "OLS of log(mean orientation_growth_ratio) on log(n); bootstrap resamples circuits independently within each n cell",
            "plateau_g": "OLS of mean orientation_growth_ratio on [1, 1/n]; intercept is exploratory and not a proof of a nonzero limit",
            "plateau_rho": "OLS of mean enhancement rho on [1, 1/n]; intercept is exploratory and not a proof of the physical asymptotic limit",
        },
        "diagnostic_dependence": "orientation_growth_ratio is not independent of rho: g=|rho-1|/[sigma_rho sqrt(r d_eff)], and sigma_rho sqrt(r d_eff) approaches an O(1) factor (often near sqrt(2)) in the high-dimensional regime. Treat g as a normalized restatement of the physical rank-law bias, not as separate evidence for the same claim.",
        "classification": "descriptive screen only; g_last>1 identifies a supercritical bridge ratio, otherwise the frozen rho equivalence band [0.90,1.10] is used",
        "new_quantum_simulations": False,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Exploratory scaling audit of physical orientation relative to the Haar population-null scale")
    parser.add_argument("--per-circuit", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--master-seed", type=int, default=77124000)
    args = parser.parse_args()
    build_scaling_analysis(args.per_circuit, args.output, args.master_seed)


if __name__ == "__main__":
    main()
