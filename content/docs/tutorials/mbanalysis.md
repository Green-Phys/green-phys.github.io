---
title: MBAnalysis Package
linkTitle: MBAnalysis
weight: 3
math: true
---

The [Green-MBTools package](https://github.com/Green-Phys/green-mbtools) is a Python toolkit for initialization and post-processing of Green's function calculations in the Green Software Package.
The package has two sub-modules:

* `mint` (Mean-field INput generation Toolkit) generates input files for the Green WeakCoupling and SEET solvers.
* `pesto` (Post-processing Evaluation Software TOols) provides access to various post-processing tools such as analytical continuation, wannier interpolation, orthogonalization schemes, Mulliken analysis and Matsubara transformations.

{{< note >}}
The `green_mbtools.pesto` was previously known as the `mbanalysis` package, and can still be imported with the alias `mbanalysis`.
{{< /note >}}

For a complete guide and source-code documentation, see the [package website](https:://Green-Phys.github.io/green-mbtools).
Several example python scripts for the `pesto` module are provided in the [Github](https://github.com/Green-Phys/green-mbtools/tree/master/examples) repository. Some of the key components are discussed below.

## Installation

To install the `green-mbtools` binary package simply execute

```Shell
pip install green-mbtools
```

This is already explained in the [installation](/content/docs/installation/from_sources.md) and [input preparation](/content/docs/getting-started/preparing_input.md) steps.
For more details on installation, check the [Green-MBTools package website](https://green-phys.github.io/green-mbtools).

## Quickstart

Several [example scripts](https://github.com/Green-Phys/green-mbtools/tree/master/examples) are provided in the
Github repository of the _Green-MBTools_ package, particularly for the post-processing of Green output.
For detailed explanation of these scripts, please visit the [package website](http://Green-Phys.github.io/green-mbtools/examples.html).
A typical post-processing pipeline looks as follows:

### Step 1: Initialise the MB post processing class
To get started with the post-processing of `green-mbpt` output, we can initialize the ``MB_post`` class using the
input, output and Matsubara grid (aka IR grid) files:

```python
from ase.spacegroup import crystal
from green_mbtools.pesto import mb
# alternatively
# from mbanalysis import mb
from green_mbtools.pesto import orth
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":

    # path to files
    input_path = "path/to/input.h5"
    output_path = "path/to/sim.h5"
    ir_path = "path/to/ir/grid.h5"

    # initialize the MB_post class
    my_mb = mb.initialize_MB_post(output_path, input_path, ir_path)
```

### Step 2: Wannier Interpolation
For solid-state calculations, results such as orbital occupancy and spectral function are generally visualized along
the high-symmetry path connecting special (high-symmetry) _k_-points in the Brillouin zone.

On the other hand, simulations are performed on evenly sampled _k_-points. Therefore, interpolation of results is a crucial
step in the post-processing, which can be performed using the `wannier_interpolation` member function:

```python
from ase.spacegroup import crystal
from green_mbtools.pesto import mb
# alternatively
# from mbanalysis import mb
from green_mbtools.pesto import orth
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    
    # initialization part here
    # ...

    # obtain high-symmetry path
    # e.g. assuming we are working with Silicon
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

    # interpolation
    G_tk_int, Sigma_tk_int, tau_mesh, Fk_int, Sk_int = my_mb.wannier_interpolation(kpts_inter, hermi=True)
```

Here, `kpts_inter` provide the kpoints for which the results are interpolated, and `hermi=True` specifies that the
interpolation is performed for Hermitian quantities.
The results of the interpolation are:
* `G_tk_int`: Green's function
* `Sigma_tk_int`: Self-energy
* `tau_mesh`: Imaginary time grid
* `Fk_int`: Fock matrix (with static self-energy)
* `Sk_int`: Overlap matrix

{{< tip >}}
The accuracy of interpolation depends on the density of the original Brillouin zone grid.
To reduce the errors, we recommend using PySCF to directly calculate the one-body Hamiltonain and the
overlap matrix along the high-symmetry path rather than interpolation. See, e.g.,
[examples/useful_scripts/nvnl_winter_analysis.py](https://github.com/Green-Phys/green-mbtools/tree/master/examples/useful_scripts/nvnl_winter_analysis.py>).
{{< /tip >}}


### Step 3: Orthogonalization
Simulations in the _Green_ code are performed in the atomic orbital basis, which is a non-orthogonal basis-set.
Orthogonalization utilities, offered in the `green_mbtools.pesto.orth` library, are required
to transform the output Green's function and self-energies to an orthonormal basis, which is more suited for visualization and analysis.

The _Green-MBTools_ package offers three ways to orthogonalize -- symmetric AO, canonical AO, and molecular orbitals.
Let's see an example with symmetric AOs:

```python
from ase.spacegroup import crystal
from green_mbtools.pesto import mb
# alternatively
# from mbanalysis import mb
from green_mbtools.pesto import orth
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    
    # initialization part here
    # ...

    gtau_orth = orth.sao_orth(G_tk_int, Sk_int, type='g')
```

The orthogonalization procedure for Green's functions or density matrices is different from that for Fock matrix or self-energy.
This can be controlled in the `orth.sao_orth` function using the parameter `type`:
* `type='g'` treats the input arrays as a Green's function or density matrix,
* `type='f'` treats them as Fock or self-energy matrix.


### Step 4: Analytic continuation

AS explained in the [Theory](/content/docs/theory/postprocessing/Analytical_Continuation.md) section,
the simulations inthe Green software suite are performed on the imaginary time and Matsubara frequency axis.
To obtain the spectral function, we need to analytically continue these results on to the real frequency axis.

Several ways are available in the literature to perform the analytic continuation of the Matsubara Green's function.
The _Green-MBTools_ package offers support for four different alternatives:
* Nevanlinna (default),
* Caratheodory,
* Pole Estimation and Semi-definite relaxation, and
* Maxent.

In our experience, Nevanlinna offers a good balance between accuracy and stability.
Therefore, it is provided as a default member function of the `MB_post` class, and can be used as:

```python
from ase.spacegroup import crystal
from green_mbtools.pesto import mb
# alternatively
# from mbanalysis import mb
from green_mbtools.pesto import orth
import matplotlib.pyplot as plt
import numpy as np

if __name__ == "__main__":
    
    # initialization part here
    # ...

    # Interpolation part here
    # ...

    # Orthogonalization part here
    # ...

    # use my_mb to do other tasks
    # e.g., Nevanlinna analytic continuation to get spectral function on real-axis
    # with frequencies between -5 and 5 a.u. with 1001 grid points
    # and broadening parameter of 0.01
    freqs, Aw = my_mb.AC_nevanlinna(gtau_orth=gtau_orth, n_real=1001, w_min=-5.0, w_max=5.0, eta=0.01)

    # trace over spin, k-points and orbitals
    Aw_traced = np.einsum('wska -> w', Aw)

    # plot the density of states
    freqs_ev = freqs * 27.211  # convert frequency from a.u. to eV
    plt.plot(freqs_ev, Aw_traced)
    plt.show()
```

## Other useful scripts

Practical scripts combining initialization, Wannier interpolation, orthogonalization, and analytic continuation for post-processing of Green simulation output are also available in the [examples/useful_scripts](https://Green-Phys/green-mbtools/tree/master/examples/useful_scripts) directory:


* `nvnl_winter_analysis.py` offers a versatile script with support for various orthogonalization schemes, and returns the full orbital resolved spectral function and occupancies along the specified high-symmetry path.
* `nvnl_winter_mol.py` offers a similar functionality for molecules, while `plot_dos_mol.py`
* `wannier_fock.py` provides a fast and inexpensive script to interpolate DFT results along the high-symmetry path and generate mean-field band structures.
* `wannier_occ.py` allows the interpolation of density matrix and occupation numbers along the high-symmetry path
