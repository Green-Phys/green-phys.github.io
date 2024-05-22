---
title: Introduction
linkTitle: Introduction
math: true
weight: 1
---


The main objective for Green Software Package is provide an accurate numerical simulation of realistic quantum systems of interacting electrons beyond density functional theory.
The interactive quantum electron system can usually be described by a Hamiltonian 

$$
\begin{aligned}
H &= \sum_{ij,\sigma} H^0_{ij} c^\dagger_{i\sigma}c_{j\sigma} + \frac{1}{2} \sum_{ijkl,\sigma\sigma'} U_{ijkl} c^\dagger_{i\sigma} c^\dagger_{j\sigma'} c_{l\sigma'}c_{k\sigma}.
\end{aligned}
$$
Depends on type of the system, indices $i,j,k,l$ can correspond to orbital indices (molecular systems) or to combination of lattice site and atom orbital (for solids). With the non-interacting
Hamiltonian
$$
H^0_{ij} = \int d\mathbf{x} \psi^\dagger_i(\mathbf{x})  \left(-\frac{\hbar^2}{2m} \nabla^2_x  - V_{ext} (\mathbf{x})\right)  \psi_j(\mathbf{x}),
$$
describing the motion of electrons in the field of an effectinve potential $V_{ext}(\mathbf{x})$ created by ions, and the electron-electron Coloumb interaction
$$
U_{ijkl} = \int d\mathbf{x_1}d\mathbf{x_2} \psi^\dagger_i(\mathbf{x_1}) \psi_k(\mathbf{x_1}) \frac{1}{|\mathbf{x_1} - \mathbf{x_2} |} \psi^\dagger_j(\mathbf{x_2}) \psi_l(\mathbf{x_2}),
$$
we can describe the quantum many-body problem of interacting electrons. The exact solution of this problem, however, exists only in very limited cases and various approximations have to be applied [^madelung].

We will be looking for a solution of many-body problem in the form of the self-energy, that can be expressed using  the method of Feynman diagrams,
as the sum of all dressed skeleton diagrams [^luttinger]. We can further split the self-energy into two parts:

$$
\Sigma_{ij}(\tau) = \Sigma^\infty_{ij} + \Sigma^c_{ij}(\tau),
$$
where $\Sigma^\infty_{ij}$ corresponds to a static part of the self-energy, and the dynamical part $\Sigma^c_{ij}(\tau)$ is susally called "correlated" self-energy.
If the correlated self-energy is neglected, the solution will correspond to Hartree-Fock approximation [^hartreefock].
Different approximations to the correlated self-energy can then be applied to get the desired level of approximation that will be discussed in next sections.


[^madelung]: Otfried Madelung, [Introduction to Solid-State Theory](https://doi.org/10.1007/978-3-642-61885-7)
[^luttinger]: J. M. Luttinger and J. C. Ward,  [Ground-State Energy of a Many-Fermion System. II](https://doi.org/10.1103/PhysRev.118.1417)
[^hartreefock]: G. D. Mahan, [Many-Particle Physics](https://doi.org/10.1007/978-1-4757-5714-9)
[^rohringer]: Georg Rohringer et al., [Diagrammatic routes to nonlocal correlations beyond dynamical mean field theory](https://doi.org/10.1103/RevModPhys.90.025003)
