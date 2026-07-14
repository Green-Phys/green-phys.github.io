---
title: Green's Functions and Self-Energies
linkTitle: Green's Functions
math: true
weight: 4
---


The previous pages introduced the finite-basis Hamiltonian, mean-field starting points, and numerical bases for imaginary-axis functions.  We now introduce the objects that GF2 and GW actually solve for: the one-particle Green's function $G$ and the self-energy $\Sigma$.  At this stage they should be viewed as general many-body objects, not yet as a particular approximation.

The central idea is simple.  Instead of trying to store the full many-electron wave function, a Green's-function calculation stores the amplitude for adding or removing one electron and letting the interacting many-electron system respond.  This object contains the density matrix, quasiparticle and satellite information, and the ingredients needed for thermodynamic quantities.  The price is that $G$ depends on imaginary time or Matsubara frequency, and interactions enter through the self-energy.

## Statistical Ensemble

Finite-temperature Green's-function theory is formulated in the grand-canonical ensemble.  The statistical weight is built from the Hamiltonian $\hat H$, particle-number operator $\hat N$, chemical potential $\mu$, and inverse temperature $\beta=1/(k_\mathrm{B}T)$:
$$
Z=\mathrm{Tr}\,
e^{-\beta(\hat H-\mu\hat N)} .
$$
The trace is over the many-electron Fock space.  The corresponding expectation value of an operator $\hat O$ is
$$
\langle \hat O\rangle =
\frac{1}{Z}\mathrm{Tr}
\left[
e^{-\beta(\hat H-\mu\hat N)}
\hat O
\right].
$$
The grand potential is
$$
\Omega=-\frac{1}{\beta}\ln Z .
$$
From $\Omega$ one obtains the average particle number, entropy, Helmholtz free energy, and internal energy through
$$
N=-\frac{\partial \Omega}{\partial \mu},
\qquad
S=-\frac{\partial \Omega}{\partial T},
\qquad
F=\Omega+\mu N,
\qquad
E=\Omega+TS+\mu N .
$$
These identities are exact.  The diagrammatic machinery enters when $Z$ or $\Omega$ is evaluated through $G$ and $\Sigma$ rather than through an explicit sum over all many-electron states.[^ThermoGF2016], [^SEETGW2017]

## Imaginary-Time Green's Function

Let $a_p$ destroy an electron in spin-orbital $p$, and let $a_q^\dagger$ create an electron in spin-orbital $q$.  The orbital labels may include spin, momentum, and basis-function indices.  In imaginary time,
$$
a_p(\tau)=
e^{\tau(\hat H-\mu\hat N)}
a_p
e^{-\tau(\hat H-\mu\hat N)} .
$$
The one-particle Green's function is the time-ordered expectation value
$$
G_{pq}(\tau)=
-\langle
T_\tau a_p(\tau)a_q^\dagger(0)
\rangle .
$$
Here $T_\tau$ orders operators along the imaginary-time interval $0\leq\tau\leq\beta$.  For $0<\tau<\beta$, this compact definition is equivalent to the trace form used in fully self-consistent periodic GW calculations.[^NaturalOrbitals2023]

The minus sign is conventional for fermions.  It is chosen so that the noninteracting Green's function has a simple pole structure and so that the density matrix is obtained directly from the equal-time limit.  In an orthonormal spin-orbital basis one commonly writes
$$
\gamma_{pq}=
\langle a_q^\dagger a_p\rangle
=
-G_{pq}(0^-).
$$
In a non-orthogonal atomic-orbital basis the same physical density must be interpreted with the overlap matrix $S$, as described in the Hamiltonian and Hartree-Fock pages.

## Matsubara Frequency

Because fermionic Green's functions are antiperiodic on the imaginary-time interval, they are represented on fermionic Matsubara frequencies
$$
\omega_n=\frac{(2n+1)\pi}{\beta}.
$$
Bosonic response functions, such as polarizations and screened interactions, use bosonic frequencies
$$
\Omega_n=\frac{2n\pi}{\beta}.
$$
The transform between imaginary time and fermionic Matsubara frequency is
$$
G_{pq}(i\omega_n)=
\int_0^\beta d\tau\,
e^{i\omega_n\tau}
G_{pq}(\tau),
$$
with inverse
$$
G_{pq}(\tau)=
\frac{1}{\beta}\sum_n
e^{-i\omega_n\tau}
G_{pq}(i\omega_n).
$$
In practical calculations these transforms are carried out using the compact bases introduced on the previous page, rather than by storing a dense uniform grid.[^YehGW2022]

## Spectral Function

The imaginary-axis Green's function is smooth, but it is connected to real-frequency excitation spectra.  For a fermionic single-particle Green's function, the spectral representation can be written
$$
G(\tau)=
-\int d\omega\,
\frac{e^{-\tau\omega}}
{1+e^{-\beta\omega}}
A(\omega).
$$
Equivalently, on the Matsubara axis,
$$
G(i\omega_n)=
\int d\omega\,
\frac{A(\omega)}
{i\omega_n-\omega}.
$$
For a matrix-valued Green's function, $A(\omega)$ is also a matrix.  The diagonal spectral function measures the distribution of addition and removal energies in a chosen orbital basis.  In periodic calculations this becomes $A^\mathbf{k}(\omega)$, the momentum-resolved spectral function used to extract band gaps and quasiparticle features.[^ShinaokaIR2017], [^YehGW2022]

Analytic continuation is the inverse problem of recovering $A(\omega)$ from values of $G$ on the imaginary axis.  It is numerically delicate because many real-frequency spectra are compatible with almost the same imaginary-axis data.  GF2 and GW therefore perform self-consistency on the imaginary axis and use continuation only afterward for spectra.

## Self-Energy and Dyson Equation

The self-energy $\Sigma$ is the object that turns an independent-particle propagator into the interacting propagator.  The Dyson equation is
$$
G^{-1}(i\omega_n)=
G_0^{-1}(i\omega_n)-\Sigma(i\omega_n).
$$
Here $G_0$ is the Green's function of an auxiliary independent-particle problem.  In a non-orthogonal basis with overlap matrix $S$, a common form is
$$
G_0^{-1}(i\omega_n)=
(i\omega_n+\mu)S-H_0 .
$$
The self-energy contains everything not present in that independent-particle problem: orbital relaxation, screening, exchange beyond the chosen reference, and dynamical correlation effects.[^NaturalOrbitals2023]

It is useful to separate the self-energy into static and dynamical parts,
$$
\Sigma(i\omega_n)=
\Sigma^\infty+\Sigma^\mathrm{dyn}(i\omega_n).
$$
The static term $\Sigma^\infty$ is the Hartree-Fock-like contribution discussed on the previous page.  The dynamical part changes with imaginary time or Matsubara frequency and describes retardation: the many-electron environment does not respond instantaneously when an electron is added or removed.  GF2 and GW differ in how they approximate this dynamical part.

The Dyson equation can also be written as
$$
G=G_0+G_0\Sigma G .
$$
This form emphasizes the physical interpretation: an electron propagates freely, scatters from the many-body medium through $\Sigma$, propagates again, and so on.  The inverse form is the one most often solved numerically.

## Energies from $G$ and $\Sigma$

Once $G$ and $\Sigma$ are known, the electronic energy can be obtained without reconstructing the many-electron wave function.  The one-body contribution is the contraction of the one-electron Hamiltonian with the density matrix,
$$
E_{1\mathrm{b}}=
\mathrm{Tr}[h\gamma].
$$
For solids, this trace includes the Brillouin-zone average over $k$-points.  The two-body contribution is commonly evaluated with the Galitskii-Migdal expression,
$$
E_{2\mathrm{b}}=
\frac{1}{2\beta}
\sum_n
\mathrm{Tr}
\left[
G(i\omega_n)\Sigma(i\omega_n)
\right].
$$
The total electronic energy is then
$$
E=E_{1\mathrm{b}}+E_{2\mathrm{b}}.
$$
With periodic $k$ labels, the trace and Matsubara sum are supplemented by the corresponding $k$-point weights.  The same structure is used in the fully self-consistent periodic GW literature, where the one-body term is written using $h_{pq}^\mathbf{k}\gamma_{pq}^\mathbf{k}$ and the two-body term as a Matsubara sum over $G^\mathbf{k}\Sigma^\mathbf{k}$.[^NaturalOrbitals2023]

## Grand Potential Functional

For conserving approximations, the grand potential can be expressed as a functional of the Green's function.  In the Luttinger-Ward construction,
$$
\Omega[G]=
\frac{1}{\beta}
\left\{
\Phi[G]
-\mathrm{Tr}\ln[-G^{-1}]
-\mathrm{Tr}[\Sigma G]
\right\}.
$$
The functional $\Phi[G]$ is the sum of linked closed skeleton diagrams, and the self-energy is generated from it by functional differentiation.  Approximations such as self-consistent GF2 and self-consistent GW are useful partly because they can be formulated from such a $\Phi$ functional.  This makes particle number, energy, and related conservation laws internally consistent when the equations are solved self-consistently.[^SEETGW2017], [^BaymKadanoff1961]

The role of this page is therefore to define the language.  The Hamiltonian supplies $H_0$, $S$, and the Coulomb integrals.  Hartree-Fock supplies the static term $\Sigma^\infty$ and useful starting density matrices.  The Matsubara basis supplies an efficient representation.  GF2 and GW, introduced next, specify concrete approximations for the dynamical self-energy $\Sigma^\mathrm{dyn}$.

[^ThermoGF2016]: "Exploring connections between statistical mechanics and Green's functions for realistic systems: Temperature dependent electronic entropy and internal energy from a self-consistent second-order Green's function," [J. Chem. Phys. 145, 204106 (2016)](https://doi.org/10.1063/1.4967449).
[^SEETGW2017]: "Testing self-energy embedding theory in combination with GW," [Phys. Rev. B 96, 155106 (2017)](https://doi.org/10.1103/PhysRevB.96.155106).
[^NaturalOrbitals2023]: "Natural orbitals and two-particle correlators as tools for the analysis of effective exchange couplings in solids," [Phys. Chem. Chem. Phys. 25, 21267 (2023)](https://pubs.rsc.org/en/content/articlelanding/2023/cp/d3cp01972d).
[^YehGW2022]: "Fully self-consistent finite-temperature GW in Gaussian Bloch orbitals for solids," [Phys. Rev. B 106, 235104 (2022)](https://doi.org/10.1103/PhysRevB.106.235104).
[^ShinaokaIR2017]: "Compressing Green's function using intermediate representation between imaginary-time and real-frequency domains," [Phys. Rev. B 96, 035147 (2017)](https://doi.org/10.1103/PhysRevB.96.035147).
[^BaymKadanoff1961]: "Conservation Laws and Correlation Functions," [Phys. Rev. 124, 287 (1961)](https://doi.org/10.1103/PhysRev.124.287).
