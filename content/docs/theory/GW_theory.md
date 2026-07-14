---
title: The GW Approximation
linkTitle: GW approximation
math: true
weight: 6
next: "/docs/theory/postprocessing"
---


The $GW$ approximation is a fully self-consistent Green's-function method in which the dynamical self-energy is built from the interacting one-particle Green's function $G$ and a screened Coulomb interaction $W$.  Green/WeakCoupling implements the finite-temperature, imaginary-axis, non-relativistic Gaussian Bloch-orbital formulation described in Ref. [^YehGW2022].  The calculation does not use a quasiparticle approximation during the self-consistency loop, and all matrix elements of the self-energy are evaluated on the Matsubara axis.[^YehGW2022]

The physical idea is different from GF2.  GF2 expands the self-energy through second order in the bare Coulomb interaction.  $GW$ instead keeps the self-energy first order in a screened interaction $W$, where $W$ itself contains an infinite random-phase-approximation-like series of polarization bubbles.  This screening is essential for extended systems, especially when bare-interaction perturbation theory is poorly behaved.[^Hedin1965][^YehGW2022]

## Dyson Equation

In the non-relativistic periodic notation of Ref. [^YehGW2022], the interacting Green's function satisfies
$$
\left[G^{\mathbf{k}}(i\omega_n)\right]^{-1}
{}=
(i\omega_n+\mu)S^{\mathbf{k}}
-H_0^{\mathbf{k}}
-\Sigma^{\mathbf{k}}(i\omega_n).
$$
Here $S^{\mathbf{k}}$ is the overlap matrix, $H_0^{\mathbf{k}}$ is the one-electron Hamiltonian, $\mu$ is the chemical potential, and $\omega_n=(2n+1)\pi/\beta$ is a fermionic Matsubara frequency.  The inverse is a matrix inverse in the orbital and spin space at fixed $\mathbf{k}$ and $i\omega_n$.

The $GW$ self-energy is split into static and dynamical pieces,
$$
\Sigma^{GW,\mathbf{k}}(i\omega_n)
{}=
\Sigma^{GW,\mathbf{k}}_\infty
+
\tilde{\Sigma}^{GW,\mathbf{k}}(i\omega_n).
$$
The static part is the Hartree-Fock self-energy built from the current correlated density matrix.  In the notation of Ref. [^YehGW2022], it is the sum of a Hartree term $J$ and an exchange term $K$,
$$
\left(\Sigma^{GW}_\infty\right)^{\mathbf{k}}_{i\sigma,j\sigma}
{}=
J^{\mathbf{k}}_{i\sigma,j\sigma}
+
K^{\mathbf{k}}_{i\sigma,j\sigma}.
$$
The new approximation specific to $GW$ is the dynamical part $\tilde{\Sigma}^{GW}$.

## Screened Interaction

The screened interaction $W$ is the Coulomb interaction dressed by repeated particle-hole polarization bubbles.  In four-index notation, the formal equation has the Dyson-like structure
$$
W(i\Omega_n)=
U+
U\Pi(i\Omega_n)W(i\Omega_n),
$$
where $U$ is the bare Coulomb interaction, $\Pi$ is the polarization, and $\Omega_n=2n\pi/\beta$ is a bosonic Matsubara frequency.  This compact expression hides orbital and momentum sums, but it is the same equation written explicitly in Ref. [^YehGW2022].

The corresponding polarization bubble in imaginary time is built from two interacting Green's functions,
$$
\Pi(\tau)\sim
\sum_\sigma
G_\sigma(\tau)G_\sigma(-\tau).
$$
This is why self-consistent $GW$ is nonlinear: $G$ determines $\Pi$, $\Pi$ determines $W$, $W$ determines $\Sigma$, and $\Sigma$ determines a new $G$ through the Dyson equation.

## Density-Fitted Form

In Green/WeakCoupling, the four-index Coulomb tensor is represented by density-fitted three-index vertices
$$
U^{\mathbf{k}_1\mathbf{k}_2\mathbf{k}_3\mathbf{k}_4}_{ijkl}
{}=
\sum_Q
V^{\mathbf{k}_1\mathbf{k}_2}_{ij}(Q)
V^{\mathbf{k}_3\mathbf{k}_4}_{kl}(Q).
$$
This is the practical form used in the non-relativistic Yeh implementation.  It reduces memory and turns the screened-interaction problem into operations in the auxiliary basis indexed by $Q$.[^YehGW2022]

For a momentum transfer $\mathbf{q}$, define the noninteracting auxiliary polarization $\tilde{P}_0^{\mathbf{q}}$.  In imaginary time,
$$
\tilde{P}^{\mathbf{q}}_{0,QQ'}(\tau)=
-\frac{1}{N_k}
\sum_{\mathbf{k}}
\sum_{\sigma s}
\sum_{abcd}
V^{\mathbf{k},\mathbf{k+q}}_{da}(Q)
G^{\mathbf{k}}_{cs,d\sigma}(-\tau)
G^{\mathbf{k+q}}_{a\sigma,bs}(\tau)
V^{\mathbf{k+q},\mathbf{k}}_{bc}(Q').
$$
The bosonic Matsubara transform is
$$
\tilde{P}^{\mathbf{q}}_{0,QQ'}(i\Omega_n)
{}=
\int_0^\beta d\tau\,
\tilde{P}^{\mathbf{q}}_{0,QQ'}(\tau)
e^{i\Omega_n\tau}.
$$

The RPA bubble series is then summed in the auxiliary basis:
$$
\tilde{P}^{\mathbf{q}}(i\Omega_n)
{}=
\left[I-\tilde{P}^{\mathbf{q}}_0(i\Omega_n)\right]^{-1}
\tilde{P}^{\mathbf{q}}_0(i\Omega_n).
$$
This $\tilde{P}$ is the renormalized auxiliary quantity that contains the repeated bubble insertions.  In the Yeh notation it generates the effective screened interaction $\tilde{W}=W-U$,
$$
\tilde{W}^{\mathbf{k},\mathbf{k-q},\mathbf{k-q},\mathbf{k}}_{iajb}
{}=
\sum_{QQ'}
V^{\mathbf{k},\mathbf{k-q}}_{ia}(Q)
\tilde{P}^{\mathbf{q}}_{QQ'}
V^{\mathbf{k-q},\mathbf{k}}_{bj}(Q').
$$
The frequency or time argument is inherited from $\tilde{P}$.

## Dynamical Self-Energy

Using the effective screened interaction, the imaginary-time $GW$ self-energy is
$$
\tilde{\Sigma}^{GW,\mathbf{k}}_{i\sigma,j\sigma}(\tau)
{}=
-\frac{1}{N_k}
\sum_{\mathbf{q}}
\sum_{ab}
G^{\mathbf{k-q}}_{a\sigma,b\sigma}(\tau)
\tilde{W}^{\mathbf{k},\mathbf{k-q},\mathbf{k-q},\mathbf{k}}_{iajb}(\tau).
$$
Substituting the density-fitted expression for $\tilde{W}$ gives the implementation form
$$
\tilde{\Sigma}^{GW,\mathbf{k}}_{i\sigma,j\sigma}(\tau)
{}=
-\frac{1}{N_k}
\sum_{\mathbf{q}}
\sum_{ab}
\sum_{QQ'}
G^{\mathbf{k-q}}_{a\sigma,b\sigma}(\tau)
V^{\mathbf{k},\mathbf{k-q}}_{ia}(Q)
\tilde{P}^{\mathbf{q}}_{QQ'}(\tau)
V^{\mathbf{k-q},\mathbf{k}}_{bj}(Q').
$$
This is the central $GW$ equation used in the non-relativistic Green/WeakCoupling implementation.[^YehGW2022]

## Self-Consistency Loop

A self-consistent $GW$ iteration follows the structure below.

1.  Start from a Green's function, usually from HF, DFT, or the noninteracting Hamiltonian.
2.  Build the correlated density matrix and the static Hartree-Fock self-energy $\Sigma_\infty^{GW}$.
3.  Build $\tilde{P}_0$ from the current $G$.
4.  Solve the auxiliary-basis RPA equation for $\tilde{P}$.
5.  Construct $\tilde{\Sigma}^{GW}(\tau)$ and transform it to Matsubara frequency.
6.  Adjust $\mu$ to obtain the target electron number.
7.  Solve the Dyson equation for a new $G$.
8.  Iterate until $G$, $\Sigma$, the energy, and the chemical potential are converged.

The key point is that the same interacting $G$ is used everywhere in the loop.  This makes the method conserving and thermodynamically consistent when solved to self-consistency.[^BaymKadanoff1961][^YehGW2022]

## Relation to Spectra

The calculation is performed entirely on the imaginary axis.  After convergence, real-frequency information is obtained by analytic continuation of the Matsubara Green's function.  Ref. [^YehGW2022] uses the relation
$$
G^{\mathbf{k}}_{i\sigma,j\sigma'}(i\omega_n)
{}=
\int d\omega\,
\frac{
A^{\mathbf{k}}_{i\sigma,j\sigma'}(\omega)
}{
i\omega_n-\omega
}.
$$
Because the Gaussian atomic-orbital basis is non-orthogonal, the Green's function is transformed to an orthonormal basis before extracting normalized diagonal spectral functions.[^YehGW2022]

## What GW Omits

Fully self-consistent $GW$ contains infinitely many bubble-screening diagrams through $W$, but it omits vertex corrections in both the self-energy and the polarization.  This is the main formal reason why self-consistent $GW$ can still deviate from exact results even after removing starting-point dependence.  Later vertex-corrected methods add diagrams beyond this approximation.

[^YehGW2022]: "Fully self-consistent finite-temperature GW in Gaussian Bloch orbitals for solids," [Phys. Rev. B 106, 235104 (2022)](https://doi.org/10.1103/PhysRevB.106.235104).
[^Hedin1965]: "New Method for Calculating the One-Particle Green's Function with Application to the Electron-Gas Problem," [Phys. Rev. 139, A796 (1965)](https://doi.org/10.1103/PhysRev.139.A796).
[^BaymKadanoff1961]: "Conservation Laws and Correlation Functions," [Phys. Rev. 124, 287 (1961)](https://doi.org/10.1103/PhysRev.124.287).
