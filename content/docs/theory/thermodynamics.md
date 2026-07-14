---
title: Thermodynamics
weight: 8
math: true
prev: "/docs/theory/analytical_continuation"
next: "/docs/theory/convergence_acceleration"
aliases:
  - /docs/theory/postprocessing/thermodynamics/
---

Finite-temperature Green's functions are useful because the same self-consistent calculation that gives the density matrix, self-energy, and spectra also gives access to electronic thermodynamics. This is especially important for metals, small-gap materials, and competing phases where the electronic entropy or Helmholtz free energy can decide which solution is thermodynamically stable.[^rusakov16]

The calculation is performed in the grand canonical ensemble, with inverse temperature $\beta=1/(k_B T)$ and chemical potential $\mu$. The basic object is the Matsubara Green's function $G(i\omega_n)$, where $\omega_n=(2n+1)\pi/\beta$ for fermions. The density matrix is obtained from the equal-time limit of $G$, and the particle number is

$$
N = \mathrm{Tr}_{1}\{\gamma S\},
$$

where $S$ is the one-particle overlap matrix and $\mathrm{Tr}_{1}$ denotes the trace over one-particle indices, including spin, orbital, and crystal momentum when present.

## Dyson equation and self-energy split

In an atomic-orbital or Bloch-orbital basis, the interacting Green's function is obtained from the Dyson equation

$$
G^{-1}(i\omega_n) = (i\omega_n+\mu)S - H_0 - \Sigma(i\omega_n).
$$

It is useful to separate the self-energy into a static Hartree-Fock part and a dynamic correlation part,

$$
\Sigma(i\omega_n) = \Sigma^\infty + \Sigma^c(i\omega_n),
$$

and define the Fock matrix $F=H_0+\Sigma^\infty$. Then

$$
G^{-1}(i\omega_n) = G_{HF}^{-1}(i\omega_n) - \Sigma^c(i\omega_n),
\qquad
G_{HF}^{-1}(i\omega_n) = (i\omega_n+\mu)S-F.
$$

This split matters for thermodynamics because the logarithm in the grand potential converges slowly if it is evaluated directly from $G^{-1}$. Using

$$
G^{-1}=G_{HF}^{-1}\left(1-G_{HF}\Sigma^c\right),
$$

one evaluates the logarithmic contribution as

$$
\mathrm{Tr}\ln[-G^{-1}] =
\mathrm{Tr}\ln[-G_{HF}^{-1}]
+\mathrm{Tr}\ln[1-G_{HF}\Sigma^c].
$$

The first term is a finite-temperature one-particle expression, while the second contains the decaying correlation correction. The self-energy in the second logarithm is the dynamic part $\Sigma^c$, not the full $\Sigma$.

## Luttinger-Ward functional

For a conserving, self-consistent approximation, the grand potential is written in terms of the Luttinger-Ward $\Phi$ functional as[^Luttinger60][^dahlen06][^yeh22]

$$
\Omega[G] =
\frac{1}{\beta}
\left(
\Phi[G]
-\mathrm{Tr}\ln[-G^{-1}]
-\mathrm{Tr}\{\Sigma[G]G\}
\right).
$$

Here $\mathrm{Tr}$ denotes the full Matsubara and one-particle trace in the convention used for $\Phi$ and $\Sigma G$. Some papers absorb the factor $1/\beta$ into the definition of $\mathrm{Tr}$; the formula above keeps it explicit.

The functional $\Phi[G]$ is the sum of closed, linked skeleton diagrams. Its key property is

$$
\beta\frac{\delta \Phi[G]}{\delta G} = \Sigma[G],
$$

up to the same trace convention. As a consequence, $\Omega[G]$ is stationary at a self-consistent solution of the Dyson equation. This stationarity is the reason $\Phi$-derivable approximations such as self-consistent GF2 and self-consistent GW are conserving and thermodynamically consistent.[^lan17]

For a two-body interaction, the skeleton expansion may be written as

$$
\Phi[G] = \sum_{m=1}^{\infty}\Phi^{(m)}[G],
\qquad
\Phi^{(m)}[G]=\frac{1}{2m}\mathrm{Tr}\{\Sigma^{(m)}[G]G\}.
$$

This identity is especially convenient in perturbative approximations because the same self-energy diagrams used in the Dyson equation determine the thermodynamic functional.

## Thermodynamic quantities

Once $\Omega$ is known, the grand partition function is

$$
\Omega=-\frac{1}{\beta}\ln Z_{GC}.
$$

The Helmholtz free energy, internal energy, entropy, and specific heat are related by

$$
A=\Omega+\mu N,
\qquad
\Omega=E-TS-\mu N,
$$

so that

$$
S=\frac{E-\Omega-\mu N}{T}.
$$

Equivalently, at fixed external parameters one may use derivative definitions such as

$$
N=-\left(\frac{\partial \Omega}{\partial \mu}\right)_T,
\qquad
S=-\left(\frac{\partial \Omega}{\partial T}\right)_\mu,
\qquad
E=\frac{\partial(\beta\Omega)}{\partial\beta}+\mu N.
$$

For fixed particle number, the electronic heat capacity is

$$
C_V=\left(\frac{\partial E}{\partial T}\right)_V
=T\left(\frac{\partial S}{\partial T}\right)_V.
$$

The internal energy is commonly evaluated from the finite-temperature Galitskii-Migdal expression. With the static self-energy included in $F$ and the dynamic part denoted by $\Sigma^c$, the molecular form used in the GF2 thermodynamics paper is[^rusakov16][^galitskii]

$$
E =
\frac{1}{2}\mathrm{Tr}_{1}\{(h+F)\gamma\}
+\frac{2}{\beta}\sum_{n}^{N_\omega}
\mathrm{Re}\,\mathrm{Tr}_{1}\{G(i\omega_n)\Sigma^c(i\omega_n)\}.
$$

For periodic systems, the one-particle trace is supplemented by the Brillouin-zone average. In a fully self-consistent $\Phi$-derivable calculation, evaluating $E$ by this formula, by thermodynamic integration, or by derivatives of $\Omega$ gives the same result within numerical accuracy.[^yeh22]

## GF2 grand potential

In self-consistent second-order perturbation theory (GF2), the self-energy is

$$
\Sigma^{GF2}(i\omega_n)=\Sigma^\infty+\Sigma^{(2)}(i\omega_n),
$$

where $\Sigma^{(2)}$ is built from the fully interacting $G$. The corresponding truncated $\Phi$ functional is

$$
\Phi^{GF2}[G]
=\frac{1}{2}\mathrm{Tr}_{1}\{\Sigma^\infty\gamma\}
+\frac{1}{4}\mathrm{Tr}\{\Sigma^{(2)}G\}.
$$

The self-energy trace separates in the same way,

$$
\mathrm{Tr}\{\Sigma^{GF2}G\}
=\mathrm{Tr}_{1}\{\Sigma^\infty\gamma\}
+\mathrm{Tr}\{\Sigma^{(2)}G\}.
$$

Combining these identities with the logarithmic split gives

$$
\Omega^{GF2} =
\frac{1}{\beta}
\left(
-\frac{1}{2}\mathrm{Tr}_{1}\{\Sigma^\infty\gamma\}
-\frac{3}{4}\mathrm{Tr}\{\Sigma^{(2)}G\}
-\mathrm{Tr}\ln[-G_{HF}^{-1}]
-\mathrm{Tr}\ln[1-G_{HF}\Sigma^{(2)}]
\right).
$$

This form is the practical GF2 expression: the static Hartree-Fock contribution, the dynamic second-order contribution, and the two logarithmic terms are evaluated from the converged Green's function and self-energy.

## GW grand potential

Self-consistent GW is also $\Phi$-derivable. Its self-energy is split as

$$
\Sigma^{GW}(i\omega_n)=\Sigma^\infty+\widetilde{\Sigma}^{GW}(i\omega_n),
$$

where $\widetilde{\Sigma}^{GW}$ is generated by the screened interaction $W$ or, equivalently, by the RPA bubble series. In the Gaussian-density-fitting formulation used in the finite-temperature scGW paper, the dynamic part of the GW $\Phi$ functional can be written in terms of the auxiliary polarization matrix $\widetilde{P}_0^{q}(i\Omega_n)$ as[^yeh22]

$$
\widetilde{\Phi}_{GW}
=\frac{1}{2N_k}\sum_q\frac{1}{\beta}\sum_n
\mathrm{tr}\left\{
\ln\left[I-\widetilde{P}_0^q(i\Omega_n)\right]
+\widetilde{P}_0^q(i\Omega_n)
\right\}.
$$

The logarithm is a matrix logarithm before the auxiliary-space trace is taken. Expanding it gives the bubble series with the first-order term removed:

$$
\ln(I-X)+X
=-\frac{1}{2}X^2-\frac{1}{3}X^3-\cdots.
$$

The full GW functional is then

$$
\Phi_{GW}[G]
=\Phi_\infty^{GW}+\widetilde{\Phi}_{GW},
\qquad
\Phi_\infty^{GW}
=-\frac{1}{2}\mathrm{Tr}_{1}\{\Sigma^\infty\gamma\},
$$

with the sign following the scGW convention used for the periodic implementation. Inserting $\Phi_{GW}$ and $\Sigma^{GW}$ into the same Luttinger-Ward expression for $\Omega[G]$ defines the GW grand potential. The thermodynamic quantities $A$, $E$, $S$, and $C_V$ are then obtained from the identities above.

The practical lesson is the same for GF2 and GW: thermodynamic quantities should be evaluated from the self-consistent Green's function and the $\Phi$ functional belonging to the same approximation. Mixing a self-energy from one approximation with a thermodynamic functional from another generally destroys the stationarity and consistency that make the calculation useful.

[^Luttinger60]: J. M. Luttinger and J. C. Ward, [Ground-State Energy of a Many-Fermion System. II](https://doi.org/10.1103/PhysRev.118.1417).
[^dahlen06]: N. E. Dahlen, R. van Leeuwen, and U. von Barth, [Variational energy functionals of the Green function and of the density tested on molecules](https://doi.org/10.1103/PhysRevA.73.012511).
[^galitskii]: B. Holm and F. Aryasetiawan, [Total energy from the Galitskii-Migdal formula using realistic spectral functions](https://doi.org/10.1103/PhysRevB.62.4858).
[^rusakov16]: A. A. Rusakov, S. Iskakov, L. N. Tran, and D. Zgid, [Exploring connections between statistical mechanics and Green's functions for realistic systems](https://arxiv.org/abs/1605.06563).
[^lan17]: T. N. Lan, A. Shee, J. Li, E. Gull, and D. Zgid, [Testing self-energy embedding theory in combination with GW](https://arxiv.org/abs/1706.05774).
[^yeh22]: C.-N. Yeh, S. Iskakov, D. Zgid, and E. Gull, [Fully self-consistent finite-temperature GW in Gaussian Bloch orbitals for solids](https://doi.org/10.1103/PhysRevB.106.235104).
