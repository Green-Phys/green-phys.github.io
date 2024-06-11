---
title: Thermodynamics
weight: 2
math: true
---

Self-consistent finite $\Phi$-derivable theories allow to get direct access to thermodynamic properties such as entropy, free energy, and specific heat.

The grand potential is defined in terms of Green's functions, self-energies, and a $\Phi$-functional as [^Luttinger60]
{{< raw >}}
$$
\begin{align*}
\Omega &= \frac{1}{\beta} \left\{ \Phi[G] - Tr\{\ln\left[-G^{-1}\right]\} - Tr\{\Sigma G\}  \right\}.
\end{align*}
$$
{{< /raw >}}
In practice, the evaluation direct evaluation of the second term in this form is complicated by the slow decay of Green's functions as a function of 
frequency. Therefore, by defining 
{{< raw >}}
$$
\begin{align}
G^{-1} &= (i\omega_n  + \mu) S - F - \Sigma_c\left[G\right],\\
G_{HF}^{-1} &= (i\omega_n  + \mu) S - F ,\\
G_{0}^{-1} &= (i\omega_n  + \mu) S - H_{0},
\end{align}
$$
{{< /raw >}}
in terms of Matsubara frequencies $i\omega_n$, the chemical potential $\mu$, the overlap matrix $S$, the non-interacting $(U=0)$ Hamiltonian $H_0$ and the Fock matrix $F=H_0 + \Sigma^\infty$,
we can evaluate the logarithmic term as[^Dahlen06]
{{< raw >}}
$$
\begin{align}
Tr\{\ln\left[-G^{-1}\right]\} = Tr\{\ln\left[-G_{HF}^{-1}\right]\} + Tr\{\ln\left[1 - G_{HF} \Sigma\right]\}
\end{align}
$$
{{< /raw >}}
The $\Phi$-functional is expressed as
$$
\begin{align}
\Phi\left[G\right] = \sum_{n = 1}^{\infty} \Phi^{(n)}\left[G\right]
 = \sum_{n = 1}^{\infty}\frac{1}{2n} Tr\{\Sigma^{(n)}\left[G\right] G\},
\end{align}
$$
where $\Sigma^{(n)}\left[G\right]$ is the total n-th order self-energy part. 
Standard textbook relations yield the entropy, specific heat, total energy and free energy as thermodynamic derivatives
{{< raw >}}
$$
\begin{align*}
    &S = -\frac{\partial \Omega}{\partial T},\\
    &C_V = T \frac{\partial S}{\partial T}, \\
    &E = T^2\frac{\partial ln Z}{\partial T}, \\
    &F = \Omega + \mu N
\end{align*}
$$
{{< /raw >}}

Alternatively, the entropy can be evaluated from the Gibbs-Duhem relation $\Omega = E - TS - \mu N$; the specific heat from its definition $C_V = \frac{\partial E}{\partial T}$; 
and the energy from the Galitskii-Migdal formula.[^galitskii]
When the fully self-consistent conserving theories are applied different approach to evaluate thermodynamic quantities will produce the same 
result [^yeh] [^iskakov]


### Grand potential in the second order approximation

Within the [second-order perturbation theory (GF2)](/docs/theory/gf2_theory), the self-energy is approximated as  $\Sigma \approx \Sigma^{[2]} = \Sigma^{\infty} + \Sigma^{(2)}$,
and using Eq. 1:

{{< raw >}}$$\Phi \approx \Phi^{[2]} = \Phi^{(1)} + \Phi^{(2)} = \frac{1}{2} Tr\{\Sigma^{\infty}\gamma\} + \frac{1}{4} Tr\{\Sigma^{(2)} G\},$${{< /raw >}}

where $\gamma = G(\tau=0^-)$ is the density matrix. Using Eqs. 1-3,5 with $\Sigma^{\infty} = F - H_{0}$, such that

{{< raw >}}
$$
 Tr\{\Sigma\left[G\right] G\}= Tr\{\Sigma^{\infty}\gamma\} + Tr\{\Sigma^{(2)} G\}.
$$
{{< /raw >}}

Combining Eq.1-Eq.5 we obtain the second order approximation of the grand potential as
{{< raw >}}
$$
\begin{align*}
\Omega^{[2]} &= \frac{1}{\beta} \left\{ \Phi^{[2]}[G] - Tr\{\ln\left[-G^{-1}\right]\} - Tr\{\Sigma^{[2]} G\}  \right\} =\nonumber\\
      &\frac{1}{\beta} \left\{ -\frac{1}{2}Tr\{\Sigma_{\infty}\gamma\} - \frac{3}{4}Tr\{\Sigma^{(2)} G\} - Tr\{\ln\left[-G_{HF}^{-1}\right]\} - Tr\{\ln\left[1 - G_{HF} \Sigma^{(2)}\right]\} \right\}
\end{align*}
$$
{{< /raw >}}

### Grand potential in the GW approximation



[^Luttinger60]: J. M. Luttinger and J. C. Ward,  [Ground-State Energy of a Many-Fermion System. II](https://doi.org/10.1103/PhysRev.118.1417)
[^Dahlen06]: Nils Erik Dahlen et al., [Variational energy functionals of the Green function and of the density tested on molecules](https://doi.org/10.1103/PhysRevA.73.012511)
[^galitskii]: B. Holm and F. Aryasetiawan, [Total energy from the Galitskii-Migdal formula using realistic spectral functions](https://doi.org/10.1103/PhysRevB.62.4858)
[^iskakov]: S. Iskakov, A. A. Rusakov, D. Zgid, and E. Gull, [Effect of propagator renormalization on the band gap of insulating solids](https://doi.org/10.1103/PhysRevB.100.085112)
[^yeh]: C.-N. Yeh, S. Iskakov, D. Zgid, and E. Gull [Fully self-consistent finite-temperature GW in Gaussian Bloch orbitals for solids](https://doi.org/10.1103/PhysRevB.106.235104)
