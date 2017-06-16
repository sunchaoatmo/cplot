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

Style = namedtuple('Style', ['name', 'sidenamefs','tickfs','format'])
nicev={"T2M":"T2M","CLDFRA":"CLT","CLDFRAl":"CLL","CLDFRAm":"CLM","CLDFRAh":"CLH","ASWDNS":"SWd","TCWPC":"TCWPC","Pr":"Pr","ALWDNS":"LWd","ALWUPS":"LWu","TMAX":"T2MAX","TMIN":"T2MIN","PRAVG":"Pr","PCT":"PCT","RAINYDAYS":"RAINYDAYS","CDD":"CDD","AT2M":"AT2M"}
#style = Style(name="PPT",sidenamefs=3,tickfs=5,format="png",Figsize=(2.73,2.9))
style = Style(name="PPT",sidenamefs=8,tickfs=7,format="png")
figsizes={4:(8.5,9.0),3:(8.5,5.4)}
figsizes={5:(8.5,8.6),4:(8.25,7.0),3:(8.5,5.4),2:(8.5,3.4)}
axes_bar={4:[0.15, 0.18, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1]}
axes_bar={5:[0.15, 0.04, 0.7, 0.1],4:[0.15, 0.03, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1],2:[0.15, 0.02, 0.7, 0.1]}

def seasonalmap(data,vname):
  plotList =data.plotlist
  YB       =data.yb
  YE       =data.ye
  plotname =data.plotname
  landmask =data.mask
  shapefile=data.shapefile
  ncols=len(plotList) if len(plotList)<5 else 5
  gs1 = gridspec.GridSpec(ncols,len(seasonname) )
  gs1.update(wspace=0., hspace=0.0)
  fig = plt.figure(figsize=figsizes[ncols])
  contourfilename=plotname+"_"+vname
  extend="both"
  suptitle="%s (%s)"%(data.title[vname],plotres[vname]['unit'])
  if data.method=="cor":
    suptitle=data.title[vname]
    clevel=[-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,
            0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    cmp   =plt.get_cmap('bwr') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
  elif data.method=="rmse":
    clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
    cmp   =plt.get_cmap('YlOrRd') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
  elif data.method=="trend":
    suptitle="%s (%s/100 years)"%(data.title[vname],plotres[vname]['unit'])
    #clevel=plotres[vname]['cleve0']
    cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('midnightblue')
    clevel=range(-20,22,2);
    clevel2=[x*2 for x in range(-10,11)]
    clevel.remove(0)
  else:
    extend="max"
    clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel1"))
    cmp=plotres[vname]['cmp1']
  if data.plottype=="diff":
    extend="both"
    suptitle="%s bias ( %s)"%(data.title[vname],plotres[vname]['unit'])
    clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
    cmp=plotres[vname]['cmp2']
  if style.format=="pdf":
    pp = PdfPages(contourfilename+'.pdf')
  else:
    page=0

  
  fig.suptitle(suptitle, fontsize=12, fontweight='bold')

###################################### Plot Contour ########################################
  contour=cwrfplot(data.lat,data.lon,data.truelat1,data.truelat2,data.cen_lat,data.cen_lon,shapefile,extend)
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
      text=name if casenumber==0 else None
      cs=contour.contourmap(data.plotdata[case][vname][k,:,:],ax1,clevel,cmp, ylabels=sidename,sidenamefontsize=style.sidenamefs,
                           text=text)
      ax1.set_xticks([])
      ax1.set_yticks([])
    
    if figurenum%(len(seasonname)*ncols)==0 or case==plotList[-1]:
      print("ncols=%s one page print for org"%(ncols))
      ax2 = fig.add_axes(axes_bar[ncols],aspect=0.02)

      cbar=fig.colorbar(cs, cax=ax2,orientation="horizontal",drawedges=False)
      cbar.outline.set_visible(False)
      cbar.ax.tick_params(labelsize=style.tickfs,length=0)
      cbar.set_ticks(clevel)
      cbar.set_ticklabels(clevel)
      if style.format=="pdf":
        pp.savefig()
      else:
        figurename=contourfilename+str(page)+"."+style.format
        page+=1
        fig.savefig(figurename,format=style.format,dpi=300) #,dpi=300)
      fig.suptitle(suptitle, fontsize=12, fontweight='bold')
      figurenum=0
      #if case is not plotList[-1]:
      fig = plt.figure(figsize=figsizes[ncols])
  if style.format=="pdf":
    pp.close()
