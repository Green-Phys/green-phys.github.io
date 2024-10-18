---
title: NCSA Delta
weight: 1
---

## Installation on NCSA Delta

{{% steps %}}

### Load necessary modules

```ShellSession
 module load gcc/11.4.0 openmpi/4.1.6 cuda/12.4.0 hdf5/1.14.2 python/3.11.6 gcc-runtime/11.4.0 openblas/0.3.25
```

The following modules will be loaded:

```
  1) gcc/11.4.0   2) openmpi/4.1.6   3) cue-login-env/1.0   4) slurm-env/0.1   5) default-s11
  6) python/3.11.6   7) hdf5/1.14.2   8) gcc-runtime/11.4.0   9) openblas/0.3.25  10) cuda/12.4.0
```

### Install Eigen

```ShellSesion
 wget https://gitlab.com/libeigen/eigen/-/archive/3.4.0/eigen-3.4.0.tar.bz2
 bzcat eigen-3.4.0.tar.bz2 | tar -x
 cmake -B eigen-build -S eigen-3.4.0 --install-prefix <install/directory/for/eigen> \
       -DCMAKE_BUILD_TYPE=Release
 cmake --build eigen-build/ -j 32 -t install
```

Here we download the latest version of the Eigen library and install it into the `<install/directory/for/eigen>` directory.

### Download Green Many-Body framework and create build directory

```ShellSession
 git clone https://github.com/Green-Phys/green-mbpt
```
### Build code
```ShellSession
 cmake -S green-mbpt -B green-mbpt-build -DCMAKE_INSTALL_PREFIX=<install/directory/for/GREEN> \
       -DCMAKE_BUILD_TYPE=Release -DCUSTOM_KERNELS="https://github.com/Green-Phys/green-gpu"
 cmake --build green-mbpt-build -j 8
 cmake --build green-mbpt-build -t test
```

Here we configure the `Green` package to use a custom GPU kernel and to be installed into the `<install/directory/for/GREEN>` directory.
After the build is finished, we run tests to check that `Green` package was built successfully (please note that the GPU test will fail as there is no
CUDA-enabled device available on a login node).

### Install code

```ShellSession
 cmake --install green-mbpt-build
```

`Green` will be installed into the directory specified during the build stage. To change the installation location, provide a path to a new location with the `--prefix` parameter.

{{% /steps %}}