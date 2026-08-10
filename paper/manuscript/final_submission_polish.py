from pathlib import Path

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_rewrite.tex"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # Never box prose. Keep the core message as plain centered emphasis, with no
    # equation number and no frame around the text.
    boxed = r"""The resulting message is deliberately limited:
\begin{equation}
\boxed{\text{rank fixes a baseline; spectral orientation controls actual retained tangent information.}}
\label{eq:message}
\end{equation}
"""
    plain = r"""The resulting message is deliberately limited:
\begin{center}
\emph{Rank fixes a baseline; spectral orientation controls actual retained tangent information.}
\end{center}
"""
    if boxed in text:
        text = text.replace(boxed, plain, 1)

    # Acknowledgment ORCID: clickable icon only, never expose the numeric ORCID
    # as prose in the rendered acknowledgment.
    old_ack = r"The author thanks Mohamed Bennai (\href{https://orcid.org/0000-0002-7364-5171}{ORCID: 0000-0002-7364-5171}) for helpful discussions."
    new_ack = r"The author thanks Mohamed Bennai\,\orcidlink{0000-0002-7364-5171} for helpful discussions."
    text = text.replace(old_ack, new_ack)

    TARGET.write_text(text, encoding="utf-8")
    print(f"final manuscript polish applied to {TARGET}")


if __name__ == "__main__":
    main()
