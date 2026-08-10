from __future__ import annotations

"""Generate publication-grade figures used by the production rewrite.

The script intentionally reads small, paper-facing CSV tables committed under
``paper/prx/data`` so that figure generation is deterministic and does not
require rerunning the quantum simulations.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "paper" / "prx" / "data"
OUT = ROOT / "paper" / "prx" / "figures" / "production"
OUT.mkdir(parents=True, exist_ok=True)

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
            "font.size": 10.0,
            "axes.labelsize": 10.5,
            "axes.titlesize": 11.0,
            "legend.fontsize": 9.0,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
            "axes.linewidth": 0.85,
            "xtick.major.width": 0.85,
            "ytick.major.width": 0.85,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def _save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT / f"{name}.png", dpi=360, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def u1_scaling() -> None:
    summary = pd.read_csv(DATA / "u1_alignment_scaling_summary.csv")
    fits = pd.read_csv(DATA / "u1_alignment_scaling_fits.csv")
    d = summary[summary.metric == "cumulative_aligned_subspace_overlap"].copy()

    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.45), sharey=True)
    legend_handles = None
    legend_labels = None

    for ax, order, color, title in [
        (axes[0], 1, BLUE, r"one-body span, $k=1$"),
        (axes[1], 2, ORANGE, r"cumulative span, $k\leq2$"),
    ]:
        g = d[d.walsh_order == order].sort_values("n")
        yerr = np.vstack([g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]])
        ax.errorbar(
            g["n"],
            g["mean"],
            yerr=yerr,
            fmt="o",
            ms=4.7,
            capsize=2.6,
            lw=1.25,
            color=color,
            label="data + 95% CI",
        )
        fit = fits[(fits.walsh_order == order) & (fits.window == "n8_to_n18")].iloc[0]
        x = np.linspace(8, 18, 300)
        power = fit.power_prefactor * x ** (-fit.power_alpha)
        expo = fit.exp_prefactor * np.exp(-fit.exp_rate_b * x)
        ax.plot(x, power, color=color, lw=1.8, label="power fit")
        ax.plot(x, expo, color=GREY, lw=1.4, ls="--", label="exponential fit")
        ax.set_title(title)
        ax.set_xlabel("qubits $n$")
        ax.set_xticks([8, 10, 12, 14, 16, 18])
        ax.set_xlim(7.5, 18.5)
        ax.grid(axis="y", alpha=0.18, lw=0.6)
        ax.text(
            0.04,
            0.07,
            rf"$\alpha={fit.power_alpha:.2f}$\n$\Delta$AICc={fit.delta_aicc_exp_minus_power:.1f}",
            transform=ax.transAxes,
            fontsize=8.6,
            linespacing=1.15,
        )
        if legend_handles is None:
            legend_handles, legend_labels = ax.get_legend_handles_labels()

    axes[0].set_ylabel(r"aligned-subspace fraction $A_k$")
    axes[0].set_ylim(0.20, 0.87)
    fig.legend(
        legend_handles,
        legend_labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.035),
        ncol=2,
        frameon=False,
        handlelength=2.2,
        columnspacing=1.4,
    )
    fig.suptitle(r"Persistent low-weight alignment in the half-filled $U(1)$ family", y=1.005)
    fig.subplots_adjust(left=0.10, right=0.995, top=0.82, bottom=0.30, wspace=0.12)
    _save(fig, "fig_u1_alignment_scaling")


def symmetry_breaking() -> None:
    df = pd.read_csv(DATA / "symmetry_breaking_pilot_verified.csv")
    d = df[(df.n == 8) & (df.metric == "A1")].copy()

    fig, ax = plt.subplots(figsize=(4.7, 3.75))
    configs = [
        ("preserve_Z", BLUE, "o", r"preserve $U(1)$: $R_Z$"),
        ("break_X", ORANGE, "s", r"break $U(1)$: $R_X$"),
    ]
    for kind, color, marker, label in configs:
        g = d[d.kind == kind].sort_values("eps")
        yerr = np.vstack([g["mean"] - g["ci_low"], g["ci_high"] - g["mean"]])
        ax.errorbar(
            g["eps"],
            g["mean"],
            yerr=yerr,
            marker=marker,
            ms=4.7,
            capsize=2.6,
            lw=1.6,
            color=color,
            label=label,
        )

    baseline = 8 / (2**8 - 1)
    ax.axhline(baseline, color=GREY, ls=":", lw=1.3, label="rank reference")
    ax.set_xscale("symlog", linthresh=0.01, linscale=0.8)
    ax.set_xticks([0, 0.03, 0.1, 0.3, 1.0])
    ax.set_xticklabels(["0", "0.03", "0.1", "0.3", "1"])
    ax.set_xlabel(r"perturbation strength $\epsilon$")
    ax.set_ylabel(r"one-body alignment $A_1$")
    ax.set_ylim(0.0, 0.60)
    ax.grid(axis="y", alpha=0.18, lw=0.6)

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.01),
        ncol=3,
        handlelength=1.8,
        columnspacing=1.0,
        fontsize=8.4,
    )
    fig.subplots_adjust(left=0.17, right=0.98, bottom=0.30, top=0.96)
    _save(fig, "fig_symmetry_breaking_control")


def fixed_weight_rank_fraction() -> None:
    n = np.arange(4, 23)
    N = 2**n - 1
    r1 = n
    r2 = n + n * (n - 1) / 2

    fig, ax = plt.subplots(figsize=(4.7, 3.45))
    y1 = r1 / N
    y2 = r2 / N
    ax.plot(n, y1, "o-", ms=3.7, lw=1.5, color=BLUE)
    ax.plot(n, y2, "s-", ms=3.7, lw=1.5, color=ORANGE)
    ax.set_yscale("log")
    ax.set_xlabel("qubits $n$")
    ax.set_ylabel(r"rank fraction $r_k/(2^n-1)$")
    ax.set_xticks([4, 8, 12, 16, 20, 22])
    ax.grid(which="major", axis="y", alpha=0.18, lw=0.6)
    ax.set_title("Rank-only baseline for fixed-weight diagonal readout", pad=8)

    ax.annotate(
        r"weight $\leq2$",
        xy=(19, y2[n.tolist().index(19)]),
        xytext=(-4, 10),
        textcoords="offset points",
        ha="right",
        va="bottom",
        color=ORANGE,
        fontsize=9.0,
    )
    ax.annotate(
        r"weight $\leq1$",
        xy=(19, y1[n.tolist().index(19)]),
        xytext=(-4, -12),
        textcoords="offset points",
        ha="right",
        va="top",
        color=BLUE,
        fontsize=9.0,
    )
    fig.subplots_adjust(left=0.18, right=0.98, bottom=0.16, top=0.88)
    _save(fig, "fig_fixed_weight_rank_fraction")


def main() -> None:
    _style()
    u1_scaling()
    symmetry_breaking()
    fixed_weight_rank_fraction()


if __name__ == "__main__":
    main()
