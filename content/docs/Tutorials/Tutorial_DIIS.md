---
title: Tutorial: 
permalink: /Tutorial_DIIS/
math: true
weight: 41
---

### BiVO3 example
BiVO3 is an interesting realistic system that we studied before:

<https://pubs.aip.org/aip/jcp/article/156/9/094101/2840744>

It shows interesting convergence pattern and can serve as a good example on how to converge iterations. 

## Integral preparation

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
The saved files above contain  basis sets in CP2K format, while our generating script understands basis sets in NWChem format. One can either hack the python script using PySCF machinery to feed the CP2K format or convert them in a cleaner way using MolSSI tools as described here:

<https://molssi-bse.github.io/basis_set_exchange/conversion.html>

In our case, the user can execute the following commands performing conversion:
```ShellSession
  $ bse convert-basis --in-fmt cp2k --out-fmt nwchem Bi_basis Bi_basis_nwchem
  $ bse convert-basis --in-fmt cp2k --out-fmt nwchem V_basis V_basis_nwchem
  $ bse convert-basis --in-fmt cp2k --out-fmt nwchem O_basis O_basis_nwchem
```
These commands will create `Bi_basis_nwchem`, `V_basis_nwchem`, and `O_basis_nwchem` file with the basis sets in NWChem format.

Then we will need crystal cell geometry `a.dat` and atom positions `atoms.dat`:

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
export OMP_NUM_THREADS=64

python3 /home/pokhilko/dev/green/green-mbpt/python/init_data_df.py --a a.dat --atom atoms.dat --nk 2 --basis 'Bi' 'Bi_basis_nwchem' 'V' 'V_basis_nwchem' 'O' 'O_basis_nwchem' --pseudo gth-pade  --beta 3.0  --df_int 1
```

Here we generate even-tempered auxiliary basis sets, which are usually very good but large. In order to reduce the number of auxiliary basis functions, this example uses `--beta 3.0`. In this pedagogical example, PySCF HF iterations converge quickly, which is sometimes not the case in practice. 
