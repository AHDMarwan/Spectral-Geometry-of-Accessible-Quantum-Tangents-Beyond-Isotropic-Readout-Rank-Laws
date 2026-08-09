# Theory audit: asymptotic rank typicality

Status: mathematical audit of `paper/ASYMPTOTIC_RANK_TYPICALITY.tex`. This note is not a preregistered numerical analysis and is not a novelty claim.

## 1. Exact Haar/Grassmann second moment

Let `P` be the orthogonal projector onto a Haar-uniform real rank-`r` subspace of `R^N`. Orthogonal invariance implies that its second moment has the tensor form

\[
\mathbb E[P_{ij}P_{kl}]
=a\,\delta_{ij}\delta_{kl}
+b\,(\delta_{ik}\delta_{jl}+\delta_{il}\delta_{jk}).
\]

The deterministic identities `Tr(P)=r` and `Tr(P^2)=r` imply

\[
aN^2+2bN=r^2,
\qquad
aN+b(N^2+N)=r,
\]

so

\[
a=\frac{r(Nr+r-2)}{N(N-1)(N+2)},
\qquad
b=\frac{r(N-r)}{N(N-1)(N+2)}.
\]

For any fixed real symmetric `C` with `Tr(C)=1`,

\[
\mathbb E\{[\operatorname{Tr}(PC)]^2\}
=a+2b\operatorname{Tr}(C^2).
\]

Subtracting `(r/N)^2` gives

\[
\operatorname{Var}[\operatorname{Tr}(PC)]
=\frac{2r(N-r)(N\operatorname{Tr}(C^2)-1)}
{N^2(N-1)(N+2)}.
\]

Therefore, for

\[
\rho=\frac{\operatorname{Tr}(PC)}{r/N},
\]

we obtain exactly

\[
\mathbb E\rho=1,
\qquad
\operatorname{Var}(\rho)
=\frac{2(N-r)(Nq-1)}{r(N-1)(N+2)},
\quad q=\operatorname{Tr}(C^2).
\]

This independently reproduces the formula used by the rigorous-v2 orientation null.

## 2. Concentration bound

For `C >= 0`, `Tr(C)=1`, we have `1/N <= q <= 1`. Since `r>=1`,

\[
N-r\le N-1,
\]

and since `q>=0`,

\[
Nq-1\le Nq\le q(N+2).
\]

Both factors on the left are nonnegative. Hence

\[
(N-r)(Nq-1)\le q(N-1)(N+2),
\]

which proves

\[
\boxed{\operatorname{Var}(\rho)\le \frac{2q}{r}
=\frac{2}{r d_{\rm eff}}.}
\]

Chebyshev therefore gives

\[
\Pr(|\rho-1|\ge\varepsilon)
\le \min\left\{1,\frac{2}{\varepsilon^2 r d_{\rm eff}}\right\}.
\]

The bound does not assume isotropy and remains valid when `d_eff/N -> 0`.

## 3. Asymptotic consequences

If `r_n d_eff,n -> infinity`, then `rho_n -> 1` in probability. For fixed full-support diagonal weight `k`,

\[
r_k(n)=\sum_{j=1}^k {n\choose j}=\Theta(n^k),
\]

and `d_eff >= 1`, so the condition holds for every fixed `k>=1` under the random-relative-orientation model.

If additionally

\[
\sum_n \frac{1}{r_n d_{\rm eff,n}}<\infty,
\]

then the first Borel--Cantelli lemma gives almost-sure convergence. Independence across `n` is not required for this first-lemma implication. For fixed full-support `k>=2`, summability follows already from `d_eff>=1` and `r_k(n)=Theta(n^k)`.

The full-support formula for `r_k(n)` must not be applied to symmetry-reduced score spaces. In the U(1) sector, the archived `score_dimension` and `readout_rank` are the operative quantities.

## 4. Physical-readout bridge

For a fixed physical projector define the population-null scale

\[
\sigma_{\rho,n}^2
=\frac{2(N_n-r_n)(N_n\operatorname{Tr}(C_n^2)-1)}
{r_n(N_n-1)(N_n+2)}
\]

and

\[
z_n^{\rm(pop)}=\frac{\rho_n^{\rm(phys)}-1}{\sigma_{\rho,n}}.
\]

The identity

\[
|\rho_n^{\rm(phys)}-1|
=|z_n^{\rm(pop)}|\sigma_{\rho,n}
\le |z_n^{\rm(pop)}|\sqrt{\frac{2}{r_nd_{\rm eff,n}}}
\]

shows that

\[
\frac{|z_n^{\rm(pop)}|}{\sqrt{r_nd_{\rm eff,n}}}\to0
\]

is a sufficient condition for the fixed physical readout to become rank-typical. It is not a necessary condition, and finite-size fitting of this ratio is diagnostic rather than a proof of its limiting behavior.

## 5. Literature positioning

The projector-moment machinery itself should be treated as standard, not as the novelty claim. Orthogonal/Grassmann Haar moments are consequences of invariant integration / Weingarten calculus. Useful primary references include:

- Benoit Collins and Sho Matsumoto, *Weingarten calculus via orthogonality relations: new applications*, arXiv:1701.04493.
- Thomas Bendokat, Ralf Zimmermann, and P.-A. Absil, *A Grassmann Manifold Handbook: Basic Geometry and Computational Aspects*, arXiv:2011.13699.
- Karel Devriendt, Hannah Friedman, Bernhard Reinke, and Bernd Sturmfels, *The Two Lives of the Grassmannian*, arXiv:2401.03684 (projector representation of the real Grassmannian).

The defensible contribution to emphasize is the operational application: accessible quantum tangent covariance can be strongly anisotropic while random-relative-orientation low-weight accessibility concentrates at its rank baseline; the physical-circuit data then diagnose when actual readouts follow that regime and when symmetry creates a growing orientation anomaly.

A full priority/novelty search against the quantum-trainability literature is separate from this algebraic validity audit.
