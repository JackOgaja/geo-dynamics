
.. image:: https://travis-ci.com/JackOgaja/geo-dynamics.svg?branch=master
    :target: https://travis-ci.com/JackOgaja/geo-dynamics
.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
    :target: https://github.com/JackOgaja/geo-dynamics/blob/master/LICENSE.md

Geo-dynamics:
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

:Language: 
    Python

*Dependencies*
::
   - numpy
   - geopy
   - netCDF4

*To install:*
::
    ~$ git clone https://github.com/JackOgaja/geo-dynamics.git
    ~$ cd geo-dynamics 

Usage:
::
    ~$ ./run_vsf.sh

