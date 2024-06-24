---
title: Preparing Input (PySCF)
linkTitle: Preparing Input (PySCF)
weight : 1
---

The first step of any simulations with `Green` is the preparation of the input data, which includes the calculation of the Coulomb and one-body integrals as well as a starting density matrix out of geometry, atom, k-point, and basis information.
`Green` provides a convenient `python` package `green-mbtools` Currently we use an interface with [PySCF](https://pyscf.org/) to prepare input data.
If your python installation does not have `green-mbtools` available (type `python` and, in the python prompt, `import green_mbtools`), you will need to follow the instructions at [PyPI](https://pypi.org/project/green-mbtools) 
or execute `pip install green-mbtools`.

## Initial Mean Field solution

To generate input data a user has to call the `python/init_data_df.py` script located either in the source directory or in the installation directory (for a simple example see the [Si example](./examples/si)).
The following parameters are mandatory:

  - `--a`  path to a file containing the crystal geometry in the xyz format.
  - `--atom`  path to a file containing the unit cell description.
  - `--nk`  number of the reciprocal space points in each direction.
  - `--basis`  Gaussian basis set. The basis set can be specified either as a single basis for every atom in the unit cell or for each atom individually.

### Pseudopotentials

Some basis sets require to use effective potential for core electron that are removed from the calculation. For that reason `Green` allows to specify
psuedo potential using `--pseudo` keyword. 

By default the script will  `init_data_df.py` will generate the file `input.h5`. This file contains all necessary parameters and an initial mean-field solution of the system. In addition, the script will generate the `df_int` and `df_hf_int` directories
which contain the Coloumb and one-body integrals of the system.

### High-symmetry path

After the simulation is performed, results (such as band structures) could be displayed along a high-symmetry path.
Before performing Green's function calculations, it helps to prepare the overlap matrix and one-electron integrals along this path in the Brillouin zone.
To obtain these quantities, we use `init_data_df.py` once again, but with the flag `--job sym_path`.
In addition to this option, one needs to specify the high-symmetry points on the path and the total number of points along the path by providing the two parameters `--high_symmetry_path` and `--high_symmetry_path_points`.
To see all available high-symmetry points for a chosen system, use theoption `--print_high_symmetry_points`.


## Coulomb integrals generation

### Finite size correction
