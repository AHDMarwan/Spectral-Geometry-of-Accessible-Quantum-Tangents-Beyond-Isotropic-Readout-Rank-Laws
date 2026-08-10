from __future__ import annotations

"""Generate publication-grade figures used by the production rewrite.

The script reads small, paper-facing CSV tables committed under ``paper/prx/data``
so that figure generation is deterministic and does not require rerunning the
quantum simulations.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "paper" / "prx" / "data"
OUT = ROOT / "paper" / "prx" / "figures" / "production"
OUT.mkdir(parents=True, exist_ok=True)

# Journal-friendly, color-blind-safe palette; marker/line-style differences
# keep the figures readable in grayscale as well.
BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
PURPLE = "#7B2CBF"
GREY = "#5B5B5B"
LIGHT_GREY = "#D9D9D9"


def _style() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9.5,
            "axes.labelsize": 10,
            "axes.titlesize": 10.5,
            "legend.fontsize": 8.5,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "axes.linewidth": 0.8,
            "xtick.major.width": 0.8,
            "ytick.major.width": 0.8,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def _save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight")
    fig.savefig(OUT / f"{name}.png", dpi=360, bbox_inches="tight")
    plt.close(fig)


def u1_scaling() -> None:
    summary = pd.read_csv(DATA / "u1_alignment_scaling_summary.csv")
    fits = pd.read_csv(DATA / "u1_alignment_scaling_fits.csv")
    d = summary[summary.metric == "cumulative_aligned_subspace_overlap"].copy()

    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.0), sharey=True)
    for ax, order, color, title in [
        (axes[0], 1, BLUE, r"one-body span, $k=1$"),
        (axes[1], 2, ORANGE, r"cumulative span, $k\leq2$"),
    ]:
        g = d[d.walsh_order == order].sort_values("n")
        yerr = np.vstack([g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]])
        ax.errorbar(
            g["n"], g["mean"], yerr=yerr, fmt="o", ms=4.5,
            capsize=2.5, lw=1.2, color=color, label="circuit bootstrap"
        )
        fit = fits[(fits.walsh_order == order) & (fits.window == "n8_to_n18")].iloc[0]
        x = np.linspace(8, 18, 300)
        power = fit.power_prefactor * x ** (-fit.power_alpha)
        expo = fit.exp_prefactor * np.exp(-fit.exp_rate_b * x)
        ax.plot(x, power, color=color, lw=1.7,
                label=rf"power $n^{{-{fit.power_alpha:.2f}}}$")
        ax.plot(x, expo, color=GREY, lw=1.3, ls="--", label="exponential")
        ax.set_title(title)
        ax.set_xlabel("qubits $n$")
        ax.set_xticks([8, 10, 12, 14, 16, 18])
        ax.set_xlim(7.5, 18.5)
        ax.grid(axis="y", alpha=0.18, lw=0.6)
        ax.text(
            0.04, 0.07,
            rf"$\Delta$AICc = {fit.delta_aicc_exp_minus_power:.1f}",
            transform=ax.transAxes, fontsize=8.5,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=LIGHT_GREY, lw=0.7),
        )
    axes[0].set_ylabel(r"aligned-subspace fraction $A_k$")
    axes[0].set_ylim(0.20, 0.87)
    axes[1].legend(frameon=False, loc="upper right")
    fig.suptitle(r"Persistent low-weight alignment in the half-filled $U(1)$ family", y=1.03)
    fig.tight_layout()
    _save(fig, "fig_u1_alignment_scaling")


def symmetry_breaking() -> None:
    df = pd.read_csv(DATA / "symmetry_breaking_pilot_verified.csv")
    d = df[(df.n == 8) & (df.metric == "A1")].copy()

    fig, ax = plt.subplots(figsize=(4.55, 3.25))
    configs = [
        ("preserve_Z", BLUE, "o", r"symmetry-preserving $R_Z$"),
        ("break_X", ORANGE, "s", r"symmetry-breaking $R_X$"),
    ]
    for kind, color, marker, label in configs:
        g = d[d.kind == kind].sort_values("eps")
        yerr = np.vstack([g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]])
        ax.errorbar(
            g["eps"], g["mean"], yerr=yerr, marker=marker, ms=4.5,
            capsize=2.5, lw=1.5, color=color, label=label,
        )
    baseline = 8 / (2**8 - 1)
    ax.axhline(baseline, color=GREY, ls=":", lw=1.2,
               label=r"full-space rank baseline $8/255$")
    ax.set_xscale("symlog", linthresh=0.01, linscale=0.8)
    ax.set_xticks([0, 0.03, 0.1, 0.3, 1.0])
    ax.set_xticklabels(["0", "0.03", "0.1", "0.3", "1"])
    ax.set_xlabel(r"perturbation strength $\epsilon$")
    ax.set_ylabel(r"one-body alignment $A_1$")
    ax.set_ylim(0.0, 0.60)
    ax.grid(axis="y", alpha=0.18, lw=0.6)
    ax.legend(frameon=False, loc="upper right")
    ax.set_title(r"Symmetry-breaking control at $n=8$")
    fig.tight_layout()
    _save(fig, "fig_symmetry_breaking_control")


def fixed_weight_rank_fraction() -> None:
    n = np.arange(4, 23)
    N = 2**n - 1
    r1 = n
    r2 = n + n * (n - 1) / 2

    fig, ax = plt.subplots(figsize=(4.7, 3.25))
    ax.plot(n, r1 / N, "o-", ms=3.5, lw=1.4, color=BLUE, label=r"weight $\leq1$")
    ax.plot(n, r2 / N, "s-", ms=3.5, lw=1.4, color=ORANGE, label=r"weight $\leq2$")
    ax.set_yscale("log")
    ax.set_xlabel("qubits $n$")
    ax.set_ylabel(r"rank fraction $r_k/(2^n-1)$")
    ax.set_xticks([4, 8, 12, 16, 20, 22])
    ax.grid(which="major", axis="y", alpha=0.18, lw=0.6)
    ax.legend(frameon=False)
    ax.set_title("Rank-only baseline for fixed-weight diagonal readout")
    fig.tight_layout()
    _save(fig, "fig_fixed_weight_rank_fraction")


def operational_bridge() -> None:
    df = pd.read_csv(DATA / "operational_bridge_summary.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.05), sharex=True)
    families = [
        ("SU2-HaarU4-brickwork", BLUE, "o", "Haar-$U(4)$"),
        ("U1-RZ-XY-line", ORANGE, "s", "$U(1)$"),
    ]
    for ax, metric, title in [
        (axes[0], "gradient_signal", r"directional gradient-energy gain"),
        (axes[1], "finite_shot_snr", r"finite-shot SNR gain"),
    ]:
        for family, color, marker, label in families:
            g = df[(df.family == family) & (df.metric == metric)].sort_values("n")
            ax.plot(g.n, g.gain, marker=marker, color=color, lw=1.6, ms=4.5, label=label)
        ax.axhline(1.0, color=GREY, ls=":", lw=1.0)
        ax.set_title(title)
        ax.set_xlabel("qubits $n$")
        ax.set_xticks([8, 10, 12])
        ax.grid(axis="y", alpha=0.18, lw=0.6)
    axes[0].set_ylabel("aligned / physical")
    axes[0].set_yscale("log")
    axes[0].set_yticks([1, 2, 4, 8])
    axes[0].get_yaxis().set_major_formatter(plt.ScalarFormatter())
    axes[1].legend(frameon=False, loc="upper left")
    fig.suptitle("Orientation changes usable signal at fixed rank and shot budget", y=1.03)
    fig.tight_layout()
    _save(fig, "fig_operational_bridge")


def noise_robustness() -> None:
    df = pd.read_csv(DATA / "noise_robustness_summary.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.05), sharex=True)
    for ax, family, color, title in [
        (axes[0], "SU2-HaarU4-brickwork", BLUE, r"Haar-$U(4)$"),
        (axes[1], "U1-RZ-XY-line", ORANGE, r"$U(1)$"),
    ]:
        d = df[df.family == family]
        for n, marker in [(8, "o"), (10, "s"), (12, "^")]:
            g = d[d.n == n].sort_values("bitflip_rate")
            yerr = np.vstack([g.gradient_signal_gain - g.ci_low, g.ci_high - g.gradient_signal_gain])
            ax.errorbar(
                100 * g.bitflip_rate, g.gradient_signal_gain, yerr=yerr,
                marker=marker, ms=4.2, lw=1.4, capsize=2.2, color=color,
                alpha=0.55 + 0.2 * ((n - 8) / 2), label=rf"$n={n}$",
            )
        ax.axhline(1.0, color=GREY, ls=":", lw=1.0)
        ax.set_title(title)
        ax.set_xlabel("bit-flip readout noise (%)")
        ax.set_xticks([0, 1, 3, 5])
        ax.grid(axis="y", alpha=0.18, lw=0.6)
        ax.legend(frameon=False)
    axes[0].set_ylabel("aligned / physical gradient signal")
    axes[0].set_yscale("log")
    axes[0].set_yticks([1, 2, 4, 8])
    axes[0].get_yaxis().set_major_formatter(plt.ScalarFormatter())
    fig.suptitle("Noise-aware orientation advantage", y=1.03)
    fig.tight_layout()
    _save(fig, "fig_noise_robustness")


def main() -> None:
    _style()
    u1_scaling()
    symmetry_breaking()
    fixed_weight_rank_fraction()
    operational_bridge()
    noise_robustness()


if __name__ == "__main__":
    main()
