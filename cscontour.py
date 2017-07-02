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
figsizes={5:(8.5,9.0),4:(8.25,7.0),3:(8.5,5.4),2:(8.5,3.61)}
figsizes={5:(8.5,9.35),4:(8.25,7.25),3:(8.5,5.6),2:(8.5,3.61)}
# US figsizes={5:(8.5,8.7),4:(8.25,7.0),3:(8.5,4.05),2:(8.5,3.61)}
axes_bar={4:[0.15, 0.18, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1]}
axes_bar={5:[0.15, 0.04, 0.7, 0.1],4:[0.15, 0.03, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1],2:[0.15, 0.02, 0.7, 0.1]}
def cshistplot(sample,alpha,xsample,ax,lw,label,color,shade,legend=True,hist=False,**kwargs):
  import numpy as np
  import scipy
  if hist:
    hist,bin_edges=np.histogram(sample, bins='fd', range=None)
    x=(bin_edges[1:]+bin_edges[:-1])*.5
    y=hist/float(len(sample))*100.0
  else:
    x=np.linspace(xsample[0],xsample[-1],100)
    kernal=scipy.stats.gaussian_kde(sample, bw_method= "silverman")
    y=kernal(x)
  ax.plot(x, y, color=color, label=label,lw=lw, **kwargs)
  if shade:
    ax.fill_between(x, 1e-12, y, facecolor=color, alpha=alpha)

  # Draw the legend here
  if legend:
    ax.legend(loc="best")
 

def seasonalmap(data,vname,crt=-9999):
  plotList =data.plotlist
  YB       =data.yb
  YE       =data.ye
  plotname =data.plotname
  landmask =data.mask
  shapefile=data.shapefile
  ncols=len(plotList) if len(plotList)<5 else 5
  if data.contourmappdf:
    if  "cor"in data.method:
      clevelpdf= [ -0.9,-0.6,-0.3,0.0,0.3,0.6,0.9]
    elif  "ets"in data.method:
      clevelpdf= data.ets_level
    else:
      try:
        clevelpdf=getattr(data,"%s_%s"%(vname.lower(),"clevel2"))[:]
      except:
        clevelpdf=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))[:]
      clevelpdf.insert(  len(clevelpdf)/2,0.0)
    ncols+=1
    gs0 = gridspec.GridSpec(ncols,len(seasonname) )
    gs0.update(hspace=0.23, wspace=0.0)

  fig = plt.figure(figsize=figsizes[ncols])
  contourfilename=plotname+"_"+"".join(vname)
  if crt>0:
    contourfilename+=str(crt)
  extend="both"
  lefttick,righttick,legloc,labloc1,labloc2,ndx="on","off",2,0,1,1
  if "cor" in data.method:
    lefttick,righttick,legloc,labloc1,labloc2,ndx="on","off",2,0,1,1
    suptitle=data.title[vname]
    clevel=[ -0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    cmp   =cmap_hotcold18 #plt.get_cmap('seismic') #;cmp.set_under('b')
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
  elif data.method=="ets":
    extend="both"
    suptitle="ETS %s crt=%s"%(data.title[vname],crt)
    cmp   =cmap_WBGYR;cmp.set_under('white')
    clevel=data.ets_level
    lefttick,righttick,legloc,labloc1,labloc2,ndx="off","on",2,-2,-1,2
  else:
    suptitle="%s (%s)"%(sim_nicename.get(vname,vname),plotres[vname]['unit'])
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
  legloc=0

  
  fig.suptitle(suptitle, fontsize=12, fontweight='bold')
###################################### Plot PDF ########################################
  figurenum=0
  if data.contourmappdf:
    import seaborn.apionly as sns
    pdfmax=0.0
    for k,name in enumerate(seasonname):
      ax1 = plt.subplot(gs0[figurenum])
      for casenumber,case in enumerate(plotList):
        legname = sim_nicename.get(case,case)
        pdfdata=ma.masked_array((data.plotdata[case][vname][k,:,:]), mask=data.eastmask)
        color=data.casecolors[case]  #tableau20[2*(casenumber-1)] 
        alpha=data.casealphas[case]  #tableau20[2*(casenumber-1)] 
        cshistplot(pdfdata[:,:].compressed(),alpha,clevelpdf,ax=ax1,lw=0.5,label=legname,color=color,shade=True)
       # sns.kdeplot(data.pdfdata[case][vname][k,:,:].compressed(),lw=0.2
       #             ,gridsize=50
       #             ,label=legname,color=color1,shade=True)
      pdfmax=ax1.get_ylim()[1] if ax1.get_ylim()[1]>pdfmax else pdfmax
      figurenum+=1
    try:
      pdfmax= min(pdfmax,getattr(data,"%s_pdfmax"%vname.lower()))
    except:
      pass
    figurenum=0
    from math import ceil 
    from matplotlib.ticker import AutoMinorLocator,NullFormatter,MultipleLocator, FormatStrFormatter
    minorLocator = AutoMinorLocator() #MultipleLocator(5)
    for k,name in enumerate(seasonname):
      ax1 = plt.subplot(gs0[figurenum])
      tickloc=np.linspace(0,pdfmax,num=8) #[x for x  in range(0,int(pdfmax),int(pdfmax)/5)]
      dy =int(ceil(pdfmax/5.0))
      tickloc=[x for x  in range(0,int(ceil(pdfmax)),dy)]
      ax1.set_yticks(tickloc)
      ax1.yaxis.set_minor_locator(minorLocator)
      plt.yticks(ax1.get_yticks(),"")
      if k==0:
        leg=ax1.legend(bbox_to_anchor=(0.05,0.92,0.01,0.03),mode="expand",handlelength=0.5,borderaxespad=0.,frameon=False,   fontsize=6)
        #leg=ax1.legend(bbox_to_anchor=(0.57,0.92,0.01,0.03),mode="expand",handlelength=0.5,borderaxespad=0.,frameon=False,   fontsize=6)
        #leg=ax1.legend(bbox_to_anchor=(0.5,0.92,0.01,0.03),borderaxespad=0.,frameon=False,   fontsize=6)
        #leg=ax1.legend(loc=legloc,borderaxespad=0.,frameon=False, fontsize=6)
        #leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)
        for legobj in leg.legendHandles:
              legobj.set_linewidth(1.0)
        for y in ax1.get_yticks()[1:]:
          ax1.text((clevelpdf[labloc1]*0.9+clevelpdf[labloc2]*0.1), y, y,fontsize=6,
          verticalalignment='center', horizontalalignment='left') #,
        ax1.text(0.1, 0.1, 'Frequency ',fontsize=7,
           verticalalignment='bottom', horizontalalignment='left',
           transform=ax1.transAxes,rotation="vertical")
      else:
        ax1.get_legend().set_visible(False)
      if "cor" in data.method or "bias" in data.method:
        plt.axvline(0, color='black',lw=0.8,ls=":")
      plt.xticks(clevelpdf[1:-1:ndx], (x for x in clevelpdf[1:-1:ndx]))
      plt.tick_params(axis='both', which='major', labelsize=6)
      for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(0.01)
      plt.tick_params(
        which='major',      # both major and minor ticks are affected
        direction="in",
        right=righttick,         # ticks along the top edge are off
        bottom='on',         # ticks along the top edge are off
        left=lefttick,         # ticks along the top edge are off
        top='off',         # ticks along the top edge are off
        length=2,width=0.6
        ) 
      plt.tick_params(
        which='minor',      # both major and minor ticks are affected
        direction="in",
        right=righttick,         # ticks along the top edge are off
        bottom='off',         # ticks along the top edge are off
        left=lefttick,         # ticks along the top edge are off
        top='off',         # ticks along the top edge are off
        length=1,width=0.6
        ) 

      plt.ylim([0,float(pdfmax)])
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
        if float(x).is_integer():
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
      #fig = plt.figure(figsize=figsizes[ncols])
      fig.clf()
  if style.format=="pdf":
    pp.close()
  plt.close()
  print("finished %s plotting "%contourfilename)
