---
title: SEET Impurity Solver
linkTitle: SEET Impurity Solver
weight: 3
---

[Self-Energy Embedding Theory (SEET)](/docs/theory/embedding_theory) runs through
`green-mbpt`'s `embedding.exe` together with an exact-diagonalization impurity solver
provided by [`green-seet-solvers`](https://github.com/Green-Phys/green-seet-solvers).

For Green **1.0.0-alpha (`v1.0.0a0`) and later**, `embedding.exe` is built as part of the
standard [General Installation](/docs/installation/from_sources/) — no separate branch or
build is required for the framework itself. Unless you supply your own impurity solver,
you will need the Green exact-diagonalization impurity solver, which you will need to
build in addition, as described below. See the
[SEET example](/docs/getting-started/examples/seet/) for how to run a calculation once
everything is installed.

{{% steps %}}

### Prerequisites

System libraries:
 1. MPI
 2. HDF5
 3. BLAS
 4. CMake (version >= 3.27)
 5. C++17 compatible compiler

Third-party libraries:
 1. Eigen3
 2. Boost

### Build the exact-diagonalization impurity solver

Clone [`green-seet-solvers`](https://github.com/Green-Phys/green-seet-solvers) — the
exact-diagonalization solver for the SEET impurity problem — and build it:

```ShellSession
git clone https://github.com/Green-Phys/green-seet-solvers
cmake -S green-seet-solvers -B build \
   --install-prefix `pwd`/install/seet_solvers \
   -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 32
cmake --build build -t install
rm -rf build
```

{{% /steps %}}

## Legacy: Green v0.3.2

{{< callout type="warning" >}}
On Green **v0.3.2**, `embedding.exe` is **not** part of the default `green-mbpt` build.
To obtain the SEET framework on that release, build `green-mbpt` from the **`seet-v0.3.2`**
tag (preserved on the `seet-legacy` branch) as shown below. The exact-diagonalization
impurity solver above is still required.

Do **not** use the current `SEET` branch for this: it has since migrated to the newer,
non-templated symmetry library (Green `v1.0.0a0` and later) and will not compile against
`green-symmetry` v0.3.2. The `seet-v0.3.2` tag is the last state compatible with the
v0.3.2 dependency stack and already defaults `GREEN_RELEASE` to `v0.3.2`, so the plain
`cmake` invocation below pulls the correct dependency versions with no extra flags.
{{< /callout >}}

```ShellSession
git clone https://github.com/Green-Phys/green-mbpt
cd green-mbpt
git checkout seet-v0.3.2
cd ..
cmake -S green-mbpt -B build \
   --install-prefix `pwd`/install/green-mbpt \
   -DCMAKE_BUILD_TYPE=Release
cmake --build build -j 32
cmake --build build -t test install
rm -rf build
```

### Installation issues
If you encounter issues with compiling, installing, or testing the package, please file an
issue on our [GitHub issues page](https://github.com/Green-Phys/green-mbpt/issues), and we
will do our best to help.
