from __future__ import annotations

"""Insert the all-family PennyLane circuit figure into the production rewrite.

Idempotent: safe to run on every paper-production CI pass.
"""

from pathlib import Path

TARGET = Path("paper/manuscript/spectral_geometry_rewrite.tex")

FIGURE = r"""

\begin{figure*}[t]
\centering
\includegraphics[width=.49\textwidth]{generated_circuits/circuit_ry_rz_cz.pdf}\hfill
\includegraphics[width=.49\textwidth]{generated_circuits/circuit_su2_cnot.pdf}\\[2pt]
\includegraphics[width=.49\textwidth]{generated_circuits/circuit_su2_cz_ring.pdf}\hfill
\includegraphics[width=.49\textwidth]{generated_circuits/circuit_su2_cz_random_matching.pdf}\\[2pt]
\includegraphics[width=.49\textwidth]{generated_circuits/circuit_su2_haar_u4.pdf}\hfill
\includegraphics[width=.49\textwidth]{generated_circuits/circuit_u1_rz_xy.pdf}
\caption{Circuit families used in the numerical campaign, rendered directly from PennyLane circuit definitions \cite{Bergholm2018}. From top left to bottom right: RY--RZ--CZ line, SU2--CNOT line, SU2--CZ ring, SU2--CZ random matching, SU2--Haar-$U(4)$ brickwork, and the half-filled $U(1)$ RZ--XY line. For legibility the drawings show $n=6$ and two representative layers; the production simulations use the depths and system sizes specified in the numerical protocol. The $U(1)$ panel begins from the alternating half-filled computational-basis state, matching the simulation code. Generic unitary boxes in the last row represent the actual two-qubit matrices used by the simulator rather than a gate decomposition.}
\label{fig:circuits}
\end{figure*}
"""

BIB = r"""

\bibitem{Bergholm2018}
V. Bergholm, J. Izaac, M. Schuld, C. Gogolin, S. Ahmed, V. Ajith, et al.,
PennyLane: Automatic differentiation of hybrid quantum-classical computations,
arXiv:1811.04968 (2018).
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    if "\\label{fig:circuits}" not in text:
        anchor = "\\section{Rank typicality without isotropy in generic circuits}"
        if anchor not in text:
            raise RuntimeError("could not find circuit-figure insertion anchor")
        text = text.replace(anchor, FIGURE + "\n" + anchor, 1)

    if "\\bibitem{Bergholm2018}" not in text:
        endbib = "\\end{thebibliography}"
        if endbib not in text:
            raise RuntimeError("bibliography must be present before circuit citation insertion")
        text = text.replace(endbib, BIB + "\n" + endbib, 1)

    TARGET.write_text(text, encoding="utf-8")
    print(f"updated {TARGET}")


if __name__ == "__main__":
    main()
