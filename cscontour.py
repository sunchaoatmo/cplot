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

def tickcs(righttick,lefttick):
  import matplotlib.pyplot as plt
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

Style = namedtuple('Style', ['name', 'sidenamefs','tickfs','format'])
nicev={"T2M":"T2M","CLDFRA":"CLT","CLDFRAl":"CLL","CLDFRAm":"CLM","CLDFRAh":"CLH","ASWDNS":"SWd","TCWPC":"TCWPC","Pr":"Pr","ALWDNS":"LWd","ALWUPS":"LWu","TMAX":"T2MAX","TMIN":"T2MIN","PRAVG":"Pr","PCT":"PCT","RAINYDAYS":"RAINYDAYS","CDD":"CDD","AT2M":"AT2M"}
#style = Style(name="PPT",sidenamefs=3,tickfs=5,format="png",Figsize=(2.73,2.9))
style = Style(name="PPT",sidenamefs=8,tickfs=7,format="pdf")
"""
figsizes={5:(8.5,9.0),4:(8.25,7.0),3:(8.5,5.4),2:(8.5,3.61)}
figsizes={5:(8.5,9.35),4:(8.25,7.25),3:(8.5,5.6),2:(8.5,3.61)}
axes_bar={4:[0.15, 0.18, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1]}
axes_bar={5:[0.15, 0.04, 0.7, 0.1],4:[0.15, 0.03, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1],2:[0.15, 0.02, 0.7, 0.1]}
"""
def cshistplot(sample,alpha,xsample,ax,lw,label,color,shade,legend=True,hist=False,**kwargs):
  import numpy as np
  from scipy import stats
  if hist:
    hist,bin_edges=np.histogram(sample, bins='fd', range=None)
    x=(bin_edges[1:]+bin_edges[:-1])*.5
    y=hist/float(len(sample))*100.0
  else:
    x=np.linspace(xsample[0],xsample[-1],100)
    kernal=stats.gaussian_kde(sample, bw_method= "scott")
    #kernal=stats.gaussian_kde(sample, bw_method= "silverman")
    y=kernal(x)
    if max(y)<1:
      y=y*100
  ax.plot(x, y, color=color, label=label,lw=lw, **kwargs)
  if shade:
    ax.fill_between(x, 1e-12, y, facecolor=color, alpha=alpha)

  # Draw the legend here
  ax.legend(loc="best")
 

def seasonalmap(data,vname,crt=-9999):
  print(data.nlat)
  if data.nlat==108:
    # setting for US domain
    figsizes={6:(8.5,12.35),5:(8.5,9.35),4:(8.25,7.25),3:(8.5,5.6),2:(8.5,3.61)}
    season_x,season_y=0.1,0.05
    case_x,case_y    =0.55,0.05
  else:
    # setting for China domain
    figsizes={6:(8.5,12.35),5:(8.5,9.35),4:(8.25,7.25),3:(8.5,5.6),2:(8.5,3.61),1:(8.5,3.61)}
    season_x,season_y=0.5,0.8
    case_x,case_y    =0.02,0.05

  axes_bar={6:[0.15, 0.04, 0.7, 0.1],
            5:[0.15, 0.04, 0.7, 0.1],
            4:[0.15, 0.03, 0.7, 0.1],3:[0.15, 0.03, 0.7, 0.1],2:[0.15, 0.02, 0.7, 0.1]}
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
  lefttick,righttick,legloc,labloc1,labloc2,ndx,xloc,xloc2="on","off",1,0,1,1,0.1,0.05
  legloc=(0.05,0.92,0.01,0.03)
  if "cor" in data.method:
    lefttick,righttick,labloc1,labloc2,ndx="on","off",0,1,1
    suptitle=data.title[vname]
    clevel=[ -0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    cmp   =cmap_hotcold18 #plt.get_cmap('seismic') #;cmp.set_under('b')
  elif data.method=="rmse":
    lefttick,righttick,legloc,labloc1,labloc2,ndx,xloc,xloc2="on","off",1,0,1,1,0.9,0.05
    legloc=(0.6,0.92,0.01,0.03)
    suptitle="%s (%s)"%(data.title[vname],plotres[vname]['unit'])
    clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
    cmp   =plt.get_cmap('YlOrRd') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
  elif data.method=="trend":
    suptitle="%s (%s/100 years)"%(data.title[vname],plotres[vname]['unit'])
    cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('midnightblue')
    #clevel=range(-20,22,2);
    clevel=[-8+x*0.5 for x in range(33)]
    clevel2=clevel
    clevel.remove(0)
  elif data.method=="ets":
    xloc=0.8
    xloc2=0.9
    extend="both"
    icrt=data.crts_level.index(crt)
    if icrt<len(data.crts_level)-1:
      suptitle="%s crt=%s-%s"%(data.title[vname],data.crts_level[icrt],data.crts_level[icrt+1])
    else:
      suptitle="%s crt=%s above"%(data.title[vname],crt)
    cmp   =cmap_WBGYR;cmp.set_under('white')
    clevel=data.ets_level
    lefttick,righttick,labloc1,labloc2,ndx="off","on",-2,-1,2
    legloc=(0.45,0.97,0.01,0.03)
  else:
    legloc=(0.45,0.97,0.01,0.03)
    lefttick,righttick,labloc1,labloc2,ndx="off","on",-2,-1,2
    xloc=0.8
    xloc2=0.9
    #xloc2=0.95
    ndx=3
    suptitle="%s (%s)"%(sim_nicename.get(vname,vname),plotres[vname]['unit'])
    extend="max"
    clevel=getattr(data,"%s_%s"%(vname.lower(),"clevel1"))
    cmp=plotres[vname]['cmp1']
  if data.method=="diff":
    extend="both"
    lefttick,righttick,legloc,labloc1,labloc2,ndx,xloc,xloc2="on","off",1,0,1,2,0.1,0.2
    legloc=(0.63,0.68,0.01,0.03)
    #legloc=(0.63,0.92,0.01,0.03)
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
  if data.contourmappdf:
    pdfmax=0.0
    for k,name in enumerate(seasonname):
      ax1 = plt.subplot(gs0[figurenum])
      for casenumber,case in enumerate(plotList):
        legname = sim_nicename.get(case,case)
        pdfdata=ma.masked_array((data.plotdata[case][vname][k,:,:]), mask=data.eastmask)
        from writenc import writetonc
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
        #leg=ax1.legend(mode="expand",handlelength=0.5,borderaxespad=0.,frameon=False,   fontsize=6)
        leg=ax1.legend(bbox_to_anchor=legloc,mode="expand",handlelength=0.5,borderaxespad=0.,frameon=False,   fontsize=6)
        for legobj in leg.legendHandles:
              legobj.set_linewidth(1.0)
        for y in ax1.get_yticks()[1:]:
          #ax1.text((clevelpdf[labloc1]*0.9+clevelpdf[labloc2]*0.1), y, y,fontsize=6,
          ax1.text((clevelpdf[1]*xloc2+clevelpdf[0]*(1-xloc2)), y, y,fontsize=6,
          verticalalignment='center', horizontalalignment='left') #,
        #ax1.text(xloc, 0.2, 'Frequency (%)',fontsize=7,
        #   verticalalignment='bottom', horizontalalignment='left',
        #   transform=ax1.transAxes,rotation="vertical")
      else:
        ax1.get_legend().set_visible(False)
      if "cor" in data.method or "diff" in data.method:
        plt.axvline(0, color='black',lw=0.8,ls=":")
      if np.abs(np.max(clevelpdf)) >1:
        xtickslab=[int(x) for x in clevelpdf[1:-1:ndx]]
      else:
        xtickslab=[x for x in clevelpdf[1:-1:ndx]]
      plt.xticks(clevelpdf[1:-1:ndx], xtickslab)
      plt.tick_params(axis='both', which='major', labelsize=6)
      for axis in ['top','bottom','left','right']:
        ax1.spines[axis].set_linewidth(0.01)
      tickcs(righttick,lefttick)
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
      cs=contour.contourmap(data.plotdata[case][vname][k,:,:],ax1,clevel,cmp, 
                            ylabels=sidename,sidenamefontsize=style.sidenamefs,
                            season_x=season_x,season_y=season_y,
                            case_x=case_x,case_y=case_y,
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

def Varmaps(data,crt=-9999):
  #figsizes={5:(8.5,9.35),4:(8.25,7.2),3:(8.5,5.6),2:(8.5,3.61)}
  axes_bar={5:[0.15, 0.04, 0.25, 0.1],4:[0.15, 0.03, 0.22, 0.1],3:[0.15, 0.03, 0.25, 0.1],2:[0.15, 0.02, 0.25, 0.1]}
  if data.nlat==108:
    # setting for US domain
    #figsizes={5:(8.5,9.35),4:(8.25,7.20),3:(9.25,7.2),2:(8.5,3.61)}
    figsizes={5:(8.5,9.35),4:(8.,7.0),3:(9.25,7.2),2:(8.5,3.61)}
    season_x,season_y=0.9,0.2
    case_x,case_y    =0.55,0.05
  else:
    # setting for China domain
    figsizes={5:(8.5,9.35),4:(8.25,7.25),3:(8.5,5.6),2:(8.5,3.61)}
    season_x,season_y=0.5,0.8
    case_x,case_y    =0.02,0.05
  axes_bar0=[0.15,0.405,0.665]
  plotList =data.plotlist
  YB       =data.yb
  YE       =data.ye
  plotname =data.plotname
  landmask =data.mask
  shapefile=data.shapefile
  ncols=len(plotList) if len(plotList)<5 else 5
  beg_r=0
  if data.contourmappdf:
    beg_r=1
    clevelpdf={}
    for vname in data.vnames:
      if  "cor"in data.method:
        clevelpdf[vname]= [ -0.9,-0.6,-0.3,0.0,0.3,0.6,0.9]
      elif  "ets"in data.method:
        clevelpdf[vname]= data.ets_level
      else:
        try:
          clevelpdf[vname]=getattr(data,"%s_%s"%(vname.lower(),"clevel2"))[:]
        except:
          clevelpdf[vname]=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))[:]
        clevelpdf[vname].insert(  len(clevelpdf[vname])/2,0.0)
    ncols+=1
    gs0 = gridspec.GridSpec(ncols,len(data.vnames) )
    gs0.update(hspace=0.23, wspace=0.0)

  fig = plt.figure(figsize=figsizes[ncols])
  contourfilename=plotname
  if crt>0:
    contourfilename+=str(crt)
  lefttick,righttick,legloc,labloc1,labloc2,ndx,xloc="on","off",'upper right',0,1,2,0.9
  clevel={}
  cmp   ={}
  extend={}
  for vname in data.vnames:
    extend[vname]="both"
    if "cor" in data.method:
      lefttick,righttick,legloc,labloc1,labloc2,ndx="on","off",2,0,1,1
      clevel[vname]=[ -0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
      cmp[vnames]   =cmap_hotcold18 #plt.get_cmap('seismic') #;cmp.set_under('b')
    elif data.method=="rmse":
      clevel[vname]=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
      cmp[vname]   =plt.get_cmap('YlOrRd') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
    elif data.method=="trend":
      cmp[vname]   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('midnightblue')
      clevel[vname]=range(-20,22,2);
      clevel.remove(0)
    elif data.method=="ets":
      xloc=0.8
      extend[vname]="both"
      cmp[vname]   =cmap_WBGYR;cmp.set_under('white')
      clevel[vname]=data.ets_level
      lefttick,righttick,legloc,labloc1,labloc2,ndx="off","on",2,-2,-1,2
    else:
      extend[vname]="max"
      clevel[vname]=getattr(data,"%s_%s"%(vname.lower(),"clevel1"))
      cmp[vname]=plotres[vname]['cmp1']
    if data.method=="diff":
      ndx=2
      extend[vname]="both"
      clevel[vname]=getattr(data,"%s_%s"%(vname.lower(),"clevel0"))
      cmp[vname]=plotres[vname]['cmp2']
  if style.format=="pdf":
    pp = PdfPages(contourfilename+'.pdf')
  else:
    page=0

  from math import ceil 
  from matplotlib.ticker import AutoMinorLocator,NullFormatter,MultipleLocator, FormatStrFormatter
###################################### Plot PDF ########################################
  pdfmax={}
  contour={}
  for k,name in enumerate([seasonname[0]]):
    figurenum=0
    fig.suptitle("CWRF Outperforms ERI Seasonal Precipitation: %s"%name, fontsize=12, fontweight='bold')
    if data.contourmappdf:
      pdfmax=0.0
      for ivname,vname in enumerate(data.vnames):
        ax1 = plt.subplot(gs0[figurenum])
        for casenumber,case in enumerate(plotList):
          legname = sim_nicename.get(case,case)
          pdfdata=ma.masked_array((data.plotdata[case][vname][k,:,:]), mask=data.eastmask)
          color=data.casecolors[case]  #tableau20[2*(casenumber-1)] 
          alpha=data.casealphas[case]  #tableau20[2*(casenumber-1)] 
          cshistplot(pdfdata[:,:].compressed(),alpha,clevelpdf[vname],ax=ax1,lw=0.5,label=legname,color=color,shade=True)
        pdfmax=ax1.get_ylim()[1] if ax1.get_ylim()[1]>pdfmax else pdfmax
        figurenum+=1
        try:
          pdfmax= min(pdfmax,getattr(data,"%s_pdfmax"%vname.lower()))
        except:
          pass
      figurenum=0
      minorLocator = AutoMinorLocator() #MultipleLocator(5)
      for ivname,vname in enumerate(data.vnames):
        ax1 = plt.subplot(gs0[figurenum])
        ax1.set_title(sim_nicename.get(vname,vname)) #,fontdict={"fontweight":'bold'})
        tickloc=np.linspace(0,pdfmax,num=8) #[x for x  in range(0,int(pdfmax),int(pdfmax)/5)]
        dy =int(ceil(pdfmax/5.0))
        tickloc=[x for x  in range(0,int(ceil(pdfmax)),dy)]
        ax1.set_yticks(tickloc)
        print(tickloc)
        ax1.yaxis.set_minor_locator(minorLocator)
        plt.yticks(ax1.get_yticks(),"")
        if ivname==0:
          leg=ax1.legend(bbox_to_anchor=(0.75,0.92,0.01,0.03),mode="expand",handlelength=0.5,borderaxespad=0.,frameon=False,   fontsize=6)
          for legobj in leg.legendHandles:
                legobj.set_linewidth(1.0)
          for y in ax1.get_yticks()[1:]:
            ax1.text((clevelpdf[vname][labloc1]*0.9+clevelpdf[vname][labloc2]*0.1), y, y,fontsize=6,
            verticalalignment='center', horizontalalignment='left') #,
          ax1.text(xloc, 0.15, 'Frequency ',fontsize=7,
             verticalalignment='bottom', horizontalalignment='left',
             transform=ax1.transAxes,rotation="vertical")
        else:
          ax1.get_legend().set_visible(False)
        if "cor" in data.method or "bias" in data.method:
          plt.axvline(0, color='black',lw=0.8,ls=":")
        if np.abs(np.max(clevelpdf[vname])) >1:
          xtickslab=[int(x) for x in clevelpdf[vname][1:-1:ndx]]
        else:
          xtickslab=[x for x in clevelpdf[vname][1:-1:ndx]]
        plt.xticks(clevelpdf[vname][1:-1:ndx], xtickslab)
        plt.tick_params(axis='both', which='major', labelsize=6)
        for axis in ['top','bottom','left','right']:
          ax1.spines[axis].set_linewidth(0.01)
        tickcs(righttick,lefttick)
        plt.ylim([0,float(pdfmax)])
        plt.xlim([clevelpdf[vname][0],clevelpdf[vname][-1]])
        figurenum+=1

###################################### Plot Contour ########################################
    gs1 = gridspec.GridSpec(ncols,len(data.vnames) )
    gs1.update(hspace=0.0, wspace=0.0)
    ax2={}
    cbar={}
    cs  ={}
    for ivname,vname in enumerate(data.vnames):
      if k==0:
        contour[vname]=cwrfplot(data.lat,data.lon,data.truelat1,data.truelat2,data.cen_lat,data.cen_lon,shapefile,extend[vname])
      if not data.contourmappdf:
        ax1 = plt.subplot(gs1[0,ivname])
        ax1.set_title(sim_nicename.get(vname,vname)) #,fontdict={"fontweight":'bold'})
      for casenumber,case in enumerate(plotList):
        if ivname==0: 
          sidename = sim_nicename.get(case,case)
        else:
          sidename=None
        ax1 = plt.subplot(gs1[beg_r+casenumber,ivname])
        figurenum+=1
        text=None
        cs[vname]=contour[vname].contourmap(data.plotdata[case][vname][k,:,:],ax1,
                             clevel[vname],cmp[vname], ylabels=sidename,sidenamefontsize=style.sidenamefs,
                             season_x=season_x,season_y=season_y,
                             case_x=case_x,case_y=case_y,
                             text=text)
        ax1.set_xticks([])
        ax1.set_yticks([])
      
    for ivname,vname in enumerate(data.vnames):
      bar_loc=axes_bar[ncols][:]
      bar_loc[0]=axes_bar0[ivname]
      ax2[vname] = fig.add_axes(bar_loc,aspect=0.03)
      cbar[vname]=plt.colorbar(cs[vname], cax=ax2[vname],orientation="horizontal",drawedges=False)
      #cbar[vname]=fig.colorbar(cs[vname], cax=ax2[vname],orientation="horizontal",drawedges=False)
      cbar[vname].outline.set_visible(False)
      cbar[vname].ax.tick_params(labelsize=style.tickfs,length=0)
      cbar[vname].set_ticks(clevel[vname][::ndx])
      clevel_label=[]
      for x in clevel[vname]:
        if float(x).is_integer():
          clevel_label.append(int(x))
        else:
          clevel_label.append(x)
      cbar[vname].set_ticklabels(clevel_label[::ndx])
    if style.format=="pdf":
      pp.savefig()
    else:
      figurename=contourfilename+str(page)+"."+style.format
      page+=1
      fig.savefig(figurename,format=style.format,dpi=300) #,dpi=300)
    fig.clf()
  if style.format=="pdf":
    pp.close()
  plt.close()
  print("finished %s plotting "%contourfilename)
