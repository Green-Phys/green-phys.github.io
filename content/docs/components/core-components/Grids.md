---
title: Sparse grid utilities for IR and Chebyshev representations
linkTitle: Time/Frequency grids
weight: 4
---

Sparse grid utilities for IR and Chebyshev representations

## Essential contents for a temperature-independent sparse grid

- `stats`: Bose or Fermi statistics.
- `xgrid`: Real space grid points in $x \in (-1, 1)$.
- `ngrid`: Frequency space grid points in Matsubara indices $n$, such that
  $\omega_n = (2n+\zeta)\pi/\beta$.
- `wgrid`: Frequency space grid points assuming $\beta=1$.
- `uxl`: Transformation matrix from the basis representation `l` to real space
  grid points `x`.
- `ulx`: Inverse of `uxl`.
- `u1l_pos`: Basis representation for $x=+1$.
- `u1l_neg`: Basis representation for $x=-1$.
- `uwl`: Transformation matrix from the basis representation `l` to frequency
  space grid points `w`.
- `ulw`: Inverse of `uwl`.
- `metadata`: Group for representation-depend information, for example:
    - For Chebyshev: `ncoeff` for maximum number of coefficients.
    - For IR: `lambda` for dimensionless cutoff $\Lambda$, `ncoeff` for maximum
      number of coefficients.

## Directory structure

- `python/sparse_grid/`: python code for generating and parsing sparse grid data.
    - `python/sparse_grid/ir/`: IR-specific code.
    - `python/sparse_grid/chebyshev/`: Chebyshev-specific code.
    - `python/sparse_grid/repn.py`: Common module interface for representations.
    - `python/generate.py`: Script for generating HDF5 archives.
- `c++/`: C++ interface for loading and representing sparse grid data.
    - `green/grids/`: Public headers.
- `data/`: Pre-generated data files.
- `examples`: Usage examples.

## Dependencies

- Python:
    - Hiroshi's `sparse_ir`
    - `numpy`, `scipy`, `h5py`, `mpmath`, ...
- C++:
    - Green/h5pp: for compatibility with h5py
    - Green/ndarrays: for compatibility with numpy.ndarray
    - Green/params: for comandline parameters

