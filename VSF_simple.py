# -*- coding: utf-8 -*-

__version__ = '0.1.0'
__description__ = ''
__author__ = 'Jack Ogaja  <jack.ogaja@gmail.com> '
__license__ = 'MIT'

#

from multiprocessing import Process, Manager
import numpy as np
from scipy.special import *
from geopy.distance import vincenty  # vincenty is depracated, Try geopy.distance.geodesic
from matplotlib.pyplot import *
from netCDF4 import Dataset
import itertools
#

def VSFcalc(u,v,lat,lon, nd):
    """
    : Describe your function here
    """

    # vectorize the computation:
    # Slice the arrays for differencing
    du_j = u[1:nd,:] - u[0:nd-1,:]
    dv_j = v[1:nd,:] - v[0:nd-1,:]

    arr1 = np.array((lat[0:nd-1,:]))
    arr2 = np.array((lon[0:nd-1,:]))
    arr3 = np.array((lat[1:nd,:]))
    arr4 = np.array((lon[1:nd,:]))

    # Warning: geopy.distance.vincenty is depracated!
    #          Try geopy.distance.geodesic for more accurate numbers
    print('')
    print(' Begin "vincenty" calculations... ')
    # This part consumes more resources and can be parallelized
    # if you intend to manipulate a 3D array or larger 2D arrays
    # It takes about 30seconds for the current array dims nd, nt
    dx_j = [ vincenty((kj,lj),(mj,nj)).km if np.isfinite(oj) else np.nan 
             for kj,lj,mj,nj,oj in np.nditer([arr1,arr2,arr1,arr4,du_j]) ] 
    dy_j = [ vincenty((kj,lj),(mj,nj)).km if np.isfinite(oj) else np.nan 
             for kj,lj,mj,nj,oj in np.nditer([arr1,arr2,arr3,arr2,du_j]) ] 
    dr_j = [ vincenty((kj,lj),(mj,nj)).km if np.isfinite(oj) else np.nan 
             for kj,lj,mj,nj,oj in np.nditer([arr1,arr2,arr3,arr4,du_j]) ] 
    # "dr_j2" would be necessary if an iterator is returned by the function
    #dr_j2 = [ (yield vincenty((kj,lj),(mj,nj)).km) if np.isfinite(oj) else (yield np.nan) 
    #         for kj,lj,mj,nj,oj in np.nditer([arr1,arr2,arr3,arr4,du_j]) ] 

    dx_s = [ np.sign(kj-lj) if np.isfinite(oj) else np.nan 
             for kj,lj,oj in np.nditer([arr4,arr2,du_j]) ] 
    dy_s = [ np.sign(kj-lj) if np.isfinite(oj) else np.nan 
             for kj,lj,oj in np.nditer([arr3,arr1,du_j]) ] 
    print(' "vincenty" calculations Finished')

    # Mask the variables to avoid 'NaNs'
    dx_j = np.ma.masked_where(np.isfinite(dx_j), dx_j)
    dy_j = np.ma.masked_where(np.isfinite(dy_j), dy_j)
    dx_s = np.ma.masked_where(np.isfinite(dx_s), dx_s)
    dy_s = np.ma.masked_where(np.isfinite(dy_s), dy_s)

    print(' Begin functions mapping... ')
    # - "dx=dx_j.data*dx_s.data" and dy=dy_j.data*dy_s.data"
    #   would also work but could result to
    #   erroneous numbers. It is not clear how Numpy handles 'NaN'
    # - Using the conditions a below will only give correct results
    #   if both boolean values of the ordered pair are similar
    #   otherwise the truth table of the if condition will not
    #   result to the expected results
    # - The map function generates an iterator which is more efficient
    dx   = map( lambda x: x[0]*x[1] if np.any([x[0], x[1]], axis=0)   
                else np.nan, list(zip(dx_j.data,dx_s.data))) 
    dy   = map( lambda y: y[0]*y[1] if np.any([y[0], y[1]], axis=0)  
                else np.nan, list(zip(dy_j.data,dy_s.data)))  

    # It is necessary to copy your generators here for multiple usage
    dx, dxObj = itertools.tee(dx)
    dy, dyObj = itertools.tee(dy)
   
    # - "dl=(du_j*dx + dv_j*dy)/dr_j" and "dt=(-du_j*dy + dv_j*dx)/dr_j" 
    #   would also work but could result to
    #   erroneous numbers. It is not clear how Numpy handles 'NaN'
    # - Using the conditions a below will only give correct results
    #   if both boolean values of the ordered tuple are similar
    #   otherwise the truth table of the if condition will not
    #   result to the expected results
    # - The map function generates an iterator which is more efficient
    dl   = map( lambda dj: (dj[0]*dj[2] + dj[1]*dj[3])/dj[4] if np.any([dj[0], dj[4]], axis=0)     
                else np.nan, list(zip(*du_j,*dv_j,list(dx),list(dy),dr_j)))    
    dt   = map( lambda dj: (-dj[0]*dj[3] + dj[1]*dj[2])/dj[4] if np.any([dj[0], dj[4]], axis=0)     
                else np.nan, list(zip(*du_j,*dv_j,list(dxObj),list(dyObj),dr_j)))      
    print(' Functions mapping Finished ')

    print('... returning a list of output')
    # returning list consumes a lot of memory
    # and slows down the I/O. This can be avoided
    # by returning an iterator which can be 
    # used to write data to an appendable text file
    return list(dl), list(dt), dr_j

if __name__ == '__main__': 
    
 #clear figures and console
 close("all")
 print(chr(27) + "[2J")

 # Define paths and filenames, load data
 path = 'data/' 
 source = Dataset(path+'GLAD.nc','r')

 u = source.variables['u'][:]
 u = np.transpose(u)
 v = source.variables['v'][:]
 v = np.transpose(v)
 lat = source.variables['lat'][:]
 lat = np.transpose(lat)
 lon = source.variables['lon'][:]
 lon = np.transpose(lon)

 [nd,nt] =u.shape
# nd = 4
 
 print('')
 print(' DIMS: [nd, nt] = {}, {}'.format(nd,nt))    

 # Call the function
 lj, tj, rj = VSFcalc(u,v,lat,lon, nd)

 print('')
 print(' Writing output')
 np.savetxt('output/l.txt',lj,fmt='%.5f')
 np.savetxt('output/t.txt',tj,fmt='%.5f')
 np.savetxt('output/r.txt',rj,fmt='%.5f')
    

