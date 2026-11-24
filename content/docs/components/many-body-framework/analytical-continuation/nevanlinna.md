---
title: Analytic Continuation – Nevanlinna and Carathéodory methods
linkTitle: Nevanlinna method
weight: 7
---

The Nevanlinna analytic continuation method continues scalar (or diagonal) Matsubara data to the real axis
while preserving causality. It is described in

- J. Fei, C.-N. Yeh, E. Gull, *Nevanlinna Analytical Continuation*,
  [Phys. Rev. Lett. **126**, 056402 (2021)](https://doi.org/10.1103/PhysRevLett.126.056402).

Its generalization to matrix-valued functions, the Carathéodory method, is described in

- J. Fei, C.-N. Yeh, D. Zgid, E. Gull, *Analytical continuation of matrix-valued functions: Carathéodory formalism*,
  [Phys. Rev. B **104**, 165111 (2021)](https://doi.org/10.1103/PhysRevB.104.165111).

There is also an undergraduate thesis that has many more details:
<https://deepblue.lib.umich.edu/handle/2027.42/167885>

## Code

- **Nevanlinna (C++):** [`green-ac`](https://github.com/Green-Phys/green-ac) provides the `ac.exe` executable and the
  `green_ac` Python module. See [Installation → Analytical Continuation](/docs/installation/general_ac/) for how to build it
  and [Post-processing](/docs/getting-started/postprocessing/) for how to run `ac.exe` on Green output.
- **Python interface:** [`green-mbtools`](https://github.com/Green-Phys/green-mbtools) wraps both methods in
  `green_mbtools.pesto.analyt_cont`:
  - `nevan_run` – Nevanlinna continuation (calls `green_ac`),
  - `es_nevan_run` – Nevanlinna continuation after projecting the data onto a causal pole representation,
  - `caratheodory_run` – Carathéodory continuation of matrix-valued data (the Carathéodory solver ships with `green-mbtools`).

  See `examples/nevanlinna.py` and `examples/es_nevanlinna.py` in the `green-mbtools` repository.

## Talk

Jiani Fei gave a talk on how to use the Nevanlinna code and the
mathematical background:

{{< youtube id="aEGrqG9EY98" >}}

[Here](/files/Nevanlinna_group_meeting_220628.key.pdf) are her slides.

The talk mentions source files for the optimization procedure. The 2021 version of that code shown in
the talk is available [here](/files/Nevanlinna_Schur.zip); it predates `green-ac` and is kept for reference only.
