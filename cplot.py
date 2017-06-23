#!/usr/bin/env python
from config  import readini
#from context import reginalmetfield

(period,vnames,cases,nlevel,datapath,cutpoints,neof,
 masktype,method,plottype,shapefile,obsname,GCM_name,Hovmoller,Time_control,PDF,PLOT,Taylor,regmapfile)=readini()

wrfinputfile="%s/wrfinput_d01"%datapath
landmaskfile="%s/landmask.nc"%datapath

if period=="seasonal":
  from seasonal import seasonal_data
  cwrfdata=seasonal_data(period,vnames,cases,nlevel,cutpoints,neof,
                 method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
                 wrfinputfile,landmaskfile,masktype,PLOT,Taylor,regmapfile)
elif period=="monthly":
  from monthly import monthly_data
  cwrfdata=monthly_data(period,vnames,cases,nlevel,cutpoints,neof,
                 method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
                 wrfinputfile,landmaskfile,masktype,PLOT)
elif period=="daily":
  from daily import daily_data
  cwrfdata=daily_data(period,vnames,cases,nlevel,cutpoints,neof,
                 method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
                 wrfinputfile,landmaskfile,masktype,PLOT,Hovmoller,PDF,regmapfile)

cwrfdata.Read()
cwrfdata.Analysis()
cwrfdata.Plot()
cwrfdata.Output()
