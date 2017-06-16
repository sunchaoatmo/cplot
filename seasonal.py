from context import reginalmetfield
class seasonal_data(reginalmetfield):
  def __init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT):
    reginalmetfield.__init__(self,period,vnames,cases,nlevel,cutpoints,neof,
               method,plottype,shapefile,datapath,obsname,GCM_name,Time_control,
               wrfinputfile,landmaskfile,masktype,PLOT)

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


