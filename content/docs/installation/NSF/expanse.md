---
title: SDSC Expanse
weight: 2
---

## Installation on SDSC Expanse

{{% steps %}}

### Load necessary modules

```ShellSession
 module load gcc 
 module load cmake/3.21.4 mvapich2/2.3.7 hdf5/1.10.7 eigen/3.4.0 openblas/dynamic/0.3.7
```
   - Notice that we use mvapich2 as an MPI implementation
   - We strongly advice you to use openblas/dynamic/0.3.7 module for BLAS implementation. Other BLAS modules cause errors when combined with Eigen.

### Download Green Many-Body framework and create build directory

We recommend building a specific released version — for example the latest stable [`v0.3.2`](https://github.com/Green-Phys/green-mbpt/releases/tag/v0.3.2) or the latest pre-release [`v1.0.0a1`](https://github.com/Green-Phys/green-mbpt/releases/tag/v1.0.0a1). See the [releases page](https://github.com/Green-Phys/green-mbpt/releases) for newer tags.

```ShellSession
 git clone --branch v0.3.2 --depth 1 https://github.com/Green-Phys/green-mbpt
 cd green-mbpt
 mkdir build
 cd build
```
### Build code
```ShellSession
 CC=mpicc CXX=mpicxx cmake .. -DCMAKE_BUILD_TYPE=Release
 make -j 8 && make test
```

   - Make sure to specify `CC=mpicc` and `CXX=mpicxx`, HDF5 library headers include `<mpi.h>` if MPI module is loaded even if your code does not use MPI.

{{% /steps %}}