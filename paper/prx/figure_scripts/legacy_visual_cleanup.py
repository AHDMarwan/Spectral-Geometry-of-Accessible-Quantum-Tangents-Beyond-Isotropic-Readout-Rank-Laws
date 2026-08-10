from pathlib import Path
import re

TARGET = Path(__file__).resolve().parents[1] / "make_prx_figures.py"

HELPER = r'''
def legend_below(fig, ncol=4):
    """Place one deduplicated shared legend below the plotted axes.

    The legend is kept inside the exported figure canvas so that, when LaTeX
    places the caption, the visual order is: plot -> legend -> caption.
    """
    handles = []
    labels = []
    seen = set()
    for axis in fig.axes:
        hs, ls = axis.get_legend_handles_labels()
        for h, lab in zip(hs, ls):
            if not lab or lab.startswith('_') or lab in seen:
                continue
            seen.add(lab)
            handles.append(h)
            labels.append(lab)
    if not handles:
        return
    cols = min(ncol, len(handles))
    fig.legend(
        handles,
        labels,
        loc='lower center',
        bbox_to_anchor=(0.5, 0.015),
        ncol=cols,
        frameon=False,
        handlelength=1.8,
        handletextpad=0.45,
        columnspacing=1.05,
        fontsize=7.8,
    )
    fig.subplots_adjust(bottom=0.24)
'''


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = text.replace("'legend.fontsize': 7.5,", "'legend.fontsize': 8.0,")

    # Add the shared-legend helper once, immediately after the panel helper.
    if "def legend_below(fig, ncol=4):" not in text:
        anchor = "def panel(ax, label):\n    ax.text(-0.13, 1.06, label, transform=ax.transAxes, fontsize=10.5,\n            fontweight='bold', va='top', ha='left')\n"
        if anchor not in text:
            raise RuntimeError("panel helper anchor not found")
        text = text.replace(anchor, anchor + "\n" + HELPER + "\n", 1)

    # Remove every axes-level legend from the generator.  These were the
    # source of the duplicated keys visible in the proof.
    text = re.sub(r"(?m)^\s*ax\.legend\([^\n]*\)\s*\n", "", text)

    # Remove any prior figure-level legend blocks if a previous production
    # pass inserted one.  The helper above will create exactly one legend.
    text = re.sub(
        r"(?ms)^\s*fig\.legend\(.*?\n\s*\)\s*\n",
        "",
        text,
    )

    # Insert exactly one shared legend immediately before every exported
    # figure.  Figures with no labelled artists simply get no key.
    if "legend_below(fig)\nfig.savefig" not in text:
        text = text.replace("fig.savefig(", "legend_below(fig)\nfig.savefig(")
        text = text.replace("fig.tight_layout(); legend_below(fig)", "fig.tight_layout()\nlegend_below(fig)")

    TARGET.write_text(text, encoding="utf-8")
    print(f"moved all legacy figure legends below the plots in {TARGET}")


if __name__ == "__main__":
    main()
