#!/usr/bin/env python3.5

import os,sys,inspect
from netCDF4 import Dataset
import numpy as np
from geopy.distance import vincenty

try:
       sys.path.insert(1, os.path.join(sys.path[0], '..'))
       import VSF_simple as vsf
except ImportError:
       raise ImportError('cannot import VSF_simple module')

def test_vsfPytestCall():
    # Define paths and filenames, load data
    path = 'data/'
    source = Dataset(path+'GLAD.nc','r')

    u = source.variables['u'][0:100]
    u = np.transpose(u)
    v = source.variables['v'][0:100]
    v = np.transpose(v)
    lat = source.variables['lat'][0:100]
    lat = np.transpose(lat)
    lon = source.variables['lon'][0:100]
    lon = np.transpose(lon)

    [nd,nt] =u.shape

    print('')
    print(' DIMS: [nd, nt] = {}, {}'.format(nd,nt))

    # Call the function
    lj, tj, rj = vsf.VSFcalc(u,v,lat,lon, nd)

    print(lj, tj, rj)

if __name__ == '__main__':

    test_vsfPytestCall()
