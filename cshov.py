#!/usr/bin/env python
from netCDF4 import Dataset
from netCDF4 import date2num
import numpy as np                                            
import matplotlib.pyplot as plt
import datetime                                               
from plotset import plotres
from cstoolkit import tableau20 

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
def hovplot(data,vname):

  LLJ_sm=data.start_month # starting the ananlysis from 6
  LLJ_em=data.end_month # 
  YB=data.yb
  YE=data.ye
  years=range(YB,YE+1)

  xlat=np.arange(data.start_lat,data.end_lat,data.dlat)
  clevel=plotres[vname]['cleve1']
  for case in data.cases:
    SUPTITLE="%s:%s-%s %s(%s)"%(case,str(data.yb),str(data.ye),vname,plotres[vname]['unit'])
    fig = plt.figure(figsize=(10,8))
    fig.suptitle(SUPTITLE, fontsize=12, fontweight='bold')
    ax = plt.subplot()
    CS = plt.contourf(data.plotdata[case][vname],levels=clevel,cmap=plt.get_cmap('jet'))
    fig.colorbar(CS)
    x_tickloc_major=[]
    labels_major   =[]
    initial_date=datetime.datetime(years[0],LLJ_sm , 1, 0,0,0)                
    x_tickloc_major=[0]
    curdate=datetime.datetime(years[0],LLJ_sm , 1, 0,0,0)                
    units_cur=data.time[case][vname].units
    calendar_cur=data.time[case][vname].calendar
    T0=date2num( curdate,units=units_cur,calendar=calendar_cur)
    labels_major=[curdate.strftime("%b-%d")]
    for imonth,month in enumerate(range(LLJ_sm+1,LLJ_em+2)):
      curdate=datetime.datetime(years[0],month , 1, 0,0,0)                
      T_loc=date2num( curdate,units=units_cur,calendar=calendar_cur)-T0
      ax.plot([T_loc,T_loc],[0,len(xlat)-1], lw=1, c="r",linestyle="--")
      x_tickloc_major.append(T_loc)
      labels_major.append(curdate.strftime("%b-%d"))
    ax.set_xticks( x_tickloc_major )
    ax.set_xticklabels(labels_major,rotation=90,weight='bold',color='brown')
    ax.set_yticks( range(0,len(xlat),10) )
    ax.set_yticklabels(xlat[::10])
    ax.set_ylabel("latitude", fontsize=8, fontweight='bold')
    ax.set_xlabel(vname, fontsize=8, fontweight='bold')
    fig.savefig(data.plotname+case+".pdf")
