from __future__ import annotations

"""Generate the additional PRA-v2 referee-facing control figure."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "paper" / "manuscript" / "data"
OUT = ROOT / "paper" / "manuscript" / "figures" / "production"
OUT.mkdir(parents=True, exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA / "pra_v2_u1_sector_null.csv")
    fig, axes = plt.subplots(1, 2, figsize=(7.15, 3.35), sharey=True)

    for ax, k, title in [
        (axes[0], 1, r"one-body span, $k=1$"),
        (axes[1], 2, r"cumulative span, $k\leq2$"),
    ]:
        g = df[df["walsh_order"] == k].sort_values("n")
        yerr = np.vstack(
            [
                g["observed_mean"] - g["observed_ci_low"],
                g["observed_ci_high"] - g["observed_mean"],
            ]
        )
        ax.errorbar(
            g["n"],
            g["observed_mean"],
            yerr=yerr,
            fmt="o-",
            capsize=2.4,
            lw=1.5,
            ms=4.5,
            label="physical U(1) alignment",
        )
        ax.plot(
            g["n"],
            g["sector_null_mean"],
            "s--",
            lw=1.35,
            ms=4.0,
            label="sector random-orientation mean",
        )
        lower = np.maximum(g["sector_null_mean"] - 2.0 * g["sector_null_sd"], 1e-12)
        upper = g["sector_null_mean"] + 2.0 * g["sector_null_sd"]
        ax.fill_between(g["n"], lower, upper, alpha=0.16, label=r"null mean $\pm2$ SD")
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_xlabel("qubits $n$")
        ax.set_xticks([8, 10, 12, 14, 16, 18])
        ax.grid(axis="y", which="major", alpha=0.20, lw=0.6)

        last = g[g["n"] == 18].iloc[0]
        ax.text(
            0.05,
            0.07,
            f"n=18: {last.observed_over_null:.0f}x null",
            transform=ax.transAxes,
            fontsize=8.6,
        )

    axes[0].set_ylabel(r"aligned-subspace fraction $A_k$")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.035),
        ncol=3,
        frameon=False,
        fontsize=8.3,
    )
    fig.suptitle(r"Fixed-charge sector null for low-weight alignment", y=1.01)
    fig.subplots_adjust(left=0.11, right=0.995, top=0.82, bottom=0.28, wspace=0.10)
    fig.savefig(OUT / "fig_u1_sector_null.pdf", bbox_inches="tight", pad_inches=0.04)
    fig.savefig(OUT / "fig_u1_sector_null.png", dpi=360, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


if __name__ == "__main__":
    main()
