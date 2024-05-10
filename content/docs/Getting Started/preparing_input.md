---
title: Preparing Input (PySCF)
linkTitle: Preparing Input (PySCF)
weight : 1
---

The first step of any simulations with `Green` is the preparation of the input data, which includes the calculation of the Coulomb and one-body integrals as well as a starting density matrix out of geometry, atom, k-point, and basis information.
Currently  we use an interface with [PySCF](https://pyscf.org/) to prepare input data.
If your python installation does not have pyscf available (type `python` and, in the python prompt, `import pyscf`), you will need to follow the instructions at [PySCF](https://pyscf.org/) or execute `pip install pyscf`. Similarly, since `init_data_df.py` 
depends on the [numba](https://numba.pydata.org/) module, you may need to install it as `pip install numba`.

## Initial Mean Field solution

To generate input data a user has to call the `python/init_data_df.py` script located in the source directory (for a simple example see [next page](/docs/getting-started/si)).
The following parameters are mandatory:

  - `--a`  path to a file containing crystal geometry in xyz format
  - `--atom`  path to a file containing unit cell description
  - `--nk`  number of reciprocal space points in each direction
  - `--basis`  Gaussian basis set, it can be specified as a single basis for every atom in the unit cell or for each atom individually

### Pseudopotentials

Some basis sets require to use effective potential for core electron that are removed from the calculation. For that reason `Green` allows to specify
psuedo potential using `--pseudo` keyword. 

By default the script will  `init_data_df.py` will generate the file `input.h5`. This file contains all necessary parameters and an initial mean-field solution of the system. In addition, the script will generate the `df_int` and `df_hf_int` directories
which contain the Coloumb and one-body integrals of the system.

### High-symmetry path

After the simulation is performed, results (such as band structures) could be displayed along a high-symmetry path. To obtain a specific high-symmetry path,
specify the high-symmetry points on the path and the total number of points along the path by providing the two parameters `--high_symmetry_path` and `--high_symmetry_path_points`.
To see all available high-symmetry points for a chosen system, use theoption `--print_high_symmetry_points`.
The interplation along high-symmetry paths will perform a basic Wannier interpolation.

## Coulomb integrals generation

### Finite size correction