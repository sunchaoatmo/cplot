class field(object):
  def __init__(self,period,vnames,cases,nlevel,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control):
    self.period=period
    self.vnames=vnames
    self.cases =cases
    self.plotlist =cases[:]
    for key in Time_control:
       setattr(self,key,Time_control[key])
    self.neof  =neof
    self.nlevel  =nlevel
    self.method  =method
    from collections import defaultdict
    self.data    =defaultdict(dict)
    self.plotdata=defaultdict(dict)
    self.plotname="%s_%s_%s_%s"%(plottype,self.yb,self.ye,method)
    self.plottype=plottype
    self.shapefile=shapefile
    self.datapath=datapath
    self.obsname =obsname
    if method=="cor":
      self.plotlist.remove(self.obsname)
    self.GCM_name =GCM_name

class reginalmetfield(field):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype):
    from netCDF4 import Dataset
    import numpy as np

    field.__init__(self,period,vnames,cases,nlevel,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control)

    wrfinput    =Dataset(wrfinputfile)
    lm          =Dataset(landmaskfile)
    self.truelat1=wrfinput.TRUELAT1
    self.truelat2=wrfinput.TRUELAT2
    self.cen_lat=wrfinput.CEN_LAT
    self.cen_lon=wrfinput.CEN_LON
    self.cutpoints=cutpoints
    self.lat=wrfinput.variables['CLAT'][0,cutpoints:-cutpoints,cutpoints:-cutpoints]
    self.lon=wrfinput.variables['CLONG'][0,cutpoints:-cutpoints,cutpoints:-cutpoints]
    self.nlat,self.nlon=self.lat.shape
    if masktype==1:
      self.mask= (np.logical_and(lm.variables["landmask"][cutpoints:-cutpoints,cutpoints:-cutpoints],
                                              wrfinput.variables["LANDMASK"][0,cutpoints:-cutpoints,cutpoints:-cutpoints] ))
    elif masktype==-1:
      self.mask= np.logical_not((np.logical_and(lm.variables["landmask"][cutpoints:-cutpoints,cutpoints:-cutpoints],
                                              wrfinput.variables["LANDMASK"][0,cutpoints:-cutpoints,cutpoints:-cutpoints] )))
class seasonal_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype)

  def Read(self):
    from netCDF4 import Dataset,num2date
    import numpy as np
    import numpy.ma as ma
    import sys
    for case in self.cases:
      for vname in self.vnames:
        filename="%s/%s_%s_%s.nc"%(self.datapath,case,vname,self.period)
        try:
          fnc     =Dataset(filename,"r")
        except:
          sys.exit("there is no %s"%filename)
        if   self.period=="daily":
          self.data[case][vname]=fnc.variables(vname)
        elif self.period=="monthly" or self.period=="seasonal":
          YB=int(fnc.variables["time"][ 0])
          dimsize=fnc.variables[vname].shape
          if len(dimsize)==5:
            self.data[case][vname]=fnc.variables[vname][self.yb-YB:self.ye-YB,:,self.nlevel,self.cutpoints:-self.cutpoints,self.cutpoints:-self.cutpoints]
          elif len(dimsize)==4:
            self.data[case][vname]=fnc.variables[vname][self.yb-YB:self.ye-YB,:,self.cutpoints:-self.cutpoints,self.cutpoints:-self.cutpoints]
          elif len(dimsize)==3:
            m2s     ={12:0,3:1,6:2,9:3}
            times   =fnc.variables['time']
            units   =times.units
            calendar=times.calendar
            firstdate=num2date(times[0],units,calendar=calendar)
            lastdate =num2date(times[0],units,calendar=calendar)
            nyear    =lastdate.year-firstdate.year+1
# this is a backward compitalbe implementation however we know it's ugly, hope it will be useless after we update all the post processing
            nz       = 12 if self.period=="monthly" else 4
            self.data[case][vname]=np.zeros((self.ye-self.yb,nz,self.nlat,self.nlon))
            for itime,time_cur in enumerate(times):
              date_cur=num2date(time_cur,units,calendar=calendar)
              if  self.period=="seasonal":
                if date_cur.year>=self.yb-1 and date_cur.year<self.ye-1:
                  z_cur=m2s[date_cur.month]
                  y_num=date_cur.year-firstdate.year if z_cur==0 else date_cur.year-firstdate.year-1
                  self.data[case][vname][y_num,z_cur,:,:]=fnc.variables[vname][itime,self.cutpoints:-self.cutpoints,self.cutpoints:-self.cutpoints]
                elif date_cur.year==self.ye-1:
                  break
              else:
                if date_cur.year>=self.yb and date_cur.year<self.ye:
                  z_cur=date_cur.month-1
                  y_num=date_cur.year-firstdate.year
                  print(z_cur,y_num)
                elif date_cur.year==self.ye:
                  break
          else:
            sys.exit("dimen size incorrect")
          _, mask_b = np.broadcast_arrays(self.data[case][vname], self.mask[None,...])
          self.data[case][vname]=ma.masked_array((self.data[case][vname]), mask=mask_b)
          print("Read in %s data %s:%s"%(case,self.period,vname))
        else:
          sys.exit('Sorry no such an option')

  def Analysis(self):
    import numpy as np
    import numpy.ma as ma
    from constant import seasonname
    import cs_stat
    import sys
    if self.method=="mean":
      for case in self.cases:
        for vname in self.vnames:
          self.plotdata[case][vname]=np.mean(self.data[case][vname],axis=0)
    elif self.method=="cor" or self.method=="rmse":
      for case in self.plotlist:
        for vname in self.vnames:
          self.plotdata[case][vname]= np.zeros((4,self.nlat,self.nlon))
          for k,name in enumerate(seasonname):
            self.plotdata[case][vname][k,:,:]= cs_stat.cs_stat.corrcoef_2d_mask(
                                               self.data[case][vname][:,k,:,:],
                                               self.data[self.obsname][vname][:,k,:,:],
                                               self.mask,self.method   )
          _, mask_b = np.broadcast_arrays(self.plotdata[case][vname], self.mask[None,...])
          self.plotdata[case][vname]=ma.masked_array((self.plotdata[case][vname]), mask=mask_b)
    elif self.method=="eof":
      from eofs.standard import eof
      for case in self.cases:
        for vname in self.vnames:
          self.plotdata[case][vname]=[]
          for k,name in enumerate(seasonname):
            if self.period=="seasonal":
              temp   =self.data[case][vname][:,k,:,:]
            elif self.period=="monthly":
              temp   =month2season(self.data[case][vname],k)
            else:
              sys.exit('sorry no such a period')
            print(case)
            print(temp.shape)
            temp   =temp-temp.mean(axis=0)
            solver = Eof(temp)
            eofmap = solver.eofs(neofs=self.neof)
            pcs    = solver.pcs(npcs=self.neof)
            var    = solver.varianceFraction(neigs=self.neof)
            self.plotdata[case][vname].append((eofmap,pcs,var))
    if "Taylor" in self.plottype:
      stdrefs={}
      samples={}
      for k,name in enumerate(seasonname):
        stdrefs[name]=ma.std(self.plotdata[self.obsname][vname][k,:,:]) #whether or not compressed has no impact on result
      for casenumber,case in enumerate(self.cases):
        if case!=self.obsname:
          tempoutput=[]
          for k,name in enumerate(seasonname):
            temp=self.plotdata[case][vname][k,:,:]
            if self.masktype==0:
              std_sim=np.std(np.ravel(temp))/stdrefs[name]
              coef=np.corrcoef(np.ravel(temp),np.ravel(self.plotdata[self.obsname][vname][k,:,:]))
              cor=coef[0,1]
            else:
              std_sim=ma.std(temp)/stdrefs[name]
              maskval=1
              coef=np.corrcoef(temp.compressed(),self.plotdata[self.obsname][vname][k,:,:].compressed())
              cor=coef[0,1]
            tempoutput.append((std_sim,cor))
          self.plotdata[case][vname]=tempoutput


  def Plot(self):
    if self.plottype=="contour": 
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

class daily_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,Hovmoller):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype)
    for key in Hovmoller:
       setattr(self,key,Hovmoller[key])

  def Read(self):
    from netCDF4 import Dataset,num2date
    import numpy as np
    import numpy.ma as ma
    import sys
    for case in self.cases:
      for vname in self.vnames:
        filename="%s/%s_%s_%s.nc"%(self.datapath,case,vname,self.period)
        try:
          fnc     =Dataset(filename,"r")
        except:
          sys.exit("there is no %s"%filename)
        self.data[case][vname]=fnc.variables(vname)
        self.time[case][vname]=fnc.variables("time")
        _, mask_b = np.broadcast_arrays(self.data[case][vname], self.mask[None,...])
        self.data[case][vname]=ma.masked_array((self.data[case][vname]), mask=mask_b)
        print("Read in %s data %s:%s"%(case,self.period,vname))

  def Analysis(self):
    import numpy as np
    import numpy.ma as ma
    from constant import seasonname
    import cs_stat
    if "Hovmoller" in self.plottype:
      xlat_1d=np.arang(self.start_lat,self.end_lat,self.dlat)
      xlon_1d=np.arang(self.start_lon,self.end_lon,self.dlon)
      xlat, xlon = meshgrid(xlat_1d, xlon_1d)
      self.data[case][vname]
      selecttimes=selectdays(self.yb,self.ye,self.start_day,self.start_month,self.end_day,self.end_month)
      for case in self.cases:
        for vname in self.vnames:
          timeinds=np.array(selecttimes[:])-self.time[case][vname][0]
          self.plotdata[case][vname]=np.zeros((len(timeinds),len(xlat_1d),len(xlon_1d)))
          for itime,timeind in enumerate(timeinds):
            self.plotdata[case][vname][itime,:,:]=r2ll(xlat,xlon,self.lat,self.lon,self.data[case][vname][timeind ,:,:])

  def Plot(self):
    if "Hovmoller" in self.plottype:
      from cshov import hovplot
      for vname in self.vnames:
        hovplot(self,vname)

  selectdays(yb,ye,db,mb,de,me,units,calendar):
    from netCDF4 import num2date
    from calendar import monthrange
    from datetime import datetime
    for year in range(yb,ye+1):
      for month in range(mb,me+1):
        db_cur=db if month==mb else 1
        de_cur=de if month==me else monthrange(year,month)[1]
        for day in range(db_cur,de_cur+1):
          date_cur=datetime[year,month,day]
          selectday_index.append[date2num(date_cur,units,calendar=calendar)]
     return selectday_index
