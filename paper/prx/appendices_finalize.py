from pathlib import Path

PAPER = Path(__file__).resolve().parent
TARGET = PAPER / "spectral_geometry_prx_rewrite.tex"

APPENDIX_MARKER = r"\label{app:score_geometry}"

APPENDIX = r'''

\appendix

\section{Score-space construction and Fisher normalization}
\label{app:score_geometry}

For completeness, we collect here the conventions that connect the fixed measurement record to the normalized score geometry used in the main text.  Let $p_\theta(x)$ be the probability of outcome $x$ under the fixed computational-basis measurement and let $v$ be a parameter-space direction.  The directional probability tangent is $\partial_v p_\theta(x)$.  On the regular support, the Fisher-weighted tangent may be written as
\begin{equation}
 s_v(x)=\frac{\partial_v p_\theta(x)}{\sqrt{p_\theta(x)}}.
\label{eq:app-score}
\end{equation}
The probability-normalization constraint removes the constant mode, leaving an $N$-dimensional centered real score space.  The numerical protocol normalizes every regular tangent direction according to
\begin{equation}
 u_v=\frac{s_v}{\|s_v\|_2},\qquad \|u_v\|_2=1,
\label{eq:app-normalized-score}
\end{equation}
and forms
\begin{equation}
 C=\mathbb E_v[u_vu_v^{\mathsf T}],\qquad \Tr C=1.
\label{eq:app-C}
\end{equation}
Before the unit normalization in Eq.~\eqref{eq:app-normalized-score}, $\|s_v\|_2^2$ is the classical Fisher information carried by the fixed measurement along $v$ \cite{BraunsteinCaves1994,LuLuoOh2012}.  The normalized covariance $C$ therefore describes how the \emph{directions} of measurement-visible tangent variation are distributed after the overall directional Fisher scale has been factored out.

For an orthogonal readout projector $P$, linearity and cyclicity of the trace give
\begin{align}
\mathbb E_v\|Pu_v\|_2^2
&=\mathbb E_v\,u_v^{\mathsf T}Pu_v \\
&=\Tr\!\left(P\,\mathbb E_v[u_vu_v^{\mathsf T}]\right)
=\Tr(PC),
\label{eq:app-R}
\end{align}
which is the operational identity used in Eq.~\eqref{eq:R-operational}.

\section{Grassmann random-orientation moments}
\label{app:grassmann}

We give the complete moment calculation underlying Eqs.~\eqref{eq:rank-baseline}--\eqref{eq:var-bound}.  Let $P$ be Haar-uniform on the real Grassmann manifold $\mathrm{Gr}(r,N)$.  Orthogonal invariance implies
\begin{equation}
\mathbb E P=\frac rN I.
\end{equation}
Hence, for any fixed trace-one $C$,
\begin{equation}
\mathbb E\Tr(PC)=\Tr\!\left(C\,\mathbb EP\right)=\frac rN.
\end{equation}
The second moment of a random orthogonal projector has the invariant tensor form
\begin{equation}
\mathbb E[P_{ij}P_{kl}]
=a\,\delta_{ij}\delta_{kl}
+b\,(\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk}),
\label{eq:app-projector-second}
\end{equation}
with coefficients fixed by $P^2=P$ and $\Tr P=r$ \cite{CollinsMatsumoto2017}.  Solving these constraints and contracting Eq.~\eqref{eq:app-projector-second} with $C_{ji}C_{lk}$ yields
\begin{equation}
\operatorname{Var}[\Tr(PC)]
=\frac{2r(N-r)}{N^2(N-1)(N+2)}
\left[N\Tr(C^2)-1\right].
\label{eq:app-var-R}
\end{equation}
Since $\rho=N\Tr(PC)/r$, Eq.~\eqref{eq:app-var-R} gives
\begin{equation}
\operatorname{Var}(\rho)
=\frac{2(N-r)[N\Tr(C^2)-1]}
{r(N-1)(N+2)}.
\label{eq:app-var-rho}
\end{equation}
Using $N-r\le N-1$ and $N\Tr(C^2)-1\le (N+2)\Tr(C^2)$ gives
\begin{equation}
\operatorname{Var}(\rho)\le \frac{2}{r d_{\rm eff}},
\qquad d_{\rm eff}=\frac1{\Tr(C^2)}.
\label{eq:app-deff-bound}
\end{equation}
Thus concentration depends on the product $r d_{\rm eff}$, not on $d_{\rm eff}/N$ approaching unity.

\begin{figure}[t]
\centering
\includegraphics[width=.96\linewidth]{figS2_exact_null_width.pdf}
\caption{Exact random-orientation fluctuation scale for representative effective dimensions.  The standard deviation of $\rho$ narrows with increasing readout rank and effective spectral dimension; this is compatible with a strongly anisotropic covariance whenever $r d_{\rm eff}$ is large.}
\label{fig:app-null-width}
\end{figure}

\section{Fixed-weight diagonal readout spaces}
\label{app:walsh_rank}

For full computational-basis support, the centered outcome space has dimension $N=2^n-1$.  Distinct nonidentity diagonal Pauli strings are orthogonal in the uniform Walsh basis, so the cumulative weight-through-$k$ span has dimension
\begin{equation}
 r_{\le k}=\sum_{j=1}^k\binom nj.
\label{eq:app-rank-full}
\end{equation}
For fixed $k$ and large $n$, $r_{\le k}=n^k/k!\,[1+O(n^{-1})]$, which gives the exponentially small full-space rank fraction used in the main text.

In the half-filled fixed-charge sector, the outcome support contains $\binom{n}{n/2}$ basis strings and the centered score dimension is
\begin{equation}
 N_{\rm hf}=\binom{n}{n/2}-1.
\end{equation}
The fixed-charge identity $\sum_i Z_i=0$ on the half-filled support removes one one-body degree of freedom, giving
\begin{equation}
 r_1=n-1.
\end{equation}
For the cumulative one- and two-body diagonal span, the corresponding centered dimension used in the numerical protocol is
\begin{equation}
 r_{\le2}=\binom n2-1.
\end{equation}
These sector-corrected ranks are geometric bookkeeping identities; they do not by themselves imply any particular physical orientation of the tangent covariance.  Fixed-charge harmonic analysis provides a broader mathematical context for low-degree functions on a slice \cite{Filmus2016}.

\begin{figure}[t]
\centering
\includegraphics[width=.96\linewidth]{figS4_rank_fraction.pdf}
\caption{Rank fractions for low-weight diagonal readouts under full computational-basis support.  Polynomially growing low-weight spaces occupy an exponentially shrinking fraction of the centered record.}
\label{fig:app-rank-fractions}
\end{figure}

\section{Cross-fitting, Ky Fan benchmark, and statistical unit}
\label{app:crossfit}

For a covariance estimate $\widehat C_{\rm fit}$ obtained from one tangent ensemble, let $Q_r$ contain its leading $r$ eigenvectors and define the aligned projector $P_{\rm xfit}=Q_rQ_r^{\mathsf T}$.  Retention is then evaluated on an independent tangent ensemble,
\begin{equation}
 R_{\rm xfit}=\frac1{m_{\rm eval}}\sum_{a=1}^{m_{\rm eval}}
\|P_{\rm xfit}u_a^{\rm(eval)}\|_2^2.
\label{eq:app-crossfit}
\end{equation}
This separation prevents the same tangent samples from both selecting and evaluating the subspace.  By contrast, the same-sample Ky Fan quantity
\begin{equation}
 R_{\rm KF}=\sum_{j=1}^r\lambda_j(\widehat C)
\end{equation}
is an optimistic spectral upper benchmark rather than the operational estimator \cite{KyFan1949}.

The independent resampling unit is the circuit instance.  Tangent directions generated from the same circuit are correlated and are therefore not treated as independent bootstrap replicates.  Confidence intervals reported in the manuscript resample circuit instances and recompute the relevant aggregate.  The frozen profiles, seeds, shard-level outputs, and paper-facing summaries are archived in the reproducibility repository \cite{AitHaddou2026MeasurementAccessible}.

\section{Operational signal diagnostics}
\label{app:operational}

Let $F_{\rm full}(v)$ denote the classical Fisher scale of a direction before the unit normalization used to construct $u_v$.  For a rank-$r$ projector $P$, the raw retained directional Fisher energy is
\begin{equation}
 E_{\rm raw}(P)=\mathbb E_v\!\left[F_{\rm full}(v)\,\|Pu_v\|_2^2\right].
\label{eq:app-raw-energy}
\end{equation}
If a scalar readout direction is sampled isotropically inside the retained $r$-dimensional subspace, the mean squared directional signal is
\begin{equation}
 \mathbb E[g_{\rm dir}^2]=\frac{E_{\rm raw}(P)}{r}.
\label{eq:app-dir-signal}
\end{equation}
The finite-shot calculation in the numerical campaign combines this signal with the multinomial covariance of the fixed measurement record.  All orientation comparisons keep the circuit, quantum measurement, readout rank, and shot count fixed.  Consequently, ratios between physical, random-rank, and aligned readouts isolate the effect of the retained score-space orientation.  These quantities are controlled directional diagnostics and are not claims about the gradient variance of an arbitrary supervised loss.

\begin{figure*}[t]
\centering
\includegraphics[width=.97\textwidth]{appendix_operational_gains.pdf}
\caption{Additional fixed-rank operational diagnostics.  Retention, directional gradient-energy, and finite-shot SNR gains are shown for the same physical versus cross-fitted aligned comparison used in the main text.  Generic Haar-$U(4)$ circuits leave substantial room for orientation improvement, whereas the structured $U(1)$ readout is already comparatively aligned.}
\label{fig:app-operational}
\end{figure*}

\section{Additional covariance and architecture diagnostics}
\label{app:architecture}

The main text emphasizes the coexistence of near-rank-typical retention with strong anisotropy.  The following supplementary views expose the corresponding effective-dimension and orientation diagnostics directly.

\begin{figure*}[t]
\centering
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{figS1_deff_fraction.pdf}
\end{minipage}\hfill
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{figS3_orientation_z.pdf}
\end{minipage}\hfill
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{appendix_noise_robustness.pdf}
\end{minipage}
\caption{Supporting diagnostics.  Left: effective spectral fraction $d_{\rm eff}/N$.  Center: population-null orientation diagnostic for representative generic/Haar and $U(1)$ points.  Right: aligned-to-physical directional gradient-energy gain under readout bit-flip noise.  The noise comparison re-estimates the aligned subspace after noise is applied and therefore does not establish robustness of a single fixed optimized observable.}
\label{fig:app-supporting}
\end{figure*}

\section{Finite-size diagnostics for the half-filled $U(1)$ family}
\label{app:u1_scaling}

The main text reports the cross-fitted overlap through $n=18$ and compares two simple finite-size models.  We stress that this comparison is descriptive model discrimination over the simulated window rather than an asymptotic theorem.  The fitted power exponents and $\Delta\mathrm{AICc}$ values are computed from the archived paper-facing summaries \cite{AitHaddou2026MeasurementAccessible}.

\begin{figure*}[t]
\centering
\includegraphics[width=.95\textwidth]{appendix_u1_fit_diagnostics.pdf}
\caption{Finite-size diagnostics for the half-filled $U(1)$ family.  The left panels show the full $n=8$--$18$ overlap data together with the fitted power and exponential models; the right panel summarizes the model-selection difference $\Delta\mathrm{AICc}=\mathrm{AICc}_{\rm exp}-\mathrm{AICc}_{\rm power}$.  Positive values favor the power model within the tested finite-size window only.}
\label{fig:app-u1-fits}
\end{figure*}

\section{Circuit conventions and reproducibility}
\label{app:circuits_repro}

The PennyLane diagrams in the main text are schematic: parameter values are intentionally suppressed, and only a few layers are drawn for legibility.  The simulations use the exact gate constructors, depth conventions, deterministic seeds, and frozen profiles archived in the repository \cite{AitHaddou2026MeasurementAccessible}.  For reference, the individual generated circuit diagrams are collected below.

\begin{figure*}[t]
\centering
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{generated_circuits/circuit_ry_rz_cz.pdf}\\[-1mm]{\scriptsize RY--RZ--CZ}
\end{minipage}\hfill
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{generated_circuits/circuit_su2_cnot.pdf}\\[-1mm]{\scriptsize SU2--CNOT}
\end{minipage}\hfill
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{generated_circuits/circuit_su2_cz_ring.pdf}\\[-1mm]{\scriptsize SU2--CZ ring}
\end{minipage}

\vspace{2mm}
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{generated_circuits/circuit_su2_cz_random_matching.pdf}\\[-1mm]{\scriptsize SU2--CZ random matching}
\end{minipage}\hfill
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{generated_circuits/circuit_su2_haar_u4.pdf}\\[-1mm]{\scriptsize Haar-$U(4)$ brickwork}
\end{minipage}\hfill
\begin{minipage}{.32\textwidth}\centering
\includegraphics[width=\linewidth]{generated_circuits/circuit_u1_rz_xy.pdf}\\[-1mm]{\scriptsize half-filled $U(1)$ RZ--XY}
\end{minipage}
\caption{Individual PennyLane circuit schematics used by the numerical campaign.  Gate parameters are hidden in the drawings, while the source constructors and complete numerical profiles are archived with the code and results.}
\label{fig:app-circuits}
\end{figure*}

'''


def add_once(text: str, old: str, new: str) -> str:
    if new in text:
        return text
    if old not in text:
        return text
    return text.replace(old, old + new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")

    # Keep the main narrative unchanged except for short pointers to detailed
    # derivations/protocols in the appendices.
    text = add_once(
        text,
        "Equation~\\eqref{eq:var-bound} is the key separation used below.",
        " A full projector-moment derivation is given in Appendix~\\ref{app:grassmann}.",
    )
    text = add_once(
        text,
        "This is a baseline for comparison, not a statement that any physical ansatz approaches a Haar-random orientation as $n$ increases.",
        " The full- and fixed-charge rank bookkeeping is collected in Appendix~\\ref{app:walsh_rank}.",
    )
    text = add_once(
        text,
        "Because the same-sample optimum is statistically optimistic, the operational comparison uses a cross-fitted projector",
        " (Appendix~\\ref{app:crossfit})",
    )
    text = add_once(
        text,
        "These quantities are not supervised-loss gradient variances.",
        " Their precise directional definitions and fixed-shot interpretation are summarized in Appendix~\\ref{app:operational}.",
    )

    if APPENDIX_MARKER not in text:
        anchor = "\\begin{acknowledgments}"
        if anchor not in text:
            raise RuntimeError("acknowledgments anchor not found for appendix insertion")
        text = text.replace(anchor, APPENDIX + "\n" + anchor, 1)

    TARGET.write_text(text, encoding="utf-8")
    print("comprehensive appendices added; main text changed only by appendix pointers")


if __name__ == "__main__":
    main()
