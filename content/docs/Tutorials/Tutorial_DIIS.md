---
title: Tutorial: 
permalink: /Tutorial_DIIS/
math: true
weight: 41
---

## Simple example: Si
Si a a very convenient pedagogical system suitable as a simple example on how to run DIIS. As usual, we start from the integral preparation.

### Integral preparation
The files below set up the cell vectors and the coordinates, respectively:
`a.dat`:
```
0.0,  2.7155, 2.7155
2.7155, 0.0,  2.7155
2.7155, 2.7155, 0.0
```
`atoms.dat`:
```
Si 0.0  0.0  0.0
Si 1.35775 1.35775 1.35775
```

Then the actual PySCF script preparing integrals can be executed:
```
export OMP_NUM_THREADS=64 # OpenMP multithreading
python3 <source root>/green-mbpt/python/init_data_df.py          \
   --a a.dat --atom atoms.dat --nk 2 --pseudo gth-pbe            \
   --basis gth-dzvp-molopt-sr --auxbasis def2-svp-ri --df_int 1 --spin 0
```
The command above prepares integrals for `Si` using `2x2x2` Monkhorst--Pack k-point grid. Although this grid is very small, for our pedagogical purposes it is fine. The selected auxiliary basis set works reasonably well for light elements as `Si` for periodic solid calculations.

### DIIS execution
An example of the slurm script is below
```
#!/bin/bash

#SBATCH -N 1
#SBATCH -C gpu
#SBATCH -q debug
#SBATCH -J Ce_3
#SBATCH -t 00:30:00
#SBATCH --hint=nomultithread
#SBATCH --gpus-per-node=1

#OpenMP settings:
export OMP_NUM_THREADS=1
export HDF5_USE_FILE_LOCKING=FALSE
export HDF5_DISABLE_VERSION_CHECK=1

export GREEN_INSTALL=<path-to-installed-green-mbpt>
export GREEN_GRID=$GREEN_INSTALL/share/ir
export INTS=<path-to-generated-integrals>

date

srun -n 64 $GREEN_INSTALL/bin/mbpt.exe --scf_type=GW --BETA 300       \
  --grid_file $GREEN_GRID/1e5.h5 --itermax 100 --results_file Si.h5 \
  --input_file $INTS/input.h5 \
  --jobs SC   \
  --diis_start  2 \
  --diis_size  7 \
  --verbose 4 \
  --mixing_type CDIIS --damping 0.3  \
  --dfintegral_hf_file="$INTS/df_hf_int"  \
  --dfintegral_file="$INTS/df_int" \
  --kernel GPU --cuda_low_gpu_memory true --cuda_low_cpu_memory true >& Si_NEW.txt
```
Here `--diis_start` defines at which iteration DIIS will start, `--diis_size` defines the maximum size of the DIIS subspace, `--versbose` determines how verbose the output will be (large values are useful for troubleshooting), `--mixed_type` determines which mixing will be used (`DIIS` for difference residuals and `CDIIS` for commutator residuals), `--damping` is used only for the few first iterations building the DIIS subspace.

<!-- ![Performance of different convergence algorithms for Si](Si_DIIS.pdf) -->

<img
  src="Si_DIIS.pdf"
  alt="Performance of different convergence algorithms for Si"
/>



## Advanced example: BiVO3
BiVO3 is an interesting realistic system that we studied before:

<https://pubs.aip.org/aip/jcp/article/156/9/094101/2840744>

It shows an interesting convergence pattern and can serve as a good example on how to converge iterations. 
Thanks to Yanbing for sharing geometries and basis sets!

### Integral preparation

As usual, we need to generate integrals first. However, there are only very few basis sets available for Bi. For solids we commonly use basis sets from `molopt` family with `gth` pseudopotentials. MolSSI's Basis Set Exchange library, however, lack some of these basis sets. We can, for example, download the missing basis sets from CP2K:

<https://pierre-24.github.io/cp2k-basis/developers/library_content>

Then get the necessary basis sets and save them into the corresponding files, for example:
`Bi_basis`:
```
 Bi TZVP-MOLOPT-SR-GTH TZVP-MOLOPT-SR-GTH-q5
 1
 2 0 2 5 3 3 1
      1.66692829 -0.36896598 -0.13784534  0.01904790 -0.08133298  0.12465455  0.08937937 -0.15628186
      1.31794172  0.60312607  0.24301591 -0.07495626  0.24674021 -0.16489926 -0.06073193  0.26733662
      0.22222138 -0.51586411 -0.32950897  0.27952407 -0.92969758  0.19556854 -0.12518709 -0.75590352
      0.07452444 -0.43811758  0.89405382 -0.00047494 -0.09939405 -0.01225247  0.98609977 -0.39542603
      0.06672543 -0.20503722 -0.11846324 -0.95701871  0.24142794  0.95857827  0.01607445 -0.41994669
#
```

`V_basis`:
```
V TZVP-MOLOPT-SR-GTH TZVP-MOLOPT-SR-GTH-q13
 1
 2 0 3 6 4 3 3 1
      7.98462375  0.02087541 -0.00975098  0.02120107  0.03099923 -0.17157839 -0.01684344  0.01682335  0.09036199 -0.01161683  0.09137089 -0.00318569
      4.19216995  0.42475532 -0.25067357  0.26611498  0.33725015  0.19107997 -0.00355376 -0.01871944  0.30728774  0.04029333  0.33566567 -0.01236813
      1.67440329 -0.60690412  0.29451036 -0.14319412 -0.33682980  0.66551468 -0.01422047  0.37747378  0.49587427  0.03394291  0.72419759 -0.18175053
      0.66666458 -0.61757168 -0.08479144  0.28100055  0.72222853  0.63922519 -0.06264901  0.02670691  0.67892663 -0.28749821 -0.52617981 -0.77180670
      0.24241988  0.09883238  0.10332899 -0.87706388  0.45031275  0.23669763  0.69335240 -0.66031685  0.43624695  0.41501290 -0.26308693 -0.58022549
      0.06739027  0.24423739  0.91239512  0.24500289  0.21783356 -0.16280323  0.71752282  0.64818862 -0.01627523  0.86150940 -0.09185774 -0.18562438
#
```

`O_basis`:
```
#BASIS SET
 O  DZVP-MOLOPT-SR-GTH DZVP-MOLOPT-SR-GTH-q8
 1
 2 0 2 5 2 2 1
     10.389228018317  0.126240722900  0.069215797900 -0.061302037200 -0.026862701100  0.029845227500
      3.849621072005  0.139933704300  0.115634538900 -0.190087511700 -0.006283021000  0.060939733900
      1.388401188741 -0.434348231700 -0.322839719400 -0.377726982800 -0.224839187800  0.732321580100
      0.496955043655 -0.852791790900 -0.095944016600 -0.454266086000  0.380324658600  0.893564918400
      0.162491615040 -0.242351537800  1.102830348700 -0.257388983000  1.054102919900  0.152954188700
#
```
The saved files above contain  basis sets in the CP2K format, while our generating script understands basis sets in the NWChem format. One can either hack the python script using the PySCF machinery to feed the CP2K format or convert them in a cleaner way using the MolSSI tools as described here:

<https://molssi-bse.github.io/basis_set_exchange/conversion.html>

In our case, the user can execute the following commands performing conversion:
```ShellSession
  $ bse convert-basis --in-fmt cp2k --out-fmt nwchem Bi_basis Bi_basis_nwchem
  $ bse convert-basis --in-fmt cp2k --out-fmt nwchem V_basis V_basis_nwchem
  $ bse convert-basis --in-fmt cp2k --out-fmt nwchem O_basis O_basis_nwchem
```
These commands will create `Bi_basis_nwchem`, `V_basis_nwchem`, and `O_basis_nwchem` file with the basis sets in NWChem format.

Then we will need the crystal cell geometry `a.dat` and the atom positions `atoms.dat`:

`a.dat`:
```
0.392700000000E+01   0.000000000000E+00   0.000000000000E+00
0.000000000000E+00   0.392700000000E+01   0.000000000000E+00
0.000000000000E+00   0.000000000000E+00   0.785400000000E+01
```

`atoms.dat`:
```
V     1.963500000000E+00  1.963500000000E+00 -1.9635000
V     1.963500000000E+00  1.963500000000E+00  1.9635000
BI    0.000000000000E+00  0.000000000000E+00  0.0000000
BI    0.000000000000E+00  0.000000000000E+00  3.9270000
O     0.000000000000E+00  1.963500000000E+00 -1.9635000
O     0.000000000000E+00  1.963500000000E+00  1.9635000
O     1.963500000000E+00  0.000000000000E+00 -1.9635000
O     1.963500000000E+00  0.000000000000E+00  1.9635000
O     1.963500000000E+00  1.963500000000E+00  0.0000000
O     1.963500000000E+00  1.963500000000E+00  3.9270000
```

Then the actual PySCF script can be executed:
```
export OMP_NUM_THREADS=64 # OpenMP multithreading
python3 <source root>/green-mbpt/python/init_data_df.py          \
   --a a.dat --atom atoms.dat --nk 2                             \
   --basis 'Bi' 'Bi_basis_nwchem' 'V' 'V_basis_nwchem'           \
   'O' 'O_basis_nwchem' --pseudo gth-pade  --beta 3.0  --df_int 1
```

Here we generate even-tempered auxiliary basis sets, which are usually very good but large. In order to reduce the number of auxiliary basis functions, this example uses `--beta 3.0`. In this pedagogical example, PySCF HF iterations converge quickly, which is sometimes not the case in practice. 

### GW iterations
