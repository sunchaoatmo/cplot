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
    self.filename=defaultdict(dict)
    self.time    =defaultdict(dict)
    self.plotdata=defaultdict(dict)
    self.plotname="%s-%s-%s"%(self.yb,self.ye,method)
    self.title   ={}
    for vname in vnames:
      self.title[vname]="%s %s %s-%s"%(vname,method if method!="mean" else "",self.yb,self.ye)
#     self.title[vname]="%s %s %s-%s"%(vname.replace("2",""),method if method!="mean" else "",self.yb,self.ye)
    self.plottype=plottype
    self.shapefile=shapefile
    self.datapath=datapath
    self.obsname =obsname
    if method=="cor" or method=="rmse" or plottype=="diff" or "Taylor" in plottype:
      self.plotlist.remove(self.obsname)
    self.GCM_name =GCM_name

  def Output(self):
    pass

class reginalmetfield(field):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,maskval=0,regmapfile=None):
    from netCDF4 import Dataset
    import numpy as np
    import numpy.ma as ma

    field.__init__(self,period,vnames,cases,nlevel,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control)

    wrfinput    =Dataset(wrfinputfile)
    lm          =Dataset(landmaskfile)
    if regmapfile:
      regmapnc    =Dataset(regmapfile)
      process_dict ={"mask":"LANDMASK","lat":'CLAT',"lon":'CLONG',"terrain":"HGT","regmap":"reg_mask"}
    else:
      process_dict ={"mask":"LANDMASK","lat":'CLAT',"lon":'CLONG',"terrain":"HGT"}
    self.truelat1=wrfinput.TRUELAT1
    self.truelat2=wrfinput.TRUELAT2
    self.cen_lat=wrfinput.CEN_LAT
    self.cen_lon=wrfinput.CEN_LON
    self.cutpoints=cutpoints
    self.maskval=maskval
    self.masktype=masktype
    for key,keyname in process_dict.iteritems():
       filenc=regmapnc if keyname=="reg_mask" else wrfinput
       setattr(self,key,filenc.variables[keyname][0,cutpoints[0]:-cutpoints[1],cutpoints[2]:-cutpoints[3]])
    self.nlat,self.nlon=self.lat.shape

    self.mask= (np.logical_and(lm.variables["landmask"][cutpoints[0]:-cutpoints[1],cutpoints[2]:-cutpoints[3]],
                self.mask ))

    if masktype==-1:
      self.mask= np.logical_not(self.mask)

    self.terrain =ma.masked_array(self.terrain,mask=self.mask)

    if regmapfile:
      self.regnames=regmapnc.variables['regname']
      self.nregs  =np.max(self.regmap)

class seasonal_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype)

  def Read(self):
    from netCDF4 import Dataset,num2date
    from plotset import plotres
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
        YB=int(fnc.variables["time"][ 0])
        dimsize=fnc.variables[vname].shape
        if len(dimsize)==5:
          self.data[case][vname]=fnc.variables[vname][self.yb-YB:self.ye-YB,:,self.nlevel,self.cutpoints[0]:-self.cutpoints[1],self.cutpoints[2]:-self.cutpoints[3]]
        elif len(dimsize)==4:
          self.data[case][vname]=fnc.variables[vname][self.yb-YB:self.ye-YB,:,self.cutpoints[0]:-self.cutpoints[1],self.cutpoints[2]:-self.cutpoints[3]]
        elif len(dimsize)==3:
          from datetime import datetime
          from netCDF4 import date2num
          m2s     ={12:0,3:1,6:2,9:3}
          s2m     ={0:12,1:3,2:6,3:9}
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
        _, mask_b = np.broadcast_arrays(self.data[case][vname], self.mask[None,...])
        self.data[case][vname]=ma.masked_array((self.data[case][vname]), mask=mask_b)
        if "shift" in plotres[vname]:
          self.data[case][vname]=self.data[case][vname]+plotres[vname]['shift']
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

class daily_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,Hovmoller,PDF,regmapfile):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,regmapfile=regmapfile)
    for key in Hovmoller:
       setattr(self,key,Hovmoller[key])

    for key in PDF:
       setattr(self,key,PDF[key])

    if self.method=="cor":
      self.x_min=-1.0
      self.x_max= 1.0

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
#       self.data[case][vname]=fnc.variables(vname)
        self.filename[case][vname]=filename
        self.time[case][vname]=fnc.variables["time"]

  def Analysis(self):
    import numpy as np
    import numpy.ma as ma
    from constant import seasonname
    import cs_stat

    def selectdays(yb,ye,db,de,mb,me,units,calendar):
      from netCDF4 import date2num
      from calendar import monthrange
      from datetime import datetime
#Watch out here there is a potential bug if the month number is smaller than 2
      if mb<=2:
        sys.exit("Please update the selectdays function to make it functional for Feb leap year issue. I am lasy CS.")
      numdays=0
      for month in range(mb,me+1):
        db_cur=db if month==mb else 1
        de_cur=de if month==me else monthrange(yb,month)[1]
        for day in range(db_cur,de_cur+1):
          numdays+=1
      selectday_index=np.zeros((ye-yb+1,numdays))
      for iyear,year in enumerate(range(yb,ye+1)):
        numdays=0
        for month in range(mb,me+1):
          db_cur=db if month==mb else 1
          de_cur=de if month==me else monthrange(year,month)[1]
          for iday,day in enumerate(range(db_cur,de_cur+1)):
            date_cur=datetime(year,month,day,0,0,0)
            selectday_index[iyear,numdays]=date2num(date_cur,units,calendar=calendar)
            numdays+=1
      return selectday_index

    def select_beg_end(yb,ye,nperiods,units,calendar):
      from netCDF4 import date2num
      from calendar import monthrange
      from datetime import datetime
      import numpy as np
      beg_nday=np.zeros((nperiods,nyears))
      end_nday=np.zeros((nperiods,nyears))
      sea2mon =((12,2),(3,5),(6,8),(9,11))
      for iyear,year in enumerate(range(yb,ye+1)):
        for iperiod in range(nperiods):
          if nperiods==4:
            mb,me=sea2mon[iperiod]
            yb=year-1 if iperiod==0 else year 
            ye=year
          elif nperiods==12:
            ye=year
            mb=iperiod+1
            me=iperiod+2
          else:
            sys.exit("Ouputnperiods is incorrect!")
          db=1
          de= monthrange(year,me)[1]
          date_b=datetime(yb,mb,db,0,0,0)
          date_e=datetime(ye,me,de,0,0,0)
          beg_nday[iperiod,iyear]=date2num(date_b,units,calendar=calendar)
          end_nday[iperiod,iyear]=date2num(date_e,units,calendar=calendar)
      return beg_nday,end_nday


    if "Hovmoller" in self.plottype:
      import cPickle as pickle
      xlat=np.arange(self.start_lat,self.end_lat,self.dlat)
      filenamep=self.plotname+"_dat.p"
      try:
        self.plotdata= pickle.load( open( filenamep, "rb" ) )
      except:
        for case in self.cases:
          for vname in self.vnames:
            units   =self.time[case][vname].units
            calendar=self.time[case][vname].calendar
            ntime   =len(self.time[case][vname])
            filename=self.filename[case][vname]
            nlat        =len(xlat)
            selecttimes=selectdays(self.yb,self.ye,self.start_day,self.end_day,self.start_month,self.end_month,units,calendar)
            timeinds=selecttimes-self.time[case][vname][0]+1
            [nyear,nday]=timeinds.shape
            self.plotdata[case][vname]=np.zeros((nlat,nday))
            self.plotdata[case][vname]=cs_stat.cs_stat.clim_hovm_daily(filename=filename,vname=vname,
                                       timeindex=timeinds,clat=self.lat,clon=self.lon,
                                       mask=self.mask,maskval=self.maskval,
                                       xlat=xlat,xlon_lb=self.start_lon,xlon_ub=self.end_lon,dlat=self.dlat,
                                       ncell=nlat,nday=nday,nyear=nyear,
                                       nlon=self.nlon,nlat=self.nlat,ntime=ntime)
        pickle.dump( self.plotdata, open(filenamep, "wb" ) )


    if "pdf" in self.plottype:
      import cPickle as pickle
      filenamep=self.plotname+"_dat.p"
      try:
        self.plotdata= pickle.load( open( filenamep, "rb" ) )
      except:
        nperiods=self.outputnperiod
        ncases=len(self.cases)
        nlandpoints=np.sum(self.maskval)
        nyears=self.ye-self.yb+1
        for vname in self.vnames:
          obsfilename=self.filename[self.obsname][vname]
          filenamelen = np.max(np.array([ len(self.filename[case][vname]) for case in self.cases if case!=self.obsname]))
          filenamea = [ self.filename[case][vname]+(filenamelen-len(self.filename[case][vname]))*" " 
                         for case in self.cases if case!=self.obsname]
          filename = np.array(filenamea,dtype=str(filenamelen)+'c').T
          units   =self.time[self.obsname][vname].units
          calendar=self.time[self.obsname][vname].calendar
          beg_nday,end_nday=select_beg_end(self.yb,self.ye,nperiods,units,calendar)
          ntime =end_nday[-1][-1]-beg_nday[0][0]+1
          print(self.n_bin,self.x_max)
          self.plotdata["all"][vname]=cs_stat.cs_stat.pdf_cor_rms(
                       ana_yearly=self.ana_yearly,methodname=self.method,vname=vname,
                       nlat=self.nlat,nlon=self.nlon,nregs=self.nregs,               
                       filename=filename,obsfilename=obsfilename,          
                       filenamelen=filenamelen,
                       ntime=ntime   ,nperiods=nperiods,nyears=nyears,ncases=ncases,  
                       beg_nday=beg_nday,end_nday=end_nday,             
                       mask=self.mask,maskval=self.maskval,nlandpoints=nlandpoints,      
                       regmap=self.regmap,                        
                       n_bin=self.n_bin,x_min=self.x_min,x_max=self.x_max)
        pickle.dump( self.plotdata, open(filenamep, "wb" ) )

  def Plot(self):
    if "Hovmoller" in self.plottype:
      from cshov import hovplot
      for vname in self.vnames:
        hovplot(self,vname)
    elif "pdf" in self.plottype:
      from cspdf import pdfplot
      for vname in self.vnames:
        pdfplot(self,vname)
