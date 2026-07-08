---
title: General Installation on Linux machines
linkTitle: General Installation
weight: 1
---

{{< tabs items="Weak-Coupling Code, Continuation" >}}

{{< tab >}}
### Weak-coupling Many-Body Perturbation theory solver

{{% steps %}}

### Prerequisites: HPC libraries and tools
Building Green requires a C++17 compiler, a working build toolchain, and the
following third-party software:

  * Third-Party Dependencies
    - Eigen3 >= 3.4.0
    - MPI
    - HDF5 >= 1.10.0
    - BLAS
    - CMake >= 3.18
    - CUDAToolkit >= 11.0 (optional, CUDA 13+ supported)

  On a workstation, a package manager can install the compiler and libraries
  together. For example:

  ```ShellSession
  conda install -c conda-forge cxx-compiler cmake eigen hdf5 openmpi openblas gmp
  ```

  or, on macOS with Homebrew:

  ```ShellSession
  brew install cmake eigen hdf5 open-mpi openblas gmp
  ```

  or, on macOS with MacPorts:

  ```ShellSession
  sudo port install cmake eigen3 hdf5 openmpi OpenBLAS gmp
  ```

  Activate the Conda environment, or ensure the Homebrew or MacPorts packages
  are on your search path, before configuring the build. HPC systems commonly
  provide the same compiler and libraries through environment modules instead.

  These packages are external to Green. Their installation will depend on your computer. Important: ensure there is only one version of each dependency being used across all steps. Eigen3 is a C++ matrix library, you can find more information [here](https://eigen.tuxfamily.org/). MPI is the Message Passing Interface, several standard implementations exist, including [OpenMPI](https://www.open-mpi.org/) and [MPICH](https://www.mpich.org/). High performance computers will have proprietary MPI installations, and most clusters provide a version for all users. [HDF5](https://www.hdfgroup.org/solutions/hdf5/) is a library for binary data storage. More information on  BLAS, the Basic Linear Algebra System, can be found on [netlib.org](https://netlib.org). However, most computers provide highly optimized versions tuned for their respective hardware. Do NOT install the reference BLAS from netlib but instead have a look at a generic high-performance implementation from [OpenBLAS](https://www.openblas.net/) and the hardware-specific vendor libraries (among many others: [Apple](https://developer.apple.com/documentation/accelerate/blas/), [Intel MKL/OneAPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html), [AMD AOCL](https://www.amd.com/en/developer/aocl.html), [IBM ESSL](https://www.ibm.com/docs/en/essl/6.2?topic=whats-new)).
    [Cmake](https://cmake.org/) is a build system that will find the locations of the above packages and generate compilation instructions in Makefiles. [CUDA](https://developer.nvidia.com/cuda-toolkit) is an Nvidia GPU development environment.

### Prerequisites: Python Libraries
Please make sure to have Python and the `green-mbtools` package available.
`green-mbtools` declares PySCF, Numba, spglib, ASE, and its other Python
dependencies, so pip installs them automatically:

  ```ShellSession
  python -m pip install green-mbtools
  ```

  Numba depends on `llvmlite`. On platforms for which pip does not provide a
  compatible `llvmlite` wheel, pip attempts a lengthy source build that also
  requires a compatible LLVM installation. Check the installation output for
  this fallback and allow additional build time, or install a compatible LLVM
  toolchain before retrying. See the
  [llvmlite installation guide](https://llvmlite.readthedocs.io/en/latest/admin-guide/install.html)
  for source-build requirements.

  The minimal supported Python version is 3.8 (any minor version up to 3.12.x
  should work). For help with Python package installation, see the
  [pip documentation](https://pip.pypa.io/en/stable/installation/).

### Download and Build: CPU version
The following instructions will download and build the CPU-only version of the Many-Body Perturbation theory solver (replace /path/to/install/directory with the directory where you'd like to install the code).

To install a specific release, pass `--branch` with the desired tag. Check the [releases page](https://github.com/Green-Phys/green-mbpt/releases) for the latest tag, then clone:

  ```ShellSession
  git clone --branch <tag> --depth 1 https://github.com/Green-Phys/green-mbpt
  ```

To instead track the development tip, omit `--branch`:

The first CMake configure requires network access. Green uses CMake
`FetchContent` to download its `green-*` component libraries and, when tests
are enabled, Catch2. On an offline HPC system, configure the project only after
arranging access to those sources or pre-populating CMake's dependency cache.

  ```ShellSession
  git clone https://github.com/Green-Phys/green-mbpt
  ```

Then configure and build:

  ```ShellSession
  cmake -S green-mbpt -B green-mbpt-build               \
       -DCMAKE_INSTALL_PREFIX=/path/to/install/directory  \
       -DCMAKE_BUILD_TYPE=Release
  cmake --build green-mbpt-build -j 4
  cmake --build green-mbpt-build -t test
  ```

A successful test run ends with CTest reporting
`100% tests passed, 0 tests failed`. The number of discovered tests and the
runtime vary with the Green release, enabled options, machine, and build
parallelism. On macOS, the linker
may also report harmless `duplicate -rpath ... ignored` warnings; these do not
indicate a failed build when linking completes and the tests pass.

If dependencies are installed under a non-default prefix, add that prefix to
the configure command. For an active Conda environment, for example:

  ```ShellSession
  cmake -S green-mbpt -B green-mbpt-build               \
       -DCMAKE_INSTALL_PREFIX=/path/to/install/directory  \
       -DCMAKE_PREFIX_PATH="$CONDA_PREFIX"                 \
       -DCMAKE_BUILD_TYPE=Release
  ```

`CMAKE_PREFIX_PATH` gives CMake one common search root for packages including
MPI, HDF5, BLAS, and Eigen. Separate multiple prefixes with semicolons. For a
package-specific override, the following pointers may help:
  - For Eigen: specify `-DEigen3_DIR=/path/to/lib/cmake/eigen3`, pointing to the directory that contains `Eigen3Config.cmake`
  - For MPI: Follow the instructions on [cmake with mpi](https://cmake.org/cmake/help/latest/module/FindMPI.html)
  - For BLAS: Follow the instructions on [cmake with BLAS](https://cmake.org/cmake/help/latest/module/FindBLAS.html)
  - For HDF5: Follow the instructions on [cmake with HDF5](https://cmake.org/cmake/help/latest/module/FindHDF5.html)

***

After successfully building the code, you will need to install it. The install location is specified with `-DCMAKE_INSTALL_PREFIX=/path/to/install/directory` as a cmake command during configuration or can be 
changed by explicitly providing a new installation path to the `--prefix` parameter during the installation phase (see [cmake manual](https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake--install-0)).
To install the code run:

  ```ShellSession
  cmake --install green-mbpt-build
  ```
Your install directory will be created. A successful installation places the
following executables under its `bin` directory:

  - `mbpt.exe`
  - `embedding.exe`
  - `int-transform.exe`

### Download and Build: Nvidia GPU kernels

GPU kernels for the many-body perturbation framework use extensions from a custom repository. You enable the GPU kernels by setting the following CMake parameter:
   - `CUSTOM_KERNELS="https://github.com/Green-Phys/green-gpu"`

By default, code is generated for sm_80, sm_86, and sm_90 (Ampere and Hopper). To target a specific GPU, add `-DGPU_ARCHS="<cc>"`, where `<cc>` is your GPU's compute capability with the dot removed (e.g. `89` for compute capability 8.9). You can find your GPU's compute capability with:

  ```ShellSession
  nvidia-smi --query-gpu=compute_cap --format=csv,noheader
  ```

The following instructions will download and build the Many-Body Perturbation theory solver with additional GPU kernels (replace /path/to/install/directory with the directory where you'd like to install the code). Use the same `--branch` approach described above to target a specific release. Then configure and build:

  ```ShellSession
  git clone https://github.com/Green-Phys/green-mbpt
  cmake -S green-mbpt -B green-mbpt-build                         \
     -DCMAKE_INSTALL_PREFIX=/path/to/install/directory              \
     -DCMAKE_BUILD_TYPE=Release                                     \
     -DCUSTOM_KERNELS="https://github.com/Green-Phys/green-gpu"
  cmake --build green-mbpt-build -j 4
  cmake --build green-mbpt-build -t test
  cmake --install green-mbpt-build
  ```

{{% /steps %}}

### Download and Build: National HPC Resources
The code has been successfully built and tested on National HPC resources. Instructions for the compilation on these machines are provided below:
  - [NSF (ACCESS) Machines](/docs/installation/nsf/)
    - [SDSC Expanse](/docs/installation/nsf/expanse/)
  - [DOE Machines](/docs/installation/doe/)
    - [NERSC Perlmutter](/docs/installation/doe/perlmutter)

If you would like to have the code tested on additional machines please let us know by filing an [issue](https://green-phys.youtrack.cloud/newIssue).

### Installation issues
   If you encounter issues with compiling, installing, or testing the package please file an issue on our github issues [page](https://green-phys.youtrack.cloud/newIssue), and we will do our best to help.


{{< /tab >}}
{{< tab >}}

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
   If you encounter issues with compiling, installing, or testing the package please file an issue on our issues server [page](https://green-phys.youtrack.cloud/newIssue), and we will do our best to help.
   Help is also available on our [discord server](https://discord.gg/ty9FE6u3mg).



{{< /tab >}}

{{< /tabs >}}
