from context import reginalmetfield
class daily_data(reginalmetfield):
  def __init__(self,setting):
    reginalmetfield.__init__(self,setting)

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
        nlandpoints=np.sum(self.mask)
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
          pdf,ets=cs_stat.cs_stat.pdf_cor_rms(
                       ana_yearly=self.ana_yearly,methodname=self.method,vname=vname,
                       nlat=self.nlat,nlon=self.nlon,nregs=self.nregs,               
                       filename=filename,obsfilename=obsfilename,          
                       filenamelen=filenamelen,
                       ntime=ntime   ,nperiods=nperiods,nyears=nyears,ncases=ncases,  
                       beg_nday=beg_nday,end_nday=end_nday,             
                       mask=self.mask,maskval=self.maskval,nlandpoints=nlandpoints,      
                       regmap=self.regmap,                        
                       n_bin=self.n_bin,x_min=self.x_min,x_max=self.x_max)
          self.plotdata["all"][vname]=pdf
        pickle.dump( self.plotdata, open(filenamep, "wb" ) )

    if "ets" in self.method:
      import cPickle as pickle
      filenamep=self.plotname+"_dat.p"
      try:
        self.plotdata= pickle.load( open( filenamep, "rb" ) )
      except:
        nperiods=self.outputnperiod
        ncases=len(self.cases)
        nlandpoints=np.sum(self.mask)
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
          pdf,ets=cs_stat.cs_stat.pdf_cor_rms(
                       ana_yearly=self.ana_yearly,methodname=self.method,vname=vname,
                       nlat=self.nlat,nlon=self.nlon,nregs=self.nregs,               
                       filename=filename,obsfilename=obsfilename,          
                       filenamelen=filenamelen,
                       ntime=ntime   ,nperiods=nperiods,nyears=nyears,ncases=ncases,  
                       beg_nday=beg_nday,end_nday=end_nday,             
                       mask=self.mask,maskval=self.maskval,nlandpoints=nlandpoints,      
                       regmap=self.regmap,                        
                       n_bin=self.n_bin,x_min=self.x_min,x_max=self.x_max,
                       cutpoints=self.cutpoints,
                       crts=self.crts_level)
          self.plotdata["all"][vname]=ets
        pickle.dump( self.plotdata, open(filenamep, "wb" ) )


  def Plot(self):
    for vname in self.vnames:
      if "Hovmoller" in self.plottype:
        from cshov import hovplot
        hovplot(self,vname)
      elif "pdf" in self.plottype:
        from cspdf import pdfplot
        pdfplot(self,vname)
      elif "ets" in self.method:
        from cscontour import seasonalmap
        from constant import seasonname
        import numpy.ma as ma
        import numpy as np
        for icrt,crt in enumerate(self.crts_level):
          for icase,case in enumerate(self.plotlist):
            self.plotdata[case][vname]= np.zeros((4,self.nlat,self.nlon))
            for k,name in enumerate(seasonname):
              self.plotdata[case][vname][k,:,:]=self.plotdata["all"][vname][icrt,:,:,k,icase]
              _, mask_b = np.broadcast_arrays(self.plotdata[case][vname], self.mask[None,...])
              self.plotdata[case][vname]=ma.masked_array((self.plotdata[case][vname]), mask=mask_b)
          seasonalmap(self,vname,crt)
