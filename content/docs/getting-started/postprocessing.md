---
title: Post-processing
linkTitle: Post-processing
weight : 3
next: "/docs/getting-started/examples/si"
---

The `Green` provides several post-processing procedures such as analytical continuation packages to obtain spectral representations and
thermodynamic utilities to obtain thermodynamic quantities.

### Spectral representation

To obtain the spectral representation of a Green's function, the `Green` software stack provides an analytical continuation package.

To run the analytical continuation one have to execute the program `ac.exe` located at the installation path in the `bin` subdirectory.
The following parameters are required:
  - `--grid_file`  Sparse imaginary time/frequency grid file name
  - `--BETA`  Inverse temperature
  - `--input_file`  Name of the input file
  - `--output_file`  Name of the output file
  - `--group`  Name of the HDF5 group in the input file, that contains imaginary time data, it has to contain `mesh` and `data` datasets.
  - `--kind`  Type of analytical continuation, currently only `NEVANLINNA` is implemented.

The command `ac.exe --help` will provide additional information.
