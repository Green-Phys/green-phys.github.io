---
title: Introduction
linkTitle: Introduction
math: true
weight: 1
---


The Green Software Package provides tools for the numerical simulation of realistic quantum systems of interacting electrons with finite-temperature Green's function techniques.  The methods implemented in the weak-coupling part of the package, in particular self-consistent GF2 and self-consistent GW, start from the same information that is used in most ab initio electronic-structure calculations: atom positions, nuclear charges or pseudopotentials, a finite one-particle basis, one-electron matrix elements, and two-electron Coulomb integrals.[^YehGW2022], [^PokhilkoYeh2024]

This page introduces that starting point.  The goal is not yet to define Green's functions, self-energies, or Feynman diagrams.  Instead, we first explain the Hamiltonian and the matrices and tensors that represent it.  This is the layer where electronic-structure notation often becomes confusing: physicists may think in terms of fields and lattice sites, quantum chemists in terms of Gaussian orbitals and electron-repulsion integrals, and solid-state calculations in terms of Bloch functions and $k$-points.  Green's function calculations use all of these languages, but the underlying objects are the same.

## From electrons in space to a finite basis

In the Born-Oppenheimer approximation the nuclei are fixed during the electronic calculation.  The electronic Hamiltonian contains a one-electron part and the Coulomb repulsion between pairs of electrons,
$$
\hat H = \hat H_0 + \hat U .
$$

In atomic units, a common non-relativistic form of the one-electron operator is
$$
\hat h_0(\mathbf r)
= -\frac{1}{2}\nabla_{\mathbf r}^2 + v_\mathrm{ext}(\mathbf r),
$$

where the first term is the kinetic energy and $v_\mathrm{ext}$ is the external potential produced by nuclei, pseudopotentials, and possibly other one-body fields.  For an all-electron molecular Hamiltonian, $v_\mathrm{ext}(\mathbf r)=-\sum_A Z_A/|\mathbf r-\mathbf R_A|$.  With pseudopotentials or relativistic one-electron approximations, the detailed expression changes, but it is still represented as a one-body matrix in the chosen basis.[^YehGW2022], [^YehX2CGW2022]

Computers cannot store a wave function as an arbitrary function of continuous coordinates.  We therefore choose a finite set of one-particle basis functions
$$
\{\psi_i^{\mathbf k}(\mathbf r)\}.
$$

The index $i$ labels orbitals inside a unit cell or molecule.  The momentum label $\mathbf k$ is used for periodic solids; for molecules it is omitted.  In Gaussian-orbital calculations for solids, the basis functions are Gaussian Bloch orbitals, constructed by summing localized Gaussian functions over lattice translations with phase factors $e^{i\mathbf k\cdot\mathbf R}$.[^YehGW2022]

The basis functions need not be orthonormal.  Their overlap matrix is
$$
S_{ij}^{\mathbf k}
= \int_\Omega d\mathbf r\,
\psi_i^{\mathbf k *}(\mathbf r)\psi_j^{\mathbf k}(\mathbf r),
$$

where $\Omega$ is the molecular integration domain or, for periodic systems, the unit-cell volume.  If the basis is orthonormal, $S_{ij}^{\mathbf k}=\delta_{ij}$.  Gaussian atomic orbitals are usually non-orthogonal, so the overlap matrix is an essential part of the problem.  It appears explicitly in the matrix form of the non-interacting propagator and in generalized eigenvalue problems.  Alternatively, one can transform to an orthogonal basis, for example by a Lowdin symmetric orthogonalization, but Green's function implementations often keep $S$ explicitly.[^YehGW2022], [^PokhilkoYeh2024]

## One-electron matrix elements

Once a basis is chosen, the one-electron operator becomes a matrix.  In the notation used in recent Green's function implementations,
$$
\left(H_0\right)^{\mathbf k}_{i\sigma,j\sigma'}
= \langle \psi_i^{\mathbf k}\sigma | \hat h_0 | \psi_j^{\mathbf k}\sigma' \rangle .
$$

For a non-relativistic Hamiltonian without magnetic fields or spin-orbit coupling, spin is conserved and this reduces to
$$
\left(H_0\right)^{\mathbf k}_{i\sigma,j\sigma'}
= \delta_{\sigma\sigma'} H^{\mathbf k,0}_{ij},
$$

with
$$
H^{\mathbf k,0}_{ij}
= \int_\Omega d\mathbf r\,
\psi_i^{\mathbf k *}(\mathbf r)
\left[-\frac{1}{2}\nabla_{\mathbf r}^2 + v_\mathrm{ext}(\mathbf r)\right]
\psi_j^{\mathbf k}(\mathbf r).
$$

If spin-orbit coupling or an external magnetic field is included, $H_0$ can contain off-diagonal spin blocks.  Recent relativistic self-consistent GW work in the Zgid group uses exact-two-component one-electron Hamiltonians, where this spin structure is part of the one-electron matrix rather than an afterthought.[^YehX2CGW2022]

The symbol $H_0$ is sometimes replaced by $h$, $t$, or $H^{(0)}$ in the literature.  In older molecular GF2 and SEET papers, the compact second-quantized Hamiltonian is often written with $t_{ij}$ for the one-body term and $v_{ijkl}$ for the Coulomb integral.[^PhillipsZgid2014], [^TranSEETGW2017]  In the Green documentation we use $H_0$ or $H^{(0)}$ for the one-body matrix and $U$ for the two-body Coulomb tensor.

## Two-electron Coulomb integrals

The electron-electron interaction is represented by four-index Coulomb integrals.  Let
$K=(\mathbf k_i,\mathbf k_j,\mathbf k_k,\mathbf k_l)$ collect the momentum labels.  In the chemists' convention used by many ab initio packages and by the Green weak-coupling interface, the integral is $U^K_{ijkl}=\int d\mathbf r_1 d\mathbf r_2\,\rho^{\mathbf k_i\mathbf k_j}_{ij}(\mathbf r_1)|\mathbf r_1-\mathbf r_2|^{-1}\rho^{\mathbf k_k\mathbf k_l}_{kl}(\mathbf r_2)$, where the pair density is $\rho^{\mathbf k_a\mathbf k_b}_{ab}(\mathbf r)=\psi_a^{\mathbf k_a *}(\mathbf r)\psi_b^{\mathbf k_b}(\mathbf r)$.

For molecules the $\mathbf k$ labels are absent.  For crystals, the integral is nonzero only when crystal momentum is conserved,
$$
\mathbf k_i+\mathbf k_k-\mathbf k_j-\mathbf k_l=\mathbf G,
$$

where $\mathbf G$ is a reciprocal lattice vector.[^YehGW2022]

The tensor $U_{ijkl}$ is the bare Coulomb interaction in the finite basis.  "Bare" means that the interaction has not yet been screened by electronic polarization.  GF2 is expanded in powers of these bare Coulomb integrals.  GW instead builds a screened interaction $W$ from the same bare Coulomb input.  The distinction between $U$ and $W$ becomes important later; at the Hamiltonian level, the fundamental two-electron input is $U$.[^PokhilkoYeh2024]

Different communities place the indices in different orders.  The expression above corresponds to the chemists' integral $(ij|kl)$.  Some diagrammatic formulas instead use antisymmetrized integrals, for example $U_{ijkl}-U_{ijlk}$, or use a different ordering of creation and annihilation operators.  These are notation choices, not different Hamiltonians, provided the same convention is used consistently.

## The second-quantized Hamiltonian

The finite-basis Hamiltonian is most compactly written with creation and annihilation operators.  Let
$c^{\mathbf k\dagger}_{i\sigma}$ create an electron in orbital $i$, spin $\sigma$, and momentum $\mathbf k$, and let $c^{\mathbf k}_{i\sigma}$ destroy one.  A general periodic Hamiltonian used in self-consistent GW calculations is[^YehGW2022]
$$
\begin{aligned}
\hat H
&=
\sum_{\mathbf k}\sum_{ij}\sum_{\sigma\sigma'}
\left(H_0\right)^{\mathbf k}_{i\sigma,j\sigma'}
c^{\mathbf k\dagger}_{i\sigma}c^{\mathbf k}_{j\sigma'}
\\
&\quad
+\frac{1}{2N_k}
\sum_{ijkl}
\sum_{\mathbf k_i\mathbf k_j\mathbf k_k\mathbf k_l}
\sum_{\sigma\sigma'}
U^{\mathbf k_i\mathbf k_j\mathbf k_k\mathbf k_l}_{ijkl}
c^{\mathbf k_i\dagger}_{i\sigma}
c^{\mathbf k_k\dagger}_{k\sigma'}
c^{\mathbf k_l}_{l\sigma'}
c^{\mathbf k_j}_{j\sigma}.
\end{aligned}
$$

Here $N_k$ is the number of sampled $k$-points in the Brillouin zone.  The factor $1/2$ avoids double counting electron pairs.  The factor $1/N_k$ is the normalization associated with the reciprocal-space sampling convention.

For a molecule, the momentum labels are omitted.  The one-body part is
$\sum_{ij,\sigma\sigma'}(H_0)_{i\sigma,j\sigma'}c^\dagger_{i\sigma}c_{j\sigma'}$,
and the two-body part is
$\frac{1}{2}\sum_{ijkl,\sigma\sigma'}U_{ijkl}c^\dagger_{i\sigma}c^\dagger_{k\sigma'}c_{l\sigma'}c_{j\sigma}$.

If spin is not mixed by $H_0$, the one-body term becomes diagonal in spin.  Older molecular SEET and GF2 papers often suppress the spin indices and write the same structure as $\hat H=\sum_{ij}t_{ij}a_i^\dagger a_j+\sum_{ijkl}v_{ijkl}a_i^\dagger a_j^\dagger a_l a_k$, where the precise factor of $1/2$ and the ordering of $v_{ijkl}$ are absorbed into the author's convention.[^TranSEETGW2017]  When comparing equations across papers, always check whether the two-electron integrals are bare or antisymmetrized and whether spin orbitals or spatial orbitals are being used.

## Integral decompositions

The four-index tensor $U_{ijkl}$ is expensive to store and manipulate.  If there are $N_\mathrm{orb}$ orbitals, the molecular tensor has $O(N_\mathrm{orb}^4)$ elements, and periodic calculations add momentum indices.  Modern GF2 and GW calculations therefore rarely work directly with the full tensor.  Instead, they use decompositions such as density fitting, Cholesky decomposition, resolution of the identity, or tensor hypercontraction.[^YehGW2022], [^PokhilkoYeh2024]

A common low-rank form is $U^{\mathbf k_i\mathbf k_j\mathbf k_k\mathbf k_l}_{ijkl}=\sum_Q V^{\mathbf k_i\mathbf k_j}_{ij}(Q)V^{\mathbf k_k\mathbf k_l}_{kl}(Q)$, where $Q$ is an auxiliary index.  The matrices $V(Q)$ encode the same Coulomb interaction in a factorized form.  This decomposition is not just a storage trick: it changes the practical scaling of GW and GF2 algorithms and is one of the reasons fully self-consistent calculations on realistic molecules and solids have become feasible.[^YehGW2022], [^PokhilkoYeh2024]

## What the Hamiltonian data mean physically

The one-electron matrix $H_0$ tells us how a single electron moves through the external potential and between basis functions.  Its diagonal elements are roughly orbital energies in the chosen basis, while its off-diagonal elements describe hopping, hybridization, and spin mixing.  The overlap matrix $S$ tells us that the basis functions themselves are not necessarily independent unit vectors.  The Coulomb tensor $U$ tells us how the charge distribution associated with one pair of basis functions interacts with the charge distribution associated with another pair.

These objects are not yet a many-electron solution.  They are the finite-basis definition of the problem.  Hartree-Fock, density functional theory, GF2, GW, coupled cluster, configuration interaction, and embedding theories can all start from essentially the same $H_0$, $S$, and $U$, then make different approximations to solve the interacting-electron problem.[^SimonsBenchmark2017]

Green's function methods proceed by replacing a direct many-electron wave function with one-particle propagation and interaction effects encoded in frequency- or time-dependent quantities.  The next theory pages introduce the imaginary-time and Matsubara-frequency Green's functions, the Dyson equation, and the self-energy approximations used in GF2 and GW.

[^SzaboOstlund]: Attila Szabo and Neil S. Ostlund, [Modern Quantum Chemistry: Introduction to Advanced Electronic Structure Theory](https://store.doverpublications.com/products/9780486691862).
[^Mattuck]: Richard D. Mattuck, [A Guide to Feynman Diagrams in the Many-Body Problem](https://store.doverpublications.com/products/9780486670478).
[^Mahan]: Gerald D. Mahan, [Many-Particle Physics](https://link.springer.com/book/10.1007/978-1-4757-5714-9).
[^Coleman]: Piers Coleman, [Introduction to Many-Body Physics](https://www.cambridge.org/core/books/introduction-to-manybody-physics/B7598FC1FCEE0285F5EC767E835854C8).
[^NegeleOrland]: John Negele and Henri Orland, [Quantum Many-Particle Systems](https://www.amazon.com/Quantum-Many-particle-Systems-Frontiers-Physics/dp/0738200522).
[^KadanoffBaym]: Leo P. Kadanoff and Gordon Baym, [Quantum Statistical Mechanics](https://www.taylorfrancis.com/books/mono/10.1201/9780429493218/quantum-statistical-mechanics-leo-kadanoff).
[^AbrikosovGorkovDzyaloshinski]: A. A. Abrikosov, L. P. Gorkov, and I. E. Dzyaloshinski, [Methods of Quantum Field Theory in Statistical Physics](https://books.google.com/books/about/Methods_of_Quantum_Field_Theory_in_Stati.html).
[^Stefanucci]: Gianluca Stefanucci and Robert van Leeuwen, [Nonequilibrium Many-Body Theory of Quantum Systems](https://www.cambridge.org/core/books/nonequilibrium-many-body-theory-of-quantum-systems/DAD3F31F4304C2853879CEDC71DA7884).
[^YehGW2022]: Chia-Nan Yeh, Sergei Iskakov, Dominika Zgid, and Emanuel Gull, "Fully self-consistent finite-temperature GW in Gaussian Bloch orbitals for solids," [Phys. Rev. B 106, 235104 (2022)](https://doi.org/10.1103/PhysRevB.106.235104).
[^YehX2CGW2022]: Chia-Nan Yeh, Avijit Shee, Qiming Sun, Emanuel Gull, and Dominika Zgid, "Relativistic self-consistent GW: Exact two-component formalism with one-electron approximation for solids," [Phys. Rev. B 106, 085121 (2022)](https://doi.org/10.1103/PhysRevB.106.085121).
[^PokhilkoYeh2024]: Pavel Pokhilko, Chia-Nan Yeh, Miguel A. Morales, and Dominika Zgid, "Tensor hypercontraction for fully self-consistent imaginary-time GF2 and GWSOX methods: Theory, implementation, and role of the Green's function second-order exchange for intermolecular interactions," [J. Chem. Phys. 161, 084108 (2024)](https://doi.org/10.1063/5.0215954).
[^PhillipsZgid2014]: Jordan J. Phillips and Dominika Zgid, "Communication: The description of strong correlation within self-consistent Green's function second-order perturbation theory," [J. Chem. Phys. 140, 241101 (2014)](https://doi.org/10.1063/1.4884951).
[^TranSEETGW2017]: Tran Nguyen Lan, Avijit Shee, Jia Li, Emanuel Gull, and Dominika Zgid, "Testing self-energy embedding theory in combination with GW," [Phys. Rev. B 96, 155106 (2017)](https://doi.org/10.1103/PhysRevB.96.155106).
[^SimonsBenchmark2017]: Mario Motta et al., "Towards the solution of the many-electron problem in real materials: Equation of state of the hydrogen chain with state-of-the-art many-body methods," [Phys. Rev. X 7, 031059 (2017)](https://doi.org/10.1103/PhysRevX.7.031059).
