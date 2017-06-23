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
style = Style(name="PPT",sidenamefs=8,tickfs=7,format="pdf")
#figsizes={5:(8.5,8.6),4:(8.25,7.0),3:(8.5,5.4),2:(8.5,3.61)}
figsizes={5:(8.5,8.6),4:(8.25,7.0),3:(8.5,5.4),2:(8.5,3.61)}
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
  if data.method=="diff":
    pdfmax=getattr(data,"%s_%s"%(vname.lower(),"pdfmax"))[0]
    try:
      clevelpdf=getattr(data,"%s_%s"%(vname.lower(),"clevel2"))
    except:
      clevelpdf=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
    ncols+=1
    gs0 = gridspec.GridSpec(ncols,len(seasonname) )
    #gs0.update(hspace=0.25, wspace=0.1)
    gs0.update(hspace=0.20, wspace=0.0)
  fig = plt.figure(figsize=figsizes[ncols])
  contourfilename=plotname+"_"+vname
  extend="both"
  suptitle="%s (%s)"%(sim_nicename.get(vname,vname),plotres[vname]['unit'])
  if data.method=="cor":
    suptitle=data.title[vname]
    clevel=[ 0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
    cmp=plotres[vname]['cmp3']
    cmp   =plt.get_cmap('jet') ;cmp.set_under('w')
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
  if data.method=="diff":
    extend="both"
    suptitle="%s bias (%s)"%(sim_nicename.get(vname,vname),plotres[vname]['unit'])
    clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
    cmp=plotres[vname]['cmp2']
  if style.format=="pdf":
    pp = PdfPages(contourfilename+'.pdf')
  else:
    page=0

  
  fig.suptitle(suptitle, fontsize=12, fontweight='bold')
###################################### Plot PDF ########################################
  figurenum=0
  if data.method=="diff":
    for k,name in enumerate(seasonname):
      import seaborn.apionly as sns
      ax1 = plt.subplot(gs0[figurenum])
      for casenumber,case in enumerate(plotList):
        legname = sim_nicename.get(case,case)
        color1=tableau20[2*casenumber] 
        sns.kdeplot(data.plotdata[case][vname][k,:,:].compressed(),lw=0.2,label=legname,color=color1,shade=True)
      plt.tick_params(
        which='both',      # both major and minor ticks are affected
        right='off',         # ticks along the top edge are off
        bottom='on',         # ticks along the top edge are off
        left='on',         # ticks along the top edge are off
        top='off',         # ticks along the top edge are off
        length=2
        ) 
      tickloc=[x*0.01 for x  in range(0,int(pdfmax),int(pdfmax)/5)]
      plt.yticks(tickloc)
      plt.yticks(ax1.get_yticks(),"")
      if k!=0:
        ax1.get_legend().set_visible(False)
      else:
        leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)
        for legobj in leg.legendHandles:
              legobj.set_linewidth(1.0)
        #plt.yticks(ax1.get_yticks(), (int(x) for x in ax1.get_yticks() * 100))
        ax1.text(0.1, 0.15, 'Frequency ($\%$)',fontsize=8,
           verticalalignment='bottom', horizontalalignment='left',
           transform=ax1.transAxes,rotation="vertical")
        for y in ax1.get_yticks()[1:]:
          ax1.text((clevelpdf[1]+clevelpdf[0])*0.5, y, int(y*100),fontsize=6,
          verticalalignment='center', horizontalalignment='left',
          rotation="vertical")
      plt.axvline(0, color='grey',lw=0.2)
      plt.xticks(clevelpdf[1:-1], (int(x) for x in clevelpdf[1:-1]))
      plt.tick_params(axis='both', which='major', labelsize=6)
      for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(0.01)
      plt.ylim([0,float(pdfmax)*0.01])
      plt.xlim([clevelpdf[0],clevelpdf[-1]])
      figurenum+=1

###################################### Plot Contour ########################################
  gs1 = gridspec.GridSpec(ncols,len(seasonname) )
  gs1.update(hspace=0.0, wspace=0.0)
  contour=cwrfplot(data.lat,data.lon,data.truelat1,data.truelat2,data.cen_lat,data.cen_lon,shapefile,extend)
  for casenumber,case in enumerate(plotList):
    for k,name in enumerate(seasonname):
      if name=="DJF": 
        sidename = sim_nicename.get(case,case)
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
      clevel_label=[]
      for x in clevel:
        if x.is_integer():
          clevel_label.append(int(x))
        else:
          clevel_label.append(x)
      cbar.set_ticklabels(clevel_label)
      if style.format=="pdf":
        pp.savefig()
      else:
        figurename=contourfilename+str(page)+"."+style.format
        page+=1
        fig.savefig(figurename,format=style.format,dpi=300) #,dpi=300)
      fig.suptitle(suptitle, fontsize=12, fontweight='bold')
      figurenum=0
      fig = plt.figure(figsize=figsizes[ncols])
#   gs1.update(wspace=0., hspace=0.0)
  if style.format=="pdf":
    pp.close()
