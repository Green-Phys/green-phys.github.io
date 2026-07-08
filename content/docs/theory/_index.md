---
title: Theory
linkTitle: Theory
icon: auto_stories
weight: 1
next: "/docs/installation"
---


Green implements many-body methods based on the language of Green's functions for the simulation of realistic molecules and solids. The following pages introduce the theoretical background behind the methods available in the package.

### Introduction

An introduction to the language of Green's functions, the many-body Hamiltonian Green solves, and pointers to textbooks and review articles for readers new to diagrammatic perturbation theory.

{{< cta-button text="Read more" link="introduction" icon="info" >}}

### GF2

Self-consistent second-order perturbation theory (GF2), also known as Second Order Born — a conserving diagrammatic approximation that is accurate whenever gaps are large and interactions are weak, though it is known to fail for metals.

{{< cta-button text="Read more" link="gf2_theory" icon="functions" >}}

### GW

The fully self-consistent $GW$ approximation, implementing Hedin's equations with full frequency dependence and self-consistency on the imaginary axis, making the solution thermodynamically consistent and conserving.

{{< cta-button text="Read more" link="gw_theory" icon="science" >}}

### Post-processing

Theory behind the observables Green can extract from a finite-temperature calculation, including thermodynamic quantities and spectral properties.

{{< cta-button text="Read more" link="postprocessing" icon="analytics" >}}

### Convergence

Theory behind the convergence acceleration techniques available in Green, such as direct inversion in the iterative subspace (DIIS), for stabilizing and speeding up self-consistent iterations.

{{< cta-button text="Read more" link="convergence_acceleration" icon="trending_down" >}}