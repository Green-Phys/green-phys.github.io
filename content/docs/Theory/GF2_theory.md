---
title: Second Order approximation (GF2)
linkTitle: GF2 approximation
weight: 2
math: true
katex: true
---

The first conserving diagrammatic approximation that has nonzero contribution to the correlated self-energy is the second order perturbation theory [^holleboom].

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



[^holleboom]: L. J. Holleboom, J. G. Snijders, [A comparison between the Mo/ller–Plesset and Green’s function perturbative approaches to the calculation of the correlation energy in the many‐electron problem](https://doi.org/10.1063/1.459578)
[^rusakov]: A. A. Rusakov,  D. Zgid, [Self-consistent second-order Green’s function perturbation theory for periodic systems](https://doi.org/10.1063/1.4940900)
