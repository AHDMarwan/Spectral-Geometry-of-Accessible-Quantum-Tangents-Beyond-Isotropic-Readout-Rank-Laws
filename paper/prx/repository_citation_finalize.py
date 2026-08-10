from pathlib import Path

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_prx_rewrite.tex"
KEY = "AitHaddou2026MeasurementAccessible"

BIB = r"""

\bibitem{AitHaddou2026MeasurementAccessible}
M. Ait Haddou,
Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy,
Manuscript and reproducibility repository (2026),
\url{https://github.com/AHDMarwan/Spectral-Geometry-of-Accessible-Quantum-Tangents-Beyond-Isotropic-Readout-Rank-Laws}.
ORCID: 0009-0008-1734-1721.
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    old = (
        "The numerical campaign treats a circuit instance, not an individual tangent direction, "
        "as the independent statistical unit. Within each circuit, tangent directions estimate "
        "the score covariance and readout statistics. Confidence intervals are obtained by "
        "nonparametric bootstrap over independent circuit instances \\cite{Efron1979}. The generic "
        "aggregate is family-balanced so that no ansatz family dominates by sample count."
    )
    new = old + (
        " The source code, frozen experiment profiles, aggregate tables, shard-level outputs, and "
        "paper-facing result summaries used for the numerical claims are archived in the public "
        "reproducibility repository \\cite{" + KEY + "}."
    )
    if new not in text and old in text:
        text = text.replace(old, new, 1)

    old = (
        "The baseline campaign uses computational-basis measurement, depth proportional to system "
        "size, and diagonal $Z$ readouts through weight one and two. The nonconserving ensemble "
        "includes RY--RZ--CZ, SU2--CNOT, SU2--CZ, random-matching SU2--CZ, and Haar-$U(4)$ brickwork "
        "families. A half-filled number-conserving RZ--XY family supplies the structured $U(1)$ case "
        "study. Larger-size extensions and dedicated cross-fit experiments use frozen profiles "
        "documented in the repository."
    )
    new = old[:-1] + " \\cite{" + KEY + "}."
    if new not in text and old in text:
        text = text.replace(old, new, 1)

    old = (
        "The frozen protocols, source code, aggregate tables, shard-level outputs, and analysis "
        "scripts are available in the public project repository. The manuscript rewrite is developed "
        "on a dedicated branch so that the frozen numerical record remains separate from editorial changes."
    )
    new = (
        "The frozen protocols, source code, aggregate tables, shard-level outputs, analysis scripts, "
        "and the numerical results reported in this manuscript are available in the public project "
        "repository \\cite{" + KEY + "}. The repository records the frozen numerical provenance "
        "separately from editorial manuscript changes."
    )
    if new not in text and old in text:
        text = text.replace(old, new, 1)

    if f"\\bibitem{{{KEY}}}" not in text:
        text = text.replace("\\end{thebibliography}", BIB + "\n\\end{thebibliography}", 1)

    TARGET.write_text(text, encoding="utf-8")
    print(f"repository citation applied to {TARGET}")


if __name__ == "__main__":
    main()
