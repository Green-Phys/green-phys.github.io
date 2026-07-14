---
title: DIIS and Convergence Acceleration
linkTitle: Convergence Acceleration
permalink: /DIIS_and_Convergence_Acceleration/
math: true
weight: 9
prev: "/docs/theory/thermodynamics"
next: "/docs/installation"
---

## Why self-consistency needs acceleration

Fully self-consistent Green's-function calculations solve the Dyson equation and the self-energy equation together. On the Matsubara axis this fixed-point problem can be written schematically as

$$
G^{-1}(i\omega_n)=G_0^{-1}(i\omega_n)-\Sigma[G](i\omega_n).
$$

Here $G_0$ is the noninteracting Green's function built from the one-body Hamiltonian and chemical potential, $G$ is the interacting Green's function, and $\Sigma[G]$ is the self-energy functional. In GF2, GW, and related approximations the self-energy contains a static Hartree-Fock part and a frequency-dependent correlation part. A self-consistent cycle therefore proceeds by guessing a one-particle starting point, solving the Dyson equation for $G$, evaluating a new $\Sigma[G]$, adjusting the chemical potential if the electron number is fixed, and repeating until the Green's function, self-energy, energy, and particle number stop changing.

This direct fixed-point iteration is the Green's-function analogue of the Roothaan iteration in Hartree-Fock theory. It is simple, but it is rarely the best numerical algorithm. The self-energy is frequency dependent, the chemical potential may move during the calculation, and the grand-potential landscape is not a simple convex optimization problem. Ref. {{% citeinline %}}[^PokhilkoDyson2022]{{% /citeinline %}} emphasizes that standard electronic-structure acceleration methods cannot be transferred blindly to Dyson-equation iterations because Green's-function calculations have a non-idempotent density matrix, correlation-driven feedback, particle-number fluctuations, and a dynamical self-energy.

In the Green/WeakCoupling interface, direct iteration is selected with `--mixing_type NO_MIXING`. It is useful as a diagnostic, but practical GF2 and GW calculations usually use damping, DIIS, or commutator DIIS.

## Damping

The simplest stabilization is linear mixing, also called damping or successive overrelaxation. Instead of using the newly computed self-energy directly, the next Dyson solve uses a weighted average of the new and previous self-energies:

$$
\Sigma_m=\alpha\,\Sigma[G_{m-1}]+(1-\alpha)\Sigma_{m-1}.
$$

The parameter $\alpha$ is the mixing weight. The value $\alpha=1$ gives direct iteration. Values smaller than one damp the update and often suppress oscillations. Values larger than one are possible in the formal successive-overrelaxation language, but Green's-function calculations most commonly use damping with $0<\alpha<1$.

Self-energy mixing is selected with `--mixing_type SIGMA_MIXING`, and the mixing weight is set with `--mixing_weight`. Some calculations instead mix the Green's function itself, selected with `--mixing_type G_MIXING`. The same idea applies: the algorithm reduces the size of the nonlinear update, trading speed for stability.

Damping is robust because it does not require solving any auxiliary linear system. Its weakness is that it only looks at the most recent direction. If the iteration is slowly spiraling toward the solution, damping can require many iterations. If the approximate fixed-point map has a nearly neutral unstable direction, damping can stagnate and give the appearance of convergence while the remaining error decreases very slowly.

## Subspace acceleration

DIIS replaces one-step damping by extrapolation in a small history of previous iterates. The objects being extrapolated are the total self-energies, including both static and dynamical parts. Following Ref. {{% citeinline %}}[^PokhilkoDyson2022]{{% /citeinline %}}, one may view each stored vector as

$$
\mathbf v_m =
\begin{pmatrix}
F_m\\
\Sigma_m^\mathrm{dyn}(\tau)
\end{pmatrix}.
$$

The extrapolated vector is a linear combination of stored vectors,

$$
\mathbf v_\mathrm{ext}=\sum_i c_i\mathbf v_i,
$$

with the DIIS constraint

$$
\sum_i c_i=1.
$$

The constraint is important. If each vector is written as the exact fixed-point vector plus an error,

$$
\mathbf v_i=\mathbf v_\ast+\mathbf e_i,
$$

then an unconstrained linear combination would also rescale the desired fixed-point vector. With the constraint, the extrapolated vector becomes the fixed-point vector plus only the extrapolated error:

$$
\mathbf v_\mathrm{ext}=\mathbf v_\ast+\sum_i c_i\mathbf e_i.
$$

DIIS chooses the coefficients so that the norm of the extrapolated residual is as small as possible in the current subspace. Since the exact error $\mathbf e_i$ is unknown, the algorithm uses computable residual vectors $r_i$. Their overlaps define the small DIIS matrix

$$
B_{ij}=\langle r_i,r_j\rangle.
$$

The coefficients are obtained from

$$
\sum_j B_{ij}c_j-\lambda=0,
$$

together with the constraint

$$
\sum_i c_i=1.
$$

This is the same minimization problem used in Pulay DIIS for self-consistent-field calculations, but the vectors and residuals must be chosen for the Dyson equation.[^Pulay1980], [^Pulay1982] In practice the $B$ matrix can become ill conditioned as the residuals become small. Ref. {{% citeinline %}}[^PokhilkoDyson2022]{{% /citeinline %}} discusses a simple partitioning/preconditioning strategy: solve the coefficient equation up to an overall scale and then renormalize the coefficients so that their sum is one.

## Difference and commutator residuals

The most direct residual is the difference between consecutive self-energies:

$$
r_m^\mathrm{diff}=\Sigma_m-\Sigma_{m-1}.
$$

This residual is easy to compute and can be used with DIIS or KAIN. It measures whether the stored self-energy vectors are still changing. However, it does not directly test whether the current $G$ and $\Sigma$ satisfy the Dyson equation together.

The commutator residual is more closely tied to the Dyson equation. At convergence,

$$
G^{-1}=G_0^{-1}-\Sigma.
$$

Since a matrix commutes with its own inverse, a converged solution obeys

$$
[G(i\omega_n),G_0^{-1}(i\omega_n)-\Sigma(i\omega_n)]=0.
$$

This motivates the frequency-dependent commutator residual

$$
r_m^\mathrm{comm}(i\omega_n)=
[G_m(i\omega_n),G_0^{-1}(i\omega_n)-\Sigma_m(i\omega_n)].
$$

The norm of this residual uses matrix traces over orbital, spin, and momentum labels and sums or integrates over imaginary frequency or time. In periodic calculations, the cost of building the commutator scales similarly to one Dyson solve, $O(n_\omega n_k n^3)$, up to prefactors.[^PokhilkoDyson2022]

The commutator residual is the Green's-function analogue of the Hartree-Fock commutator $[F,P]$, which vanishes when the Fock matrix and density matrix are mutually self-consistent. In Dyson-equation calculations it has an important practical advantage: it tests consistency between $G$, $G_0$, and $\Sigma$, not only the size of the last self-energy update. In the GF2 and GW examples studied in Ref. {{% citeinline %}}[^PokhilkoDyson2022]{{% /citeinline %}}, commutator residuals used in CDIIS and LCIIS were more regular and generally outperformed difference residuals for both molecules and solids.

In the Green/WeakCoupling interface, difference-residual DIIS is selected with `--mixing_type DIIS`. Commutator-residual DIIS is selected with `--mixing_type CDIIS`. The implementation uses ordinary damping for the first few iterations, starts the DIIS extrapolation at `--diis_start`, and limits the number of stored vectors with `--diis_size`.[^GreenWeakCoupling2025]

## LCIIS, KAIN, and step control

The same convergence study also compared DIIS with two other subspace strategies: least-squares commutator in the iterative subspace (LCIIS) and the Krylov-space accelerated inexact Newton method (KAIN).[^PokhilkoDyson2022] LCIIS minimizes the norm of a commutator built from extrapolated quantities. For Green's functions, this means introducing

$$
\Sigma_\mathrm{ext}=\sum_i c_i\Sigma_i,
$$

and

$$
G_\mathrm{ext}=\sum_i c_iG_i,
$$

then minimizing the squared norm of

$$
[G_\mathrm{ext}(i\omega_n),G_0^{-1}(i\omega_n)-\Sigma_\mathrm{ext}(i\omega_n)].
$$

KAIN instead treats convergence as a nonlinear root-finding problem and approximates a Newton step in the Krylov subspace spanned by previous update directions. In the Dyson-equation application, KAIN uses the self-energy as the nonlinear vector and uses difference residuals; commutator residuals are not appropriate for KAIN because they lead to an ill-defined projected system in this formulation.[^PokhilkoDyson2022]

Subspace extrapolation can occasionally overstep. Large DIIS coefficients indicate that the extrapolated point lies far outside the region sampled by previous iterations. Ref. {{% citeinline %}}[^PokhilkoDyson2022]{{% /citeinline %}} discusses step restrictions that reinterpret extrapolation as a step away from the newest vector and rescale that step if the coefficient norm is too large. In day-to-day calculations, the same idea appears in a simpler form: use damping for the earliest iterations, keep a moderate DIIS subspace, and restart or reduce the mixing weight if the extrapolated iterations become erratic.

## Temperature continuation

Difficult GF2 and GW calculations often become harder at lower temperature because the Green's function resolves sharper features and correlation effects are less thermally smoothed. A useful strategy is therefore to converge an easier high-temperature calculation first and then lower the temperature gradually, using each converged solution as the initial guess for the next calculation. Ref. {{% citeinline %}}[^PokhilkoDyson2022]{{% /citeinline %}} found that this heating-cooling or sequential-temperature strategy, combined with CDIIS or LCIIS, could converge restricted GF2 calculations for strongly correlated bond-breaking examples that were otherwise difficult or impossible to converge.

This continuation strategy does not change the equations being solved. It only changes the path by which the nonlinear solver reaches the low-temperature fixed point. That distinction matters: convergence acceleration should not be judged only by the final residual, but also by whether the solver has been guided to the physically intended solution when multiple self-consistent solutions are possible.

## Practical interpretation

For small or weakly correlated systems, simple damping may be enough. For production fully self-consistent GF2 and GW calculations, CDIIS is usually the more informative default because its residual is built from the Dyson equation itself. Difference-residual DIIS remains useful and inexpensive, especially for diagnosing whether the self-energy update is changing smoothly. Larger subspaces can stabilize hard calculations, but very large or noisy coefficients are a warning sign. In those cases, increasing the damping period, reducing the mixing weight, restarting the subspace, or using temperature continuation is often more productive than simply increasing the iteration limit.

[^PokhilkoDyson2022]: P. Pokhilko, C.-N. Yeh, and D. Zgid, "Iterative subspace algorithms for finite-temperature solution of Dyson equation," *Journal of Chemical Physics* **156**, 094101 (2022). [https://doi.org/10.1063/5.0082586](https://doi.org/10.1063/5.0082586)

[^Pulay1980]: P. Pulay, "Convergence acceleration of iterative sequences. The case of SCF iteration," *Chemical Physics Letters* **73**, 393-398 (1980). [https://doi.org/10.1016/0009-2614(80)80396-4](https://doi.org/10.1016/0009-2614(80)80396-4)

[^Pulay1982]: P. Pulay, "Improved SCF convergence acceleration," *Journal of Computational Chemistry* **3**, 556-560 (1982). [https://doi.org/10.1002/jcc.540030413](https://doi.org/10.1002/jcc.540030413)

[^GreenWeakCoupling2025]: S. Iskakov, C.-N. Yeh, P. Pokhilko, T. Chen, D. Zgid, and E. Gull, "Green/WeakCoupling: Implementation of fully self-consistent finite-temperature many-body perturbation theory for molecules and solids," *Computer Physics Communications* **306**, 109380 (2025). [https://doi.org/10.1016/j.cpc.2024.109380](https://doi.org/10.1016/j.cpc.2024.109380)
