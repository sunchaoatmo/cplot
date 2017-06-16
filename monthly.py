from context import reginalmetfield
class monthly_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT)

  def Read(self):
    from netCDF4 import Dataset,num2date
    from plotset import plotres
    import numpy as np
    import numpy.ma as ma
    import sys
    nseasons=4
    m2s     ={12:0,3:1,6:2,9:3}
    s2m     ={0:12,1:3,2:6,3:9}
    for case in self.cases:
      for vname in self.vnames:
        filename="%s/%s_%s_%s.nc"%(self.datapath,case,vname,self.period)
        try:
          fnc     =Dataset(filename,"r")
        except:
          sys.exit("there is no %s"%filename)
        YB=int(fnc.variables["time"][ 0])
        dimsize=fnc.variables[vname].shape
        nyear=dimsize[0]
        nx=dimsize[-2]-self.cutpoints[1]-self.cutpoints[0]
        ny=dimsize[-1]-self.cutpoints[2]-self.cutpoints[3]
        self.plotdata[case][vname]=np.zeros((nyear,nseasons,nx,ny))
        if len(dimsize)==5:
          self.data[case][vname]=fnc.variables[vname][self.yb-YB:self.ye-YB,:,self.nlevel,self.cutpoints[0]:-self.cutpoints[1],self.cutpoints[2]:-self.cutpoints[3]]
        elif len(dimsize)==4:
          self.data[case][vname]=fnc.variables[vname][self.yb-YB:self.ye-YB,:,self.cutpoints[0]:-self.cutpoints[1],self.cutpoints[2]:-self.cutpoints[3]]
        elif len(dimsize)==3:
          from datetime import datetime
          from netCDF4 import date2num
          times   =fnc.variables['time']
          units   =times.units
          calendar=times.calendar
          firstdate=num2date(times[0],units,calendar=calendar)
          lastdate =num2date(times[0],units,calendar=calendar)
          nyear    =lastdate.year-firstdate.year+1
# this is a backward compitalbe implementation however we know it's ugly, hope it will be useless after we update all the post processing
          nz       = 12 if self.period=="monthly" else 4
          self.data[case][vname]=np.zeros((self.ye-self.yb,nz,self.nlat,self.nlon))
          convert=60*60*24 if vname=="PRAVG" else 1
          for iyear,year in enumerate(range(self.yb,self.ye)):
            for iseason in range(4):
              month=s2m[iseason]
              year_cur= year-1 if iseason==0 else year
              date_cur=datetime(year_cur,month,1,0,0,0)
              time_cur=date2num(date_cur,units,calendar=calendar)
              itime   =np.where(times==time_cur)[0]
              self.data[case][vname][iyear,iseason,:,:]=convert*fnc.variables[vname][itime,self.cutpoints[0]:-self.cutpoints[1],self.cutpoints[2]:-self.cutpoints[3]]
        else:
          sys.exit("dimen size incorrect")
#       _, mask_b = np.broadcast_arrays(self.data[case][vname], self.mask[None,...])
#       self.data[case][vname]=ma.masked_array((self.data[case][vname]), mask=mask_b)
        if "shift" in plotres[vname]:
          self.data[case][vname]=self.data[case][vname]+plotres[vname]['shift']
        for iseason in range(nseasons):
          mb=s2m[iseason]
          me=mb+3
          print(self.data[case][vname][:,:,:,:].shape)
          print(self.data[case][vname][:,mb:me,:,:].shape)
          self.plotdata[case][vname][:,iseason,:,:]=np.mean(self.data[case][vname][:,mb:me,:,:])
        print("Read in %s data %s:%s"%(case,self.period,vname))

  def Analysis(self):
    import numpy as np
    import numpy.ma as ma
    from constant import seasonname
    import cs_stat
    import sys
    for vname in self.vnames:
      for case in self.cases:
        if self.method=="eof":
          from eofs.standard import Eof
          self.plotdata[case][vname]=[]
          for k,name in enumerate(seasonname):
            temp   =self.data[case][vname][:,k,:,:]
            temp   =temp-temp.mean(axis=0)
            solver = Eof(temp)
            eofmap = solver.eofs(neofs=self.neof)
            pcs    = solver.pcs(npcs=self.neof)
            var    = solver.varianceFraction(neigs=self.neof)
            self.plotdata[case][vname].append((eofmap,pcs,var))
        else: #if self.method=="cor" or self.method=="rmse" or self.method=="trend" or self.method=="mean":
          self.plotdata[case][vname]= np.zeros((4,self.nlat,self.nlon))
          for k,name in enumerate(seasonname):
            self.plotdata[case][vname][k,:,:]= cs_stat.cs_stat.ananual_ana(
                                               sim=self.data[case][vname][:,k,:,:],
                                               obs=self.data[self.obsname][vname][:,k,:,:],
                                               mask=self.mask,
                                               methodname=self.method ,
                                               maskval=self.maskval  )
          _, mask_b = np.broadcast_arrays(self.plotdata[case][vname], self.mask[None,...])
          self.plotdata[case][vname]=ma.masked_array((self.plotdata[case][vname]), mask=mask_b)


      for casenumber,case in enumerate(self.plotlist):
        if "Taylor" in self.plottype:
          stdrefs={}
          samples={}
          tempoutput=[]
          for k,name in enumerate(seasonname):
            stdrefs[name]=ma.std(self.plotdata[self.obsname][vname][k,:,:]) #whether or not compressed has no impact on result
            temp=self.plotdata[case][vname][k,:,:]
            std_sim=ma.std(temp)/stdrefs[name]
            coef=np.corrcoef(temp.compressed(),self.plotdata[self.obsname][vname][k,:,:].compressed())
            cor=coef[0,1]
            tempoutput.append((std_sim,cor))
          self.plotdata[case][vname]=tempoutput
        if self.plottype=="diff":
          self.plotdata[case][vname]=self.plotdata[case][vname]-self.plotdata[self.obsname][vname]


  def Plot(self):
    if self.plottype=="contour" or self.plottype=="diff": 
      if self.method=="eof":
        from cseof import eofplot
        for vname in self.vnames:
          eofplot(self,vname)
      else:
        from cscontour import seasonalmap
        for vname in self.vnames:
          seasonalmap(self,vname)
    elif self.plottype=="Taylor": 
      from cstaylor import seasonaltaylor
      for vname in self.vnames:
        seasonaltaylor(self,vname)
    elif self.plottype=="CTaylor": 
      from cstaylor import combinedtaylor
      combinedtaylor(self)

  def month2season(data_i,k):
    nyear,nmonth,nlat,nlon=data_i.shape
    index=0
    begmonth=[11,2,5,8]
    data_o=np.zeros((nyear-1)*3,nlat,nlon)
    for year in range(1,1+nyear):
      if k==0:
        data_o[index,:,:]=data_i[year-1,11,:,:] 
        index+=1
        data_o[index,:,:]=data_i[year,0,:,:] 
        index+=1
        data_o[index,:,:]=data_i[year,1,:,:] 
        index+=1
      else:
        for i in range(3):
          data_o[index,:,:]=data_i[year,begmonth(k)+i,:,:] 
          index+=1
    return data_o

  def Output(self):
    if self.plottype=="CTaylor": 
      from cstaylor import writedata
      for vname in self.vnames:
        writedata(self,vname)


