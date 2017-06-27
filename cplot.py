#!/usr/bin/env python
from config  import readini
#from context import reginalmetfield

settings=readini()

period=settings["MAIN"]["period"]

if period=="seasonal":
  from seasonal import seasonal_data
  cwrfdata=seasonal_data(settings)
  #cwrfdata=seasonal_data(period,vnames,cases,nlevel,cutpoints,neof,
  #               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
  #               wrfinputfile,landmaskfile,masktype,PLOT,Taylor,regmapfile)
elif period=="monthly":
  from monthly import monthly_data
  cwrfdata=monthly_data(settings)
  #cwrfdata=monthly_data(period,vnames,cases,nlevel,cutpoints,neof,
  #               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
  #               wrfinputfile,landmaskfile,masktype,PLOT,Taylor)
elif period=="daily":
  from daily import daily_data
  cwrfdata=daily_data(settings)
  #cwrfdata=daily_data(period,vnames,cases,nlevel,cutpoints,neof,
  #               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
  #               wrfinputfile,landmaskfile,masktype,PLOT,Hovmoller,PDF,regmapfile)

cwrfdata.Read()
cwrfdata.Analysis()
cwrfdata.Plot()
cwrfdata.Output()
