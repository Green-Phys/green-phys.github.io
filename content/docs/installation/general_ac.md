---
title: Analytical Continuation
linkTitle: Analytical Continuation
weight: 2
---

### Analytical continuation package

{{% steps %}}

### Prerequisites: HPC libraries and tools
Please make sure to have the following third-party software installed and available:

  * Third-Party Dependencies
    - Eigen3 >= 3.4.0
    - MPI
    - HDF5 >= 1.10.0
    - BLAS
    - CMake >= 3.18
    - GMP

These packages are the same as the ones required for the mbpt code, except for GMP. [GMP](https://gmplib.org/) is a multiple-precision floating-point library. If it is installed but your compiler does not find it automatically, try setting the environment variable GMP_DIR to specify the directory where cmake should look for gmp.h and the gmp libraries.

### Download and Build
The following instructions will download and build the Analytical Continuation package (replace /path/to/install/directory with the directory where you'd like to install the code):

```ShellSession
  git clone https://github.com/Green-Phys/green-ac.git
  cmake -S green-ac -B green-ac-build                     \
          -DCMAKE_INSTALL_PREFIX=/path/to/install/directory \
          -DCMAKE_BUILD_TYPE=Release
  cmake --build green-ac-build -j 4 
  cmake --build green-ac-build -t test install
```

If dependencies are installed under a non-default prefix, pass it during
configuration, for example `-DCMAKE_PREFIX_PATH="$CONDA_PREFIX"` for an active
Conda environment. This gives CMake one common search root for MPI, HDF5, BLAS,
Eigen, and GMP. For a package-specific override, the following pointers may
help:
  - For Eigen: specify `-DEigen3_DIR=/path/to/lib/cmake/eigen3`, pointing to the directory that contains `Eigen3Config.cmake`
  - For MPI: Follow the instructions on [cmake with mpi](https://cmake.org/cmake/help/latest/module/FindMPI.html)
  - For BLAS: Follow the instructions on [cmake with BLAS](https://cmake.org/cmake/help/latest/module/FindBLAS.html)
  - For HDF5: Follow the instructions on [cmake with HDF5](https://cmake.org/cmake/help/latest/module/FindHDF5.html)
  - For GMP: specify in the environment variable `GMP_DIR`: `GMP_DIR=/path/to/gmp/installation`
{{% /steps %}}


### Installation issues
   If you encounter issues with compiling, installing, or testing the package please file an issue on our issues server [page](https://github.com/Green-Phys/green-mbpt/issues/new/choose), and we will do our best to help.
   Help is also available on our [discord server](https://discord.gg/ty9FE6u3mg).
