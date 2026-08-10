from pathlib import Path

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_prx_rewrite.tex"
URL = "https://github.com/AHDMarwan/Spectral-Geometry-of-Accessible-Quantum-Tangents-Beyond-Isotropic-Readout-Rank-Laws"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    old = rf"""\bibitem{{AitHaddou2026MeasurementAccessible}}
M. Ait Haddou,
Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy,
Manuscript and reproducibility repository (2026),
\url{{{URL}}}.
ORCID: 0009-0008-1734-1721.
"""
    new = rf"""\bibitem{{AitHaddou2026MeasurementAccessible}}
M. Ait Haddou,
Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy,
Manuscript and reproducibility repository (2026),
\href{{{URL}}}{{GitHub reproducibility repository}}.
"""

    if old in text:
        text = text.replace(old, new, 1)
    else:
        # Rerun-safe cleanup for already compact entries or partially transformed text.
        text = text.replace(
            rf"\url{{{URL}}}",
            rf"\href{{{URL}}}{{GitHub reproducibility repository}}",
        )
        text = text.replace("ORCID: 0009-0008-1734-1721.\n", "")

    TARGET.write_text(text, encoding="utf-8")
    print("applied compact clickable repository bibliography entry")


if __name__ == "__main__":
    main()
