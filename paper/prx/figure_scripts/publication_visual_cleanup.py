from pathlib import Path

TARGET = Path(__file__).resolve().parent / "make_publication_figures.py"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # U(1) scaling: keep the shared key below the panels, inside the exported
    # canvas so LaTeX renders plot -> legend -> caption.
    text = text.replace(
        'bbox_to_anchor=(0.5, -0.035),',
        'bbox_to_anchor=(0.5, 0.015),',
    )
    text = text.replace(
        'fig.subplots_adjust(left=0.10, right=0.995, top=0.82, bottom=0.30, wspace=0.12)',
        'fig.subplots_adjust(left=0.10, right=0.995, top=0.82, bottom=0.32, wspace=0.12)',
    )

    # Symmetry-breaking control: move the figure-level key from the top to the
    # bottom, below the axes and above the LaTeX caption.
    text = text.replace('loc="upper center",', 'loc="lower center",', 1)
    text = text.replace('bbox_to_anchor=(0.5, 0.995),', 'bbox_to_anchor=(0.5, 0.015),', 1)
    text = text.replace(
        'fig.subplots_adjust(left=0.17, right=0.98, bottom=0.17, top=0.82)',
        'fig.subplots_adjust(left=0.17, right=0.98, bottom=0.30, top=0.96)',
    )

    TARGET.write_text(text, encoding="utf-8")
    print(f"moved publication figure legends below plots in {TARGET}")


if __name__ == "__main__":
    main()
