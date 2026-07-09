---
title: Counterterm Solver
linkTitle: Counterterm
permalink: /Counterterm_Solver/
---

The counterterm solver is a hybrid Hamiltonian-diagrammatic quantum impurity solver. Hamiltonian-based
approaches, which rely on an explicit bath discretization, are typically limited to a small number of bath
sites or small entanglement, while diagrammatic methods suffer from sign problems, slow convergence, or
diagram truncation approximations. The counterterm solver combines the two: augmenting a diagrammatic
expansion with a small auxiliary bath (the "counterterms") reduces the residual problem to a regime where
low-order perturbation theory is highly accurate and rapidly converging.

The method is described in:

Yang Yu, Gaurav Harsha, Lei Zhang, Agnieszka Jażdżewska, Dominika Zgid, Xinyang Dong, Emanuel Gull,
["Hybrid Hamiltonian-diagrammatic quantum impurity solver"](https://arxiv.org/abs/2606.11095),
arXiv:2606.11095 (2026).

In a simple benchmark, the precision of the hybrid approach surpasses bold-line calculations by several
orders of magnitude; for a strongly interacting two-orbital model with a severe sign problem, convergence
is achieved at three orders of magnitude lower computational cost than competing methods; and convergence
to the unknown exact result is rapidly accelerated in a difficult realistic problem.

To get started, head to the repository at
[green-jl-counterterms](https://github.com/Green-Phys/green-jl-counterterms) and follow the instructions
there.

A video tutorial is in preparation.
