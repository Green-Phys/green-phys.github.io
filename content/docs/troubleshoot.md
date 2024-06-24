---
title: Solutions to common problems
linkTitle: Troubleshooting
icon: troubleshoot
weight: 6
prev: "/docs/tutorials"
---

## Calculation does not converge

Quite often the default choice for convergence acceleration will not lead to a converged solution.
By default we choose to use a simple mixing of the self-energy, where the self-energy at the current iteration is mixed with the 
self-energy from the previous iteration. Adjusting the mixing parameter (choosing smaller value for `--mixing_weight` parameter)
can usually stabilize convergence but makes it slower. In many cases the better option is to use
advanced convergence acceleration techniques, such as direct inversion in the iterative subspace (DIIS)  method. For more details
on how to use it read the [DIIS tutorial](/docs/tutorials/diis).

