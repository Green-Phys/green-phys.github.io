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
Please make sure to have the following third-party software installed and available:

  * Third-Party Dependencies
    - Eigen3 >= 3.4.0
    - MPI
    - HDF5 >= 1.10.0
    - BLAS
    - CMake >= 3.18
    - CUDAToolkit > 12.0 (optional)

  These packages are external to Green. Their installation will depend on your computer. Eigen3 is a C++ matrix library, you can find more information [here](https://eigen.tuxfamily.org/). MPI is the Message Passing Interface, several standard implementations exist, including [OpenMPI](https://www.open-mpi.org/) and [MPICH](https://www.mpich.org/). High performance computers will have proprietary MPI installations, and most clusters provide a version for all users. [HDF5](https://www.hdfgroup.org/solutions/hdf5/) is a library for binary data storage. More information on  BLAS, the Basic Linear Algebra System, can be found on [netlib.org](netlib.org). However, most computers provide highly optimized versions tuned for their respective hardware. Do NOT install the reference BLAS from netlib but instead have a look at a generic high-performance implementation from [OpenBLAS](https://www.openblas.net/) and the hardware-specific vendor libraries (among many others: [Apple](https://developer.apple.com/documentation/accelerate/blas/), [Intel MKL/OneAPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html), [AMD AOCL](https://www.amd.com/en/developer/aocl.html), [IBM ESSL](https://www.ibm.com/docs/en/essl/6.2?topic=whats-new)).
    [Cmake](https://cmake.org/) is a build system that will find the locations of the above packages and generate compilation instructions in Makefiles. [CUDA](https://developer.nvidia.com/cuda-toolkit) is an Nvidia GPU development environment.

### Prerequisites: Python Libraries
Please make sure to have python and the `green-mbtools` python package available. `green-mbtools` python package has the following dependencies:

   * Third-Party Dependencies
     - pySCF
     - numba
     - spglib
     - ase

  These are third-party packages that you can install using your favorite python package manager, such as pip:
  ```ShellSession
  $ pip install green-mbtools pyscf numba spglib ase
  ```

   The minimal supported python version is 3.8 (any minor version up to 3.12.x should work). Note that some installations use pip3 instead of pip, for help on python package installation see https://pypi.org/project/pip/ .

### Download and Build: CPU version
The following instructions will download and build the CPU-only version of the Many-Body Perturbation theory solver (replace /path/to/install/directory with the directory where you'd like to install the code):

  ```ShellSession
  $ git clone https://github.com/Green-Phys/green-mbpt
  $ cmake -S green-mbpt -B green-mbpt-build               \
       -DCMAKE_INSTALL_PREFIX=/path/to/install/directory  \
       -DCMAKE_BUILD_TYPE=Release
  $ cmake --build green-mbpt-build -j 4
  $ cmake --build green-mbpt-build -t test
  ```

If you have a non-standard installation location of the dependent packages installed in step 1, cmake will fail to find the package. Green uses the standard cmake mechanism (FindXXX.cmake) to find packages. The following pointers may help:
  - For Eigen: specify in the cmake line: -DEigen3_DIR=/header/directory/of/eigen
  - For MPI: Follow the instructions on [cmake with mpi](https://cmake.org/cmake/help/latest/module/FindMPI.html)
  - For BLAS: Follow the instructions on [cmake with BLAS](https://cmake.org/cmake/help/latest/module/FindBLAS.html)
  - For HDF5: Follow the instructions on [cmake with HDF5](https://cmake.org/cmake/help/latest/module/FindHDF5.html)

***

After successfully building the code, you will need to install it. The install location is specified with `-DCMAKE_INSTALL_PREFIX=/path/to/install/directory` as a cmake command during configuration or can be 
changed by explicitly providing a new installation path to the `--prefix` parameter during the installation phase (see [cmake manual](https://cmake.org/cmake/help/latest/manual/cmake.1.html#cmdoption-cmake--install-0)).
To install the code run:

  ```ShellSession
  $ cmake --install green-mbpt-build
  ```
Your install directory will be created; if everything was successful you can find the executable mbpt.exe under the bin directory of your installation path.

### Download and Build: Nvidia GPU kernels

GPU kernels for the many-body perturbation framework use extensions from a custom repository. You enable the GPU kernels by setting the following CMake parameter:
   - `CUSTOM_KERNELS="https://github.com/Green-Phys/green-gpu"`

The following instructions will download and build the Many-Body Perturbation theory solver with additional GPU kernels (replace /path/to/install/directory with the directory where you'd like to install the code):

  ```ShellSession
  $ git clone https://github.com/Green-Phys/green-mbpt
  $ cmake -S green-mbpt -B green-mbpt-build                         \
     -DCMAKE_INSTALL_PREFIX=/path/to/install/directory              \
     -DCMAKE_BUILD_TYPE=Release                                     \
     -DCUSTOM_KERNELS="https://github.com/Green-Phys/green-gpu"
  $ cmake --build green-mbpt-build -j 4
  $ cmake --build green-mbpt-build -t test install
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
  $ git clone https://github.com/Green-Phys/green-ac.git
  $ cmake -S green-ac -B green-ac-build                     \
          -DCMAKE_INSTALL_PREFIX=/path/to/install/directory \
          -DCMAKE_BUILD_TYPE=Release
  $ cmake --build green-ac-build -j 4 
  $ cmake --build green-ac-build -t test install
```

If you have a non-standard installation location of the dependent packages installed in step 1, cmake will fail to find the package. Green uses the standard cmake mechanism (FindXXX.cmake) to find packages. The following pointers may help:
  - For Eigen: specify in the cmake line: -DEigen3_DIR=/header/directory/of/eigen
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
