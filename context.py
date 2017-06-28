class field(object):
  def __init__(self,settings):
    from itertools import combinations
    from collections import defaultdict
    from plotset     import tableau20
    for section,items in settings.iteritems():
      for key,value in items.iteritems():
       setattr(self,key,value)
    self.wrfinputfile="%s/wrfinput_d01"%self.datapath
    self.landmaskfile="%s/landmask.nc"%self.datapath
    self.casecolors  =dict(zip(self.cases,[tableau20[ic] for ic in self.colors]))

      
    self.plotlist =self.cases[:]
    self.data    =defaultdict(dict)
    self.filename=defaultdict(dict)
    self.time    =defaultdict(dict)
    self.plotdata=defaultdict(dict)
    self.plotname="%s-%s-%s-%s"%(self.yb,self.ye,self.method,self.period)
    self.title   ={}
    if "X" in self.method:
      self.xvnames=[combined for combined in combinations(self.vnames, 2)] 
      for vname in self.xvnames:
        self.title[vname]="%s vs %s cor %s-%s"%(vname[0],vname[1],self.yb,self.ye)
    else:
      for vname in self.vnames:
        self.title[vname]="%s %s %s-%s"%(vname,self.method if self.method!="mean" else "",self.yb,self.ye)
    if "ets"==self.method or "cor"==self.method or "Tcor"==self.method or self.method=="rmse" or self.method=="diff" or "Taylor" in self.plottype:
      self.plotlist.remove(self.obsname)

  def Output(self):
    pass

class reginalmetfield(field):
  def __init__(self,setting):
    from netCDF4 import Dataset
    import numpy as np
    import numpy.ma as ma

    field.__init__(self,setting)

    """
    field.__init__(self,period,vnames,cases,nlevel,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control)
    """

    wrfinput    =Dataset(self.wrfinputfile)
    lm          =Dataset(self.landmaskfile)
    if self.regmapfile:
      regmapnc    =Dataset(self.regmapfile)
      process_dict ={"mask":"LANDMASK","lat":'CLAT',"lon":'CLONG',"terrain":"HGT","regmap":"reg_mask","regnames":"regname"}
    else:
      process_dict ={"mask":"LANDMASK","lat":'CLAT',"lon":'CLONG',"terrain":"HGT"}
    self.truelat1=wrfinput.TRUELAT1
    self.truelat2=wrfinput.TRUELAT2
    self.cen_lat=wrfinput.CEN_LAT
    self.cen_lon=wrfinput.CEN_LON
    cutpoints=[int(x) for x in self.cutpoints]

    for key,keyname in process_dict.iteritems():
       if "reg" in keyname:
         filenc=regmapnc
         try:
           setattr(self,key,filenc.variables[keyname][cutpoints[0]:-cutpoints[1],cutpoints[2]:-cutpoints[3]])
         except:
           setattr(self,key,filenc.variables[keyname])
       else:
         filenc=wrfinput
         setattr(self,key,filenc.variables[keyname][0,cutpoints[0]:-cutpoints[1],cutpoints[2]:-cutpoints[3]])
    self.nlat,self.nlon=self.lat.shape
    self.mask=lm.variables["landmask"][cutpoints[0]:-cutpoints[1],cutpoints[2]:-cutpoints[3]]*self.mask

    if self.masktype==-1:
      self.mask= np.logical_not(self.mask)

    self.terrain =ma.masked_array(self.terrain,mask=self.mask)


  def d2p(outputdict,fnc):
    # watach out the dict is altered in this fun!!!
    # This function will convert the data from daily axis to [year, ipeiod, i,j] settings, so the ipeiod can be season or monthly
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
    nz       = 12 if self.period=="monthly" else 4
    outputdict[case][vname]=np.zeros((self.ye-self.yb,nz,self.nlat,self.nlon))
    convert=60*60*24 if vname=="PRAVG" else 1
    for iyear,year in enumerate(range(self.yb,self.ye)):
      for iseason in range(4):
        month=s2m[iseason]
        year_cur= year-1 if iseason==0 else year
        date_cur=datetime(year_cur,month,1,0,0,0)
        time_cur=date2num(date_cur,units,calendar=calendar)
        itime   =np.where(times==time_cur)[0]
        outputdict[case][vname][iyear,iseason,:,:]=convert*fnc.variables[vname][itime,self.cutpoints[0]:-self.cutpoints[1],self.cutpoints[2]:-self.cutpoints[3]]

  def Read(self):
    from netCDF4 import Dataset,num2date
    from plotset import plotres
    import numpy as np
    import numpy.ma as ma
    import sys
    for case in self.cases:
      for vname in self.vnames:
        if vname not in ["PRAVG","PCT","CDD","RAINYDAYS","R10"]: 
          filename="%s/%s_%s_%s.nc"%(self.datapath,case,vname,self.period)
        else:
          filename="%s/%s_%s_%s.nc"%(self.datapath,case,"PR",self.period)
        print(filename)

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
          d2p(self.data[case][vname],fnc.variables[vname])
        else:
          sys.exit("dimen size incorrect")
        if "shift" in plotres[vname]:
          self.data[case][vname]=self.data[case][vname]+plotres[vname]['shift']
        print("Read in %s data %s:%s"%(case,self.period,vname))


  def Analysis(self):
    if "X" in self.method:
      self.Xanalysis()
    else:
      self.Ianalysis()

  def Ianalysis(self):
    if self.tltype=="spatial":
      self.spatialanalysis()
    elif self.tltype=="temporal":
      self.temporalanalysis()

  def Xanalysis(self):
    import numpy as np
    from constant import seasonname
    import cs_stat
    import numpy.ma as ma
    for case in self.cases:
      for vname in self.xvnames:
        self.plotdata[case][vname]= np.zeros((4,self.nlat,self.nlon))
        for k,name in enumerate(seasonname):
          self.plotdata[case][vname][k]= cs_stat.cs_stat.xananual_ana(
                                             sim1=self.data[case][vname[0]][:,k,:,:],
                                             obs1=self.data[self.obsname][vname[0]][:,k,:,:],
                                             sim2=self.data[case][vname[1]][:,k,:,:],
                                             obs2=self.data[self.obsname][vname[1]][:,k,:,:],
                                             mask=self.mask,
                                             methodname=self.method ,
                                             maskval=self.maskval  )
        _, mask_b = np.broadcast_arrays(self.plotdata[case][vname], self.mask[None,...])
        self.plotdata[case][vname]=ma.masked_array((self.plotdata[case][vname]), mask=mask_b)



  def temporalanalysis(self):
    import numpy as np
    import numpy.ma as ma
    from constant import seasonname
    import cs_stat
    import sys
    for vname in self.vnames:
      for case in self.plotlist:
        self.plotdata[case][vname]= np.zeros((int(self.nregs)+1,4,self.ye-self.yb+1,2))
        self.plotdata[case][vname]= cs_stat.cs_stat.ananual_temp(
                                             sim=self.data[case][vname],
                                             obs=self.data[self.obsname][vname],
                                             mask=self.mask,
                                             maskval=self.maskval  ,regmap=self.regmap,nregs=int(self.nregs))


  def spatialanalysis(self):
    import numpy as np
    import numpy.ma as ma
    from constant import seasonname
    import cs_stat
    import sys
    def taylorcalculator(obs,sim):
      stdrefs=ma.std(obs) #whether or not compressed has no impact on result
      std_sim=ma.std(sim)/stdrefs
      coef=np.corrcoef(sim,obs)
      return (std_sim,coef[0,1])

    for vname in self.vnames:
      for case in self.cases:
        if self.method=="eof":
          from eofs.standard import eof
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
            self.plotdata[case][vname][k]= cs_stat.cs_stat.ananual_ana(
                                               sim=self.data[case][vname][:,k,:,:],
                                               obs=self.data[self.obsname][vname][:,k,:,:],
                                               mask=self.mask,
                                               methodname=self.method ,
                                               maskval=self.maskval  )
          _, mask_b = np.broadcast_arrays(self.plotdata[case][vname], self.mask[None,...])
          self.plotdata[case][vname]=ma.masked_array((self.plotdata[case][vname]), mask=mask_b)



      for case in self.plotlist:
        if "Taylor" in self.plottype:
          tempoutput=np.zeros((int(self.nregs)+1,len(seasonname),2))
          for k,name in enumerate(seasonname):
            tempoutput[0,k,:]=taylorcalculator(self.plotdata[self.obsname][vname][k,:,:].compressed(),
                                               self.plotdata[case][vname][k,:,:].compressed())
            for ireg in range(1,1+int(self.nregs)):
              tempoutput[ireg,k,:]=taylorcalculator(self.plotdata[self.obsname][vname][k,self.regmap==ireg].compressed(),
                                                    self.plotdata[case][vname][k,self.regmap==ireg].compressed())
          self.plotdata[case][vname]=tempoutput

  def Plot(self):
    if self.plottype=="contour": # or self.plottype=="diff": 
      for vname in getattr(self,"xvnames",self.vnames):
        if self.method=="eof":
          from cseof import eofplot
          eofplot(self,vname)
        else:
          from cscontour import seasonalmap
          seasonalmap(self,vname)
    elif self.plottype=="Taylor": 
      from cstaylor import seasonaltaylor
      for vname in self.vnames:
        seasonaltaylor(self,vname)
    elif self.plottype=="CTaylor": 
      from cstaylor import combinedtaylor
      combinedtaylor(self)


