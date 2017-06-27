from context import reginalmetfield
class monthly_data(reginalmetfield):
  def __init__(self,setting):
    reginalmetfield.__init__(self,setting)
  """
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT,Taylor):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT,Taylor)
  """
  def m2season(self,case,vname):
    import numpy as np
    m2s     ={12:0,3:1,6:2,9:3}
    s2m     ={0:12,1:3,2:6,3:9}
    irec=[0 for iseason in range(4)]
    seasonofmonth={12:0,1:0 ,2:0,
                   3:1 ,4:1 ,5:1,
                   6:2 ,7:2 ,8:2,
                   9:3 ,10:3,11:3}
    self.plotdata[case][vname]= np.zeros((self.ye-self.yb+1,4,self.nlat,self.nlon))
    for iyear in range(0,self.ye-self.yb+1):
      for imonth in range(0,12):
        year_cur= iyear-1 if iyear>0 and imonth==11 else iyear
        iseason=seasonofmonth[imonth+1]-1
        self.plotdata[case][vname][irec[iseason],iseason,:,:]=self.data[case][vname][year_cur,imonth,:,:]
        irec[iseason]+=1


  def Readjust(self):
    for vname in self.vnames:
      for case in self.cases:
        self.m2season(case,vname)
    self.data=self.plotdata[:]  #copy back HARD!


  def Analysis(self):
    if self.plottype=="timeserial":
      self.Tanalysis()
    else:   #  bad desgin for catch all, need to retouch later on if self.plottype=="contour":
      self.Readjust()
      reginalmetfield.Ianalysis()

  def Tanalysis(self):
    import numpy as np
    from constant import seasonname
    import cs_stat
    import numpy.ma as ma
    for case in self.plotlist:
      for vname in self.vnames:
        self.plotdata[case][vname]=np.zeros((self.ye-self.yb+1))
        self.plotdata[case][vname]=cs_stat.cs_stat.tananual_ana(
                                             sim=self.data[case][vname],
                                             obs=self.data[self.obsname][vname],
                                             mask=self.mask,
                                             maskval=self.maskval,   
                                             methodname=self.method
                                             )

  def Plot(self):
    if self.plottype=="timeserial":
      self.Tplot()
    else:
      reginalmetfield.plot(self)

  def Tplot(self):
    from cstimeserial import corplot
    for vname in self.vnames:
      corplot(self,vname)
