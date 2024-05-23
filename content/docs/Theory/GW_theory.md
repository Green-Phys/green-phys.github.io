---
title: GW Background and Theory
linkTitle: GW approximation
math: true
weight: 3
---


In $GW$ approximation [^bloch], the correlated self-energy is approximated as the sum of an infinite series of RPA-like `bubble' diagrams [^hedin]. 
On the imaginary-time axis, ${(\Sigma^{GW})}^{\bf{k}}(\tau)$ reads 
{{< raw >}}
$$
{(\Sigma^{GW})}^{\mathbf{k}}_{i\sigma,j\sigma}(\tau) = -\frac{1}{N_{k}}\sum_{\mathbf{q}}\sum_{ab} G^{\mathbf{k-q}}_{a\sigma,b\sigma}(\tau)\tilde{W}^{\mathbf{k},\mathbf{k-q},\mathbf{k-q},\mathbf{k}}_{ i a  b j}(\tau)
$$
{{< /raw >}}
where $\tilde{W}$ is the effective screened interaction tensor, defined as the difference between the full dynamically screened interaction $W$ and the bare interaction $\boldsymbol{U}$, i.e. $\tilde{W} = W - U$. 
Here and following, the indices $\set{i,j, k, l, a, b}$ are orbital indices, $\set{k,q}$ are crystal momentum, and $N_{k}$ is the number of momentum considered for a finite cluster.
In the $GW$ approximation, the screened interaction $W$ is expressed in the frequency space as [^hedin]
{{< raw >}}
$$
\begin{aligned}
&W^{\mathbf{k}_{1}\mathbf{k}_{2}\mathbf{k}_{3}\mathbf{k}_{4}}_{\ i\ \ j \ k\  \ l}(i\Omega_{n}) = U^{\mathbf{k}_{1}\mathbf{k}_{2}\mathbf{k}_{3}\mathbf{k}_{4}}_{\ i\ \ j \ k\  \ l}\nonumber\\
&+\frac{1}{N_{k}}\sum_{\mathbf{k}_{5}\mathbf{k}_{6}\mathbf{k}_{7}\mathbf{k}_{8}}\sum_{abcd}U^{\mathbf{k}_{1}\mathbf{k}_{2}\mathbf{k}_{5}\mathbf{k}_{6}}_{\ i\ \ j \ a\  \ b} \mathit{\Pi}^{\mathbf{k}_{5}\mathbf{k}_{6}\mathbf{k}_{7}\mathbf{k}_{8}}_{\ a\ b \ c\  \ d}(i\Omega_{n})W^{\mathbf{k}_{7}\mathbf{k}_{8}\mathbf{k}_{3}\mathbf{k}_{4}}_{\ c\ d \ \ k\  \ l}(i\Omega_{n})
\end{aligned}
$$
{{< /raw >}}
where $\boldsymbol{\mathit{\Pi}}$ is the non-interacting polarization function 
{{< raw >}}
$$
\mathit{\Pi^{\mathbf{k}_{1}\mathbf{k}_{2}\mathbf{k}_{3}\mathbf{k}_{4}}_{\ a\ b \ c\  \ d}(\tau)} = \sum_{\sigma}G^{\mathbf{k}_{1}}_{d\sigma,a\sigma}(\tau)G^{\mathbf{k}_{2}}_{b\sigma ,c\sigma}(-\tau)\delta_{\mathbf{k}_{1}\mathbf{k}_{4}}\delta_{\mathbf{k}_{2}\mathbf{k}_{3}}. 
$$
{{< /raw >}}
There is also an impllimentation of the GW approximation with exact two-component formalism with one-electron approximation (X2C-1e) for solving a relativistic case [^rel]

![gw](/theory/bubbles.png)
[^hedin]: L. Hedin, [Phys. Rev. 139, A796 (1965)](https://doi.org/10.1103/PhysRev.139.A796)
[^bloch]: C. Yeh, S. Iskakov, D. Zgid, and E. Gull [Phys. Rev. B 106, 235104](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.106.235104)
[^rel]: C. Yeh, A. Shee, Q. Sun, E. Gull, and D. Zgid [Phys. Rev. B 106, 085121](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.106.085121)
