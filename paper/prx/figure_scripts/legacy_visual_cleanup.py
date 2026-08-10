from pathlib import Path

TARGET = Path(__file__).resolve().parents[1] / "make_prx_figures.py"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = text.replace("'legend.fontsize': 7.5,", "'legend.fontsize': 8.0,")
    TARGET.write_text(text, encoding="utf-8")
    print(f"applied base visual cleanup to {TARGET}")


if __name__ == "__main__":
    main()
