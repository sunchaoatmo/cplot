#!/usr/bin/env python
import ESMF
from netCDF4 import Dataset
import numpy as np
def r2ll(xlat,xlon,clat,clon,regfield):
  ctk=ESMF.TypeKind.R8
  max_index = np.array(xlon.shape)
  grid = ESMF.Grid(max_index, staggerloc=[ESMF.StaggerLoc.CENTER], coord_sys=ESMF.CoordSys.CART, coord_typekind=ctk)
  [x, y] = [0, 1]
  xcoords=xlon
  ycoords=xlat
  gridXCenter = grid.get_coords(x)
  x_par = xcoords[grid.lower_bounds[ESMF.StaggerLoc.CENTER][x]:grid.upper_bounds[ESMF.StaggerLoc.CENTER][x]]
  gridXCenter[...] = x_par
  gridYCenter = grid.get_coords(y)
  y_par = ycoords[grid.lower_bounds[ESMF.StaggerLoc.CENTER][y]:grid.upper_bounds[ESMF.StaggerLoc.CENTER][y]]
  gridYCenter[...] = y_par
  srcfield = ESMF.Field(grid, name='srcfield', staggerloc=ESMF.StaggerLoc.CENTER)
  max_index = np.array(clon.shape)
  grid_cwrf = ESMF.Grid(max_index, staggerloc=[ESMF.StaggerLoc.CENTER], coord_sys=ESMF.CoordSys.CART, coord_typekind=ctk)
  gridXCenter = grid_cwrf.get_coords(x)
  gridXCenter[...]=clon[grid_cwrf.lower_bounds[ESMF.StaggerLoc.CENTER][x]:grid_cwrf.upper_bounds[ESMF.StaggerLoc.CENTER][x]]
  gridYCenter = grid_cwrf.get_coords(y)
  gridYCenter[...]=clat[grid_cwrf.lower_bounds[ESMF.StaggerLoc.CENTER][y]:grid_cwrf.upper_bounds[ESMF.StaggerLoc.CENTER][y]]
  dstfield = ESMF.Field(grid_cwrf, name='dstfield', staggerloc=ESMF.StaggerLoc.CENTER)
  regridSrc2Dst = ESMF.Regrid(srcfield, dstfield,
                                      regrid_method=ESMF.RegridMethod.NEAREST_DTOS,
                                      unmapped_action=ESMF.UnmappedAction.ERROR)
  srcfield.data[:] =regdata
  dstfield = regridSrc2Dst(srcfield, dstfield)
  return dstfield.data[:]
