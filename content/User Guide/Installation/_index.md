---
title: Installation
weight: 1
---

### Weak-coupling Many-Body Perturbation theory solver

0. Please make sure to have the following third-party software installed and available:

  * Third-Party Dependencies
    - Eigen3 >= 3.4.0
    - MPI
    - HDF5 >= 1.10.0
    - BLAS
    - CMake >= 3.18

    These packages are external to Green. Their installation will depend on your computer. Eigen3 is a C++ matrix library, you can find more information [here](https://eigen.tuxfamily.org/). MPI is the Message Passing Interface, several standard implementations exist, including [OpenMPI](https://www.open-mpi.org/) and [MPICH](https://www.mpich.org/). High performance computers will have proprietary MPI installations, and most clusters provide a version for all users. [HDF5](https://www.hdfgroup.org/solutions/hdf5/) is a library for binary data storage. More information on  BLAS, the Basic Linear Algebra System, can be found on [netlib.org](netlib.org). However, most computers provide highly optimized versions tuned for their respective hardware. Do NOT install the reference BLAS from netlib but instead have a look at a generic high-performance implementation from [OpenBLAS](https://www.openblas.net/) and the hardware-specific vendor libraries (among many others: [Apple](https://developer.apple.com/documentation/accelerate/blas/), [Intel MKL/OneAPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/onemkl.html), [AMD AOCL](https://www.amd.com/en/developer/aocl.html), [IBM ESSL](https://www.ibm.com/docs/en/essl/6.2?topic=whats-new)).
    [Cmake](https://cmake.org/) is a build system that will find the locations of the above packages and generate compilation instructions in Makefiles.

1. The following instructions will download and build the Many-Body Perturbation theory solver (replace /path/to/install/directory with the directory where you'd like to install the code):

  ```ShellSession
  $ git clone https://github.com/Green-Phys/green-mbpt
  $ mkdir build
  $ cd build
  $ cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/path/to/install/directory ../green-mbpt
  $ make -j 4 && make test
  ```

If you have a non-standard installation location of the dependent packages installed in step 1, cmake will fail to find the package. Green uses the standard cmake mechanism (FindXXX.cmake) to find  packages. The following pointers may help:
  - For Eigen: specify in the cmake line: -DEigen3_DIR=/header/directory/of/eigen
  - For MPI: Follow the instructions on [cmake with mpi](https://cmake.org/cmake/help/latest/module/FindMPI.html)
  - For BLAS: Follow the instructions on [cmake with BLAS](https://cmake.org/cmake/help/latest/module/FindBLAS.html)
  - For HDF5: Follow the instructions on [cmake with HDF5](https://cmake.org/cmake/help/latest/module/FindHDF5.html)

***

After successfully building the code, you will need to install it. The install location is either specified with -DCMAKE_INSTALL_PREFIX=/path/to/install/directory as a cmake command during configuration or can be edited in CMakeCache.txt after compilation (see [cmake manual](https://cmake.org/cmake/help/latest/variable/CMAKE_INSTALL_PREFIX.html)).

  ```ShellSession
  $ cmake install
  ```
Your install directory will be created; if everything was successful you can find the executable mbpt.exe under the bin directory of your installation path.

2. The code has been tested on the following national-wide HPC resources:

  - [NSF (ACCESS) Machines](/user-guide/installation/nsf/)
    - [SDSC Expanse](/user-guide/installation/nsf/expanse/)
  - [DOE Machines](/user-guide/installation/doe/)
    - NERSC Perlmutter
  If you would like to have the code tested on additional machines please let us know by filing an [issue](https://github.com/Green-Phys/green-mbpt/issues).

3. Installation issues
   If you encounter issues with compiling, installing, or testing the package please file an issue on our github issues page, [https://github.com/Green-Phys/green-mbpt/issues](https://github.com/Green-Phys/green-mbpt/issues), and we will do our best to help.
