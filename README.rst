
.. image:: https://travis-ci.com/JackOgaja/dataprocessing.svg?branch=master
    :target: https://travis-ci.com/JackOgaja/dataprocessing

data processing:
================

- This repository contains standalone codes and scripts written in: 
  python, matlab, NCL, shell-scripts, C and Fortran for geodynamic studies.  
- The individual codes and scripts are internally documented for easy application.  
- The codes and scripts currently available are listed below:  

Codes:
======
1. Vortex-surface Fields: VSF_simple.py  
- Reads geophysical data stored in NetCDF format 
- Calculates Vortex-surface Fields applying solutions of geodesics using Vincenty formula and 
- Writes ascii output.  

   - Language : Python

*Dependencies*
::
   - numpy
   - geopy
   - netCDF4

*To install:*
::
    ~$ git clone https://github.com/JackOgaja/geodynamics.git
    ~$ cd dataprocessing 

Usage:
::
    ~$ ./run_vsf.sh

