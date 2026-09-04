---
title: HDF5 Data Formats
linkTitle: HDF5 Data Formats
weight: 3
---

These pages describe the GREEN 1.0 HDF5 file interface exchanged by `green-mbtools`, `green-mbpt`, and their associated post-processing workflows.

```text
green-mbtools ──writes──> input.h5 ──read by──> green-mbpt
                                                     │
                                                     ├──writes──> sim.h5
                                                     └──writes──> output_hs.h5 (optional)
```

{{< cta-button text="Input file reference" link="input-file" icon="input" >}}
{{< cta-button text="Output files reference" link="output-files" icon="output" >}}

## Dimensions and notation

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

{{< callout type="info" >}}
This reference applies to GREEN 1.0 and is maintained as the current stable reference. Pre-1.0 inputs may use a different layout.
{{< /callout >}}
