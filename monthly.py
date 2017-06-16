from context import reginalmetfield
class monthly_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT)
  def m2season(self,case,vname):
    m2s     ={12:0,3:1,6:2,9:3}
    s2m     ={0:12,1:3,2:6,3:9}
    irec=[0 for iseason in range(4)]
    seasonofmonth={12:0,1:0 ,2:0,
                   3:1 ,4:1 ,5:1,
                   6:2 ,7:2 ,8:2,
                   9:3 ,10:3,11:3}
    for iyear in range(0,self.ye-self.yb+1):
      for imonth in range(0,12):
        year_cur= iyear-1 if iyear>0 and imonth==11 else iyear
        iseason=seasonofmonth[imonth]-1
        self.plotdata[case][vname][irec[iseason],iseason,:,:]=self.data[case][vname][year_cur,imonth,:,:]
        irec[iseason]+=1


  def Readjust(self):
    for vname in self.vnames:
      for case in self.cases:
        self.m2season(case,vname)
    self.data=self.plotdata[:]  #copy back HARD!


