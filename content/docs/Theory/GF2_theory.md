---
title: Second Order approximation (GF2)
linkTitle: GF2 approximation
weight: 2
math: true
katex: true
---
Self-consistent second order perturbation theory is a
conserving diagrammatic approximation with nonzero contribution to the correlated self-energy. It is also known as Second Order Born. The method has been introduced to molecules in modern times by Holleboom and Snijders [^holleboom]. Generally it is considered accurate whenever gaps are large and interactions are weak but is known to fail for metals. Unlike GW, it contains a second-order exchagne term but does not include higher order screening contributions.

The second-order contribution to the self-energy in imaginary time and momentum space is[^rusakov]
{{< raw >}}
$$
\begin{align*}
\Sigma^{(2)}_{ij}(\tau,\mathbf{k}) = - \frac{1}{N_{\mathbf{k}}^3}\sum\limits_{\substack{klmnop\\ \mathbf{k_1}\mathbf{k_2}\mathbf{k_3} }} & 
(2U^{\mathbf{k_1}\mathbf{k}\mathbf{k_2}\mathbf{k_3}}_{qjln} - U^{\mathbf{k_2}\mathbf{k}\mathbf{k_1}\mathbf{k_3}}_{ljqn})
\times U^{\mathbf{k}\mathbf{k_1}\mathbf{k_3}\mathbf{k_2}}_{ipmk}
\\ \times
 &G^{\mathbf{k_1}}_{pq}(\tau)G^{\mathbf{k_2}}_{kl}(\tau)G^{\mathbf{k_3}}_{nm}(-\tau)\delta_{\mathbf{k}+\mathbf{k_3},\mathbf{k_1}+\mathbf{k_2} },
\end{align*}
$$
{{< /raw >}}

here {{< raw >}}$G^\mathbf{k}_{ij}(\tau)${{< /raw >}} is imaginary time Green\'s function, 
{{< raw >}}
$U^{\mathbf{k}\mathbf{k_1}\mathbf{k_2}\mathbf{k_3}}_{ijkl}$
{{< /raw >}}
is the Coloumb interaction
tensor, and $\delta_{\mathbf{k}+\mathbf{k_3},\mathbf{k_1}+\mathbf{k_2} }$ guarantees the momentum conservation.

Implementation details for Green's software are given in this [^rusakov] paper.



[^holleboom]: L. J. Holleboom, J. G. Snijders, [A comparison between the Mo/ller–Plesset and Green’s function perturbative approaches to the calculation of the correlation energy in the many‐electron problem](https://doi.org/10.1063/1.459578)
[^rusakov]: A. A. Rusakov,  D. Zgid, [Self-consistent second-order Green’s function perturbation theory for periodic systems](https://doi.org/10.1063/1.4940900)
[^BandGapPaper]: Sergei Iskakov, Alexander A. Rusakov, Dominika Zgid, and Emanuel Gull, [Effect of propagator renormalization on the band gap of insulating solids](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.100.085112)
