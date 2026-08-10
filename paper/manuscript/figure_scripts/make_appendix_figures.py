from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "paper" / "manuscript" / "data"
OUT = ROOT / "paper" / "manuscript" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = "#0072B2"
ORANGE = "#D55E00"
GREEN = "#009E73"
GREY = "#666666"
BLACK = "#222222"


def style():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 9.0,
        "axes.labelsize": 9.5,
        "axes.titlesize": 10.0,
        "legend.fontsize": 8.0,
        "xtick.labelsize": 8.5,
        "ytick.labelsize": 8.5,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def save(fig, name):
    fig.savefig(OUT / f"{name}.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT / f"{name}.png", dpi=320, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def legend_below(fig, handles, labels, ncol):
    fig.legend(
        handles,
        labels,
        frameon=False,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.01),
        ncol=ncol,
        handlelength=2.0,
        columnspacing=1.3,
    )


def operational_gains():
    n = np.array([8, 10, 12])
    haar_grad = np.array([2.963, 4.6385, 9.5843])
    haar_snr = np.array([1.734, 2.125, 3.111])
    u1_grad = np.array([1.148, 1.189, 1.210])
    u1_snr = np.array([1.068, 1.097, 1.112])

    fig, axes = plt.subplots(1, 2, figsize=(7.1, 3.1))
    axes[0].plot(n, haar_grad, "o-", color=BLUE, lw=1.6, ms=4.5, label=r"Haar-$U(4)$")
    axes[0].plot(n, u1_grad, "s-", color=ORANGE, lw=1.6, ms=4.5, label=r"$U(1)$")
    axes[0].axhline(1, color=GREY, lw=1.0, ls=":")
    axes[0].set_xlabel("qubits $n$")
    axes[0].set_ylabel("aligned / physical gain")
    axes[0].set_title("Directional gradient energy")
    axes[0].set_xticks(n)
    axes[0].grid(axis="y", alpha=.18)

    axes[1].plot(n, haar_snr, "o-", color=BLUE, lw=1.6, ms=4.5, label=r"Haar-$U(4)$")
    axes[1].plot(n, u1_snr, "s-", color=ORANGE, lw=1.6, ms=4.5, label=r"$U(1)$")
    axes[1].axhline(1, color=GREY, lw=1.0, ls=":")
    axes[1].set_xlabel("qubits $n$")
    axes[1].set_ylabel("aligned / physical gain")
    axes[1].set_title("Finite-shot SNR")
    axes[1].set_xticks(n)
    axes[1].grid(axis="y", alpha=.18)

    h, l = axes[0].get_legend_handles_labels()
    legend_below(fig, h, l, 2)
    fig.subplots_adjust(left=.10, right=.99, top=.90, bottom=.24, wspace=.28)
    save(fig, "appendix_operational_gains")


def noise_robustness():
    noise = np.array([0.00, 0.01, 0.03, 0.05])
    haar = np.array([9.584, 6.919, 4.491, 3.127])
    haar_lo = np.array([9.360, 6.760, 4.394, 3.059])
    haar_hi = np.array([9.830, 7.102, 4.604, 3.204])
    u1 = np.array([1.210, 1.264, 1.201, 1.150])

    fig, ax = plt.subplots(figsize=(3.6, 2.8))
    ax.errorbar(
        100*noise, haar,
        yerr=np.vstack([haar-haar_lo, haar_hi-haar]),
        marker="o", color=BLUE, lw=1.5, ms=4.2, capsize=2.2,
        label=r"Haar-$U(4)$",
    )
    ax.plot(100*noise, u1, "s-", color=ORANGE, lw=1.5, ms=4.2, label=r"$U(1)$")
    ax.axhline(1, color=GREY, lw=.9, ls=":")
    ax.set_xlabel("bit-flip probability (\%)")
    ax.set_ylabel("gradient-energy gain")
    ax.set_xticks([0,1,3,5])
    ax.set_title("Readout-noise robustness")
    ax.grid(axis="y", alpha=.18)
    h,l=ax.get_legend_handles_labels()
    legend_below(fig,h,l,2)
    fig.subplots_adjust(left=.18,right=.98,top=.88,bottom=.30)
    save(fig, "appendix_noise_robustness")


def u1_fit_diagnostics():
    summary = pd.read_csv(DATA / "u1_alignment_scaling_summary.csv")
    fits = pd.read_csv(DATA / "u1_alignment_scaling_fits.csv")
    d = summary[summary.metric == "cumulative_aligned_subspace_overlap"].copy()

    fig, axes = plt.subplots(1, 3, figsize=(7.15, 3.05))
    legend_handles = None
    legend_labels = None
    bars = []
    barlabels = []

    for ax, order, color, title in [
        (axes[0], 1, BLUE, r"one-body $A_1$"),
        (axes[1], 2, ORANGE, r"cumulative $A_{\leq2}$"),
    ]:
        g = d[d.walsh_order == order].sort_values("n")
        yerr = np.vstack([g["mean"]-g["ci_low"], g["ci_high"]-g["mean"]])
        ax.errorbar(g["n"], g["mean"], yerr=yerr, fmt="o", color=color,
                    ms=4, capsize=2.2, lw=1.2, label="data + 95% CI")
        fit = fits[(fits.walsh_order == order) & (fits.window == "n8_to_n18")].iloc[0]
        x = np.linspace(8,18,250)
        ax.plot(x, fit.power_prefactor*x**(-fit.power_alpha), color=color, lw=1.6, label="power fit")
        ax.plot(x, fit.exp_prefactor*np.exp(-fit.exp_rate_b*x), color=GREY, ls="--", lw=1.3, label="exponential fit")
        ax.set_title(title)
        ax.set_xlabel("qubits $n$")
        ax.set_xticks([8,10,12,14,16,18])
        ax.grid(axis="y", alpha=.18)
        ax.text(.05,.06,rf"$\alpha={fit.power_alpha:.2f}$; $\Delta$AICc={fit.delta_aicc_exp_minus_power:.1f}",transform=ax.transAxes,fontsize=7.6)
        bars.append(fit.delta_aicc_exp_minus_power)
        barlabels.append(r"$A_1$" if order == 1 else r"$A_{\leq2}$")
        if legend_handles is None:
            legend_handles, legend_labels = ax.get_legend_handles_labels()

    axes[0].set_ylabel("aligned-subspace fraction")
    axes[0].set_ylim(.20,.86)
    axes[1].set_ylim(.20,.86)

    axes[2].bar(np.arange(2), bars, color=[BLUE, ORANGE], width=.58)
    axes[2].axhline(0,color=BLACK,lw=.8)
    axes[2].set_xticks(np.arange(2), barlabels)
    axes[2].set_ylabel(r"$\Delta$AICc (exp $-$ power)")
    axes[2].set_title("Finite-size model preference")
    axes[2].grid(axis="y", alpha=.18)

    legend_below(fig, legend_handles, legend_labels, 3)
    fig.subplots_adjust(left=.08,right=.995,top=.88,bottom=.25,wspace=.30)
    save(fig, "appendix_u1_fit_diagnostics")


def main():
    style()
    operational_gains()
    noise_robustness()
    u1_fit_diagnostics()


if __name__ == "__main__":
    main()
