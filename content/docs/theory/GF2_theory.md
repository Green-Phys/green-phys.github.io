---
title: Self-Consistent Second-Order Perturbation Theory (GF2)
linkTitle: GF2 approximation
weight: 5
math: true
katex: true
---


GF2 is the fully self-consistent second-order Green's-function perturbation theory.  It is also called the second-order Born approximation.  In the language of the previous pages, GF2 is an approximation for the dynamical self-energy $\Sigma^\mathrm{dyn}$: the Hamiltonian, overlap matrix, Coulomb integrals, density matrix, static term $\Sigma^\infty$, and Dyson equation remain the same.[^RusakovPeriodic2016], [^GreenWeakCoupling2024]

The important phrase is "fully self-consistent."  GF2 does not evaluate a second-order correction once on top of fixed Hartree-Fock or DFT orbitals.  Instead, it builds a second-order self-energy from the current interacting Green's function $G$, solves the Dyson equation to obtain a new $G$, updates the density matrix and static self-energy, adjusts the chemical potential, and repeats the process.  The propagator lines in the GF2 diagrams are therefore "bold" lines: they are the dressed, self-consistent Green's function rather than the noninteracting propagator.[^THCGF2GWSOX2024]

## What GF2 Keeps

GF2 is a conserving, $\Phi$-derivable approximation: its self-energy can be obtained from a Luttinger-Ward functional containing all skeleton diagrams through second order in the bare Coulomb interaction.[^SEETGW2017]  Because it is self-consistent and $\Phi$-derivable, particle number and energy are treated consistently within the approximation.

The static part of the GF2 self-energy is the Hartree-Fock-like term,
$$
\Sigma(i\omega_n)=
\Sigma^\infty+\Sigma^{(2)}(i\omega_n).
$$
The new object is the dynamical second-order term $\Sigma^{(2)}$.  It contains the direct second-order diagram and the second-order exchange diagram.  This is a useful distinction from fully self-consistent GW: GW screens the direct interaction through $W$ and therefore resums bubble diagrams, but ordinary GW does not contain the bare second-order exchange diagram.[^GreenWeakCoupling2024], [^THCGF2GWSOX2024]

Thus GF2 is not simply MP2 written in a different notation.  If the second-order self-energy is evaluated once from a mean-field Green's function, the result is closely related to finite-temperature second-order perturbation theory.  In GF2, the Dyson iteration feeds the resulting self-energy back into $G$, which effectively generates higher-order contributions through self-consistency.[^RusakovPeriodic2016]

## Compact Molecular Form

For a finite molecule in an orthogonal orbital basis, the molecular GF2 self-energy is often written in imaginary time as
$$
\Sigma^{(2)}_{ij}(\tau)=
-\sum_{klmnpq}
G_{kl}(\tau)G_{mn}(\tau)G_{pq}(-\tau)
v_{imqk}
\left(
2v_{lpnj}-v_{lpjn}
\right).
$$
This expression is the form used in molecular GF2 and in self-energy embedding discussions.[^SEETGW2017]  The three Green's functions describe the three dressed fermion propagator lines in the second-order skeleton diagrams.  The two Coulomb integrals $v$ are bare, unscreened electron-electron interactions.  The factor $2v_{lpnj}$ is the closed-shell spin-summed direct term, while $-v_{lpjn}$ is the exchange term.

Several conventions exist for the ordering of the indices of the Coulomb integral.  The formula above follows the convention used in the cited molecular GF2 literature.  If another code stores electron-repulsion integrals with a different index order, the same physical contraction may look transposed or permuted.

## Periodic and Spin-Resolved Form

Green/WeakCoupling uses a spin-resolved periodic notation and a decomposed Coulomb interaction.  The static and dynamical pieces are separated as
$$
\Sigma_{ij}(\tau)=
\Sigma^\infty_{ij}\delta_\tau+
\tilde{\Sigma}_{ij}(\tau),
$$
where $\tilde{\Sigma}$ is the time-dependent part.  For GF2, $\tilde{\Sigma}=\Sigma^{(2)}$.

With $N_k$ sampled momenta, momentum labels $\mathbf{k}$, spin labels $\sigma$, and decomposed Coulomb vertices $V(Q)$, the implemented second-order self-energy is[^GreenWeakCoupling2024]
$$
\tilde{\Sigma}^{\mathbf{k},(2)}_{\sigma,ij}(\tau)=
-\frac{1}{N_k^3}
\sum_{\mathbf{k}_1\mathbf{k}_2\mathbf{k}_3}
\sum_{klmnpq}
\sum_{sPQ}
X_{\sigma s}\,
Y\,
G^{\mathbf{k}_1}_{\sigma,pq}(\tau)
G^{\mathbf{k}_2}_{s,kl}(\tau)
G^{\mathbf{k}_3}_{s,nm}(-\tau)
\delta_{\mathbf{k}+\mathbf{k}_3,\mathbf{k}_1+\mathbf{k}_2}.
$$
The two vertex contractions are
$$
X_{\sigma s}=
V^{\mathbf{k}_1\mathbf{k}}_{qj}(P)
V^{\mathbf{k}_2\mathbf{k}_3}_{ln}(P)
{}-
V^{\mathbf{k}_2\mathbf{k}}_{lj}(P)
V^{\mathbf{k}_1\mathbf{k}_3}_{qn}(P)
\delta_{\sigma s}.
$$
The remaining vertex product is
$$
Y=
V^{\mathbf{k}\mathbf{k}_1}_{ip}(Q)
V^{\mathbf{k}_3\mathbf{k}_2}_{mk}(Q).
$$
The first term in $X_{\sigma s}$ is the direct second-order contribution.  The second term is the exchange contribution, and it acts only for equal spin, which is why it carries $\delta_{\sigma s}$.  The final Kronecker delta enforces conservation of crystal momentum.

Equivalently, if the Coulomb interaction is stored as a four-index tensor rather than as decomposed vertices, the same periodic contraction can be written schematically as
$$
\Sigma^{\mathbf{k},(2)}_{ij}(\tau)=
-\frac{1}{N_k^3}
\sum
G(\tau)G(\tau)G(-\tau)
U
\left(2U-U_\mathrm{ex}\right)
\delta_{\mathbf{k}+\mathbf{k}_3,\mathbf{k}_1+\mathbf{k}_2}.
$$
This schematic form is useful for recognizing the direct-minus-exchange structure, but the decomposed expression above is closer to the implementation in Green/WeakCoupling.

## Self-Consistency Loop

A GF2 calculation proceeds through the following conceptual loop.[^GreenWeakCoupling2024]

1.  Start from a mean-field Green's function, usually from HF or DFT data.
2.  Build the density matrix from the current $G$.
3.  Construct the static self-energy $\Sigma^\infty$ from that density matrix.
4.  Evaluate the dynamical second-order self-energy $\Sigma^{(2)}(\tau)$.
5.  Transform $\Sigma^{(2)}$ between imaginary time and Matsubara frequency as needed.
6.  Adjust the chemical potential so that the target electron number is obtained.
7.  Solve the Dyson equation for a new $G$.
8.  Mix or accelerate the iteration until the energy, density matrix, or self-energy is converged.

For Green/WeakCoupling, the Matsubara-frequency Dyson equation is
$$
G^{\mathbf{k}}(i\omega_n)=
\left[
(i\omega_n+\mu)S^\mathbf{k}
-H^{0,\mathbf{k}}
-\Sigma^{\infty,\mathbf{k}}
-\tilde{\Sigma}^{\mathbf{k}}(i\omega_n)
\right]^{-1}.
$$
This is the same Dyson equation introduced earlier, now with the GF2 choice $\tilde{\Sigma}=\Sigma^{(2)}$.

## Energy Evaluation

After convergence, GF2 energies are evaluated from the interacting Green's function and self-energy.  In the molecular notation used in recent fully self-consistent GF2 and GWSOX work,
$$
\gamma_{pq}=-G_{qp}(0^-),
$$
$$
E_\infty=
\sum_{pq}
\left(
h_{pq}+\frac{1}{2}\Sigma^{HF}_{pq}[G]
\right)
\gamma_{pq},
$$
and
$$
E_\mathrm{dyn}=
\frac{1}{\beta}
\sum_{\omega_n}
\sum_{pq}
G_{qp}(i\omega_n)
\Sigma^{dyn}_{pq}(i\omega_n).
$$
For GF2, $\Sigma^{dyn}$ is the second-order self-energy.  The total electronic energy is
$$
E=E_\infty+E_\mathrm{dyn}.
$$
Older periodic GF2 papers write the same idea as a one-body term evaluated with the correlated density matrix and a Galitskii-Migdal two-body term involving a Matsubara sum over $G\Sigma$.[^RusakovPeriodic2016]

## Strengths and Limitations

GF2 is most reliable for weakly to moderately correlated systems where the bare interaction expansion remains controlled.  It is often more robust than non-self-consistent second-order perturbation theory because the Dyson iteration renormalizes the propagator and can soften divergences that appear in MP2-like treatments.[^RusakovPeriodic2016]

The same self-consistency also makes GF2 nonlinear.  Multiple self-consistent solutions can exist, and convergence can depend on the starting point, temperature path, chemical-potential updates, and mixing strategy.[^MultipleSolutions2021]  This is not a bug in the formula; it is a consequence of solving a nonlinear many-body fixed-point problem.

GF2 also has a clear diagrammatic limitation.  It uses bare Coulomb interactions through second order.  It does not contain the infinite screened interaction $W$ of GW, so it can overestimate correlation in situations where screening is essential, such as large dispersion-bound molecular complexes.[^THCGF2GWSOX2024]  Conversely, because GF2 includes the second-order exchange diagram, it contains vertex information that ordinary GW omits.  This difference becomes important in comparisons among scGF2, scGW, and scGWSOX.

In short, GF2 is the natural next step beyond Hartree-Fock in the Green's-function hierarchy: keep the static Hartree-Fock self-energy, add the complete second-order dynamical self-energy in the bare interaction, and solve the resulting Dyson equation self-consistently.

[^RusakovPeriodic2016]: "Self-consistent second-order Green's function perturbation theory for periodic systems," [J. Chem. Phys. 144, 054106 (2016)](https://doi.org/10.1063/1.4940900).
[^GreenWeakCoupling2024]: "Green/WeakCoupling: Implementation of fully self-consistent finite-temperature many-body perturbation theory for molecules and solids," [Comput. Phys. Commun. 306, 109380 (2025)](https://doi.org/10.1016/j.cpc.2024.109380).
[^THCGF2GWSOX2024]: "Tensor hypercontraction for fully self-consistent imaginary-time GF2 and GWSOX methods: Theory, implementation, and role of the Green's function second-order exchange for intermolecular interactions," [J. Chem. Phys. 161, 084108 (2024)](https://doi.org/10.1063/5.0215954).
[^SEETGW2017]: "Testing self-energy embedding theory in combination with GW," [Phys. Rev. B 96, 155106 (2017)](https://doi.org/10.1103/PhysRevB.96.155106).
[^MultipleSolutions2021]: "Interpretation of multiple solutions in fully iterative GF2 and GW schemes using local analysis of two-particle density matrices," [J. Chem. Phys. 155, 024101 (2021)](https://doi.org/10.1063/5.0055191).
