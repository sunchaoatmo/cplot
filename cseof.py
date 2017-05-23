#!/usr/bin/env python
from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
from cstoolkit import tableau20 
from constant  import *
from collections import namedtuple
from cstoolkit import cwrfplot
from plotset import *

Style = namedtuple('Style', ['name', 'sidenamefs','tickfs','format','Figsize'])
style = Style(name="Paper",sidenamefs=6,tickfs=6,format="png",Figsize=(4.1,6.5))

def eofplot(data,vname):
  print("geting the matrix")
  sign={}
  for k,name in enumerate(seasonname):
    for npc in range(data.neof):
      for case in data.cases:
        if case in sim_nicename:
          sidename = sim_nicename[case]
        else:
          sidename = case
        sign[(name,sidename,npc)]=1.0
  sign[('DJF','CWRF',0)]=-1.0
  sign[('DJF','CWRF',1)]=-1.0
  sign[('DJF','ERI',2)]=-1.0

  sign[('JJA','CWRF',0)]=-1.0
  sign[('JJA','CWRF',1)]=-1.0

  sign[('SON','ERI',1)]=-1.0
  print("Got it!")

  clevel=[0.01*x for x in range(-5,6)];
  if data.period=="seasonal":
    time_axis=range(data.yb,data.ye)
  elif data.period=="monthly":
    time_axis=range(0,3*(data.ye-data.ye))
  else:
    import sys
    sys.exit("no avaible period!!")
  locx=time_axis[-1]*0.9
  plt.style.use('seaborn-bright')
  sns.set_style("darkgrid")
  sns.set_context("paper")
  plt.figure(figsize=(8, 6))
  ncols=len(data.cases)+1
  gs1 = gridspec.GridSpec(ncols,data.neof)
  seasonname2=["DJF", "MAM", "JJA", "SON"]
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  unit=plotres[vname]['unit']
  if style.format=="pdf":
    figurename=vname+data.plotname+".pdf"
    pp = PdfPages(figurename)
  else:
    page=0
  eofcontour=cwrfplot(data.lat,data.lon,data.truelat1,data.truelat2,data.cen_lat,data.cen_lon,data.shapefile)
  for k,name in enumerate(seasonname):
    fig = plt.figure(figsize=style.Figsize)
    fig.suptitle("%s-%s %s eof (%s):%s"%(str(data.yb),str(data.ye),vname,unit,name), fontsize=6, fontweight='bold')
    for npc in range(data.neof):
      ax1   =plt.subplot(gs1[npc])
      ax1.text(locx, 0.83, name, color='black', fontsize=3, bbox=props,ha='center',weight='bold',family='monospace')
      var=data.plotdata[data.obsname][vname][k][2]
      eof=data.plotdata[data.obsname][vname][k][0]
      ax1.set_title("Variance Explained:%5.2f%%"%(var[npc]*100),fontsize=4)
      for case in data.cases:
        linewidth=0.4
        linestyle="-"
        if case=="ERI":
          color1=tableau20[0]
        elif case=="OBS":
          color1="black"
        elif "RegCM" in case:
          color1=tableau20[-2]
        else:
          color1='r'
        pcs=data.plotdata[case][vname][k][1]
        plt.plot(time_axis,sign[(name,sidename,npc)]*pcs[:,npc],linewidth=linewidth, linestyle=linestyle,
             color=color1,markersize=2,label=sim_nicename[case])
        plt.xticks(rotation=90,fontsize=4)
        plt.yticks(fontsize=4)
      if npc==data.neof-1:
        ax1.legend(fontsize=4.2,bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0.)
      print("finish obs")
      for casenumber,case in enumerate(data.cases):
        temp=data.plotdata[case][vname][k][0][npc,:,:]
        ax1   =plt.subplot(gs1[(casenumber+1)*data.neof+npc])
        if case in sim_nicename:
          sidename = sim_nicename[case]
        else:
          sidename = case
        temp=temp*sign[(name,sidename,npc)]
        cs=eofcontour.contourmap(temp,ax1,clevel,cmp, ylabels=sidename,sidenamefontsize=style.sidenamefs  )
        [i.set_linewidth(0.1) for i in ax1.spines.itervalues()]
      ax2 = fig.add_axes([0.15, 0.01, 0.7, 0.1],aspect=0.02)
      cbar=fig.colorbar(cs, cax=ax2,orientation="horizontal",drawedges=False)
      cbar.outline.set_visible(False)
      cbar.ax.tick_params(labelsize=style.tickfs,length=0)
      cbar.set_ticks(clevel)
      if style=="PPT":
          fig.suptitle("%s-%s %s(%s)"%(str(args.yb),str(args.ye),Vname,units), fontsize=12, fontweight='bold')
    if style.format=="pdf":
      pp.savefig()
    else:
      figurename=vname+"_"+data.plotname+name+"."+style.format
      page+=1
      fig.savefig(figurename,format=style.format,dpi=1000) # ,dpi=1000) #,dpi=300)
    print("finished %s"%figurename)
