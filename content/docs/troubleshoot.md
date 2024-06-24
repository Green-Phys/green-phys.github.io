---
title: Solutions to common problems
linkTitle: Troubleshooting
icon: troubleshoot
weight: 6
math: true
prev: "/docs/tutorials"
---

## Calculation does not converge

Quite often the self-consistent iterations will not lead to a converged solution. There are several possible causes for calculation to diverge, the two main reasons are:
  - Self-consistent iterations are unstable;
  - Non-uniform Fourier transform has a large leakage.

### Instability of self-consistent iterations
When the initial starting point of the self-consistent iterations lays far away from the solution, iterative solver may experience one 
of the following behavior: diverge, oscilate between multiple meta-stable points, show no pattern of divergence or convergence.

To stabilize the self-consistent iterations `Green` provides several options.
By default we choose to use a simple mixing of the self-energy, where the self-energy at the current iteration is mixed with the 
self-energy from the previous iteration. Adjusting the mixing parameter (choosing smaller value for `--mixing_weight` parameter)
can usually stabilize convergence but makes it slower. In many cases the better option is to use
advanced convergence acceleration techniques, such as direct inversion in the iterative subspace (DIIS)  method. For more details
on how to use it read the [DIIS tutorial](/docs/tutorials/diis).

### Large leakage in non-uniform Fourier transformation
All dynamical quantites in `Green` use non-uniform compact representation in imaginary time/Matsubara frequency domain.
The choice of non-uniform grid has to address two main aspects: 
  - being compact to reduce computational complexity;
  - being large enough to properly capture short time/large frequency asymptotic behavior.
If the grid is too small large spectral leakage can occure during the Foruier transfrom in time/frequency domain,
that may result in large calculation errors and potentially break down of self-consistent iterations.
During the calculations, `Green` computes the spectral leakage every time the Fourier transfrom in time/frequency domain
is performed. If the spectral leakage is larger than $10^{-8}$ the following warning message will be printed into standard output:
```ShellSession
WARNING: The leakage is larger than 1e-8
```
When the `Green`/`WeakCoupling` simulations are done in single precision, spectral leakage will almost always exceed $10^{-8}$ cutoff
and we suggest to monitor spectral leakage for couple of iterations and if it does not grow, the calculations are expected to be 
stable and no further actions are needed.
