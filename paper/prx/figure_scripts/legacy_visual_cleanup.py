from pathlib import Path
import re

TARGET = Path(__file__).resolve().parents[1] / "make_prx_figures.py"

HELPER = r'''
def legend_below(fig, ncol=4):
    """Place one deduplicated shared legend below the plotted axes.

    The legend stays inside the exported figure canvas so the visual order in
    the manuscript is plot -> legend -> caption.
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
        bbox_to_anchor=(0.5, 0.018),
        ncol=cols,
        frameon=False,
        handlelength=1.8,
        handletextpad=0.45,
        columnspacing=1.05,
        fontsize=7.8,
    )
    fig.subplots_adjust(bottom=0.27)
'''


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = text.replace("'legend.fontsize': 7.5,", "'legend.fontsize': 8.0,")

    # First remove every axes-level legend and any old figure-level legend from
    # the ORIGINAL generator.  This must happen before adding the helper; an
    # earlier version removed the helper's own fig.legend call as well.
    text = re.sub(r"(?m)^\s*ax\.legend\([^\n]*\)\s*\n", "", text)
    text = re.sub(
        r"(?ms)^\s*fig\.legend\(.*?\n\s*\)\s*\n",
        "",
        text,
    )

    # Remove a stale helper definition from a previous ephemeral workflow pass,
    # then insert one known-good helper.
    text = re.sub(
        r"(?ms)^def legend_below\(fig, ncol=4\):.*?(?=^# -------------------- data --------------------)",
        "",
        text,
    )
    anchor = (
        "def panel(ax, label):\n"
        "    ax.text(-0.13, 1.06, label, transform=ax.transAxes, fontsize=10.5,\n"
        "            fontweight='bold', va='top', ha='left')\n"
    )
    if anchor not in text:
        raise RuntimeError("panel helper anchor not found")
    text = text.replace(anchor, anchor + "\n" + HELPER + "\n", 1)

    # Ensure every exported legacy figure calls the shared legend helper once.
    text = text.replace("legend_below(fig)\nfig.savefig(", "fig.savefig(")
    text = text.replace("fig.savefig(", "legend_below(fig)\nfig.savefig(")
    text = text.replace("fig.tight_layout(); legend_below(fig)", "fig.tight_layout()\nlegend_below(fig)")

    # Hard validation: do not silently produce figures with the legend helper
    # stripped out again.
    if "fig.legend(" not in text:
        raise RuntimeError("shared fig.legend call missing after cleanup")
    if "legend_below(fig)\nfig.savefig" not in text:
        raise RuntimeError("legend_below call missing before figure export")

    TARGET.write_text(text, encoding="utf-8")
    print(f"renderable shared legends placed below legacy plots in {TARGET}")


if __name__ == "__main__":
    main()
