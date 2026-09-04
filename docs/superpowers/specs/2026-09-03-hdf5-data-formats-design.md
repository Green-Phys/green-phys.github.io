# HDF5 Data Formats Documentation Design

## Goal

Resolve website issue #115 by publishing a technically precise, user-oriented reference for the HDF5 files exchanged between `green-mbtools` 1.0 and `green-mbpt` 1.0.

## Scope

The reference documents three files:

- `input.h5`, produced by `green-mbtools` and consumed by `green-mbpt` and post-processing tools.
- The main `green-mbpt` results file selected by `--results_file`, conventionally `sim.h5`.
- The optional high-symmetry-path results file selected by `--high_symmetry_output_file`, conventionally `output_hs.h5`.

The reference does not document `dm.h5`, density-fitted integral directories such as `df_int`, or SEET-specific impurity and double-counting artifacts. It does not modify `mbpt.exe` or `embedding.exe`; linking to the website from those executables is a later, dependent change in the `green-mbpt` repository.

## Source of Truth

The initial reference describes the stable 1.0 file contracts. Dataset claims must be checked against the `green-mbtools` `v1.0.0` writers and the `green-mbpt` `v1.0.0` writers, including the matching `green-sc` output routines. Representative v1.0 HDF5 fixtures provide a second check for path, rank, dtype, and encoding.

The documentation is a curated explanation, not generated `h5dump` output. Source code establishes semantics and optionality; fixtures establish the concrete on-disk representation. Each page states that it applies to GREEN 1.0 and is the rolling reference for the current stable format.

## Information Architecture

Create a new reference section under Components:

```text
content/docs/components/data-formats/
├── _index.md
├── input-file.md
└── output-files.md
```

The public URLs are:

- `/docs/components/data-formats/`
- `/docs/components/data-formats/input-file/`
- `/docs/components/data-formats/output-files/`

`data-formats/_index.md` has weight 3, following Core Components and Many-Body Framework. The child pages use weights 1 and 2.

The Components landing page gains an “HDF5 Data Formats” entry. The new section is the canonical reference. Getting Started remains task-oriented and links into the reference at the moment users encounter each file.

## Overview Page

The overview page explains the producer/consumer flow:

```text
green-mbtools ──writes──> input.h5 ──read by──> green-mbpt
                                                     │
                                                     ├──writes──> sim.h5
                                                     └──writes──> output_hs.h5 (optional)
```

It defines notation shared by the detailed pages:

| Symbol | Meaning |
|---|---|
| `nao` | Number of atomic orbitals in the AO basis. |
| `nso` | Stored one-particle basis dimension. |
| `ns` | Number of stored spin channels. |
| `nk` | Number of k-points in the full Brillouin-zone mesh. |
| `ink` | Number of stored irreducible k-points. |
| `nq`, `inq` | Full and irreducible auxiliary q-point counts. |
| `NQ` | Auxiliary-basis dimension. |
| `nts` | Number of fermionic imaginary-time sampling points. |
| `nhs_k` | Number of points on the requested high-symmetry path. |

The page links to both detailed references and includes a short version/compatibility callout.

## Input File Page

The input page starts with a representative v1.0 tree, followed by curated tables. Every table row contains the HDF5 path, shape, on-disk type, required/optional status, and physical or operational meaning. Related datasets may share a row only when their shapes and semantics are genuinely parallel.

The page is organized as follows:

1. **File identity and dimensions**
   - Root `__green_version__` attribute.
   - `/params/{nao,nso,ns,nel_cell,nk,NQ}`.
   - `/Cell`, labeled as opaque PySCF serialization rather than a stable user-facing schema.
2. **Mean-field data**
   - `/HF/{Fock-k,S-k,H-k}` and their matrix index order.
   - `/HF/{Energy,Energy_nuc,madelung}`.
   - `/HF/{mo_energy,mo_coeff}`, explicitly noting that rank and dtype depend on the mean-field mode.
   - `/HF/Nk` and `/HF/nk`, with a warning not to confuse them with `/params/nk`, `/symmetry/k/nk`, or `/symmetry/k/nk_list`.
3. **Mulliken metadata**
   - `/mulliken/{Zs,last_ao}`.
4. **k-point symmetry and reconstruction**
   - `/symmetry/k` meshes, dimensions, mappings, weights, time-reversal flags, stars, and AO transforms.
   - Explain that `bz2ibz` stores the full-grid representative index rather than a compact IBZ ordinal.
   - Provide the matrix reconstruction rule and define the role of `tr_conj`.
5. **q-point and pair symmetry (advanced)**
   - `/symmetry/q` and `/symmetry/pairs` paths.
   - Explain that q-points are the unique wrapped differences of k-point pairs and need not be identical to the k mesh.
6. **Optional orthogonalization**
   - `/orthogonalization` group, its `mode` attribute, `X_k`, and `X_inv_k`.
7. **Optional high-symmetry-path input**
   - `/high_symm_path/{k_mesh,r_mesh,Hk,Sk,xpath,special_points,special_labels}`.
   - Link forward to the high-symmetry output section.
8. **Reading the file with Python**
   - A minimal read-only `h5py` example that obtains dimensions and decodes an HF matrix.

The page explains the `green-mbtools` convention for complex HF matrices: a floating-point dataset with a trailing length-two real/imaginary axis and `__complex__=1`. It does not imply that all HDF5 files in GREEN use this representation.

Molecular inputs retain the symmetry hierarchy as a one-point identity case. The page notes this rather than presenting symmetry groups as periodic-only.

## Output Files Page

The output page begins with the main results file and then documents the separate optional high-symmetry file.

### Main Results

A representative tree shows `/iter` and one `/iterN` group. The page explains:

- `/iter` is the latest fully written checkpoint number, not a count of iteration groups and not a convergence flag.
- `N` in `/iterN` is the self-consistency iteration number.
- Each completed iteration contains `Sigma1`, `Selfenergy`, `G_tau`, the associated imaginary-time meshes, `Energy_1b`, `Energy_HF`, `Energy_2b`, and `mu`.
- Tensor index order is documented explicitly. Dynamic tensors use `[nts, ns, ink, nso, nso]`; `Sigma1` omits the time axis and uses `[ns, ink, nso, nso]`.
- `Energy_HF` includes nuclear energy. The total printed by the solver is `Energy_HF + Energy_2b`; `Energy_1b` is a decomposition term and is not added again.
- The file does not store convergence residuals, wall-clock timings, the chosen MBPT method, or a complete parameter snapshot. The documentation must not imply that it does.

The root `__grids_version__` attribute and every `/iterN` path receive a table row with type, shape, status, and meaning.

The page states that energies and imaginary-time quantities follow GREEN's atomic-unit convention, while the HDF5 datasets themselves do not carry unit attributes.

The output tensors use an HDF5 compound type with float64 real and imaginary components, rather than the trailing real/imaginary axis used by `green-mbtools` for the HF input matrices. A read-only `h5py` example finds the latest checkpoint and loads its Green's function, self-energy, chemical potential, and total energy.

### High-Symmetry Results

The page documents:

- Root `__grids_version__` attribute.
- `/G_tau_hs/{data,mesh}`.
- `/Sigma_1_hs`.
- `/Hk_hs` and `/Sk_hs`.

It states that `/G_tau_hs/data` has shape `[nts, ns, nhs_k, nso]` and contains only the orbital diagonal; it is not a square matrix in its final dimensions. It also states that this file is produced only for a WINTER/high-symmetry-path job with matching high-symmetry input data.

## Legacy Warning

The overview and input-file pages include a concise legacy callout:

- Pre-1.0 input files may use `/grid/*` rather than the v1.0 `/symmetry/*` hierarchy.
- Users should regenerate `input.h5` with `green-mbtools` 1.0 instead of translating old symmetry metadata manually.
- The reference intentionally does not enumerate every pre-1.0 layout.

The output page makes no unsupported claim about historical result layouts, including whether `mu` was present.

## Getting Started Integration

Add contextual links without duplicating schema content:

- `content/docs/getting-started/preparing_input.md` links from its first explanation of `input.h5` to the input reference.
- `content/docs/getting-started/running_greens.md` links from its explanation of `--results_file` to the main output reference.
- The band-path interpolation subsection in `running_greens.md` links directly to the high-symmetry output section.
- `content/docs/getting-started/postprocessing.md` links to the data-formats overview when explaining HDF5 inputs to post-processing tools.

No tutorial or legacy page is rewritten as part of this issue.

## Maintainability

- Use normal Markdown tables and headings so Hugo provides stable anchors and responsive horizontal scrolling through the existing theme.
- Keep conceptual explanations outside tables; tables remain scannable reference material.
- Mark internal or mode-dependent paths explicitly rather than presenting every dataset as a stable required interface.
- Keep the public overview URL stable so a later `green-mbpt` change can print it from `mbpt.exe` and `embedding.exe`.
- When the stable file format changes, update the producer's release notes and these pages together. Verify paths against both writers and representative files rather than copying an old tree.

## Verification

Before opening the website PR:

1. Build the complete site with `hugo --minify`.
2. Confirm that the three new pages appear under Components and that all Getting Started links resolve to the intended pages or anchor.
3. Compare every documented input path and shape with a representative `green-mbtools` v1.0 file and its writer.
4. Compare every documented output path and shape with representative GW/GF2/X2C result files and the `green-mbpt`/`green-sc` writers.
5. Confirm that the main output and high-symmetry examples are clearly distinguished.
6. Run `git diff --check` and verify that the unrelated untracked `content/docs/installation/spack_install.md` remains untouched.

## Success Criteria

- A user can identify which program produces each documented file.
- A user can determine each documented dataset's purpose, index order, dtype, units convention, and optionality without reading source code.
- A user can safely locate and read the latest completed result checkpoint.
- A user does not mistake the high-symmetry Green's function for a full matrix.
- A user with a pre-1.0 input is directed to regenerate it rather than infer a migration.
- The canonical reference is discoverable from both Components and the relevant Getting Started steps.
