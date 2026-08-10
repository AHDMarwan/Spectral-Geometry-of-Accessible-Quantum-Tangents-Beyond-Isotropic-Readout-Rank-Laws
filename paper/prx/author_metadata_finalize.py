from pathlib import Path

PAPER = Path(__file__).resolve().parent
CANONICAL = PAPER / "spectral_geometry_prx.tex"
TARGET = PAPER / "spectral_geometry_prx_rewrite.tex"

ORCID = "0009-0008-1734-1721"
EMAIL = "aithaddou.marwan@outlook.com"


def main() -> None:
    # The canonical manuscript is the last complete promoted build.  Start from
    # it so the production rewrite cannot remain accidentally truncated between
    # workflow runs.
    text = CANONICAL.read_text(encoding="utf-8")

    if "\\usepackage{orcidlink}" not in text:
        text = text.replace("\\usepackage{amsthm}\n", "\\usepackage{amsthm}\n\\usepackage{orcidlink}\n", 1)

    old_author = (
        "\\author{Marwan Ait Haddou}\n"
        "\\thanks{ORCID: \\href{https://orcid.org/0009-0008-1734-1721}{0009-0008-1734-1721}}\n"
        "\\affiliation{Independent Researcher}"
    )
    new_author = (
        f"\\author{{Marwan Ait Haddou\\,\\orcidlink{{{ORCID}}}}}\n"
        f"\\email{{{EMAIL}}}\n"
        "\\affiliation{Independent Researcher}"
    )
    if old_author in text:
        text = text.replace(old_author, new_author, 1)
    else:
        # Rerun-safe normalization if metadata was already partially updated.
        text = text.replace(
            "\\author{Marwan Ait Haddou}\n\\affiliation{Independent Researcher}",
            new_author,
            1,
        )
        text = text.replace(
            f"\\author{{Marwan Ait Haddou\\,\\orcidlink{{{ORCID}}}}}\n\\affiliation{{Independent Researcher}}",
            new_author,
            1,
        )

    # Do not display the numeric ORCID as prose anywhere in the author block.
    text = text.replace(
        f"\\thanks{{ORCID: \\href{{https://orcid.org/{ORCID}}}{{{ORCID}}}}}\n",
        "",
    )

    TARGET.write_text(text, encoding="utf-8")
    print(f"restored complete rewrite and applied author metadata to {TARGET}")


if __name__ == "__main__":
    main()
