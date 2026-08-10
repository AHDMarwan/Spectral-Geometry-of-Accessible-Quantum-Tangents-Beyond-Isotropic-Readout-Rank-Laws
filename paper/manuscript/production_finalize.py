from __future__ import annotations

"""Apply the production citation/data pass to the manuscript rewrite.

This script is deliberately idempotent.  It inserts verified prior-art citations,
updates the completed n=18 U(1) results, adds the verified symmetry-breaking
control, and imports the established bibliography from the original manuscript
plus new production references.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper" / "prx"
TARGET = PAPER / "spectral_geometry_rewrite.tex"
ORIGINAL = PAPER / "spectral_geometry.tex"


def replace_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f"production patch anchor not found:\n{old[:180]}")
    return text.replace(old, new, 1)


def bibliography_block() -> str:
    src = ORIGINAL.read_text(encoding="utf-8")
    a = src.index("\\begin{thebibliography}")
    b = src.index("\\end{thebibliography}") + len("\\end{thebibliography}")
    block = src[a:b]

    additions = r"""

\bibitem{Fernandez2025}
A. Fernandez, F. Schneider, M. Mahsereci, and P. Hennig,
Connecting Parameter Magnitudes and Hessian Eigenspaces at Scale using Sketched Methods,
Trans. Mach. Learn. Res. (2025), arXiv:2504.14701.

\bibitem{LuSha2025}
J. Lu and K. Sha,
Quantum Fisher information matrix via its classical counterpart from random measurements,
arXiv:2509.08196 (2025).

\bibitem{Fontana2024}
E. Fontana, D. Herman, S. Chakrabarti, N. Kumar, R. Yalovetzky, J. Heredge,
S. H. Sureshbabu, and M. Pistoia,
Characterizing barren plateaus in quantum ans\"atze with the adjoint representation,
Nat. Commun. \textbf{15}, 7171 (2024),
doi:10.1038/s41467-024-49910-w.

\bibitem{Ragone2024}
M. Ragone, B. N. Bakalov, F. Sauvage, A. F. Kemper, C. Ortiz Marrero,
M. Larocca, and M. Cerezo,
A Lie algebraic theory of barren plateaus for deep parameterized quantum circuits,
Nat. Commun. \textbf{15}, 7172 (2024),
doi:10.1038/s41467-024-49909-3.

\bibitem{Monbroussou2025}
L. Monbroussou, E. Z. Mamon, J. Landman, A. B. Grilo, R. Kukla, and E. Kashefi,
Trainability and Expressivity of Hamming-Weight Preserving Quantum Circuits for Machine Learning,
Quantum \textbf{9}, 1745 (2025),
doi:10.22331/q-2025-05-15-1745.

\bibitem{UgailHoward2026}
H. Ugail and N. Howard,
A Coherence Law for Trainability in Noisy Equivariant Quantum Neural Networks,
arXiv:2606.30688 (2026).

\bibitem{Bermejo2026}
P. Bermejo, P. Braccia, M. S. Rudolph, Z. Holmes, L. Cincio, and M. Cerezo,
Quantum Convolutional Neural Networks are Effectively Classically Simulable,
PRX Quantum \textbf{7}, 020304 (2026),
doi:10.1103/8qt9-72ts.

\bibitem{Filmus2016}
Y. Filmus,
An Orthogonal Basis for Functions over a Slice of the Boolean Hypercube,
Electron. J. Combin. \textbf{23}(1), P1.23 (2016),
doi:10.37236/4567.

\bibitem{Khemani2018}
V. Khemani, A. Vishwanath, and D. A. Huse,
Operator Spreading and the Emergence of Dissipative Hydrodynamics under Unitary Evolution with Conservation Laws,
Phys. Rev. X \textbf{8}, 031057 (2018),
doi:10.1103/PhysRevX.8.031057.

\bibitem{Rakovszky2018}
T. Rakovszky, F. Pollmann, and C. W. von Keyserlingk,
Diffusive Hydrodynamics of Out-of-Time-Ordered Correlators with Charge Conservation,
Phys. Rev. X \textbf{8}, 031058 (2018),
doi:10.1103/PhysRevX.8.031058.
"""
    if "\\bibitem{Fernandez2025}" not in block:
        block = block.replace("\\end{thebibliography}", additions + "\n\\end{thebibliography}")
    return block


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    text = replace_once(
        text,
        "Random measurements can also approximate quantum Fisher geometry after averaging over measurement bases. These results establish that measurement choice, observable structure, and circuit architecture matter.",
        "Random measurements can also approximate quantum Fisher geometry after averaging over measurement bases \\cite{LuSha2025}. These results establish that measurement choice, observable structure, and circuit architecture matter.",
    )

    text = replace_once(
        text,
        "The random-subspace identity itself is standard Grassmann geometry. We use it for a different purpose:",
        "The random-subspace identity itself is standard Grassmann geometry \\cite{CollinsMatsumoto2017,Bendokat2024,Fernandez2025}. We use it for a different purpose:",
    )

    text = replace_once(
        text,
        "The identity is a standard random-subspace result. Its role here is to provide a controlled null model for readout orientation inside a fixed measurement-induced score space.\n\nStandard second-moment integration gives",
        "The identity is a standard random-subspace result \\cite{CollinsMatsumoto2017,Bendokat2024,Fernandez2025}. Its role here is to provide a controlled null model for readout orientation inside a fixed measurement-induced score space.\n\nUsing standard Grassmann projector moments \\cite{CollinsMatsumoto2017}, we obtain",
    )

    text = replace_once(
        text,
        "For a fixed covariance $C$ with eigenvalues $\\lambda_1\\ge\\cdots\\ge\\lambda_N$, the Ky Fan variational principle gives",
        "For a fixed covariance $C$ with eigenvalues $\\lambda_1\\ge\\cdots\\ge\\lambda_N$, the Ky Fan variational principle \\cite{KyFan1949} gives",
    )

    text = replace_once(
        text,
        "Confidence intervals are obtained by nonparametric bootstrap over independent circuit instances.",
        "Confidence intervals are obtained by nonparametric bootstrap over independent circuit instances \\cite{Efron1979}.",
    )

    old_u1 = r"""The stronger diagnostic is direct subspace overlap. Let $P_{\rm top}$ denote the cross-fitted leading tangent subspace of rank equal to the centered one-body readout rank, and let $P_{\le k}$ denote the cumulative low-weight Walsh span. We use
\begin{equation}
A_k=\frac{1}{r_1}\Tr(P_{\le k}P_{\rm top})
\label{eq:Ak}
\end{equation}
to quantify how much of the leading tangent subspace lies in low-weight sectors. For generic Haar circuits, $A_1$ decreases from approximately $0.0280$ at $n=8$ to $0.0028$ at $n=12$. In the $U(1)$ family it remains much larger: approximately $0.552$, $0.450$, and $0.396$ at $n=8,10,12$, with preliminary completed values near $0.341$ and $0.309$ at $n=14,16$. The cumulative weight-through-two overlap remains similarly elevated.

This observation should not be read as a new theorem that $U(1)$ symmetry improves trainability. Symmetry-preserving ansatzes, dynamical Lie-algebra restrictions, observable-dependent gradient scaling, and conserved-density hydrodynamics all provide relevant prior context. The present result is narrower: in this specific half-filled variational family, the leading measurement-induced tangent subspace is unusually visible to low-weight diagonal $Z$ readout under the rank-controlled metric used throughout this paper.

A small control further shows that the alignment is sensitive to exact conservation. Symmetry-preserving $Z$ perturbations leave the overlap largely intact, whereas nontrainable symmetry-breaking $X$ rotations strongly suppress it at fixed trainable parameter count. We use this as a control on the observed alignment, not as a mechanism-identification experiment. In particular, the present data do not distinguish among readout--charge compatibility, fixed-charge harmonic geometry, restricted controllability, and hydrodynamic slow modes.
"""

    new_u1 = r"""The stronger diagnostic is direct subspace overlap. Let $P_{\rm top}$ denote the cross-fitted leading tangent subspace of rank equal to the centered one-body readout rank, and let $P_{\le k}$ denote the cumulative low-weight Walsh span. We use
\begin{equation}
A_k=\frac{1}{r_1}\Tr(P_{\le k}P_{\rm top})
\label{eq:Ak}
\end{equation}
to quantify how much of the leading tangent subspace lies in low-weight sectors. This is a VQC-specific use of a standard projector/subspace-overlap construction rather than a claim that subspace overlap itself is new \cite{Fernandez2025}. Across $n=8,10,12,14,16,18$, the one-body values are $0.552$, $0.450$, $0.396$, $0.341$, $0.309$, and $0.284$, respectively. The final $n=18$ estimate is
\begin{equation}
A_1(18)=0.283586\;[0.277044,0.290865],
\end{equation}
while the cumulative weight-through-two overlap is
\begin{equation}
A_{\le2}(18)=0.463538\;[0.457425,0.469591].
\end{equation}
Each size uses 20 independent circuit instances.

Over the tested window $n=8$--$18$, two-parameter log-space model comparison favors a finite-size power form over an exponential form. The fitted exponents are $0.8223\,[0.7694,0.8735]$ for $A_1$ and $0.7041\,[0.6798,0.7281]$ for $A_{\le2}$, with $\Delta\mathrm{AICc}=14.39$ and $12.82$, respectively, in favor of the power model. These are finite-size model-discrimination results only; they are not asymptotic lower bounds and are not identified with a hydrodynamic exponent.

\begin{figure*}[t]
\centering
\includegraphics[width=.93\textwidth]{production/fig_u1_alignment_scaling.pdf}
\caption{Finite-size low-weight alignment in the half-filled $U(1)$ family. Points and error bars are circuit-level means and 95\% bootstrap intervals for the cross-fitted leading rank-$r_1$ tangent subspace. Solid curves are the two-parameter power fits and dashed curves are exponential fits over $n=8$--$18$. Positive $\Delta$AICc favors the power model over the tested window. The comparison is descriptive finite-size model selection, not an asymptotic or hydrodynamic theorem.}
\label{fig:u1-scaling}
\end{figure*}

This observation should not be read as a new theorem that $U(1)$ symmetry improves trainability. Hamming-weight-preserving trainability, Lie-algebraic restrictions, low-bodyness concentration in structured quantum models, and readout-visible sector coherence in noisy equivariant circuits are established neighboring phenomena \cite{Monbroussou2025,Fontana2024,Ragone2024,Bermejo2026,UgailHoward2026}. In addition, fixed-charge slice geometry supplies a non-dynamical structural null \cite{Filmus2016}, while conserved-density hydrodynamics supplies a distinct dynamical mechanism in random circuits \cite{Khemani2018,Rakovszky2018}. The present result is narrower: in this specific half-filled variational family, the leading measurement-induced tangent subspace is unusually visible to low-weight diagonal $Z$ readout under the rank-controlled metric used throughout this paper.

A separately archived pilot tests sensitivity to exact conservation at fixed trainable parameter count. At $n=8$, the unperturbed one-body alignment is $A_1=0.517\,[0.486,0.549]$. A symmetry-preserving $R_Z$ perturbation of strength $\epsilon=0.3$ leaves $A_1=0.481\,[0.454,0.518]$, whereas a nontrainable symmetry-breaking $R_X$ perturbation at the same strength gives $A_1=0.0295\,[0.0248,0.0338]$. The physical one-body retention simultaneously falls from $0.430$ to $0.0325$ in the breaking control. We use this as a sensitivity control, not as a mechanism-identification experiment: it does not separate readout--charge compatibility, fixed-charge harmonic geometry, restricted controllability, and hydrodynamic slow modes.

\begin{figure}[t]
\centering
\includegraphics[width=.98\linewidth]{production/fig_symmetry_breaking_control.pdf}
\caption{Verified symmetry-breaking pilot at $n=8$. Symmetry-preserving $R_Z$ perturbations leave the one-body tangent-subspace overlap comparatively stable, while nontrainable $R_X$ perturbations that break charge conservation suppress it toward the full-score-space rank scale. Error bars are 95\% circuit-bootstrap intervals over 10 circuit instances. The dotted line is a visual full-space rank reference after charge breaking, not a fit and not a sector-Haar null.}
\label{fig:symmetry-breaking}
\end{figure}
"""
    text = replace_once(text, old_u1, new_u1)

    text = replace_once(
        text,
        "Similar Grassmann overlap identities are standard in random-projection theory and appear in neighboring classical subspace-overlap problems. Likewise, the Ky Fan optimum is standard spectral optimization.",
        "Similar Grassmann overlap identities are standard in random-projection theory and appear in neighboring classical subspace-overlap problems \\cite{Fernandez2025}. Random-measurement work also establishes a distinct Haar-averaged CFIM--QFIM relation with variance and concentration bounds when the measurement basis itself is randomized \\cite{LuSha2025}. Likewise, the Ky Fan optimum is standard spectral optimization \\cite{KyFan1949}.",
    )

    text = replace_once(
        text,
        "Existing symmetry, Lie-algebraic, fixed-charge, and hydrodynamic theories offer plausible explanations for this structure.",
        "Existing Hamming-weight-preserving trainability and Lie-algebraic theories \\cite{Monbroussou2025,Fontana2024,Ragone2024}, readout-visible equivariant coherence \\cite{UgailHoward2026}, fixed-charge slice geometry \\cite{Filmus2016}, and conserved-density hydrodynamics \\cite{Khemani2018,Rakovszky2018} offer plausible but non-equivalent explanations for this structure.",
    )

    if "fig_fixed_weight_rank_fraction.pdf" not in text:
        anchor = "This is a baseline for comparison, not a statement that any physical ansatz approaches a Haar-random orientation as $n$ increases."
        insertion = anchor + r"""

\begin{figure}[t]
\centering
\includegraphics[width=.98\linewidth]{production/fig_fixed_weight_rank_fraction.pdf}
\caption{Rank-only scale for fixed-weight diagonal readout under full computational-basis support. For fixed Pauli weight, the retained subspace rank grows polynomially while the centered score-space dimension grows exponentially. The plotted fractions are geometric baselines only; physical retention depends on spectral orientation.}
\label{fig:rank-fraction-production}
\end{figure}
"""
        text = replace_once(text, anchor, insertion)

    if "\\begin{thebibliography}" not in text:
        status = "% -----------------------------------------------------------------------------\n% REWRITE STATUS"
        if status in text:
            text = text.replace(status, bibliography_block() + "\n\n" + status, 1)
        else:
            text = text.replace("\\end{document}", bibliography_block() + "\n\n\\end{document}", 1)

    # The n=18 run and pilot verification are now completed.
    text = text.replace(
        "% 2. insert the final n=18 U(1) scaling point after the running workflow completes;\n",
        "% 2. final n=18 U(1) scaling point inserted and cross-checked against archived summary;\n",
    )
    text = text.replace(
        "% 4. verify the symmetry-breaking pilot from archived raw outputs before publication.\n",
        "% 4. symmetry-breaking pilot verified against archived raw/summary CSV; retain pilot wording.\n",
    )

    TARGET.write_text(text, encoding="utf-8")
    print(f"updated {TARGET}")


if __name__ == "__main__":
    main()
