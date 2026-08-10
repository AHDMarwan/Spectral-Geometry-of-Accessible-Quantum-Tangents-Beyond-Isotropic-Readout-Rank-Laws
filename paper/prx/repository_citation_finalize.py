from pathlib import Path

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_prx_rewrite.tex"
KEY = "AitHaddou2026MeasurementAccessible"
REPO_URL = "https://github.com/AHDMarwan/Spectral-Geometry-of-Accessible-Quantum-Tangents-Beyond-Isotropic-Readout-Rank-Laws"
DOI = "10.5281/zenodo.21877379"
DOI_URL = f"https://doi.org/{DOI}"

BIB = rf"""

\bibitem{{{KEY}}}
M. Ait Haddou,
Spectral Geometry of Accessible Quantum Tangents: Reproducibility Suite,
Zenodo (2026),
\href{{{DOI_URL}}}{{doi:{DOI}}}.
ORCID: 0009-0008-1734-1721.
"""


def add_cite(text: str, sentence: str) -> str:
    cited = sentence[:-1] + f" \\cite{{{KEY}}}." if sentence.endswith(".") else sentence + f" \\cite{{{KEY}}}"
    if cited in text:
        return text
    if sentence in text:
        return text.replace(sentence, cited, 1)
    return text


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
        "reproducibility release \\cite{" + KEY + "}."
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

    result_sentences = [
        "The $n=18$ point is a single-architecture stress test rather than the family-balanced estimator used through $n=16$.",
        "Thus the physical low-weight readout can remain close to the rank reference while the covariance becomes highly concentrated spectrally.",
        "We do not assign a microscopic gate-level cause in the present work.",
        "The physical readout therefore misses tangent mass that is available at exactly the same rank. This is the central distinction between rank and orientation.",
        "The physical readout is not optimal, but it is already much closer to the leading tangent subspace than the generic Haar-$U(4)$ readout.",
        "A random rank-matched subspace remains close to the physical generic baseline, as expected from the rank-only null model.",
        "The contrast between the two families is itself informative: equal rank leaves substantial room for readout design in generic circuits, while the structured $U(1)$ readout already captures much of the accessible leading tangent structure.",
        "At $n=18$, for example, the one-body $U(1)$ retention is approximately $0.215$, compared with the Haar-$U(4)$ value $6.38\\times10^{-5}$; the two-body values are approximately $0.401$ and $6.25\\times10^{-4}$, respectively.",
        "Each size uses 20 independent circuit instances.",
        "These are finite-size model-discrimination results only; they are not asymptotic lower bounds and are not identified with a hydrodynamic exponent.",
        "The physical one-body retention simultaneously falls from $0.430$ to $0.0325$ in the breaking control.",
        "Across the generic data, $F_{\\rm full}/F_Q$ is approximately $0.49$, while the $U(1)$ values remain near $0.47$--$0.48$.",
    ]
    for sentence in result_sentences:
        text = add_cite(text, sentence)

    old = (
        "The frozen protocols, source code, aggregate tables, shard-level outputs, and analysis "
        "scripts are available in the public project repository. The manuscript rewrite is developed "
        "on a dedicated branch so that the frozen numerical record remains separate from editorial changes."
    )
    new = (
        "The frozen protocols, source code, aggregate tables, shard-level outputs, analysis scripts, "
        "and the numerical results reported in this manuscript are available in the public project "
        "repository and archived reproducibility release \\cite{" + KEY + "}. The repository records "
        "the frozen numerical provenance separately from editorial manuscript changes."
    )
    if new not in text and old in text:
        text = text.replace(old, new, 1)

    old_bib = rf"""\bibitem{{{KEY}}}
M. Ait Haddou,
Measurement-Accessible Quantum Tangent Geometry: Rank Typicality Without Isotropy,
Manuscript and reproducibility repository (2026),
\url{{{REPO_URL}}}.
ORCID: 0009-0008-1734-1721."""
    new_bib = BIB.strip()
    if old_bib in text:
        text = text.replace(old_bib, new_bib, 1)
    elif f"\\bibitem{{{KEY}}}" not in text:
        text = text.replace("\\end{thebibliography}", BIB + "\n\\end{thebibliography}", 1)

    TARGET.write_text(text, encoding="utf-8")
    print(f"repository citation applied to {TARGET}")


if __name__ == "__main__":
    main()
