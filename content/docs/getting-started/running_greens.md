---
title: Running Green Weak Coupling
linkTitle: Weak Coupling Solution
weight : 2
---

To perform weak-coupling simulations, one have to call `mbpt.exe` executable located at the installation path in the `bin` subdirectory.
Minimal parameters that are needed to run weak-coupling simulations are following:

  - `--BETA`  inverse temperature
  - `--scf_type` type of self-consistent approximation, should be either `GW`, `GF2` or `HF`
  - `--grid_file`  path to a file containing non-uniform grids, program will check three possible locations:
    - current directory or absolute path
    - `<installation directory>/share`
    - build directory of weak-coupling code

Currently, we provide IR (`ir` subdirectory) and Chebyshev grids (`cheb` subdirectory) for nonuniform imaginary time representation.
For more details on nonuniform grids, please follow this [link](/docs/theory/matsubara-and-imaginary-time/)


After successful completion, results are written to [`--results_file`](/docs/components/data-formats/output-files/#main-results-file), which defaults to `sim.h5`.
To get information about other parameters and their default values call `mbpt.exe --help`..

### Band-path interpolation

If input data contains information about high-symmetry path,
diagonal part of the Green's function can be evaluated on provided high-symmetry path using $\mathbf{k}$-space interpolation, and results will be stored 
in the `G_tau_hs` group in the [high-symmetry output file](/docs/components/data-formats/output-files/#high-symmetry-path-output) (by default set to `output_hs.h5`).
To run band-path interpolation option `--jobs` has to be set to `WINTER`.
WINTER also requires matching `/high_symm_path` data in `input.h5` and an existing `--results_file` checkpoint from an earlier SC run or an earlier ordered SC job; it interpolates the checkpoint selected by `/iter`.
