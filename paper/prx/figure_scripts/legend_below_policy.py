from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "make_prx_figures.py"


def rep(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"legend-policy anchor not found: {old[:140]}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # Fig. 1: one shared legend below the full figure.
    text = rep(
        text,
        "ax.legend(frameon=False,loc='lower left')\nclean(ax)\nfig.savefig(OUT/'fig1_framework_theory.pdf',bbox_inches='tight')",
        "h,l=ax.get_legend_handles_labels()\nclean(ax)\nfig.legend(h,l,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.03),ncol=2,handlelength=2.0,columnspacing=1.5)\nfig.subplots_adjust(bottom=.24)\nfig.savefig(OUT/'fig1_framework_theory.pdf',bbox_inches='tight')",
    )

    # Fig. 2: collect the two panel keys and put a single two-row legend below.
    text = rep(text, "ax.legend(frameon=False,loc='lower left',handlelength=1.6)\nclean(ax)", "clean(ax)")
    text = rep(text, "ax.legend(frameon=False,loc='lower left',handlelength=1.5)\nclean(ax)", "clean(ax)")
    text = rep(
        text,
        "clean(ax)\nfig.savefig(OUT/'fig2_rank_architecture_anisotropy.pdf',bbox_inches='tight')",
        "clean(ax)\nh1,l1=fig.axes[0].get_legend_handles_labels()\nh2,l2=fig.axes[1].get_legend_handles_labels()\nfig.legend(h1+h2,l1+l2,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.07),ncol=3,handlelength=1.8,columnspacing=1.2)\nfig.subplots_adjust(bottom=.27)\nfig.savefig(OUT/'fig2_rank_architecture_anisotropy.pdf',bbox_inches='tight')",
    )

    # Fig. 3: no in-panel legends; one shared key below the panels.
    text = rep(text, "ax.legend(frameon=False,loc='upper left')\nclean(ax)", "clean(ax)")
    text = rep(text, "ax.legend(frameon=False,loc='lower left')\nclean(ax)", "clean(ax)")
    text = rep(text, "ax.legend(frameon=False,loc='upper left')\nclean(ax)\nfig.savefig(OUT/'fig3_symmetry_accessibility.pdf',bbox_inches='tight')", "clean(ax)\nh0,l0=fig.axes[0].get_legend_handles_labels()\nh1,l1=fig.axes[1].get_legend_handles_labels()\nfig.legend(h0+h1,l0+l1,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.06),ncol=4,handlelength=1.8,columnspacing=1.2)\nfig.subplots_adjust(bottom=.26)\nfig.savefig(OUT/'fig3_symmetry_accessibility.pdf',bbox_inches='tight')")

    # Fig. 4: combine spectral-comparison and depth keys below the full figure.
    text = rep(text, "ax.legend(frameon=False,ncol=3,loc='lower center',bbox_to_anchor=(.5,-.28),handletextpad=.35,columnspacing=.8)\nclean(ax)", "clean(ax)")
    text = rep(text, "ax.legend(frameon=False)\nclean(ax)\nfig.savefig(OUT/'fig4_spectral_mechanism_depth.pdf',bbox_inches='tight')", "clean(ax)\nh0,l0=fig.axes[0].get_legend_handles_labels()\nh1,l1=fig.axes[1].get_legend_handles_labels()\nfig.legend(h0+h1,l0+l1,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.04),ncol=5,handlelength=1.7,columnspacing=1.0,fontsize=7.7)\nfig.subplots_adjust(bottom=.23)\nfig.savefig(OUT/'fig4_spectral_mechanism_depth.pdf',bbox_inches='tight')")

    # Fig. 5: shared generic/U(1) key below all panels.
    text = rep(text, "ax.legend(frameon=False,loc='lower right')\nclean(ax)", "clean(ax)")
    text = rep(text, "clean(ax)\nfig.savefig(OUT/'fig5_full_record_vs_accessible.pdf',bbox_inches='tight')", "clean(ax)\nh,l=fig.axes[0].get_legend_handles_labels()\nfig.legend(h,l,frameon=False,loc='lower center',bbox_to_anchor=(.5,-.04),ncol=2,handlelength=1.9,columnspacing=1.5)\nfig.subplots_adjust(bottom=.23)\nfig.savefig(OUT/'fig5_full_record_vs_accessible.pdf',bbox_inches='tight')")

    # Supplementary single-panel figures: legends below axes, never over data.
    text = rep(text, "ax.legend(frameon=False); clean(ax)\nfig.tight_layout(); fig.savefig(OUT/'figS1_deff_fraction.pdf',bbox_inches='tight')", "ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.20),ncol=2); clean(ax)\nfig.tight_layout(rect=(0,.12,1,1)); fig.savefig(OUT/'figS1_deff_fraction.pdf',bbox_inches='tight')")
    text = rep(text, "ax.legend(frameon=False,ncol=2,fontsize=6.7); clean(ax)\nfig.tight_layout(); fig.savefig(OUT/'figS2_exact_null_width.pdf',bbox_inches='tight')", "ax.legend(frameon=False,ncol=2,fontsize=6.7,loc='upper center',bbox_to_anchor=(.5,-.20)); clean(ax)\nfig.tight_layout(rect=(0,.16,1,1)); fig.savefig(OUT/'figS2_exact_null_width.pdf',bbox_inches='tight')")
    text = rep(text, "ax.legend(frameon=False,fontsize=6.8); clean(ax)\nfig.tight_layout(); fig.savefig(OUT/'figS3_orientation_z.pdf',bbox_inches='tight')", "ax.legend(frameon=False,fontsize=6.8,loc='upper center',bbox_to_anchor=(.5,-.26),ncol=2); clean(ax)\nfig.tight_layout(rect=(0,.18,1,1)); fig.savefig(OUT/'figS3_orientation_z.pdf',bbox_inches='tight')")
    text = rep(text, "ax.legend(frameon=False); clean(ax)\nfig.tight_layout(); fig.savefig(OUT/'figS4_rank_fraction.pdf',bbox_inches='tight')", "ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.20),ncol=2); clean(ax)\nfig.tight_layout(rect=(0,.12,1,1)); fig.savefig(OUT/'figS4_rank_fraction.pdf',bbox_inches='tight')")

    TARGET.write_text(text, encoding="utf-8")
    print(f"applied below-figure legend policy to {TARGET}")


if __name__ == "__main__":
    main()
