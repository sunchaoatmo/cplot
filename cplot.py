#!/usr/bin/env python
from config  import readini
#from context import reginalmetfield

(period,vnames,cases,nlevel,datapath,cutpoints,neof,
 masktype,method,plottype,shapefile,obsname,GCM_name,Hovmoller,Time_control)=readini()

wrfinputfile="%s/wrfinput_d01"%datapath
landmaskfile="%s/landmask.nc"%datapath

if period=="seasonal":
  from context import seasonal_data
  cwrfdata=seasonal_data(period,vnames,cases,nlevel,cutpoints,neof,
                 method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
                 wrfinputfile,landmaskfile,masktype)
elif period=="monthly":
  from context import monthly_data
  cwrfdata=monthly_data(period,vnames,cases,nlevel,cutpoints,neof,
                 method,plottype,shapefile,datapath,obsname,GCM_name,Hovmoller,Time_control,
                 wrfinputfile,landmaskfile,masktype)
elif period=="daily":
  from context import daily_data
  cwrfdata=daily_data(period,vnames,cases,nlevel,cutpoints,neof,
                 method,plottype,shapefile,datapath,obsname,GCM_name,Hovmoller,Time_control,
                 wrfinputfile,landmaskfile,masktype,Hovmoller)

cwrfdata.Read()
cwrfdata.Analysis()
cwrfdata.Plot()
