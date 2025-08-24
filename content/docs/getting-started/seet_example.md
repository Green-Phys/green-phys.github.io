---
title: SEET Example
linkTitle: SEET Example
weight : 7
hidden: false
---

{{< tabs items="Installation, Initialization, Integral Transformation, Embedding solution" >}}


{{< tab >}}

### Prerequsite

System libraries:
 1. MPI
 2. HDF5
 3. BLAS
 4. CMake
 5. C++17 compatible compiler

Third party libraries:
 1. Eigen3
 2. Boost

### Install dependencies

First, clone required repositories:

```
git clone https://github.com/ALPSCore/ALPSCore
git clone https://github.com/opencollab/arpack-ng
git clone https://github.com/Q-Solvers/EDLib
git clone https://github.com/Green-Phys/seet_solvers
```

 1. ALPSCore -- Core libraries of ALPS software package

```
cmake -S ALPSCore -B build --install-prefix `pwd`/install/ALPSCore
cmake --build build -j 32
cmake --build build -t test install
rm -rf build
```

 2. ARPACK -- Arnoldi/Lancsoz factorization library

```
cmake -S arpack-ng -B build \
  --install-prefix `pwd`/install/arpack  -DMPI=ON \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 32
cmake --build build -t test install
rm -rf build
```

 3. EDLib -- Exact diagonalization library for quantum electron problems

```
cmake -S EDLib -B build --install-prefix `pwd`/install/EDLib \
  -DCMAKE_BUILD_TYPE=Release \
  -DALPSCore_DIR=`pwd`/install/ALPSCore/share/ALPSCore \
  -DARPACK_DIR=`pwd`/install/arpack -DUSE_MPI=MPI
cmake --build build -j 32
cmake --build build -t install
rm -rf build
```

 4. `seet_solver` -- Exact diagonalization solver for SEET impurity problem
 
```
cmake -S seet_solvers -B build \
   --install-prefix `pwd`/install/seet_solvers \
   -DCMAKE_BUILD_TYPE=Release         \
   -DALPSCore_DIR=`pwd`/install/ALPSCore/share/ALPSCore  \
   -DARPACK_DIR=`pwd`/install/arpack \
   -DEDLib_DIR=`pwd`/install/EDLib/share/EDLib/cmake \
   -DUSE_MPI=MPI
cmake --build build -j 32
cmake --build `pwd`/build -t install
rm -rf build
```

### SEET framework build

```
git clone https://github.com/Green-Phys/green-mbpt
cd green-mbpt
git checkout SEET
cd ..
cmake -S green-mbpt -B build \
   --install-prefix `pwd`/install/green-mbpt \
   -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 32
cmake --build build -t test install
rm -rf build
```

{{< /tab >}}

{{< tab >}}
First, we assume that we have solved weak-coupling problem for the input file `input.h5` and the results are in the `sim.h5` file.

```
python <installation path>/python/init_seet.py --orth true --gf2_input_file sim.h5 \
       --transform_file transform.h5 --active_space 0 1 --active_space 2 3   \
       --from_ibz true --orth_method symmetrical_orbitals --input_file input.h5
```

Here we construct orthogonal transformation matrices using symmetrical orthogonalization. We choose two active subspaces of correlated orbitals (`{0, 1}` and `{2, 3}`),
note that these are orbital numbers in the chosen orthogonal basis. Since `Green` results are obtained in the reduced Brillouin zone we specify `--from_ibz=true`.

As the result we will get `transform.h5` file with orthogonal trasformation matrices and projection matrices.

{{< /tab >}}

{{< tab >}}

The next preprocessing step for SEET solver is the two integrals transformation for embedding problems.
This is done by calling 

```
<installation path>/bin/int-transform.exe --input_file transform.h5 --in_file input.h5 --in_int_file df_int --transform 1
```

Here the following parameters have to be provided:
  - `--input_file` -- file with the trasformation matrices that has been obtained at the previous step
  - `--in_file` -- input file for the weak-coupling problem
  - `--in_int_file` -- path to two body integrals that will be used for impurity problem. Note that `Green` has two sets of integrals,
  one to be used for Hartree-Fock solution, and one that is used for `GW` calculations. We strongly advice using `GW` integrals
  as they contain additional finite-size correction.

This procedure is time consuming and we advice to submit it as job on cluster.

{{< /tab >}}
{{< tab >}}

After all the preparations are done, SEET can be run as

```
<installation path>/bin/embedding.exe --scf_type=GW --BETA 100   \
  --grid_file ir/1e4.h5 --itermax 1 --results_file sim.seet.h5 --weak_results sim.h5 --embedding_type SEET        \
  --mixing_type CDIIS --diis_start 2 --diis_size 5 --mixing_weight 0.3 \
  --seet_input transform.h5 --bath_file bath.txt  \
  --impurity_solver_exec <path to seet ED solver> \
  --impurity_solver_params " --arpack.NEV=8 --arpack.NCV=20 --lanc.NOMEGA=1000 --FREQ_FILE=<installation path>/share/ir/1e4.h5 --FREQ_PATH=/fermi/ngrid " \
  --dc_data_prefix "dc_int" \
  --seet_root_dir "./seet" \
  --spin_symm true
```

The following parameters in additional to regular `Green` parameters are used

 - `--weak_results` -- initial results obtained from weak-coupling solver
 - `--embedding_type` -- type of SEET, `FC_SEET` for full self-consistency, `SEET` for inner self-consistency
 - `--seet_input` -- transformation matricies for impurity problems
 - `--bath_file` -- initial guess for impurity bath parameters
 - `--impurity_solver_exec` -- path to `seet_solvers` exact diagonalization executable
 - `--impurity_solver_params` -- parameters for Exact diagonalization solver
 - `--dc_data_prefix` -- prefix for double-counting directories (has to be `dc_int`)
 - `--seet_root_dir` -- root directory for `SEET` intermediate input/outputs
 - `--spin_symm` -- whether the bath spin-symmetrization is needed during bath-fitting

{{< /tab >}}

{{< /tabs >}}