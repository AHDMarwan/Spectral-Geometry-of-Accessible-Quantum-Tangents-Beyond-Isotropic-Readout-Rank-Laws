from pathlib import Path
import re

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_prx_rewrite.tex"

BENNAI_ORCID = "0000-0002-7364-5171"
PRIOR_KEY = "AitHaddou2026IsotropicRankLaws"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # Never box prose in the manuscript. Normalize the central message to a
    # plain centered emphasized sentence, with no equation number or frame.
    boxed_patterns = [
        r"\\begin\{equation\}\s*\\boxed\{\\text\{rank fixes a baseline; spectral orientation controls actual retained tangent information\.\}\}\s*\\label\{eq:message\}\s*\\end\{equation\}",
        r"\\begin\{equation\}\s*\\boxed\{\\text\{rank fixes a baseline; spectral orientation controls actual retained tangent information\}\}\s*\\label\{eq:message\}\s*\\end\{equation\}",
    ]
    replacement = (
        "\\begin{center}\n"
        "\\emph{Rank fixes a baseline; spectral orientation controls actual retained tangent information.}\n"
        "\\end{center}"
    )
    for pat in boxed_patterns:
        # Use a callable replacement so Python's regex engine does not parse
        # LaTeX backslashes (e.g. \emph) as replacement escapes.
        text = re.sub(pat, lambda _m: replacement, text, flags=re.S)

    # Remove a stale equation label if a previous build left it behind.
    text = text.replace("\\label{eq:message}\n", "")

    # Mohamed Bennai: show only the clickable ORCID icon, never the numeric
    # identifier as visible prose.
    variants = [
        f"Mohamed Bennai (\\href{{https://orcid.org/{BENNAI_ORCID}}}{{ORCID: {BENNAI_ORCID}}})",
        f"Mohamed Bennai (ORCID: {BENNAI_ORCID})",
        f"Mohamed Bennai, ORCID: {BENNAI_ORCID}",
        f"Mohamed Bennai ({BENNAI_ORCID})",
    ]
    for old in variants:
        text = text.replace(old, f"Mohamed Bennai\\,\\orcidlink{{{BENNAI_ORCID}}}")

    linked_numeric = re.compile(
        rf"Mohamed Bennai\s*\(\\href\{{https://orcid\.org/{re.escape(BENNAI_ORCID)}\}}\{{[^}}]*\}}\)"
    )
    text = linked_numeric.sub(
        lambda _m: f"Mohamed Bennai\\,\\orcidlink{{{BENNAI_ORCID}}}", text
    )

    if f"\\cite{{{PRIOR_KEY}}}" not in text:
        raise RuntimeError("temporary citation to the submitted isotropic rank-law manuscript is missing")
    if f"\\bibitem{{{PRIOR_KEY}}}" not in text:
        raise RuntimeError("temporary bibliography entry for the submitted isotropic rank-law manuscript is missing")

    TARGET.write_text(text, encoding="utf-8")
    print(f"enforced final manuscript visual policy in {TARGET}")


if __name__ == "__main__":
    main()
