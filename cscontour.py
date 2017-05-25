#!/usr/bin/env python
import numpy as np# reshape
from netCDF4 import Dataset
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.spines import Spine 
import matplotlib.gridspec as gridspec
from matplotlib.backends.backend_pdf import PdfPages
import numpy.ma as ma
from collections import defaultdict
from collections import namedtuple

from plotset import *
from cstoolkit import *
from constant  import *

Style = namedtuple('Style', ['name', 'sidenamefs','tickfs','format','Figsize'])
nicev={"T2M":"T2M","CLDFRA":"CLT","CLDFRAl":"CLL","CLDFRAm":"CLM","CLDFRAh":"CLH","ASWDNS":"SWd","TCWPC":"TCWPC","Pr":"Pr","ALWDNS":"LWd","ALWUPS":"LWu","TMAX":"T2MAX","TMIN":"T2MIN","PRAVG":"Pr","PCT":"PCT","RAINYDAYS":"RAINYDAYS","CDD":"CDD","AT2M":"AT2M"}
style = Style(name="Paper",sidenamefs=6,tickfs=6,format="pdf",Figsize=(4.1,2.4))
style = Style(name="PPT",sidenamefs=3,tickfs=6,format="png",Figsize=(4.0,2.9))

def seasonalmap(data,vname):
  plotList =data.plotlist
  YB       =data.yb
  YE       =data.ye
  plotname =data.plotname
  landmask =data.mask
  shapefile=data.shapefile
  ncols=5  #len(plotList)+1
  gs1 = gridspec.GridSpec(ncols,len(seasonname) )
  gs1.update(wspace=0., hspace=0.20)
  fig = plt.figure(figsize=style.Figsize)
  contourfilename=plotname+"_"+vname
  if data.method=="cor":
    clevel=[-1,-0.95,-0.90,-0.85,-0.80,-0.75,-0.70,-0.65,-0.60,-0.55,-0.50,-0.45,-0.40,-0.35,-0.30,
            0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1]
    cmp   =plt.get_cmap('bwr') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
  elif data.method=="rmse":
    clevel=plotres[vname]['cleve3']
    cmp   =plt.get_cmap('YlOrRd') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
  elif data.method=="trend":
    if vname=="PRAVG":
      clevel=range(-10,11); [x*1 for x in range(-5,6)]
      clevel2=[x*1 for x in range(-10,11)]
    else:
      clevel=range(-20,22,2);
      clevel2=[x*2 for x in range(-10,11)]
    clevel.remove(0)
    cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
  else:
    clevel=plotres[vname]['cleve1']
    cmp=plotres[vname]['cmp1']
  if style.format=="pdf":
    pp = PdfPages(contourfilename+'.pdf')
  else:
    page=0

  SUPTITLE="%s-%s %s(%s)"%(str(YB),str(YE),vname,plotres[vname]['unit'])
  if data.method=="trend":
    SUPTITLE="%s-%s %s trend %s/100year"%(str(data.yb),str(data.ye),vname,plotres[vname]['unit'])
  else:
    SUPTITLE="%s-%s %s(%s)"%(str(data.yb),str(data.ye),vname,plotres[vname]['unit'])
  fig.suptitle(SUPTITLE, fontsize=12, fontweight='bold')

###################################### Plot Contour ########################################
  contour=cwrfplot(data.lat,data.lon,data.truelat1,data.truelat2,data.cen_lat,data.cen_lon,shapefile)
  figurenum=0
  for casenumber,case in enumerate(plotList):
    for k,name in enumerate(seasonname):
      if name=="DJF": 
        if case in sim_nicename:
          sidename = sim_nicename[case]
        else:
          sidename = case
      else:
        sidename=None
      ax1 = plt.subplot(gs1[figurenum])
      figurenum+=1
      cs=contour.contourmap(data.plotdata[case][vname][k,:,:],ax1,clevel,cmp, ylabels=sidename,sidenamefontsize=style.sidenamefs  )
      ax1.set_xticks([])
      ax1.set_yticks([])
    
    if figurenum%(len(seasonname)*ncols)==0 or case==plotList[-1]:
      print("one page print for org")
      if ncols==4:
        ax2 = fig.add_axes([0.15, 0.03, 0.7, 0.1],aspect=0.02)
      elif ncols==3:
        ax2 = fig.add_axes([0.15, 0.03, 0.7, 0.1],aspect=0.02)
      else:
        ax2 = fig.add_axes([0.15, 0.01, 0.7, 0.1],aspect=0.02)
      cbar=fig.colorbar(cs, cax=ax2,orientation="horizontal",drawedges=False)
      cbar.outline.set_visible(False)
      cbar.ax.tick_params(labelsize=style.tickfs,length=0)
      cbar.set_ticks(clevel)
      plt.xticks(rotation=90)
      if style.format=="pdf":
        pp.savefig()
      else:
        figurename=contourfilename+str(page)+"."+style.format
        page+=1
        fig.savefig(figurename,format=style.format,dpi=1000) #,dpi=300)
      fig = plt.figure(figsize=style.Figsize)
      fig.suptitle(SUPTITLE, fontsize=12, fontweight='bold')
      figurenum=0
