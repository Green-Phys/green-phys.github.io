---
title: Post-Processing with Green-MBTools (Pesto)
linkTitle: Pesto (Post-Processing)
weight: 3
math: true
---

The [Green-MBTools package](https://github.com/Green-Phys/green-mbtools) is a Python toolkit for initialization and post-processing of Green's function calculations in the Green Software Package.
It has two sub-modules:

* `mint` (Mean-field INput generation Toolkit) generates input files for the Green WeakCoupling and SEET solvers.
* `pesto` (Post-processing Evaluation Software TOols) provides post-processing tools such as analytic continuation, Wannier interpolation, orthogonalization schemes, Mulliken analysis, and Matsubara transformations.

This tutorial focuses on `pesto`.

{{< note >}}
`green_mbtools.pesto` was previously distributed as the standalone `mbanalysis` package. Existing scripts that do `from mbanalysis import mb` will keep working, since `mbanalysis` is kept as a compatibility alias for `green_mbtools.pesto`.
{{< /note >}}

For a complete guide and source-code documentation, see the [package website](https://green-phys.github.io/green-mbtools).
Several example Python scripts for the `pesto` module are provided in the [GitHub repository](https://github.com/Green-Phys/green-mbtools/tree/master/examples); the key components are walked through below.

## Installation

To install the `green-mbtools` binary package, run

```Shell
pip install green-mbtools
```

This is also covered in the [installation](/docs/installation/from_sources) and [input preparation](/docs/getting-started/preparing_input) guides.
For more detail, see the [Green-MBTools package website](https://green-phys.github.io/green-mbtools).

## Quickstart

Several [example scripts](https://github.com/Green-Phys/green-mbtools/tree/master/examples) covering post-processing of Green output are provided in the Green-MBTools repository.
For a detailed explanation of these scripts, see the [package website](https://green-phys.github.io/green-mbtools/examples.html).

A typical post-processing pipeline has four steps: initialize the post-processing class, interpolate onto a high-symmetry path, orthogonalize the basis, and analytically continue to the real axis.
The snippets below build on one another and share a single set of imports:

```python
from ase.spacegroup import crystal
from green_mbtools.pesto import mb, orth
import matplotlib.pyplot as plt
import numpy as np
```

{{< tip >}}
Migrating an older script? Replace `from mbanalysis import mb` with `from green_mbtools.pesto import mb` -- the API is unchanged.
{{< /tip >}}

### Step 1: Initialize the post-processing class

To post-process `green-mbpt` output, initialize the `MB_post` class from the input, output, and Matsubara-grid (IR grid) files:

```python
# path to files
input_path = "path/to/input.h5"
output_path = "path/to/sim.h5"
ir_path = "path/to/ir/grid.h5"

my_mb = mb.initialize_MB_post(output_path, input_path, ir_path)
```

### Step 2: Wannier interpolation

For solid-state calculations, quantities such as orbital occupancy and the spectral function are usually plotted along the
high-symmetry path connecting special _k_-points in the Brillouin zone. Simulations, however, run on an evenly sampled
_k_-point mesh, so interpolating results onto the high-symmetry path is a necessary post-processing step. The
`wannier_interpolation` member function handles this:

```python
# high-symmetry path, e.g. for silicon
a, b, c = 5.43, 5.43, 5.43  # angstroms
alpha, beta, gamma = 90, 90, 90  # angles
group = 227
cc = crystal(
    symbols=['Si', 'Si'],
    basis=[(0.0, 0.0, 0.0), (0.25, 0.25, 0.25)],
    spacegroup=group,
    cellpar=[a, b, c, alpha, beta, gamma], primitive_cell=True
)
path = cc.cell.bandpath('LGXKGK', npoints=100)
kpts_inter = path.kpts

G_tk_int, Sigma_tk_int, tau_mesh, Fk_int, Sk_int = my_mb.wannier_interpolation(kpts_inter, hermi=True)
```

`kpts_inter` gives the _k_-points onto which results are interpolated, and `hermi=True` tells the routine that the
interpolated quantities are Hermitian. The interpolation returns:

* `G_tk_int`: Green's function
* `Sigma_tk_int`: self-energy
* `tau_mesh`: imaginary-time grid
* `Fk_int`: Fock matrix (including the static part of the self-energy)
* `Sk_int`: overlap matrix

{{< tip >}}
Interpolation accuracy depends on the density of the original Brillouin-zone grid. For better accuracy, use PySCF to
compute the one-body Hamiltonian and overlap matrix directly along the high-symmetry path instead of interpolating them. See
[examples/useful_scripts/nvnl_winter_analysis.py](https://github.com/Green-Phys/green-mbtools/tree/master/examples/useful_scripts/nvnl_winter_analysis.py)
for an example.
{{< /tip >}}

### Step 3: Orthogonalization

Simulations in _Green_ are performed in the atomic-orbital basis, which is non-orthogonal. The `green_mbtools.pesto.orth`
module transforms the output Green's function and self-energy into an orthonormal basis, which is better suited to
visualization and analysis.

Green-MBTools supports three orthogonalization schemes: symmetric atomic orbitals (AO), canonical AO, and molecular orbitals.
Here's an example using symmetric AOs:

```python
gtau_orth = orth.sao_orth(G_tk_int, Sk_int, type='g')
```

Orthogonalizing a Green's function or density matrix differs from orthogonalizing a Fock matrix or self-energy; the
`type` keyword tells `sao_orth` which case applies:

* `type='g'` for a Green's function or density matrix,
* `type='f'` for a Fock or self-energy matrix.

### Step 4: Analytic continuation

Green simulations run on the imaginary-time and Matsubara-frequency axes. To obtain the spectral function, these results
must be analytically continued to the real-frequency axis.

Green-MBTools supports four analytic continuation methods:

* Nevanlinna (default),
* Caratheodory,
* Pole estimation and semi-definite relaxation (PES), and
* Maxent.

Nevanlinna offers a good balance of accuracy and stability in our experience, so it's exposed as a default member
function of `MB_post`:

```python
# Nevanlinna analytic continuation to get the spectral function on the real axis,
# with frequencies between -5 and 5 a.u. over 1001 grid points and a broadening of 0.01
freqs, Aw = my_mb.AC_nevanlinna(gtau_orth=gtau_orth, n_real=1001, w_min=-5.0, w_max=5.0, eta=0.01)

# trace over spin, k-points, and orbitals
Aw_traced = np.einsum('wska -> w', Aw)

# plot the density of states
freqs_ev = freqs * 27.211  # convert frequency from a.u. to eV
plt.plot(freqs_ev, Aw_traced)
plt.show()
```

### Putting it all together

```python
from ase.spacegroup import crystal
from green_mbtools.pesto import mb, orth
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    # Step 1: initialize
    input_path = "path/to/input.h5"
    output_path = "path/to/sim.h5"
    ir_path = "path/to/ir/grid.h5"
    my_mb = mb.initialize_MB_post(output_path, input_path, ir_path)

    # Step 2: Wannier interpolation (silicon high-symmetry path)
    a, b, c = 5.43, 5.43, 5.43
    alpha, beta, gamma = 90, 90, 90
    cc = crystal(
        symbols=['Si', 'Si'],
        basis=[(0.0, 0.0, 0.0), (0.25, 0.25, 0.25)],
        spacegroup=227,
        cellpar=[a, b, c, alpha, beta, gamma], primitive_cell=True
    )
    kpts_inter = cc.cell.bandpath('LGXKGK', npoints=100).kpts
    G_tk_int, Sigma_tk_int, tau_mesh, Fk_int, Sk_int = my_mb.wannier_interpolation(kpts_inter, hermi=True)

    # Step 3: orthogonalize to the symmetric-AO basis
    gtau_orth = orth.sao_orth(G_tk_int, Sk_int, type='g')

    # Step 4: analytically continue and plot the density of states
    freqs, Aw = my_mb.AC_nevanlinna(gtau_orth=gtau_orth, n_real=1001, w_min=-5.0, w_max=5.0, eta=0.01)
    Aw_traced = np.einsum('wska -> w', Aw)
    freqs_ev = freqs * 27.211

    plt.plot(freqs_ev, Aw_traced)
    plt.show()
```

## Other useful scripts

Practical scripts combining initialization, Wannier interpolation, orthogonalization, and analytic continuation are
available in the [examples/useful_scripts](https://github.com/Green-Phys/green-mbtools/tree/master/examples/useful_scripts)
directory:

* `nvnl_winter_analysis.py` supports various orthogonalization schemes and returns the full orbital-resolved spectral
  function and occupancies along a specified high-symmetry path.
* `nvnl_winter_mol.py` provides the same functionality for molecules; `plot_dos_mol.py` plots the resulting molecular
  density of states.
* `wannier_fock.py` is a fast, inexpensive script that interpolates DFT results along the high-symmetry path to
  generate mean-field band structures.
* `wannier_occ.py` interpolates the density matrix and occupation numbers along the high-symmetry path.
