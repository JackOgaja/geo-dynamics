# -*- coding: utf-8 -*-
"""
"""

from multiprocessing import Process, Manager
from numpy import *
from scipy.special import *
from geopy.distance import vincenty
from matplotlib.pyplot import *
from netCDF4 import Dataset


#clear figures and console
close("all")
print(chr(27) + "[2J")

# Define paths and filenames, load data
path = '/Users/JennaPalmer/Google Drive/Baylor & Jenna/Gulf of Maine/Data/'
source = Dataset(path+'GLAD.nc','r')


u = source.variables['u'][:]
u = transpose(u)
v = source.variables['v'][:]
v = transpose(v)
lat = source.variables['lat'][:]
lat = transpose(lat)
lon = source.variables['lon'][:]
lon = transpose(lon)

#[nd,nt] =u.shape
nt = 20
    
def VSFcalc(d,u,v,lat,lon,tt):
    print(tt)
#    [nd,nt] =u.shape
    nd = 4
    # grab current list element for timestep
    ltemp = list(d['l'])
    ttemp = list(d['t'])
    rtemp = list(d['r'])
    
    # initialize variables
    combos = int(comb(nd,2))
    l = zeros((combos,))
    t = zeros((combos,))
    r = zeros((combos,))
 
    # set counter for number of drifter pairs
    dpair = 0
    
    for ii in range(0,nd-1):
        for jj in range(ii+1,nd):           
            du = u[jj,tt]-u[ii,tt]
            dv = v[jj,tt]-v[ii,tt]
            
            if isnan(du) == False:
                dx = vincenty((lat[ii,tt],lon[ii,tt]),(lat[ii,tt],lon[jj,tt])).km
                dy = vincenty((lat[ii,tt],lon[ii,tt]),(lat[jj,tt],lon[ii,tt])).km
                dr = vincenty((lat[ii,tt],lon[ii,tt]),(lat[jj,tt],lon[jj,tt])).km
            
                # get correct sign as vincenty returns absolute distance
                dx = sign(lon[jj,tt]-lon[ii,tt])*dx
                dy = sign(lat[jj,tt]-lat[ii,tt])*dy
            
            
                dl = (du*dx + dv*dy)/dr
                dt = (-du*dy + dv*dx)/dr
                l[dpair] = dl
                t[dpair] = dt
                r[dpair] = dr
                
            else:
                l[dpair] = nan
                t[dpair] = nan
                r[dpair] = nan
            dpair = dpair + 1
            
    ltemp.append(l)
    d['l'] = ltemp
    ttemp.append(t)
    d['t'] = ttemp
    rtemp.append(r)
    d['r'] = rtemp


if __name__ == '__main__': 
   
    manager = Manager()
    d = manager.dict()
    
    d['l'] = []
    d['t'] = []
    d['r'] = []
    job = [Process(target=VSFcalc, args =(d,u,v,lat,lon,tt)) for tt in range(nt)]
    _ = [p.start() for p in job]
    _ = [p.join() for p in job]
    
    
    nd = 4 
    
    # send to array and textfile to compare to matlab output
    combos = int(comb(nd,2))
    x=zeros((combos,nt))
    
    keys = ['l','t','r']
        
    for key in keys:
        for tt in range(3):   
            x[:,tt] = data[key][tt]

        savetxt(key + '.txt',x,fmt='%.5f')
    

