from netCDF4 import Dataset
import numpy as np
class static:
  def __init__(self,wrfinputfile,landmaskfile,cutpoints,masktype):
    wrfinput    =Dataset(wrfinputfile)
    lm          =Dataset(landmaskfile)
    self.truelat1=wrfinput.TRUELAT1
    self.truelat2=wrfinput.TRUELAT2
    self.cen_lat=wrfinput.CEN_LAT
    self.cen_lon=wrfinput.CEN_LON
    self.lat=wrfinput.variables['CLAT'][0,cutpoints:-cutpoints,cutpoints:-cutpoints]
    self.lon=wrfinput.variables['CLONG'][0,cutpoints:-cutpoints,cutpoints:-cutpoints]
    if masktype==1:
      self.mask= (np.logical_and(lm.variables["landmask"][cutpoints:-cutpoints,cutpoints:-cutpoints],
                                              wrfinput.variables["LANDMASK"][0,cutpoints:-cutpoints,cutpoints:-cutpoints] ))
    elif masktype==-1:
      self.mask= np.logical_not((np.logical_and(lm.variables["landmask"][cutpoints:-cutpoints,cutpoints:-cutpoints],
                                              wrfinput.variables["LANDMASK"][0,cutpoints:-cutpoints,cutpoints:-cutpoints] )))
