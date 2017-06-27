from context import reginalmetfield
class seasonal_data(reginalmetfield):
  def __init__(self,settings):
    reginalmetfield.__init__(self,settings)
  """
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT,Taylor,regmapfile):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT,Taylor,regmapfile=regmapfile)
  """


  def Output(self):
    if self.plottype=="Taylor": 
      from cstaylor import writedata
      for vname in self.vnames:
        writedata(self,vname)


