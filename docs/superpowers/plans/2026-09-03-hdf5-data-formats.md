# HDF5 Data Formats Documentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a discoverable GREEN 1.0 reference for `input.h5`, the main `green-mbpt` results file, and the optional high-symmetry results file.

**Architecture:** Add a three-page HDF5 Data Formats section under Components, with one overview and separate input/output references. Keep procedural Getting Started pages concise by linking them to this canonical reference instead of duplicating schema details.

**Tech Stack:** Hugo 0.146+, Markdown/Goldmark, Hextra theme, HDF5 command-line tools, Python 3 with `h5py` and NumPy.

**Spec:** `docs/superpowers/specs/2026-09-03-hdf5-data-formats-design.md`

## Global Constraints

- Document the stable GREEN 1.0 formats produced by `green-mbtools` 1.0 and `green-mbpt` 1.0.
- The canonical public root URL is `/docs/components/data-formats/`.
- Fully document only `input.h5`, the `--results_file` output, and `--high_symmetry_output_file` output.
- Do not document `dm.h5`, `df_int`, or SEET-specific files.
- Do not change `mbpt.exe`, `embedding.exe`, or either source repository.
- Use `nso` to mean “number of spin orbitals.”
- Mark optional, mode-dependent, opaque, and advanced/internal data explicitly.
- State units as conventions and never imply that unit metadata is stored in the HDF5 datasets.
- Treat `green-mbtools` `v1.0.0` and `green-mbpt` `v1.0.0` writers as the semantic source of truth; use fixtures only to confirm on-disk representation.
- Keep the unrelated untracked `content/docs/installation/spack_install.md` untouched and out of every commit.

---

### Task 1: Add the HDF5 Data Formats overview and Components navigation

**Files:**
- Create: `content/docs/components/data-formats/_index.md`
- Modify: `content/docs/components/_index.md`

**Interfaces:**
- Consumes: the approved information architecture and shared symbols from the design spec.
- Produces: stable routes `/docs/components/data-formats/`, `/input-file/`, and `/output-files/`; shared notation used verbatim by Tasks 2 and 3.

- [ ] **Step 1: Verify the overview route does not exist yet**

Run:

```bash
test -e content/docs/components/data-formats/_index.md
```

Expected: exit 1 because the new section has not been created.

- [ ] **Step 2: Create the section overview**

Create `content/docs/components/data-formats/_index.md` with this front matter:

```yaml
---
title: HDF5 Data Formats
linkTitle: HDF5 Data Formats
weight: 3
---
```

The body must contain, in this order:

1. A one-paragraph statement that the pages describe the GREEN 1.0 file interface.
2. This producer/consumer flow in a fenced `text` block:

```text
green-mbtools ──writes──> input.h5 ──read by──> green-mbpt
                                                     │
                                                     ├──writes──> sim.h5
                                                     └──writes──> output_hs.h5 (optional)
```

3. Two Hextra CTA buttons:

```markdown
{{< cta-button text="Input file reference" link="input-file" icon="input" >}}
{{< cta-button text="Output files reference" link="output-files" icon="output" >}}
```

4. A “Dimensions and notation” table with exactly these definitions:

| Symbol | Definition |
|---|---|
| `nao` | Number of atomic orbitals. |
| `nso` | Number of spin orbitals. |
| `n_ortho` | Number of orbitals retained in the orthogonalized basis. |
| `ns` | Number of stored spin channels. |
| `nk` | Number of k-points in the full Brillouin-zone mesh. |
| `ink` | Number of stored irreducible k-points. |
| `nq` | Number of q-points in the full auxiliary mesh. |
| `inq` | Number of stored irreducible q-points. |
| `NQ` | Number of auxiliary basis functions. |
| `nts` | Number of fermionic imaginary-time sampling points. |
| `nhs_k` | Number of k-points on the requested high-symmetry path. |

5. A compatibility callout stating that the reference applies to GREEN 1.0, is maintained as the current stable reference, and that pre-1.0 inputs may use a different layout.

- [ ] **Step 3: Add the section to the Components landing page**

Append this block after the Many-Body Framework entry in `content/docs/components/_index.md`:

```markdown
- ### [HDF5 Data Formats](/docs/components/data-formats)
   - Input data produced by `green-mbtools`
   - Iteration results produced by `green-mbpt`
   - Optional high-symmetry-path output
```

- [ ] **Step 4: Build and verify the overview**

Run:

```bash
hugo --minify --destination /tmp/green-phys-issue-115-task1
test -f /tmp/green-phys-issue-115-task1/docs/components/data-formats/index.html
rg -n "Number of spin orbitals|green-mbtools|output_hs.h5" /tmp/green-phys-issue-115-task1/docs/components/data-formats/index.html
```

Expected: Hugo exits 0; the generated overview exists; all three strings are present.

- [ ] **Step 5: Commit the overview**

```bash
git add content/docs/components/_index.md content/docs/components/data-formats/_index.md
git commit -m "docs: add HDF5 data formats overview"
```

---

### Task 2: Document the GREEN 1.0 input file

**Files:**
- Create: `content/docs/components/data-formats/input-file.md`

**Interfaces:**
- Consumes: shared symbols defined by Task 1; `green-mbtools` `v1.0.0` writers in `../green-mbtools/green_mbtools/mint/common_utils.py` and `pyscf_init.py`.
- Produces: route `/docs/components/data-formats/input-file/` and anchor `#high-symmetry-path-input`, linked by Tasks 3 and 4.

- [ ] **Step 1: Verify the input reference does not exist yet**

Run:

```bash
test -e content/docs/components/data-formats/input-file.md
```

Expected: exit 1.

- [ ] **Step 2: Create the page shell and representative tree**

Use this front matter:

```yaml
---
title: Input File
linkTitle: Input File
weight: 1
---
```

Introduce `input.h5` as the file written by `green-mbtools` and read by `green-mbpt`. State that the page describes 1.0, then show a representative tree containing these groups and leaves:

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

Mention the root `__green_version__` attribute above the tree rather than rendering it as a child dataset.

- [ ] **Step 3: Add the identity, dimension, mean-field, and Mulliken tables**

Each table must use columns `Path`, `Shape`, `Type`, `Status`, and `Meaning`. Cover these exact contracts:

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
| `/HF/Fock-k` | `[ns,nk,nso,nso,2]` | float64 + `__complex__=1` | required | Mean-field Fock matrices; final axis stores real and imaginary parts. |
| `/HF/S-k` | `[ns,nk,nso,nso,2]` | float64 + `__complex__=1` | required | Overlap matrices in the stored basis. |
| `/HF/H-k` | `[ns,nk,nso,nso,2]` | float64 + `__complex__=1` | required | One-electron/core Hamiltonian matrices. |
| `/HF/Energy` | scalar | float64 | required | Mean-field total energy in Hartree. |
| `/HF/Energy_nuc` | scalar | float64 | required | Nuclear-repulsion energy in Hartree. |
| `/HF/madelung` | scalar | float64 | required | Periodic Madelung correction in Hartree; zero for molecules. |
| `/HF/Nk` | scalar | integer | required | Plane-wave count requested for integral evaluation; distinct from k-point counts. |
| `/HF/nk` | scalar | integer | required | Product of the requested k-mesh dimensions. |
| `/HF/mo_energy` | mode-dependent | float64 | required | PySCF molecular-orbital energies; rank varies with restricted/unrestricted/X2C mode. |
| `/HF/mo_coeff` | mode-dependent | float64 or complex128 | required | PySCF molecular-orbital coefficients; rank and dtype vary by mode. |
| `/mulliken/Zs` | `[natom]` | integer | required | Nuclear charge for each atom. |
| `/mulliken/last_ao` | `[natom]` | integer | required, advanced | Exclusive AO end index for each atom. |

Add a warning immediately after the table that `/HF/Nk`, `/HF/nk`, `/params/nk`, `/symmetry/k/nk`, and `/symmetry/k/nk_list` are not interchangeable.

- [ ] **Step 4: Add k-point symmetry documentation and reconstruction rule**

Document every path below with the same five table columns:

- `mesh [nk,3] float64`: full absolute reciprocal coordinates; unit metadata is not stored.
- `mesh_scaled [nk,3] float64`: full fractional reciprocal coordinates.
- `nk scalar integer`: full k-point count.
- `ink scalar integer`: irreducible k-point count.
- `nk_list [3] integer`: requested mesh dimensions.
- `ibz2bz [ink] integer`: full-grid index of each irreducible representative.
- `bz2ibz [nk] integer`: full-grid representative index for every full-grid point; explicitly not a compact IBZ ordinal.
- `weight_ibz [nk] integer`: star size at representative positions and zero elsewhere.
- `tr_conj [nk] integer/bool`: whether time-reversal conjugation is used during reconstruction.
- `n_stars scalar integer` and `stars/<i> [star_size] integer`: star count and member indices.
- `k_sym_transform_ao [nk,nso,nso] complex128`: representative-to-full-point orbital transformation.

Give this reconstruction equation in display math for a matrix-valued quantity:

```text
X(k) = U(k) X(k_rep) U(k)†
```

State that the result is complex-conjugated when `tr_conj[k]` is true. State that molecular inputs retain this hierarchy as a one-Gamma-point identity case.

- [ ] **Step 5: Add advanced q-point and pair symmetry tables**

Under an “Advanced symmetry metadata” heading, document the q analogues with the same five columns:

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/symmetry/q/mesh` | `[nq,3]` | float64 | required | Full absolute reciprocal q-point coordinates; unit metadata is not stored. |
| `/symmetry/q/mesh_scaled` | `[nq,3]` | float64 | required | Full fractional reciprocal q-point coordinates. |
| `/symmetry/q/nq` | scalar | integer | required | Full q-point count. |
| `/symmetry/q/inq` | scalar | integer | required | Irreducible q-point count. |
| `/symmetry/q/ibz2bz` | `[inq]` | integer | required | Full-grid index of each irreducible q representative. |
| `/symmetry/q/bz2ibz` | `[nq]` | integer | required | Full-grid representative index for each q point. |
| `/symmetry/q/weight_ibz` | `[nq]` | integer | required | Star size at representative positions and zero elsewhere. |
| `/symmetry/q/tr_conj` | `[nq]` | integer/bool | required | Time-reversal reconstruction flags. |
| `/symmetry/q/n_stars` | scalar | integer | required | Number of q-point stars. |
| `/symmetry/q/stars/<i>` | `[star_size]` | integer | required, advanced | Full-grid members of q-point star `i`. |
| `/symmetry/q/k_sym_transform_j2c` | `[nq,NQ,NQ]` | complex128 | required, advanced | Auxiliary-basis symmetry transform for the Coulomb metric. |
| `/symmetry/q/k_sym_transform_p0` | `[nq,NQ,NQ]` | complex128 | required, advanced | Auxiliary-basis symmetry transform for the reference q point. |

Explain that q is the unique wrapped set of k-point differences and need not equal the k mesh.

Document pair paths exactly:

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/symmetry/pairs/kpair_idx` | `[nk(nk+1)/2,2]` | integer | required, advanced | Triangular `(i,j)` pairs with `j <= i`. |
| `/symmetry/pairs/conj_pairs_list` | `[nk(nk+1)/2]` | integer | required, advanced | Conjugation-equivalent pair map. |
| `/symmetry/pairs/trans_pairs_list` | `[nk(nk+1)/2]` | integer | required, advanced | Transpose-equivalent pair map. |
| `/symmetry/pairs/kpair_irre_list` | `[num_kpair_stored]` | integer | required, advanced | Stored irreducible-pair indices. |
| `/symmetry/pairs/num_kpair_stored` | scalar | integer | required, advanced | Number of stored irreducible pairs. |

- [ ] **Step 6: Add optional orthogonalization and high-symmetry input sections**

Document `/orthogonalization` as present only when `--orth` is not `none`:

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/orthogonalization/@mode` | scalar | string | optional | Selected orthogonalization mode. |
| `/orthogonalization/X_k` | `[nk,n_ortho,nao]` | complex128 | optional | AO-to-orthogonal transformation. |
| `/orthogonalization/X_inv_k` | `[nk,nao,n_ortho]` | complex128 | optional | Inverse/back transformation. |

For X2C, describe the analogous spin-orbital dimensions rather than promising AO-only shapes.

Under the exact heading `## High-symmetry-path input`, add this table and link to `/docs/components/data-formats/output-files/#high-symmetry-path-output`:

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/high_symm_path/k_mesh` | `[nhs_k,3]` | float64 | optional | Fractional reciprocal coordinates along the requested path. |
| `/high_symm_path/r_mesh` | mesh-dependent | float64 | optional, advanced | Real-space lattice-vector mesh used for interpolation. |
| `/high_symm_path/Hk` | `[nhs_k,nso,nso]` | complex128 | optional | One-electron Hamiltonian along the path. |
| `/high_symm_path/Sk` | `[nhs_k,nso,nso]` | complex128 | optional | Overlap matrix along the path. |
| `/high_symm_path/xpath` | `[nhs_k]` | float64 | optional | Cumulative plotting coordinate along the path. |
| `/high_symm_path/special_points` | path-dependent | float64 | optional | Plotting coordinates of labeled special points. |
| `/high_symm_path/special_labels` | path-dependent | string | optional | Labels of the special points. |

Explain that the group is created only when high-symmetry-path evaluation is requested and that path-dependent lengths follow the selected path.

- [ ] **Step 7: Add complex encoding, Python example, and legacy warning**

Explain that `Fock-k`, `S-k`, and `H-k` use a final length-two real/imaginary axis, while other input datasets such as symmetry transforms or `mo_coeff` may use HDF5 compound complex values.

Include this executable example:

```python
import h5py

with h5py.File("input.h5", "r") as data:
    nk = int(data["params/nk"][()])
    nso = int(data["params/nso"][()])
    stored = data["HF/Fock-k"][...]
    fock = stored[..., 0] + 1j * stored[..., 1]

print(nk, nso, fock.shape)
```

Add a warning callout with these exact facts: pre-1.0 files may use `/grid/*`; v1.0 uses `/symmetry/*`; users should regenerate inputs with `green-mbtools` 1.0 rather than manually translating symmetry metadata; the page does not enumerate every legacy layout.

- [ ] **Step 8: Verify the input page against source and render it**

Run:

```bash
rg -n 'symmetry/k/nk_list|__green_version__|HF/Fock-k' ../green-mbtools/green_mbtools/mint/common_utils.py
hugo --minify --destination /tmp/green-phys-issue-115-task2
test -f /tmp/green-phys-issue-115-task2/docs/components/data-formats/input-file/index.html
rg -n 'bz2ibz|Number of spin orbitals|grid/|High-symmetry-path input' /tmp/green-phys-issue-115-task2/docs/components/data-formats/input-file/index.html
```

Expected: writer paths are found; Hugo exits 0; the page and all four concepts render.

- [ ] **Step 9: Commit the input reference**

```bash
git add content/docs/components/data-formats/input-file.md
git commit -m "docs: document GREEN 1.0 input file"
```

---

### Task 3: Document the main and high-symmetry output files

**Files:**
- Create: `content/docs/components/data-formats/output-files.md`

**Interfaces:**
- Consumes: shared symbols from Task 1 and the high-symmetry input anchor from Task 2; `green-mbpt` `v1.0.0` and matching `green-sc` writers.
- Produces: route `/docs/components/data-formats/output-files/`, anchor `#main-results-file`, and anchor `#high-symmetry-path-output` for Task 4.

- [ ] **Step 1: Verify the output reference does not exist yet**

Run:

```bash
test -e content/docs/components/data-formats/output-files.md
```

Expected: exit 1.

- [ ] **Step 2: Create the page shell and main-results tree**

Use this front matter:

```yaml
---
title: Output Files
linkTitle: Output Files
weight: 2
---
```

Under the exact heading `## Main results file`, identify the file as `--results_file`, default `sim.h5`, and show:

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

Mention the root `__grids_version__` attribute above the tree. Explain that `/iter` is the number of the latest fully written checkpoint, not the group count or a convergence flag.

- [ ] **Step 3: Add the complete main-results schema table**

Use columns `Path`, `Shape`, `Type`, `Status`, and `Meaning`, with these exact contracts:

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

Immediately explain:

```text
E_total = Energy_HF + Energy_2b
```

State that `Energy_1b` is a decomposition term and must not be added again. State that the file does not record convergence residuals, convergence status, timings, method name, or a full parameter snapshot.

- [ ] **Step 4: Add the output encoding and Python example**

State that complex output arrays use an HDF5 compound type with float64 real and imaginary components; `h5py` exposes the tested files as `complex128`. Contrast this with the trailing real/imaginary axis on the three HF input matrices.

Include this example:

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

State that the numerical quantities use GREEN's atomic-unit convention but that unit attributes are not stored in the datasets.

- [ ] **Step 5: Add the high-symmetry-path output reference**

Under the exact heading `## High-symmetry-path output`, identify `--high_symmetry_output_file`, default `output_hs.h5`, and link back to `/docs/components/data-formats/input-file/#high-symmetry-path-input`.

Document this complete schema:

| Path | Shape | Type | Status | Meaning |
|---|---|---|---|---|
| `/@__grids_version__` | scalar | UTF-8 string | required | GREEN grids-library version. |
| `/G_tau_hs/data` | `[nts,ns,nhs_k,nso]` | complex128 | required | Orbital-diagonal Green's function along the selected path. |
| `/G_tau_hs/mesh` | `[nts]` | float64 | required | Imaginary-time sampling points. |
| `/Sigma_1_hs` | `[ns,nhs_k,nso,nso]` | complex128 | required | Interpolated static self-energy. |
| `/Hk_hs` | `[nhs_k,nso,nso]` | complex128 | required | One-electron Hamiltonian along the path. |
| `/Sk_hs` | `[nhs_k,nso,nso]` | complex128 | required | Overlap matrix along the path. |

Add a warning that `/G_tau_hs/data` is diagonal-only: its final dimension is one orbital index, not two matrix indices. State that the file is produced only by a WINTER/high-symmetry-path job with matching `/high_symm_path` input.

- [ ] **Step 6: Verify output paths, shapes, and rendering**

Run:

```bash
h5ls -r ../green-mbpt/test/data/new_data/GW/sim.h5
hugo --minify --destination /tmp/green-phys-issue-115-task3
test -f /tmp/green-phys-issue-115-task3/docs/components/data-formats/output-files/index.html
rg -n 'latest fully written|Energy_HF.*Energy_2b|diagonal-only|G_tau_hs' /tmp/green-phys-issue-115-task3/docs/components/data-formats/output-files/index.html
```

Expected: the representative main-result paths match the table; Hugo exits 0; all four critical explanations render. Validate the high-symmetry paths against `../green-mbpt/src/green/mbpt/mbpt_run.h` at `v1.0.0`, because the repository has no canonical checked-in `output_hs.h5` fixture.

- [ ] **Step 7: Commit the output reference**

```bash
git add content/docs/components/data-formats/output-files.md
git commit -m "docs: document GREEN 1.0 output files"
```

---

### Task 4: Connect Getting Started and run final verification

**Files:**
- Modify: `content/docs/getting-started/preparing_input.md:27`
- Modify: `content/docs/getting-started/running_greens.md:21-30`
- Modify: `content/docs/getting-started/postprocessing.md:7-22`

**Interfaces:**
- Consumes: final URLs and anchors from Tasks 1–3.
- Produces: contextual discovery paths from task-oriented guidance to the canonical schemas.

- [ ] **Step 1: Verify the contextual links are initially absent**

Run:

```bash
rg -n '/docs/components/data-formats' content/docs/getting-started/preparing_input.md content/docs/getting-started/running_greens.md content/docs/getting-started/postprocessing.md
```

Expected: exit 1 with no matches.

- [ ] **Step 2: Link input preparation to the input reference**

Replace the first sentence that introduces `input.h5` in `preparing_input.md` with:

```markdown
By default, `init_data_df.py` generates [`input.h5`](/docs/components/data-formats/input-file/), which contains the system parameters, symmetry metadata, and initial mean-field solution needed by `green-mbpt`.
```

Keep the following explanation of integral directories intact; do not link or document their schema.

- [ ] **Step 3: Link solver output and band-path output**

Replace the `--results_file` sentence in `running_greens.md` with:

```markdown
After successful completion, results are written to [`--results_file`](/docs/components/data-formats/output-files/#main-results-file), which defaults to `sim.h5`.
```

In the band-path interpolation paragraph, link the words `high-symmetry output file` to `/docs/components/data-formats/output-files/#high-symmetry-path-output` while preserving the default filename `output_hs.h5`.

- [ ] **Step 4: Link post-processing to the format overview**

After the opening paragraph in `postprocessing.md`, add:

```markdown
For the dataset layout and dimension conventions used by GREEN's HDF5 inputs and results, see the [HDF5 Data Formats reference](/docs/components/data-formats/).
```

- [ ] **Step 5: Run the complete site and content verification**

Run:

```bash
hugo --minify --destination /tmp/green-phys-issue-115-final
test -f /tmp/green-phys-issue-115-final/docs/components/data-formats/index.html
test -f /tmp/green-phys-issue-115-final/docs/components/data-formats/input-file/index.html
test -f /tmp/green-phys-issue-115-final/docs/components/data-formats/output-files/index.html
rg -n 'data-formats/input-file' /tmp/green-phys-issue-115-final/docs/getting-started/preparing_input/index.html
rg -n 'output-files/#main-results-file|output-files/#high-symmetry-path-output' /tmp/green-phys-issue-115-final/docs/getting-started/running_greens/index.html
rg -n 'data-formats/' /tmp/green-phys-issue-115-final/docs/getting-started/postprocessing/index.html
git diff --check main..HEAD
git status --short
```

Expected: Hugo exits 0 with only pre-existing warnings; all pages and links are present; `git diff --check` is clean; status lists only the intended documentation changes plus the unrelated untracked `content/docs/installation/spack_install.md`.

- [ ] **Step 6: Review the finished reference against the specification**

Check every success criterion in `docs/superpowers/specs/2026-09-03-hdf5-data-formats-design.md`. Specifically confirm that every schema row has path, shape, dtype, status, meaning, and units convention; that legacy guidance is limited to the known input transition; and that no SEET, `dm.h5`, or `df_int` schema slipped into the pages.

- [ ] **Step 7: Commit the integration links**

```bash
git add content/docs/getting-started/preparing_input.md content/docs/getting-started/running_greens.md content/docs/getting-started/postprocessing.md
git commit -m "docs: link workflows to HDF5 reference"
```
