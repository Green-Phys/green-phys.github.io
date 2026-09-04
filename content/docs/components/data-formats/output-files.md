---
title: Output Files
linkTitle: Output Files
weight: 2
---

This page describes the GREEN 1.0 output-file contract. Shapes use the [shared notation](/docs/components/data-formats/#dimensions-and-notation).

## Main results file

`green-mbpt` writes its main results to the file selected by `--results_file`, which defaults to `sim.h5`. The root `__grids_version__` attribute appears above the iteration tree.

```text
/
├── iter
└── iterN/
    ├── Sigma1
    ├── Selfenergy/{data,mesh}
    ├── G_tau/{data,mesh}
    ├── Energy_1b
    ├── Energy_HF
    ├── Energy_2b
    └── mu
```

`/iter` is the number of the latest fully written checkpoint, not the group count or a convergence flag.

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/@__grids_version__` | scalar | UTF-8 string | required | GREEN grids-library version used to write the sampled functions. |
| `/iter` | scalar | unsigned integer | required | Latest fully written iteration number. |
| `/iterN/Sigma1` | `[ns,ink,nso,nso]` | complex128 | required | Static self-energy after mixing. |
| `/iterN/Selfenergy/data` | `[nts,ns,ink,nso,nso]` | complex128 | required | Dynamic self-energy on the imaginary-time mesh after mixing. |
| `/iterN/Selfenergy/mesh` | `[nts]` | float64 | required | Imaginary-time sampling points. |
| `/iterN/G_tau/data` | `[nts,ns,ink,nso,nso]` | complex128 | required | Green's function on the imaginary-time mesh after the Dyson solve. |
| `/iterN/G_tau/mesh` | `[nts]` | float64 | required | Imaginary-time sampling points. |
| `/iterN/Energy_1b` | scalar | float64 | required | One-body contribution in Hartree. |
| `/iterN/Energy_HF` | scalar | float64 | required | Hartree-Fock energy including nuclear energy, in Hartree. |
| `/iterN/Energy_2b` | scalar | float64 | required | Correlation/two-body energy in Hartree. |
| `/iterN/mu` | scalar | float64 | required | Chemical potential in Hartree. |

```text
E_total = Energy_HF + Energy_2b
```

`Energy_1b` is a decomposition term and must not be added again. The file does not record convergence residuals, convergence status, timings, method name, or a full parameter snapshot.

Complex output arrays use an HDF5 compound type with float64 real and imaginary components; `h5py` exposes the tested files as `complex128`. This differs from the trailing real/imaginary axis used by the three HF input matrices.

```python
import h5py

with h5py.File("sim.h5", "r") as results:
    iteration = int(results["iter"][()])
    group = results[f"iter{iteration}"]
    green_tau = group["G_tau/data"][...]
    selfenergy_tau = group["Selfenergy/data"][...]
    chemical_potential = float(group["mu"][()])
    total_energy = float(group["Energy_HF"][()] + group["Energy_2b"][()])

print(iteration, green_tau.shape, selfenergy_tau.shape)
print(chemical_potential, total_energy)
```

The numerical quantities use GREEN's atomic-unit convention, but unit attributes are not stored in the datasets.

## High-symmetry-path output

`--high_symmetry_output_file` selects the high-symmetry-path output file, which defaults to `output_hs.h5`. It is paired with the [high-symmetry-path input](/docs/components/data-formats/input-file/#high-symmetry-path-input).

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/@__grids_version__` | scalar | UTF-8 string | required | GREEN grids-library version. |
| `/G_tau_hs/data` | `[nts,ns,nhs_k,nso]` | complex128 | required | Orbital-diagonal Green's function along the selected path. |
| `/G_tau_hs/mesh` | `[nts]` | float64 | required | Imaginary-time sampling points. |
| `/Sigma_1_hs` | `[ns,nhs_k,nso,nso]` | complex128 | required | Interpolated static self-energy. |
| `/Hk_hs` | `[nhs_k,nso,nso]` | complex128 | required | One-electron Hamiltonian along the path. |
| `/Sk_hs` | `[nhs_k,nso,nso]` | complex128 | required | Overlap matrix along the path. |

{{< callout type="warning" >}}
`/G_tau_hs/data` is diagonal-only: its final dimension is one orbital index, not two matrix indices.
{{< /callout >}}

This file is produced only by a WINTER/high-symmetry-path job with matching `/high_symm_path` input.
