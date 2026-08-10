from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "make_prx_figures.py"


def replace(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"visual-cleanup anchor not found: {old[:120]}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # Slightly larger legend type at journal column width.
    text = replace(text, "'legend.fontsize': 7.5,", "'legend.fontsize': 8.2,")

    # Fig. 2: move dense legends above the data rather than covering the lower band.
    text = replace(
        text,
        "ax.legend(frameon=False,loc='lower left',handlelength=1.6)",
        "ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.01),ncol=1,handlelength=1.6,borderaxespad=0.0)",
    )
    text = replace(
        text,
        "ax.legend(frameon=False,loc='lower left',handlelength=1.5)",
        "ax.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.01),ncol=1,handlelength=1.5,borderaxespad=0.0)",
    )

    # Fig. 3: keep legends away from the steep U(1) curves.
    text = replace(
        text,
        "ax.legend(frameon=False,loc='upper left')\nclean(ax)\n\nax=fig.add_subplot(gs[0,1]); panel(ax,'b')",
        "ax.legend(frameon=False,loc='lower right')\nclean(ax)\n\nax=fig.add_subplot(gs[0,1]); panel(ax,'b')",
    )
    text = replace(
        text,
        "ax.legend(frameon=False,loc='lower left')\nclean(ax)\n\nax=fig.add_subplot(gs[0,2]); panel(ax,'c')",
        "ax.legend(frameon=False,loc='upper right')\nclean(ax)\n\nax=fig.add_subplot(gs[0,2]); panel(ax,'c')",
    )

    # Fig. 4: enlarge the equal-rank key and leave a clear gutter before the caption.
    text = replace(
        text,
        "ax.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.28),handletextpad=.35,columnspacing=.8)",
        "ax.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.31),handletextpad=.45,columnspacing=1.0,fontsize=8.0)",
    )

    # Fig. 5: use one shared legend for all three panels so panels b/c are self-decodable.
    text = replace(text, "ax.legend(frameon=False,loc='lower right')\nclean(ax)", "clean(ax)")
    text = replace(
        text,
        "clean(ax)\nfig.savefig(OUT/'fig5_full_record_vs_accessible.pdf',bbox_inches='tight')",
        "clean(ax)\nhandles = [\n    plt.Line2D([0],[0],color=BLUE,marker='o',lw=1.4,ms=4,label='generic / Haar-$U(4)^*$'),\n    plt.Line2D([0],[0],color=ORANGE,marker='s',lw=1.4,ms=4,label='$U(1)$'),\n]\nfig.legend(handles=handles,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.04),ncol=2,columnspacing=1.6)\nfig.subplots_adjust(top=.82)\nfig.savefig(OUT/'fig5_full_record_vs_accessible.pdf',bbox_inches='tight')",
    )

    TARGET.write_text(text, encoding="utf-8")
    print(f"applied legacy visual cleanup to {TARGET}")


if __name__ == "__main__":
    main()
