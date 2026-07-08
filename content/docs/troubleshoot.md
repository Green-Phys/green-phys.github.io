---
title: Solutions to common problems
linkTitle: Troubleshooting
icon: troubleshoot
weight: 6
math: true
prev: "/docs/tutorials"
---

## Calculation does not converge

Quite often the self-consistent iterations will not lead to a converged solution. There are several possible causes for calculation to diverge, the two main reasons are:
  - Self-consistent iterations are unstable;
  - Non-uniform Fourier transform has a large leakage.

### Instability of self-consistent iterations
When the initial starting point of the self-consistent iterations lays far away from the solution, iterative solver may experience one 
of the following behavior: diverge, oscilate between multiple meta-stable points, show no pattern of divergence or convergence.

To stabilize the self-consistent iterations `Green` provides several options.
By default we choose to use a simple mixing of the self-energy, where the self-energy at the current iteration is mixed with the 
self-energy from the previous iteration. Adjusting the mixing parameter (choosing smaller value for `--mixing_weight` parameter)
can usually stabilize convergence but makes it slower. In many cases the better option is to use
advanced convergence acceleration techniques, such as direct inversion in the iterative subspace (DIIS)  method. For more details
on how to use it read the [DIIS tutorial](/docs/tutorials/diis).

### Large leakage in non-uniform Fourier transformation
All dynamical quantites in `Green` use non-uniform compact representation in imaginary time/Matsubara frequency domain.
The choice of non-uniform grid has to address two main aspects: 
  - being compact to reduce computational complexity;
  - being large enough to properly capture short time/large frequency asymptotic behavior.

If the grid is too small large spectral leakage can occure during the Foruier transfrom in time/frequency domain,
that may result in large calculation errors and potentially break down of self-consistent iterations.
During the calculations, `Green` computes the spectral leakage every time the Fourier transfrom in time/frequency domain
is performed. If the spectral leakage is larger than $10^{-8}$ the following warning message will be printed into standard output:
```ShellSession
WARNING: The leakage is larger than 1e-8
```
When the `Green`/`WeakCoupling` simulations are done in single precision, spectral leakage will almost always exceed $10^{-8}$ cutoff
and we suggest to monitor spectral leakage for couple of iterations and if it does not grow, the calculations are expected to be 
stable and no further actions are needed.

## Build and installation problems

### CMake configure fails with "detected dubious ownership"

CMake uses git internally to clone sub-dependencies via FetchContent. On shared
filesystems or in containers where the directory owner differs from the current
user, git refuses to operate and FetchContent fails with a message such as:

```ShellSession
fatal: detected dubious ownership in repository at '/path/to/build/_deps/...'
```

The fix is to tell git to trust the affected directories:

```ShellSession
git config --global --add safe.directory '*'
```

### GPU build fails: `nvcc fatal: Unsupported gpu architecture 'compute_70'`

CUDA 13 dropped support for sm_70 (Volta) and sm_75 (Turing). If you are on
CUDA 13 or later, pass `-DGPU_ARCHS` to target only your GPU's architecture
instead of relying on the default list:

```ShellSession
nvidia-smi --query-gpu=compute_cap --format=csv,noheader
```

Use the reported value with the dot removed (e.g. `8.9` → `89`) in the CMake
configure step:

```ShellSession
cmake -S green-mbpt -B green-mbpt-build \
    -DCMAKE_BUILD_TYPE=Release            \
    -DCUSTOM_KERNELS="https://github.com/Green-Phys/green-gpu" \
    -DGPU_ARCHS="89"
```
