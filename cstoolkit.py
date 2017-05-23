#!/usr/bin/env python
from __future__ import division
import numpy as np# reshape
import struct
import os
from datetime import date 
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
  
# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.) 



def drange(start, stop, step):
  r = start
  while r < stop:
    yield r
    r += step

def vovercmap(data,clat,clon,fgeo,ax,firsttime,x,y,ylabels,cleve,cmp,m,k,u,v):
  # setup lambert conformal basemap.
  # lat_1 is first standard parallel.
  # lat_2 is second standard parallel (defaults to lat_1).
  # lon_0,lat_0 is central point.
  # rsphere=(6378137.00,6356752.3142) specifies WGS4 ellipsoid
  # area_thresh=1000 means don't plot coastline features less
  # than 1000 km^2 in area.
    if firsttime:
      m = Basemap(#width=12000000,height=9000000,
            #rsphere=(6378137.00,6356752.3142),
            resolution='l',projection='lcc',
            llcrnrlat=clat[0][0],urcrnrlat=clat[-1][-1],
            llcrnrlon=clon[0][0],urcrnrlon=clon[-1][-1],
            lat_1=getattr(fgeo,"TRUELAT1"),lat_2=getattr(fgeo,"TRUELAT2"),
            lat_0=getattr(fgeo,"CEN_LAT") ,lon_0=getattr(fgeo,"CEN_LON"))
      x, y = m(clon, clat)
      firsttime=False
    yy = np.arange(0, y.shape[0], 4)
    xx = np.arange(0, x.shape[1], 4)
    points = np.meshgrid(yy, xx) 
    m.drawcoastlines( linewidth=0.1)
    m.drawrivers( )
    m.etopo()
    m.drawstates(linewidth=0.1)
    #m.drawcoastlines( linewidth=0.01)
    #m.drawstates(linewidth=0.01)
    m.drawcountries()
    cs = m.contourf(x,y,data,cleve,cmap=cmp,extend='both')
    Q=m.quiver(x[points], y[points], u[points], v[points],scale=200)
    #m.barbs(x[points], y[points], u[points], v[points]) 
    #cs = m.contourf(x,y,data[:-1,:-1],cleve,cmap=cmp,extend='both')

    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(0.01)
    if k==0:
      ax.set_ylabel(ylabels, fontsize=6)
    return (firsttime,x,y,cs,m,Q);
class cwrfplot:
  def __init__(self,clat,clon,TRUELAT1,TRUELAT2,CEN_LAT,CEN_LON,shapefilepaths=None):
    self.m = Basemap( resolution='l',area_thresh=1000.,projection='lcc',
          llcrnrlat=clat[0][0],urcrnrlat=clat[-1][-1],
          llcrnrlon=clon[0][0],urcrnrlon=clon[-1][-1],
          lat_1=TRUELAT1,lat_2=TRUELAT2,
          lat_0=CEN_LAT ,lon_0=CEN_LON)
    self.x, self.y = self.m(clon, clat)
    self.segs={}
    if shapefilepaths:
      for shapefilepath in shapefilepaths:
        self.segs[shapefilepath]=self.readshapefileCS(shapefilepath,self.m)

  def readshapefileCS(self,shapefilepath,m ):
    import shapefile
    print(shapefilepath)
    r = shapefile.Reader(shapefilepath.encode('string-escape'))
    shapes = r.shapes()
    segs=[None]*len(shapes)
    for irecord, shape in enumerate(shapes):
      lons,lats = zip(*shape.points)
      lonlat = np.array(m(lons, lats)).T
      if len(shape.parts) == 1:
          segs[irecord] = [lonlat,]
      else:
          segs[irecord] = []
          for i in range(1,len(shape.parts)):
              index = shape.parts[i-1]
              index2 = shape.parts[i]
              segs[irecord].append(lonlat[index:index2])
          segs[irecord].append(lonlat[index2:])
    return segs

  def contourmap(self,data,ax,cleve,cmp, ylabels=None,sidenamefontsize=10  ):
    # setup lambert conformal basemap.
    # lat_1 is first standard parallel.
    # lat_2 is second standard parallel (defaults to lat_1).
    # lon_0,lat_0 is central point.
    # rsphere=(6378137.00,6356752.3142) specifies WGS4 ellipsoid
    # area_thresh=1000 means don't plot coastline features less
    # than 1000 km^2 in area.
    for shapefilepath,segs in self.segs.iteritems():
      from matplotlib.collections import LineCollection
      for seg in segs:
        lines = LineCollection(seg,antialiaseds=(1,))
        lines.set_edgecolors('gray')
        lines.set_linewidth(0.08)
        ax.add_collection(lines)
    self.m.drawcoastlines(linewidth=0.08,  color='gray', antialiased=1, ax=None, zorder=None)
    self.m.drawstates(linewidth=0.08,  color='gray') 
    import matplotlib.colors as mc
    norm = mc.BoundaryNorm(cleve, 256)
    cs = self.m.contourf(self.x,self.y,data,cleve,cmap=cmp,norm=norm,extend='both')
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(0.01)
    if ylabels:
      ax.set_ylabel(ylabels, fontsize=sidenamefontsize, fontweight='bold')
    [i.set_linewidth(0.1) for i in ax.spines.itervalues()]
    return (cs);

def daysbetween(by,bm,bd,ey,em,ed):
   tb=date(by,bm,bd)
   te=date(ey,em,ed)
   td=abs(te-tb).days
   return td;

def readbin(nx,ny,nm,rec,filename,endian):
   bytefloat=4
   size=nx*ny*nm
   dimsize_3d=(nm,nx,ny)
   fmt=endian+str(size)+'f'
   f=open(filename,'rb')
   f.seek(rec*nx*ny*bytefloat, os.SEEK_SET)
   value=struct.unpack(fmt, f.read(size*bytefloat))
   data =np.reshape(value,dimsize_3d)#(totalday,nx,ny))
   f.close()
   return data;

def prcdf(var,bin,dry_lim):
   var_filter=var[var>dry_lim]
   hist,bin_edge=np.histogram(var_filter, bins=bin,density=True)
#   hist=hist[::-1]
#   hist=np.cumsum(hist)
#   hist=hist[::-1]
   return hist

def eritimeselection(start_year,start_month,start_day,
                     end_year,end_month,end_day,
                     eri_time_origin,time_eri):
  from matplotlib import dates
  from datetime import date,timedelta
  time_start=date(start_year,start_month,start_day)
  time_end=date(end_year,end_month,end_day)
  start_rel_date=dates.date2num(time_start)-dates.date2num(eri_time_origin)
  end_rel_date=dates.date2num(time_end)-dates.date2num(eri_time_origin)
  start_rel_hour=int(start_rel_date*24)
  end_rel_hour=int(end_rel_date*24)
  eri_select_b=list(time_eri).index(12+start_rel_hour)
  eri_select_e=list(time_eri).index(12+  end_rel_hour)
  eri_start=eri_time_origin+timedelta(hours=int(time_eri[eri_select_b]))
  eri_end=eri_time_origin+timedelta(hours=int(time_eri[eri_select_e]))
  print("Eri data starting from %s till %s"% (eri_start.strftime('%Y%m%d'),eri_end.strftime('%Y%m%d')))
  return (eri_select_b,eri_select_e)
  
  

