---
title: Installation on NERSC Perlmutter
linkTitle: NERSC Perlmutter
weight: 2
---


### Weak-coupling Many-Body Perturbation theory solver

{{% steps %}}

### Setup Build Environment

Code has been tested for the following NERSC programming environments:

   - `PrgEnv-gnu/8.5.0`
   - `PrgEnv-intel/8.5.0`
   - `PrgEnv-aocc/8.5.0`
   - `PrgEnv-cray/8.5.0`

Load an environment by calling

```Shell
module load PrgEnv-gnu/8.5.0
```

Load third-party libraries

```Shell
module load cray-hdf5 eigen cmake
```

### Download and build the Many-Body Perturbation theory solver


{{% tabs items="CPU, GPU" %}}

{{% tab %}}
  ```Bash Session
  git clone https://github.com/Green-Phys/green-mbpt
  mkdir build
  cd build
  cmake -DCMAKE_BUILD_TYPE=Release ../green-mbpt
  make -j 4 && make test
  ```

{{% /tab %}}
{{% tab %}}
  ```Bash Session
  git clone https://github.com/Green-Phys/green-mbpt
  mkdir build
  cd build
  cmake ../green-mbpt -DCMAKE_BUILD_TYPE=Release -DCUSTOM_KERNEL=GPU_KERNEL \
           -DGREEN_KERNEL_URL="https://github.com/Green-Phys/green-gpu" \
           -DGREEN_CUSTOM_KERNEL_LIB="GREEN::GPU" \
           -DGREEN_CUSTOM_KERNEL_ENUM=GPU \
           -DGREEN_CUSTOM_KERNEL_HEADER=\<green/gpu/gpu_factory.h\>
  make -j 4 && ctest -j 1
  ```

{{% /tab %}}


{{% /tabs %}}


### Job script example

{{% tabs items="CPU, GPU" %}}

{{% tab %}}

  ```Bash Session
  #!/bin/bash

  #SBATCH -N <Number of nodes>
  #SBATCH -C cpu
  #SBATCH -q <QOS>
  #SBATCH -J <Job name>
  #SBATCH -A <Account>
  #SBATCH -t 0:30:0

  # OpenMP settings:
  export OMP_NUM_THREADS=1
  export OMP_PLACES=threads
  export OMP_PROC_BIND=spread
  export HDF5_USE_FILE_LOCKING=FALSE

  #run the application:
  srun -n 64 <build directory>/mbpt.exe --grid_file ir/1e4.h5 \
                                      --beta 100 \
                                      --scf_type GW \
                                      --itermax=1 \
                                      --results_file Si.h5 \
                                      --jobs SC
```

{{% /tab %}}
{{% tab %}}

  ```Bash Session
  #!/bin/bash

  #SBATCH -N <Number of nodes>
  #SBATCH -C gpu
  #SBATCH -q <QOS>
  #SBATCH -J <Job name>
  #SBATCH -A <Account>
  #SBATCH -t 0:30:0
  #SBATCH --gpus-per-task=4

  # OpenMP settings:
  export OMP_NUM_THREADS=1
  export OMP_PLACES=threads
  export OMP_PROC_BIND=spread
  export HDF5_USE_FILE_LOCKING=FALSE

  #run the application:
  srun -n 64 <build directory>/mbpt.exe --grid_file ir/1e4.h5 \
                                      --beta 100 \
                                      --scf_type GW \
                                      --itermax=1 \
                                      --kernel GPU \
                                      --cuda_low_gpu_memory false \
                                      --cuda_low_cpu_memory false \
                                      --results_file Si.h5 \
                                      --jobs SC
```

{{% /tab %}}


{{% /tabs %}}

{{% /steps %}}

***
