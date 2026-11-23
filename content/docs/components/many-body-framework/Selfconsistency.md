---
linkTitle: Self-consistency
title: Light-weight generic iterative self-consistency loop.
weight: 2
---


## Basic usage
`green-sc` is a header-only C++ template library that implements a generic iterative self-consistency loop.

`green-sc` pulls in its own Green dependencies (`green-grids`, `green-h5pp`, `green-params`, ...) through the
`add_green_dependency` CMake function, which the including project has to provide. The easiest way is to copy
[`cmake/GreenDeps.cmake`](https://github.com/Green-Phys/green-sc/blob/main/cmake/GreenDeps.cmake) from `green-sc`
into the `cmake/` directory of your project and add:

```CMake
set(GREEN_RELEASE "v1.0.0" CACHE STRING "Release version for Green dependencies") # or a later release
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)
include(GreenDeps)
add_green_dependency(green-sc)
```
Then link the predefined alias `GREEN::SC` to your target:
```CMake
target_link_libraries(<target> PUBLIC GREEN::SC)
```
and include the following header:
```cpp
#include <green/sc/sc_loop.h>
```

## Parameters

`green-sc` uses the [`green-params`](https://github.com/Green-Phys/green-params.git) library to read parameters either from the command line or from a parameter string;
please check the `green-params` documentation for more details. Call `green::sc::define_parameters(p)` before parsing
to register the parameters of the self-consistency loop. All of them have defaults; the most important ones are:

- `itermax` - maximum number of iterations to run (default: `1`)
- `threshold` (alias `E_thr`) - convergence threshold; iterations stop once the convergence criterion returned by `Dyson::diff` is smaller than `threshold` (default: `1e-9`)
- `mixing_type` - type of mixing between iterations, one of `NO_MIXING`, `G_MIXING`, `SIGMA_MIXING` (default), `DIIS`, `CDIIS`
- `mixing_weight` (alias `mixing_alpha`) - weight $w$ of simple mixing, $X_n \leftarrow w X_n + (1-w) X_{n-1}$ (default: `0.7`)
- `results_file` - file to store the results of each iteration (default: `sim.h5`)
- `restart` - restart from the last iteration stored in `results_file` (default: `false`)

## Interface

`sc_loop` is parametrized by a user-defined `Dyson` type and is constructed from an MPI communicator and a parameter object:

```cpp
green::sc::sc_loop<Dyson> sc(MPI_COMM_WORLD, p);
```
The `Dyson` object itself is constructed from the parameter object `p`. `Dyson` publicly defines three types: `G` - type of the Green's function, `Sigma1` - type of the static part of the self-energy,
`Sigma_tau` - type of the dynamic part of the self-energy, and implements the following methods:

- `void solve(G& g, Sigma1& sigma1, Sigma_tau& sigma_tau)` - solve the Dyson equation for given self-energies and update `g`
- `double diff(const G&, const Sigma1&, const Sigma_tau&)` - return the convergence criterion
- `void dump_iteration(size_t iter, const G&, const Sigma1&, const Sigma_tau&, const std::string& file)` - store additional data for iteration `iter` into the results file `file`
- `double mu() const` and `double& mu()` - chemical potential (read back on restart and used by some mixing schemes)
- `const std::string& get_grids_version() const` - version of the imaginary-time grid, written to the results file and checked on restart

The loop is started with
```cpp
sc.solve(solver, h0, ovlp, g, sigma1, sigma_tau);
```
where

- `solver` is a diagrammatic solver that implements `void solve(const G& g, Sigma1& sigma1, Sigma_tau& sigma_tau)`, i.e. computes the self-energies for a given Green's function. Several solvers can be combined with `green::sc::composition_solver`
- `h0` and `ovlp` (of type `Sigma1`) are the one-body Hamiltonian and the overlap matrix, used by some of the mixing schemes
- `g` is the starting guess on input and the converged Green's function on output
- `sigma1` and `sigma_tau` receive the converged static and dynamic self-energies

***
Even though we use diagrammatic names such as Green's function and self-energy, this library can be used to solve any equation that can be written
in iterative form. Here is a small, complete example that solves the quadratic equation $\beta X^2 - X + \alpha = 0$:

```cpp
#include <green/sc/sc_loop.h>

#include <cmath>
#include <iostream>

// Solve beta * X^2 - X + alpha = 0 by iterating the "Dyson-like" equation
//   X = alpha + alpha * Sigma1 * X,   with Sigma1 = (beta / alpha) * X.

// Dyson-like part: given the self-energies, update the "Green's function"
class square_equation_dyson {
public:
  using G         = double;
  using Sigma1    = double;
  using Sigma_tau = double;

  explicit square_equation_dyson(const green::params::params& p) : _alpha(p["alpha"]) {}

  void solve(G& g, Sigma1& sigma1, Sigma_tau&) {
    double g_new = _alpha + _alpha * sigma1 * g;
    _diff        = std::abs(g - g_new);
    g            = g_new;
  }
  double diff(const G&, const Sigma1&, const Sigma_tau&) { return _diff; }
  void   dump_iteration(size_t, const G&, const Sigma1&, const Sigma_tau&, const std::string&) {}
  // chemical potential (written to and read from the results file)
  double  mu() const { return _mu; }
  double& mu() { return _mu; }
  // grid version written to the results file and checked on restart;
  // a real solver returns the version of its imaginary-time grid
  const std::string& get_grids_version() const { return green::grids::GRIDS_MIN_VERSION; }

private:
  double _alpha;
  double _diff = 0.0;
  double _mu   = 0.0;
};

// "Diagrammatic" part: given the Green's function, compute the self-energies
class square_equation_solver {
public:
  using G         = double;
  using Sigma1    = double;
  using Sigma_tau = double;

  square_equation_solver(double alpha, double beta) : _U(beta / alpha) {}
  void solve(const G& g, Sigma1& sigma1, Sigma_tau&) { sigma1 = _U * g; }

private:
  double _U;
};

int main(int argc, char** argv) {
  MPI_Init(&argc, &argv);
  {
    green::params::params p("Square equation example");
    green::sc::define_parameters(p);  // itermax, threshold, mixing_type, results_file, ...
    p.define<double>("alpha", "alpha", 0.2);
    p.define<double>("beta", "beta", 0.5);
    p.parse(argc, argv);

    green::sc::sc_loop<square_equation_dyson> sc(MPI_COMM_WORLD, p);
    square_equation_solver                    solver(p["alpha"], p["beta"]);

    double h0 = 0, ovlp = 0;          // only used by some mixing schemes
    double g = 0, sigma1 = 0, sigma_tau = 0;
    sc.solve(solver, h0, ovlp, g, sigma1, sigma_tau);

    std::cout << "X = " << g << std::endl;
  }
  MPI_Finalize();
}
```
Running it with, for example, `./example --itermax 100 --threshold 1e-12` converges to $X = 1 - \sqrt{0.6} \approx 0.2254$.
