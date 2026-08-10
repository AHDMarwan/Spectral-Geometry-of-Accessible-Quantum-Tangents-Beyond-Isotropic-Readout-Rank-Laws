from __future__ import annotations

"""Insert operational-bridge and noise-robustness figures into the rewrite."""

from pathlib import Path

TARGET = Path("paper/prx/spectral_geometry_prx_rewrite.tex")

OP_FIG = r"""

\begin{figure*}[t]
\centering
\includegraphics[width=.93\textwidth]{production/fig_operational_bridge.pdf}
\caption{Operational effect of readout orientation at fixed measurement resources. The plotted ratios compare the cross-fitted tangent-aligned subspace with the physical one-body readout on the same circuits, with identical rank and a fixed shot budget. In generic Haar-$U(4)$ circuits the orientation advantage grows strongly over the tested sizes, reaching a $9.58\times$ directional gradient-energy gain and a $3.11\times$ finite-shot SNR gain at $n=12$. The $U(1)$ ratios remain much closer to unity because the physical low-weight readout is already aligned with leading tangent directions. The quantities are directional-signal diagnostics, not supervised-loss gradient variances.}
\label{fig:operational-bridge}
\end{figure*}
"""

NOISE = r"""

\subsection{Noise-aware orientation test}

We additionally apply an independent classical bit-flip channel to the computational-basis record and repeat the equal-rank comparison. The aligned projector is re-estimated after the specified noise channel, so this experiment tests whether a noise-aware tangent geometry still supports an orientation advantage; it does not test survival of one fixed observable subspace under noise. Noise-induced changes to variational trainability are well established in broader settings \cite{Wang2021}.

For Haar-$U(4)$ at $n=12$, the aligned-to-physical directional gradient-signal ratio decreases from $9.584\,[9.360,9.830]$ without added readout noise to $6.919\,[6.760,7.102]$, $4.491\,[4.394,4.604]$, and $3.127\,[3.059,3.204]$ at bit-flip rates of $1\%$, $3\%$, and $5\%$, respectively. The advantage therefore weakens but remains substantial over the tested range. In the $U(1)$ family the same ratio stays near unity, ranging from $1.210\,[1.187,1.234]$ in the clean $n=12$ cell to $1.150\,[1.135,1.165]$ at $5\%$ noise.

\begin{figure*}[t]
\centering
\includegraphics[width=.93\textwidth]{production/fig_noise_robustness.pdf}
\caption{Noise-aware equal-rank orientation comparison. Error bars are 95\% circuit-bootstrap intervals for the aligned-to-physical directional gradient-signal ratio after applying the indicated classical bit-flip channel and re-estimating the aligned subspace. Generic Haar-$U(4)$ circuits retain a clear orientation advantage as readout noise increases, although the gain decreases. The structured $U(1)$ family remains close to unity because its physical readout is already comparatively well aligned.}
\label{fig:noise-robustness}
\end{figure*}
"""


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    if "\\label{fig:operational-bridge}" not in text:
        anchor = "These quantities are not supervised-loss gradient variances."
        if anchor not in text:
            raise RuntimeError("operational figure anchor not found")
        text = text.replace(anchor, OP_FIG + "\n" + anchor, 1)

    if "\\label{fig:noise-robustness}" not in text:
        anchor = "\\section{Structured case study: a half-filled $U(1)$ circuit}"
        if anchor not in text:
            raise RuntimeError("noise section anchor not found")
        text = text.replace(anchor, NOISE + "\n" + anchor, 1)

    text = text.replace(
        "% 3. integrate the final trainability/noise figures and appendix derivations;",
        "% 3. final trainability/noise figures integrated; appendix derivations remain to verify;",
    )

    TARGET.write_text(text, encoding="utf-8")
    print(f"updated {TARGET}")


if __name__ == "__main__":
    main()
