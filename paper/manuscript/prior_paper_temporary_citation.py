from pathlib import Path

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_rewrite.tex"
KEY = "AitHaddou2026IsotropicRankLaws"

OLD_BIB = r"""

\bibitem{AitHaddou2026IsotropicRankLaws}
M. Ait Haddou,
\textit{Readout-Rank Laws for Isotropic Quantum Tangents},
manuscript submitted to arXiv (2026), arXiv identifier pending.
"""

BIB = r"""

\bibitem{AitHaddou2026IsotropicRankLaws}
M. Ait Haddou,
\textit{Readout-Rank Laws for Isotropic Quantum Tangents},
\href{https://arxiv.org/abs/2608.07628}{arXiv:2608.07628} [quant-ph] (2026).
"""


def add_after(text: str, anchor: str, addition: str) -> str:
    if addition in text:
        return text
    if anchor not in text:
        raise RuntimeError(f"prior-paper citation anchor not found: {anchor[:140]}")
    return text.replace(anchor, anchor + addition, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    intro_anchor = (
        "The random-subspace identity itself is standard Grassmann geometry "
        "\\cite{CollinsMatsumoto2017,Bendokat2024,Fernandez2025}."
    )
    intro_add = (
        " Our earlier manuscript derived the corresponding exact readout-rank law under joint "
        "state--tangent isotropy, including the finite-size Beta distributions for the successive "
        "measurement and readout projections \\cite{" + KEY + "}. The present work starts from "
        "the failure mode identified there and removes isotropy as an assumption."
    )
    text = add_after(text, intro_anchor, intro_add)

    rank_anchor = (
        "The identity is a standard random-subspace result "
        "\\cite{CollinsMatsumoto2017,Bendokat2024,Fernandez2025}."
    )
    rank_add = (
        " In the isotropic setting, the same mean $r/N$ appears as the exact readout-rank law for "
        "a fixed measurement record \\cite{" + KEY + "}; here we reinterpret it as a random-relative-"
        "orientation baseline for an arbitrary trace-one tangent covariance."
    )
    text = add_after(text, rank_anchor, rank_add)

    u1_anchor = (
        "The present result is narrower: in this specific half-filled variational family, the leading "
        "measurement-induced tangent subspace is unusually visible to low-weight diagonal $Z$ readout "
        "under the rank-controlled metric used throughout this paper."
    )
    u1_add = (
        " The same family was already identified in our isotropic-rank analysis as a strong violation "
        "of the support-corrected rank law \\cite{" + KEY + "}; the present analysis resolves that "
        "deviation spectrally in terms of persistent low-weight alignment."
    )
    text = add_after(text, u1_anchor, u1_add)

    # Migrate the temporary pre-arXiv entry if it is already present in a
    # production template. Otherwise insert the final arXiv entry once.
    if OLD_BIB in text:
        text = text.replace(OLD_BIB, BIB, 1)
    elif f"\\bibitem{{{KEY}}}" not in text:
        text = text.replace("\\end{thebibliography}", BIB + "\n\\end{thebibliography}", 1)
    elif "arXiv:2608.07628" not in text:
        raise RuntimeError("prior-paper bibliography entry exists but is neither the temporary nor final arXiv form")

    TARGET.write_text(text, encoding="utf-8")
    print(f"prior-paper arXiv citation applied to {TARGET}")


if __name__ == "__main__":
    main()
