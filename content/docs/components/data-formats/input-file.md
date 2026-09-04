---
title: Input File
linkTitle: Input File
weight: 1
---

`input.h5` is written by `green-mbtools` and read by `green-mbpt`. This page describes the GREEN 1.0 input-file contract. Shapes use the [shared notation](/docs/components/data-formats/#dimensions-and-notation).

The root attribute `__green_version__` records the version of `green-mbtools` that wrote the file.

```text
/
├── Cell
├── params/{nao,nso,ns,nel_cell,nk,NQ}
├── HF/{Fock-k,S-k,H-k,Energy,Energy_nuc,madelung,Nk,nk,mo_energy,mo_coeff}
├── mulliken/{Zs,last_ao}
├── symmetry/k/{mesh,mesh_scaled,nk,ink,nk_list,ibz2bz,bz2ibz,weight_ibz,tr_conj,n_stars,stars,k_sym_transform_ao}
├── symmetry/q/{mesh,mesh_scaled,nq,inq,ibz2bz,bz2ibz,weight_ibz,tr_conj,n_stars,stars,k_sym_transform_j2c,k_sym_transform_p0}
├── symmetry/pairs/{kpair_idx,conj_pairs_list,trans_pairs_list,kpair_irre_list,num_kpair_stored}
├── orthogonalization/{X_k,X_inv_k}        (optional)
└── high_symm_path/{k_mesh,r_mesh,Hk,Sk,xpath,special_points,special_labels} (optional)
```

## File identity and dimensions

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/@__green_version__` | scalar | UTF-8 string | required | `green-mbtools` version that wrote the file. |
| `/Cell` | scalar | UTF-8 string | required, opaque | Serialized PySCF `Cell` or `Mole`; version-coupled rather than a stable public sub-schema. |
| `/params/nao` | scalar | integer | required | Number of atomic orbitals. |
| `/params/nso` | scalar | integer | required | Number of spin orbitals. |
| `/params/ns` | scalar | integer | required | Number of stored spin channels; normally 1 for restricted or two-component X2C and 2 for unrestricted calculations. |
| `/params/nel_cell` | scalar | integer | required | Electrons per cell or molecule. |
| `/params/nk` | scalar | integer | required | Full k-mesh size. |
| `/params/NQ` | scalar | integer | required | Auxiliary-basis size. |

## Mean-field data

The matrix axes are ordered as spin channel, full k-point, row orbital, column orbital, and, where present, real/imaginary component.

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/HF/Fock-k` | `[ns,nk,nso,nso,2]` | float64 + `__complex__=1` | required | Mean-field Fock matrices; final axis stores real and imaginary parts. |
| `/HF/S-k` | `[ns,nk,nso,nso,2]` | float64 + `__complex__=1` | required | Overlap matrices in the stored basis. |
| `/HF/H-k` | `[ns,nk,nso,nso,2]` | float64 + `__complex__=1` | required | One-electron/core Hamiltonian matrices. |
| `/HF/Energy` | scalar | float64 | required | Mean-field total energy in Hartree. |
| `/HF/Energy_nuc` | scalar | float64 | required | Nuclear-repulsion energy in Hartree. |
| `/HF/madelung` | scalar | float64 | required | Periodic Madelung correction in Hartree; zero for molecules. |
| `/HF/Nk` | scalar | integer | required | Requested plane-wave mesh size in each reciprocal direction for integral evaluation; distinct from k-point counts. |
| `/HF/nk` | scalar | integer | required | Product of the requested k-mesh dimensions. |
| `/HF/mo_energy` | mode-dependent | float64 | required | PySCF molecular-orbital energies; rank varies with restricted/unrestricted/X2C mode. |
| `/HF/mo_coeff` | mode-dependent | float64 or complex128 | required | PySCF molecular-orbital coefficients; rank and dtype vary by mode. |

GREEN uses atomic-unit conventions, but these datasets do not store unit attributes. `Fock-k`, `H-k`, and `mo_energy` are in Hartree. `S-k`, symmetry transforms, fractional meshes, and lattice-vector coefficients are dimensionless. Absolute `/symmetry/k/mesh` and `/symmetry/q/mesh` coordinates are in Bohr<sup>-1</sup>.

## Mulliken metadata

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/mulliken/Zs` | `[natom]` | integer | required | Nuclear charge for each atom. |
| `/mulliken/last_ao` | `[natom]` | integer | required, advanced | Exclusive AO end index for each atom. |

Here `natom` is the number of atoms in the cell or molecule.

{{< callout type="warning" >}}
`/HF/Nk`, `/HF/nk`, `/params/nk`, `/symmetry/k/nk`, and `/symmetry/k/nk_list` are not interchangeable. They respectively describe the requested plane-wave mesh size in each reciprocal direction for integral evaluation, the product of requested k-mesh dimensions, the full stored k-mesh size, the symmetry-grid k-point count, and the three requested mesh dimensions.
{{< /callout >}}

## K-point symmetry and reconstruction

The k-point hierarchy describes the full Brillouin-zone mesh, its irreducible representatives, and transformations used to reconstruct matrix-valued quantities.

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/symmetry/k/mesh` | `[nk,3]` | float64 | required | Full absolute reciprocal coordinates; unit metadata is not stored. |
| `/symmetry/k/mesh_scaled` | `[nk,3]` | float64 | required | Full fractional reciprocal coordinates. |
| `/symmetry/k/nk` | scalar | integer | required | Full k-point count. |
| `/symmetry/k/ink` | scalar | integer | required | Irreducible k-point count. |
| `/symmetry/k/nk_list` | `[3]` | integer | required | Requested mesh dimensions. |
| `/symmetry/k/ibz2bz` | `[ink]` | integer | required | Full-grid index of each irreducible representative. |
| `/symmetry/k/bz2ibz` | `[nk]` | integer | required | Full-grid representative index for every full-grid point; not a compact IBZ ordinal. |
| `/symmetry/k/weight_ibz` | `[nk]` | int64 or float64 | required | Integer-valued star size at representative positions and zero elsewhere; periodic files normally use int64, while the molecular one-Gamma identity case uses float64. |
| `/symmetry/k/tr_conj` | `[nk]` | integer/bool | required | Whether time-reversal conjugation is used during reconstruction. |
| `/symmetry/k/n_stars` | scalar | integer | required | Number of k-point stars. |
| `/symmetry/k/stars/<i>` | `[star_size]` | integer | required | Member indices of star `i`. |
| `/symmetry/k/k_sym_transform_ao` | `[nk,nso,nso]` | complex128 | required | Representative-to-full-point orbital transformation. |

For a matrix-valued quantity, reconstruct a full-grid value from its representative as

$$
X(k) = U(k) X(k_{\mathrm{rep}}) U(k)^\dagger.
$$

When `tr_conj[k]` is true, complex-conjugate the resulting matrix. Molecular inputs retain this hierarchy as a one-Gamma-point identity case.

## Advanced symmetry metadata

The q mesh is the unique wrapped set of k-point differences. It therefore need not equal the k mesh.

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/symmetry/q/mesh` | `[nq,3]` | float64 | required | Full absolute reciprocal q-point coordinates; unit metadata is not stored. |
| `/symmetry/q/mesh_scaled` | `[nq,3]` | float64 | required | Full fractional reciprocal q-point coordinates. |
| `/symmetry/q/nq` | scalar | integer | required | Full q-point count. |
| `/symmetry/q/inq` | scalar | integer | required | Irreducible q-point count. |
| `/symmetry/q/ibz2bz` | `[inq]` | integer | required | Full-grid index of each irreducible q representative. |
| `/symmetry/q/bz2ibz` | `[nq]` | integer | required | Full-grid representative index for each q point. |
| `/symmetry/q/weight_ibz` | `[nq]` | int64 or float64 | required | Integer-valued star size at representative positions and zero elsewhere; periodic files normally use int64, while the molecular one-Gamma identity case uses float64. |
| `/symmetry/q/tr_conj` | `[nq]` | integer/bool | required | Time-reversal reconstruction flags. |
| `/symmetry/q/n_stars` | scalar | integer | required | Number of q-point stars. |
| `/symmetry/q/stars/<i>` | `[star_size]` | integer | required, advanced | Full-grid members of q-point star `i`. |
| `/symmetry/q/k_sym_transform_j2c` | `[nq,NQ,NQ]` | complex128 | required, advanced | Auxiliary-basis symmetry transform for the Coulomb metric. |
| `/symmetry/q/k_sym_transform_p0` | `[nq,NQ,NQ]` | complex128 | required, advanced | P0 polarization transform in the decomposed Coulomb-metric (`j2c`<sup>-1/2</sup>) auxiliary basis. |

The pair tables index the triangular set of full-grid k-point pairs and its symmetry reductions.

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/symmetry/pairs/kpair_idx` | `[nk(nk+1)/2,2]` | integer | required, advanced | Triangular `(i,j)` pairs with `j <= i`. |
| `/symmetry/pairs/conj_pairs_list` | `[nk(nk+1)/2]` | integer | required, advanced | Conjugation-equivalent pair map. |
| `/symmetry/pairs/trans_pairs_list` | `[nk(nk+1)/2]` | integer | required, advanced | Transpose-equivalent pair map. |
| `/symmetry/pairs/kpair_irre_list` | `[num_kpair_stored]` | integer | required, advanced | Stored irreducible-pair indices. |
| `/symmetry/pairs/num_kpair_stored` | scalar | integer | required, advanced | Number of stored irreducible pairs. |

## Optional orthogonalization

The `/orthogonalization` group is present only when `--orth` is not `none`.

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/orthogonalization/@mode` | scalar | string | optional | Selected orthogonalization mode. |
| `/orthogonalization/X_k` | `[nk,n_ortho,nao]` | complex128 | optional | AO-to-orthogonal transformation. |
| `/orthogonalization/X_inv_k` | `[nk,nao,n_ortho]` | complex128 | optional | Inverse/back transformation. |

For X2C, the analogous transformations use spin-orbital dimensions rather than the AO-only dimensions shown above.

## High-symmetry-path input

The `/high_symm_path` group is created only when high-symmetry-path evaluation is requested. Its path-dependent lengths follow the selected path. See also the [high-symmetry-path output](/docs/components/data-formats/output-files/#high-symmetry-path-output).

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/high_symm_path/k_mesh` | `[nhs_k,3]` | float64 | optional | Fractional reciprocal coordinates along the requested path. |
| `/high_symm_path/r_mesh` | `[nk,3]` | float64 | optional, advanced | Dimensionless real-space lattice-vector coefficients used for interpolation. |
| `/high_symm_path/Hk` | `[nhs_k,nso,nso]` | complex128 | optional | One-electron Hamiltonian along the path, in Hartree. |
| `/high_symm_path/Sk` | `[nhs_k,nso,nso]` | complex128 | optional | Dimensionless overlap matrix along the path. |
| `/high_symm_path/xpath` | `[nhs_k]` | float64 | optional | Cumulative plotting coordinate along the path. |
| `/high_symm_path/special_points` | `[n_special]` | float64 | optional | ASE-derived inverse-angstrom plotting coordinates of labeled special points. |
| `/high_symm_path/special_labels` | `[n_special]` | string | optional | Labels of the special points. |

`xpath` is the ASE-derived inverse-angstrom coordinate for each of the `nhs_k` path points. Here `n_special` is the number of labeled special points on the selected path; `special_points` and `special_labels` have one value per such point.

## Reading complex data with Python

`Fock-k`, `S-k`, and `H-k` use a final length-two real/imaginary axis. Other input datasets, including symmetry transforms and some `mo_coeff` values, may instead use HDF5 compound complex values.

```python
import h5py

with h5py.File("input.h5", "r") as data:
    nk = int(data["params/nk"][()])
    nso = int(data["params/nso"][()])
    stored = data["HF/Fock-k"][...]
    fock = stored[..., 0] + 1j * stored[..., 1]

print(nk, nso, fock.shape)
```

{{< callout type="warning" >}}
Pre-1.0 files may use `/grid/*`; v1.0 uses `/symmetry/*`. Regenerate inputs with `green-mbtools` 1.0 rather than manually translating symmetry metadata. This page does not enumerate every legacy layout.
{{< /callout >}}
