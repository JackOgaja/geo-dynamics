#!/bin/sh

# profile the code for optimization measurements
python3.5 -m cProfile -o tstats.out VSF_simple.py

# process the measurements into ascii 
./performance_stats.py > s_stats.tx

