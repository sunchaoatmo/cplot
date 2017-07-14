#!/usr/bin/env python
import matplotlib.gridspec as gridspec
from netCDF4 import Dataset
from netCDF4 import date2num
import numpy as np                                            
import matplotlib.pyplot as plt
import datetime                                               
from plotset import plotres,sim_nicename,tableau20
from collections import namedtuple
Style = namedtuple('Style', ['name', 'sidenamefs','tickfs','format','Figsize'])
style = Style(name="PPT",sidenamefs=3,tickfs=6,format="png",Figsize=(4.0,2.9))

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
def hovplot(data,vname):
  import matplotlib.colors as mc

  LLJ_sm=data.start_month # starting the ananlysis from 6
  LLJ_em=data.end_month # 
  YB=data.yb
  YE=data.ye
  years=range(YB,YE+1)

  xlat=np.arange(data.start_lat,data.end_lat,data.dlat)
  clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel1"))
  cmp=plotres[vname]['cmp1']
  norm = mc.BoundaryNorm(clevel, cmp.N)
  ncols=2.0 
  import math
  gs1 = gridspec.GridSpec(int(ncols),int(math.ceil(len(data.cases)/ncols)))
  fig = plt.figure(figsize=(12,8))
  fig.suptitle(data.title[vname]+plotres[vname]['unit'], fontsize=12, fontweight='bold')
  gs1.update(wspace=0.07, hspace=0.15)
  for icase,case in enumerate(data.cases):
    print(data.plotdata[case][vname].shape,case,vname)
    nlat,nday=data.plotdata[case][vname].shape
    ax = plt.subplot(gs1[icase])
    plt.xlim([0,nday-1])
    CS = plt.contourf(data.plotdata[case][vname],levels=clevel,norm=norm,cmap=cmp,extend='max')
    #if case ==data.cases[-1] or case ==data.cases[-2]:
    x_tickloc_major=[]
    labels_major   =[]
    x_tickloc_major=[0]
    curdate=datetime.datetime(years[0],LLJ_sm , 1, 0,0,0)                
    units_cur=data.time[case][vname].units
    calendar_cur=data.time[case][vname].calendar
    T0=date2num( curdate,units=units_cur,calendar=calendar_cur)
    labels_major=[curdate.strftime("%m/%d")]
    for imonth,month in enumerate(range(LLJ_sm+1,LLJ_em+1)):
      curdate=datetime.datetime(years[0],month , 1, 0,0,0)                
      T_loc=date2num( curdate,units=units_cur,calendar=calendar_cur)-T0
      ax.plot([T_loc,T_loc],[0,len(xlat)-1], lw=1, c="r",linestyle="--")
      x_tickloc_major.append(T_loc)
      labels_major.append(curdate.strftime("%m/%d"))
    ax.set_xticks( x_tickloc_major )
    ax.set_xticklabels(labels_major,color='brown')
    #else:
    #  ax.set_xticks( [] )
    #  ax.set_xticklabels([],weight='bold',color='brown')
    ax.text(0.1, 0.9, sim_nicename[case],
         verticalalignment='bottom', horizontalalignment='center',
         transform=ax.transAxes, fontweight='bold')
    if icase%ncols==0:
      ax.set_yticks( range(0,len(xlat),10) )
      ax.set_yticklabels(("%s$^\circ$ N"%int(x) for x in xlat[::10]))
    else:
      ax.set_yticks( [] )
      ax.set_yticklabels([],rotation=90,weight='bold',color='brown')
    #ax.set_title(sim_nicename[case], fontsize=8, fontweight='bold')
    for axis in ['top','bottom','left','right']:
      ax.spines[axis].set_linewidth(0.01)
    ax2 = fig.add_axes([0.15, 0.01, 0.7, 0.1],aspect=0.02)
    cbar=fig.colorbar(CS, cax=ax2,orientation="horizontal",drawedges=False)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(labelsize=style.tickfs,length=0)
    cbar.set_ticks(clevel)

  fig.savefig(data.plotname+".pdf")
