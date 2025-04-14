---
title: Embedding Theory
linkTitle: Embedding Theory
weight: 4
math: true
hidden: false
---

## Introduction

We study the periodic many-body problem defined by the Hamiltonian

{{< raw >}}
$$
H = \sum_{\boldsymbol{ij},\sigma}h^{0}_{\boldsymbol{ij}}c^{\dag}_{\boldsymbol{i}\sigma}c_{\boldsymbol{j}\sigma} + \frac{1}{2}\sum_{\boldsymbol{ijkl},\sigma\sigma'}v_{\boldsymbol{ijkl}}c^{\dag}_{\boldsymbol{i}\sigma}c^{\dag}_{\boldsymbol{k}\sigma'}c_{\boldsymbol{l}\sigma'}c_{\boldsymbol{j}\sigma}
$$
{{< /raw >}}

Exact solution for this Hamiltonian in general is not possible. One of the common approach is based on the fact that only small part of the whole system exhibits
strong electron correlation effect. This allows to create various embedding schemes, where strongly correlated orbitals are embedded into a self-consistently
adjuested dynamical environment, while the rest of the system solved approximately with weak-coupling method.

In `Green` we employ Self-energy embedding framework (SEET) [^seet] as embedding method. SEET includes non-perturbative corrections to the weak-coupling self-energy diagrams 
within subsets of potentially strongly correlated orbitals. In contrast to other embedding methods, SEET allows to choose multiple disjoint subsets $M$ 
of potentially strongly correlated orbitals, labeled by $A_1\dots,A_M$. One of the natural choice is groups of local orbitals close to the Fermi energy $E_{F}$.


The SEET correction to the total self-energy is
{{< raw >}}
$$
\begin{align}
(\Sigma^{\text{SEET}})^{\bold{k}}_{ij} &=(\Sigma^{\text{weak}})^{\bold{k}}_{ij} + \sum_{\lambda=1}^M\big[(\Sigma^{\text{non-pert}}_{A_\lambda})_{ij} - (\Sigma^{\text{DC}}_{A_\lambda})_{ij}\big]\delta_{(ij)\in A_\lambda},
\end{align}
$$
{{< /raw >}}
where $(\Sigma^{\text{weak}})^{\bold{k}}$ is the Self-energy obtained from the weak-coupling solution of the entire system, $(\Sigma^{\text{non-pert}}\_{A_\lambda})$  the non-perturbative correction to the self-energy within the orbital set $A_\lambda$, $\lambda=1,...,M$,
and the double-counting term $(\Sigma^{\text{DC}}\_{A_\lambda})$ ensures that no self-energy contribution is counted twice.



## Impurity problem construction

Within the SEET framework, each subset of potentially strongly correlated orbitals create an impurity problem that can be defined by the Hamiltonian of an impurity embedded into an electronic bath:
{{< raw >}}
$$
\begin{align}
&H^{A_{\lambda}}_{\text{imp}} = \sum_{ij\in A_{\lambda},\sigma}(\tilde{h}^{0}_{ij\sigma}-\mu\delta_{ij})c^{\dag}_{i\sigma}c_{j\sigma} + \sum_{b,\sigma}\epsilon_{b\sigma} a^{\dag}_{b\sigma}a_{b\sigma} \nonumber\\
&+ \sum_{i\in A_{\lambda},b,\sigma} (V_{ib\sigma}c^{\dag}_{i\sigma}a_{b\sigma} + h.c.) + \frac{1}{2}\sum_{\substack{ijkl\in A_{\lambda}\\ \sigma\sigma'}}v_{ijkl}c^{\dag}_{i\sigma}c^{\dag}_{k\sigma'}c_{l\sigma'}c_{j\sigma}.
\end{align}
$$
{{< /raw >}}

To ontain electronic bath parameters, we rely on the fact that the inverse Green's function restricted to subset $A_\lambda$ is not equal to the inverse of the Green's function restricted to $A_\lambda$:
{{< raw >}}
$$
\big[G(\omega_n)^{\bold{R}\bold{R}}_{ij\in A_{\lambda}}\big]^{-1} \neq \big[(G^{\bold{R}\bold{R}}(\omega_n))^{-1}\big]_{ij\in A_{\lambda}}.
$$
{{< /raw >}}

This discrepency is adsorbed into a hybrydization function $\Delta_{ij \in A_\lambda}(\omega_n) = \sum\limits_{b}\frac{V_{ib}V^*_{bj}}{\omega_n - \epsilon_b}$,
that defines an impurity problem that can be solved exactly.

## Self-consistency

![alt](/theory/scSEET_workflow.png)

Green software framework uses the following computational protocol[^seet1] [^seet2]

  0. Obtain initial condition by solving weak-coupling problem
  1. Perform single iteration weak-coupling solution with the current Green's function
  2. For each subset of strongly correlated orbitals, construct and solve impurity problem
  3. Using equation (1) obtain new total self-energy
  4. Solving Dyson equation obtain new correlated Green's function
  5. If converegence criteria is not met, return to step [1] (for full self-consistency) or to step [2] (for inner self-consistency)

[^seet]: D. Zgid, E. Gull,  [New J. Phys. 19 023047](https://doi.org/10.1088/1367-2630/aa5d34)
[^seet1]: S. Iskakov, C.-N. Yeh, E. Gull, D. Zgid [Phys. Rev. B 102 085105](https://doi.org/10.1103/PhysRevB.102.085105)
[^seet2]: C.-N. Yeh, S. Iskakov, D. Zgid, E. Gull [Phys. Rev. B 103 195149](https://doi.org/10.1103/PhysRevB.103.195149)