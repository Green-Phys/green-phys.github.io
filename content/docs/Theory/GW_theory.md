---
title: GW Background and Theory
linkTitle: GW approximation
weight: 3
math: true
---

In $GW$ approximation, the correlated self-energy is approximated as the sum of an infinite series of RPA-like `bubble' diagrams [^hedin]. 
On the imaginary-time axis, ${(\Sigma^{GW})}^{\bf{k}}(\tau)$ reads 

$$
{(\Sigma^{GW})}^{\bf{k}}_{i\sigma,j\sigma}(\tau) = -\frac{1}{N_{k}}\sum_{\bf{q}}\sum_{ab} G^{\bf{k-q}}_{a\sigma,b\sigma}(\tau)\tilde{W}^{\bf{k},\bf{k-q},\bf{k-q},\bf{k}}_{ i a  b j}(\tau)
$$

where $\tilde{W}$ is the effective screened interaction tensor, defined as the difference between the full dynamically screened interaction $W$ and the bare interaction $\boldsymbol{U}$, i.e. $\tilde{W} = W - U$. 
Here and following, the indices $\set{i,j, k, l, a, b}$ are orbital indices, $\set{k,q}$ are crystal momentum, and $N_{k}$ is the number of momentum considered for a finite cluster.
In the $GW$ approximation, the screened interaction $W$ is expressed in the frequency space as [^hedin]
{{< raw >}}
$$
\begin{aligned}
&W^{\bf{k}_{1}\bf{k}_{2}\bf{k}_{3}\bf{k}_{4}}_{\ i\ \ j \ k\  \ l}(i\Omega_{n}) = U^{\bf{k}_{1}\bf{k}_{2}\bf{k}_{3}\bf{k}_{4}}_{\ i\ \ j \ k\  \ l}\nonumber\\
&+\frac{1}{N_{k}}\sum_{\bf{k}_{5}\bf{k}_{6}\bf{k}_{7}\bf{k}_{8}}\sum_{abcd}U^{\bf{k}_{1}\bf{k}_{2}\bf{k}_{5}\bf{k}_{6}}_{\ i\ \ j \ a\  \ b} \mathit{\Pi}^{\bf{k}_{5}\bf{k}_{6}\bf{k}_{7}\bf{k}_{8}}_{\ a\ b \ c\  \ d}(i\Omega_{n})W^{\bf{k}_{7}\bf{k}_{8}\bf{k}_{3}\bf{k}_{4}}_{\ c\ d \ \ k\  \ l}(i\Omega_{n})
\end{aligned}
$$
{{< raw >}}
where $\boldsymbol{\mathit{\Pi}}$ is the non-interacting polarization function 

$$
\mathit{\Pi^{\bf{k}_{1}\bf{k}_{2}\bf{k}_{3}\bf{k}_{4}}_{\ a\ b \ c\  \ d}(\tau)} = \sum_{\sigma}G^{\bf{k}_{1}}_{d\sigma,a\sigma}(\tau)G^{\bf{k}_{2}}_{b\sigma ,c\sigma}(-\tau)\delta_{\bf{k}_{1}\bf{k}_{4}}\delta_{\bf{k}_{2}\bf{k}_{3}}. 
$$

![gw](/theory/bubbles.png)
[^hedin]: L. Hedin, [Phys. Rev. 139, A796 (1965)](https://doi.org/10.1103/PhysRev.139.A796)
