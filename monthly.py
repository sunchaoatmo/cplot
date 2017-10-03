from context import reginalmetfield
class monthly_data(reginalmetfield):
  def __init__(self,setting):
    reginalmetfield.__init__(self,setting)

  def m2season(self,case,vname):
    import numpy as np
    m2s     ={12:0,3:1,6:2,9:3}
    s2m     ={0:12,1:3,2:6,3:9}
    irec=[0 for iseason in range(4)]
    seasonofmonth={12:0,1:0 ,2:0,
                   3:1 ,4:1 ,5:1,
                   6:2 ,7:2 ,8:2,
                   9:3 ,10:3,11:3}
    self.plotdata[case][vname]= np.zeros(((self.ye-self.yb+1)*3,4,self.nlat,self.nlon))
    climate=[]
    for imonth in range(0,12):
      climate.append(np.mean(self.data[case][vname][:,imonth,:,:],axis=0))
    for iyear in range(0,self.ye-self.yb+1):
      for imonth in range(0,12):
        year_cur= iyear-1 if iyear>0 and imonth==11 else iyear
        iseason=seasonofmonth[imonth+1]
        self.plotdata[case][vname][irec[iseason],iseason,:,:]=self.data[case][vname][year_cur,imonth,:,:]-climate[imonth]
        irec[iseason]+=1


  def Readjust(self):
    for vname in self.vnames:
      for case in self.cases:
        self.m2season(case,vname)
        self.data[case][vname]=self.plotdata[case][vname][:]  #copy back HARD!


  def Analysis(self):
    if self.plottype=="timeserial":
      self.Tanalysis()
    else:   #  bad desgin for catch all, need to retouch later on if self.plottype=="contour":
      self.Readjust()
      reginalmetfield.Ianalysis(self)

  def Tanalysis(self):
    import numpy as np
    from constant import seasonname
    import cs_stat
    import numpy.ma as ma
    for case in self.cases:
      for vname in self.vnames:
        self.plotdata[case][vname]=[]
        print(case)
        cor,ets,reganon,regmean,regstd=cs_stat.cs_stat.tananual_ana(
                                           sim=self.data[case][vname],
                                           obs=self.data[self.obsname][vname],
                                           crts=self.crts_level,
                                           mask=self.regmask_new,
                                           maskval=self.maskval,
                                           #mask=self.mask,
                                           #maskval=self.maskval,   
                                           methodname=self.method
                                           )
        if self.method=="ets":
          self.plotdata[case][vname]=ets
        elif self.method=="cor":  
          self.plotdata[case][vname]=cor
        elif self.method=="mean":  
          self.plotdata[case][vname]=(reganon,regmean,regstd)

  def Plot(self):
    if self.plottype=="timeserial":
      self.Tplot()
    else:
      reginalmetfield.Plot(self)

  def Tplot(self):
    if self.method=="Tcor":
      from cstimeserial import corplot
      for vname in self.vnames:
        corplot(self,vname)
    elif self.method=="ets":
      from csets import etscontourf
      for vname in self.vnames:
        etscontourf(self,vname)
    elif self.method=="mean":
      from cstimeserial import meanplot #,monthlystdfillplot
      for vname in self.vnames:
        meanplot(self,vname)
