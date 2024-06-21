---
title: Solutions to common problems
linkTitle: Troubleshooting
icon: troubleshoot
weight: 6
prev: "/docs/tutorials"
---

## Calculations does not converge

Quite often default choice for convergence acceleration will not lead to the converged solution.
By default we choose to use simple Self-energy mixing, where the self-energy at the current iteration is mixed with the 
self-energy from the previous iteration. Adjusting the mixing parameter (choosing smaller value for `--mixing_weight` parameter)
can usually stabilize convergence but make it extremely slow. In many cases the better option would be to use
advanced convergence acceleration techniques, such as direct inversion in the iterative subspace (DIIS)  method. For more details
on how to use it please read the [DIIS tutorial](/docs/tutorials/diis).

