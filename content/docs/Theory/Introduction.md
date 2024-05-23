---
title: Introduction
linkTitle: Introduction
math: true
weight: 1
---


The Green Software Package aims to provide tools for the accurate numerical simulation of realistic quantum systems of interacting electrons with Green's function techniques.

An introduction to the theory of Green's functions and the numerical implementation of Green's function methods is available in textbooks and review articles. The following
is a small overview of textbooks that we found useful. An elementary introduction to electronic structure techniques is given by [^SzaboOstlund]. A good first view of diagrammatic
Green's function methods is presented in [^Mattuck]. More extensive derivation can be found in the condensed matter field theory textbooks of [^Mahan], [^Coleman], and [^NegeleOrland],
and [^KadanoffBaym] as well as [^AbrikosovGorkovDzyaloshinski] give expert information. For mathematical and non-equilibrium aspects, [^Stefanucci] is useful.

Most of Green considers a variant of the following problem: Find the properties of an interacting quantum system described by a Hamiltonian  of the form
$$
\begin{aligned}
H &= \sum_{ij,\sigma} H^0_{ij} c^\dagger_{i\sigma}c_{j\sigma} + \frac{1}{2} \sum_{ijkl,\sigma\sigma'} U_{ijkl} c^\dagger_{i\sigma} c^\dagger_{k\sigma'} c_{l\sigma'}c_{j\sigma}.
\end{aligned}
$$
Here, the indices $i,j,k,l$ may correspond indices of atomic orbials or to a combination of lattice site indices and atomic orbitals.[^SzaboOstlund] The one-body
Hamiltonian $H^0_{ij}$, in the simplest case, is defined as
$$
H^0_{ij} = \int d\mathbf{x} \psi^\dagger_i(\mathbf{x})  \left(-\frac{\hbar^2}{2m} \nabla^2_x  - V_{ext} (\mathbf{x})\right)  \psi_j(\mathbf{x}),
$$
and describes the motion of electrons in the field of an external potential $V_{ext}(\mathbf{x})$.
The electron-electron Coloumb repulsion is 
$$
U_{ijkl} = \int d\mathbf{x_1}d\mathbf{x_2} \psi^\dagger_i(\mathbf{x_1}) \psi_j(\mathbf{x_1}) \frac{1}{|\mathbf{x_1} - \mathbf{x_2} |} \psi^\dagger_k(\mathbf{x_2}) \psi_l(\mathbf{x_2}).
$$

Green solves problems of this type in a Green's function language where the main objects are electron Green's functions and electron self-energies expressed in terms of Feynman diagrams.[^Mattuck]

It is often convenient to split the self-energy into static and a time-dependent parts:
$$
\Sigma_{ij}(\tau) = \Sigma^\infty_{ij} + \Sigma^c_{ij}(\tau).
$$
Here $\Sigma^\infty_{ij}$ corresponds to a static, i.e. time- or frequency-independent component of the self-energy, and the dynamical part $\Sigma^c_{ij}(\tau)$ encapsulates the time dependence (the notation $\Sigma^\infty_{ij}$ refers to the infinite frequency limit of the self-energy).

The solution of Hartree-Fock equations leads only to a static self-energy and can be understood asd the lowest-order approximation of diagrammatic perturbation theory. Higher order approximations yield dynamical self-energies in addition. Both GW and GF2 are such higher order approximations.

[^SzaboOstlund]: Attila Szabo and Neil S. Ostlund, [Modern Quantum Chemistry: Introduction to Advanced Electronic Structure Theory](https://store.doverpublications.com/products/9780486691862)
[^Mattuck]: Richard D. Mattuck, [A Guide to Feynman Diagrams in the Many-Body Problem](https://store.doverpublications.com/products/9780486670478)
[^Mahan]: Gerald D. Mahan, [Many-Particle Physics](https://link.springer.com/book/10.1007/978-1-4757-5714-9).
[^Coleman]: Piers Coleman, [Introduction to Many-Body Physics](https://www.cambridge.org/core/books/introduction-to-manybody-physics/B7598FC1FCEE0285F5EC767E835854C8).
[^NegeleOrland]: John Negele and Henri Orland, [Quantum Many-Particle Systems](https://www.amazon.com/Quantum-Many-particle-Systems-Frontiers-Physics/dp/0738200522).
[^KadanoffBaym]: Leo P. Kadanoff and Gordon Baym, [Quantum Statistical Mechanics](https://www.taylorfrancis.com/books/mono/10.1201/9780429493218/quantum-statistical-mechanics-leo-kadanoff).
[^AbrikosovGorkovDzyaloshinski]: A.A. Abrikosov, L.P. Gorkov, I.E. Dzyaloshinski, [Methods of Quantum Field Theory in Statistical Physics](https://books.google.com/books/about/Methods_of_Quantum_Field_Theory_in_Stati.html).
[^Stefanucci]: Gianluca Stefanucci and Robert van Leeuwen, [Nonequilibrium Many-Body Theory of Quantum Systems](https://www.cambridge.org/core/books/nonequilibrium-manybody-theory-of-quantum-systems/DAD3F31F4304C2853879CEDC71DA7884).
