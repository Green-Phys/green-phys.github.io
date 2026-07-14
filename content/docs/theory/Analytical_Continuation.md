---
title: Analytical Continuation
weight: 7
math: true
prev: "/docs/theory/gw_theory"
next: "/docs/theory/thermodynamics"
aliases:
  - /docs/theory/postprocessing/Analytical_Continuation/
  - /docs/theory/postprocessing/analytical_continuation/
---

Finite-temperature Green's function methods naturally produce correlation functions on the
imaginary-time or Matsubara-frequency axis. Experiments, however, probe real-frequency
response functions: spectral functions, photoemission spectra, optical conductivities, and
other dynamical observables. Analytical continuation is the post-processing step that maps
imaginary-axis data to the retarded real-frequency axis.

For a fermionic one-particle Green's function, the retarded spectral function is

$$
A(\omega) = -\frac{1}{\pi}\operatorname{Im} G^R(\omega)
          = -\frac{1}{\pi}\operatorname{Im} G(\omega+i0^+),
$$

and the Matsubara Green's function is related to it by

$$
G(i\omega_n)
  = \int_{-\infty}^{\infty} d\omega\,
    \frac{A(\omega)}{i\omega_n-\omega}.
$$

Equivalently, in imaginary time,

$$
G(\tau)
  = -\int_{-\infty}^{\infty} d\omega\,
    \frac{e^{-\tau\omega}}{1+e^{-\beta\omega}} A(\omega),
\qquad 0<\tau<\beta.
$$

Both equations have the form

$$
G_n = \int d\omega\, K_n(\omega) A(\omega).
$$

The forward map $A(\omega)\mapsto G_n$ is stable: one can always integrate a proposed
real-frequency spectrum and compare it with imaginary-axis data. The inverse map is not
stable. The Matsubara and imaginary-time kernels above strongly damp high-frequency and
fine spectral information. In a discretized problem,

$$
G_i = \sum_j K_{ij} A_j,
$$

the singular values of $K$ fall rapidly. Direct inversion divides by these small singular
values, so small statistical errors, truncation errors, or roundoff errors in $G_i$ become
large oscillations in $A_j$. As a result, infinitely many spectra are usually consistent
with the input data within its numerical uncertainty. Analytical continuation is therefore
not just inversion of a kernel. It is a regularized inverse problem.

Regularization enters by adding information that is not contained in the finite noisy data:
positivity, normalization, causality, smoothness, a default model, exact analytic
structure, or compactness of a pole representation. The methods below differ mainly in
which additional principle they impose.

## Maximum Entropy

The maximum entropy method, as implemented and reviewed by Levy, LeBlanc, and Gull,
regularizes the continuation by finding a positive spectrum that both back-continues to the
input data and remains maximally featureless relative to a default model.[^levy-maxent]
Given a trial spectrum $A(\omega)$, its back-continuation is

$$
\bar{G}_n[A] = \int d\omega\, K_n(\omega) A(\omega).
$$

If the data have covariance matrix $C$, the misfit is

$$
\begin{aligned}
\chi^2[A]
  &=
  \sum_{n,m}
  \left(\bar{G}_n[A]-G_n\right)^*
  C^{-1}_{nm}
  \left(\bar{G}_m[A]-G_m\right).
\end{aligned}
$$

Maximum entropy then minimizes

$$
Q[A] = \frac{1}{2}\chi^2[A] - \alpha S[A],
$$

where $\alpha>0$ controls the tradeoff between fitting the data and keeping the spectrum
smooth. The entropy is defined relative to a positive default model $d(\omega)$,

$$
S[A]
  = -\int d\omega\, A(\omega)
      \ln\frac{A(\omega)}{d(\omega)}.
$$

Large $\alpha$ returns a spectrum close to the default model. Small $\alpha$ approaches a
least-squares fit and therefore risks amplifying the ill conditioning of the kernel. The
useful MaxEnt result lies between these limits. In Bryan's formulation, the search space is
reduced using the singular value decomposition of the kernel and spectra obtained for a
range of $\alpha$ values are weighted by their posterior probability.

MaxEnt is especially useful for noisy Monte Carlo data because it treats error bars
explicitly. It also enforces positivity and sum rules when the target object can be
interpreted as a positive spectral density. Its main limitation is that entropy favors
smooth spectra. Sharp peaks, high-energy features, band edges, and multiplet structures are
often broadened or washed out. A second limitation is structural: off-diagonal Green's
function or self-energy elements can change sign, so they are not positive probability
densities and cannot be continued by the simplest MaxEnt formulation without additional
transformations or generalized entropy constructions.

## Nevanlinna Interpolation

Nevanlinna continuation changes the regularization principle. Instead of fitting a smooth
spectrum to noisy data, it interpolates high-precision Matsubara data within the exact
analytic class of fermionic Green's functions.[^fei-nevanlinna] For a fermionic Green's
function, the negative Green's function

$$
N(z) = -G(z)
$$

is a Nevanlinna function in the upper half-plane $\mathbb{C}^+$: it is analytic for
$\operatorname{Im}z>0$ and has non-negative imaginary part,

$$
\operatorname{Im} N(z) \ge 0,\qquad z\in\mathbb{C}^+.
$$

This follows from the Lehmann representation. For positive spectral weights,

$$
G(z)=\sum_l \frac{w_l}{z-\epsilon_l}, \qquad w_l\ge 0,
$$

so for $z=x+iy$ with $y>0$,

$$
\begin{aligned}
\operatorname{Im}G(z)
  &=
  -\sum_l
  \frac{w_l y}{(x-\epsilon_l)^2+y^2}
  \le 0.
\end{aligned}
$$

Consequently $N=-G$ maps the upper half-plane into itself. Evaluating just above the real
axis then gives a non-negative spectral function,

$$
A(\omega)
  = \lim_{\eta\to 0^+}
    \frac{1}{\pi}\operatorname{Im}N(\omega+i\eta).
$$

The Nevanlinna method constructs an interpolant that passes through the Matsubara data
points and remains in this causal function class. A Mobius transform maps the upper
half-plane to the unit disk,

$$
h(z)=\frac{z-i}{z+i},
$$

and maps function values to contractive Schur functions. If the input points are
$Y_j=i\omega_j$ and the values are $C_j=N(Y_j)$, define

$$
\lambda_j = h(C_j)=\frac{C_j-i}{C_j+i}.
$$

A Nevanlinna interpolant exists only when the Pick matrix

$$
\begin{aligned}
P_{ij}
  &=
  \frac{1-\lambda_i\lambda_j^*}
       {1-h(Y_i)h(Y_j)^*}
\end{aligned}
$$

is positive semidefinite. This condition is restrictive. Exact or high-precision
diagrammatic data may satisfy it, but noisy Monte Carlo data generally does not. When it is
satisfied, the Schur algorithm produces a continued-fraction family of interpolants. The
remaining freedom can be used to select a physically useful member of that family, for
example by minimizing a smoothness functional in a Hardy-function basis.

The important conceptual distinction is that Nevanlinna is an interpolation method, not a
least-squares fit. It is therefore most appropriate for precise input data. Its benefit is
that positivity, normalization, and causality are built into the analytic class, so it can
resolve sharp and high-frequency structures that entropy-based methods tend to smear.

## Caratheodory Matrix Continuation

Most realistic Green's function calculations are matrix-valued. The object to continue is
not just $G(i\omega_n)$ but $G_{ij}(i\omega_n)$, $\Sigma_{ij}(i\omega_n)$, or a cumulant
$M_{ij}(i\omega_n)$. The diagonal elements have positive spectral densities, but
off-diagonal elements need not. Continuing only the diagonal entries and dropping the
off-diagonal self-energy is an uncontrolled approximation unless symmetry makes the
self-energy diagonal at all frequencies.

The Caratheodory formalism extends the Nevanlinna idea to matrix-valued functions.[^fei-cara]
A matrix-valued function $F(z)$ is Caratheodory on a domain if it is holomorphic and

$$
\frac{F(z)+F^\dagger(z)}{2} \succeq 0,
\qquad z\in\mathbb{C}^+,
$$

where $\succeq 0$ denotes positive semidefiniteness. For fermionic many-body quantities,
the relevant objects are Caratheodory up to a factor of $i$:

$$
iG(z)\in\mathfrak{C},\qquad
i\Sigma(z)\in\mathfrak{C},\qquad
iM(z)\in\mathfrak{C}.
$$

For example, the matrix Lehmann representation

$$
\begin{aligned}
G_{ij}(z)
  &=
  \frac{1}{Z}
  \sum_{m,n}
  \frac{
  \langle n|c_i|m\rangle
  \langle m|c_j^\dagger|n\rangle
  \left(e^{-\beta E_n}+e^{-\beta E_m}\right)}
  {z+E_n-E_m}
\end{aligned}
$$

implies that $iG(z)+(iG(z))^\dagger$ is positive semidefinite in the upper half-plane.
Analogous Lehmann representations establish the same structure for the correlated
self-energy and for the cumulant.

As in the scalar case, the problem is mapped to the unit disk. A matrix Caratheodory
function $F$ is related to a matrix Schur function $\Psi$ by the Cayley transform

$$
\Psi(z) = [I-F(z)][I+F(z)]^{-1},
\qquad
F(z) = [I+\Psi(z)]^{-1}[I-\Psi(z)].
$$

For interpolation data $F(z_j)=Y_j$, with transformed Schur values $J_j$, existence is
controlled by a matrix-valued Pick criterion. Equivalently, either of the block matrices

$$
P_C =
\left[
\frac{Y_k+Y_l^\dagger}{1-z_k^*z_l}
\right]_{k,l=1}^n,
\qquad
P_S =
\left[
\frac{I-J_k^\dagger J_l}{1-z_k^*z_l}
\right]_{k,l=1}^n
$$

must be positive semidefinite. When the criterion is satisfied, a matrix Schur recursion
constructs all causal interpolants. The continuation is basis-independent: a unitary
rotation mixes diagonal and off-diagonal entries, but preserves the matrix positivity
structure. This is what makes it possible to continue the full matrix self-energy and then
solve the Dyson equation on the real axis,

$$
\begin{aligned}
G^{-1}(\omega+i0^+)
  &=
  (\omega+i0^+ + \mu)S - F - \Sigma(\omega+i0^+),
\end{aligned}
$$

without first discarding off-diagonal dynamical information.

## Minimal Pole and Prony Continuation

The minimal pole approach uses a different regularizer: compactness of the analytic
structure.[^zhang-prony] It approximates Matsubara data by a small number of poles,

$$
G(z) = \sum_{\ell=1}^{M}\frac{A_\ell}{z-\xi_\ell},
$$

with pole locations $\xi_\ell$ in the lower half-plane and complex weights $A_\ell$. The
number of poles is not fixed a priori. It is chosen as the minimal number needed to
represent the Matsubara data to a target tolerance $\varepsilon$.

The method is based on Prony-type exponential approximation. For uniformly sampled data
$G_k=G(i\omega_{n_0+k\Delta n})$, one seeks

$$
\left|
G_k-\sum_{i=0}^{K-1} w_i \gamma_i^k
\right|
\le \varepsilon
\qquad 0\le k\le 2N.
$$

Classical Prony interpolation is unstable if it tries to pass exactly through every point.
The modern approximation version is regularized by singular value truncation: singular
values below the target precision are discarded, leaving only the significant exponential
modes. This minimum-exponential representation suppresses spurious oscillations and avoids
overfitting.

The scalar minimal-pole procedure starts by approximating the Matsubara data on a finite
imaginary-axis interval by a Prony exponential sum to tolerance $\varepsilon$. It then maps
that interval to the unit circle using the holomorphic transform

$$
w=g(z)=z_s-\sqrt{z_s^2+1},
\qquad
z_s=\frac{z-i\omega_m}{\Delta\omega_h},
$$

with inverse

$$
z=g^{-1}(w)=\frac{\Delta\omega_h}{2}\left(w-\frac{1}{w}\right)+i\omega_m.
$$

Next, compute moments on the unit circle,

$$
h_k =
\frac{1}{2\pi i}
\int_{\partial D} \tilde{G}(w)w^k\,dw,
$$

which, by the residue theorem, satisfy another Prony problem,

$$
h_k = \sum_\ell \tilde{A}_\ell \tilde{\xi}_\ell^k.
$$

Finally, recover the pole positions and weights through the inverse map,

$$
\xi_\ell = g^{-1}(\tilde{\xi}_\ell),
\qquad
A_\ell =
\left.\frac{dz}{dw}\right|_{\tilde{\xi}_\ell}
\tilde{A}_\ell.
$$

Lowering $\varepsilon$ systematically increases the accuracy and, when necessary, the
number of poles. This makes the continuation controllable: the regularization parameter is
the requested accuracy of the Matsubara representation, not a smoothness prior.

The matrix-valued generalization uses shared poles with matrix weights.[^zhang-matrix]
For a response matrix,

$$
\begin{aligned}
\mathbf{G}(z)
  &=
  \sum_{\ell=1}^{M}
  \frac{\mathbf{A}_\ell}{z-\xi_\ell},
\end{aligned}
$$

all orbital components share the same pole locations $\xi_\ell$, while the residues
$\mathbf{A}_\ell$ are matrices. This is essential: independently continuing each matrix
element may destroy the shared analytic structure and the positive-semidefinite constraints
of the full response function.

In practice, the matrix method uses ESPRIT, a robust Prony-like method. Matrix samples are
flattened into vectors and assembled into a block Hankel matrix,

$$
\mathbf{H} =
\begin{pmatrix}
\vec{f}_0 & \vec{f}_1 & \cdots & \vec{f}_L \\
\vec{f}_1 & \vec{f}_2 & \cdots & \vec{f}_{L+1} \\
\vdots    & \vdots    & \ddots & \vdots \\
\vec{f}_{N-L-1} & \vec{f}_{N-L} & \cdots & \vec{f}_{N-1}
\end{pmatrix}.
$$

The singular values of $\mathbf{H}$ determine the number of retained modes $M$: the
smallest $M$ is chosen such that the discarded singular values are below $\varepsilon$.
The shared nodes are then obtained from the rotational-invariance relation in ESPRIT, and
the matrix weights are recovered from an overdetermined Vandermonde system. Optional
constraints can enforce positive semidefinite residues for discrete fermionic spectra or
positive semidefinite spectral matrices on the real axis for continuous spectra.

Minimal-pole continuation is therefore complementary to both MaxEnt and Nevanlinna.
MaxEnt is a fit designed for noisy positive spectra. Nevanlinna and Caratheodory are causal
interpolation methods for high-precision scalar and matrix-valued data. The Prony/minimal
pole approach is an approximation method that regularizes by finding the smallest analytic
pole representation compatible with a prescribed tolerance, and it naturally extends to
off-diagonal, bosonic, anomalous, self-energy, and matrix-valued response functions.

[^levy-maxent]: R. Levy, J. P. F. LeBlanc, and E. Gull, [Implementation of the Maximum Entropy Method for Analytic Continuation](https://arxiv.org/abs/1606.00368).
[^fei-nevanlinna]: J. Fei, C.-N. Yeh, and E. Gull, [Nevanlinna Analytical Continuation](https://arxiv.org/abs/2010.04572).
[^fei-cara]: J. Fei, C.-N. Yeh, D. Zgid, and E. Gull, [Analytical Continuation of Matrix-Valued Functions: Caratheodory Formalism](https://arxiv.org/abs/2107.00788).
[^zhang-prony]: L. Zhang and E. Gull, [Minimal Pole Representation and Controlled Analytic Continuation of Matsubara Response Functions](https://arxiv.org/abs/2312.10576).
[^zhang-matrix]: L. Zhang, Y. Yu, and E. Gull, [Minimal pole representation and analytic continuation of matrix-valued correlation functions](https://arxiv.org/abs/2410.14000).
