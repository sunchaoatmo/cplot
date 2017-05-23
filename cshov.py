#!/usr/bin/env python
from netCDF4 import Dataset
from netCDF4 import date2num
import numpy as np                                            
import matplotlib.pyplot as plt
import datetime                                               
tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
for i in range(len(tableau20)):    
    r, g, b = tableau20[i]    
    tableau20[i] = (r / 255., g / 255., b / 255.)    

# Scale the RGB values to the [0, 1] range, which is the format matplotlib accepts.    
def hovplot(data,vname):

  LLJ_sm=data.start_month # starting the ananlysis from 6
  LLJ_em=data.end_month # 
  YB=data.yb
  YE=data.ye
  years=range(YB,YE+1)

  for case in data.cases:
    fig = plt.figure(figsize=(9,8.5))
    ax = plt.subplot()
    CS = plt.contourf(data.plotdata[case][vname],cmap=plt.get_cmap('jet'))
    fig.colorbar(CS)
    x_tickloc_major=[]
    labels_major   =[]
    initial_date=datetime.datetime(years[0],LLJ_sm , 1, 0,0,0)                
    x_tickloc_major=[0]
    curdate=datetime.datetime(years[0],LLJ_sm , 1, 0,0,0)                
    T0=date2num( curdate,units=units_cur,calendar=calendar_cur)
    labels_major=[curdate.strftime("%b-%d")]
    for imonth,month in enumerate(range(LLJ_sm+1,LLJ_em+2)):
      curdate=datetime.datetime(years[0],month , 1, 0,0,0)                
      T_loc=date2num( curdate,units=units_cur,calendar=calendar_cur)-T0
      ax.plot([T_loc,T_loc],[0,len(years)-1], lw=1, c="r",linestyle="--")
      x_tickloc_major.append(T_loc)
      labels_major.append(curdate.strftime("%b-%d"))
    ax.set_xticks( x_tickloc_major )
    ax.set_xticklabels(labels_major,rotation=90,weight='bold',color='brown')
    ax.set_yticks( range(0,len(years),5) )
    ax.set_yticklabels(years[::5])
    ax.set_ylabel("Year", fontsize=8, fontweight='bold')
    ax.set_xlabel("Pr  ", fontsize=8, fontweight='bold')
    fig.savefig(data.plotname+case+".pdf")
