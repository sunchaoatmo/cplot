#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib as mpl
import taylorDiagram as td
import numpy as np
import numpy.ma as ma
from matplotlib.backends.backend_pdf import PdfPages
from constant  import *
from plotset import *
def seasonaltaylor(data,vname):
  import seaborn as sns
  cases=data.cases
  colors = plt.matplotlib.cm.Set1(np.linspace(0,1,len(cases)))
  
  # Here set placement of the points marking 95th and 99th significance
  # levels. For more than 102 samples (degrees freedom > 100), critical
  # correlation levels are 0.195 and 0.254 for 95th and 99th
  # significance levels respectively. Set these by eyeball using the
  # standard deviation x and y axis.
  x95 = [0.05, 13.9] # For Prcp, this is for 95th level (r = 0.195)
  y95 = [0.0, 71.0]
  x99 = [0.05, 19.0] # For Prcp, this is for 99th level (r = 0.254)
  y99 = [0.0, 70.0]
  
  rects = dict(winter=221,
               spring=222,
               summer=223,
               autumn=224)
  
  fig = plt.figure(figsize=(11,8))
  plt.style.use(['seaborn-white','seaborn-paper'])
  mpl.rcParams['grid.linewidth'] = 0.01
  mpl.rcParams['axes.linewidth'] = 0.01
  mpl.rcParams['font.size'] = 1
  mpl.rcParams['font.family'] = "sans-serif"
  mpl.rcParams['font.sans-serif'] = "Arial"
  mpl.rcParams['xtick.labelsize'] = "xx-large"
  zorder=1
  
  stdrefs=1
  for iseason, season in enumerate(['winter','spring','summer','autumn']):
  
      dia = td.TaylorDiagram(stdrefs, fig=fig, rect=rects[season],
                          label='Obs')
  
      morder=-1
      for i,case in  enumerate(data.cases):
        if case!=data.obsname:
#         for ireg in range(data.nregs+1):
          for ireg in range(1):
            regname=str("".join(data.regnames[ireg-1]))
            stddev, corrcoef=data.plotdata[case][vname][ireg,iseason,:]
            ms=10
            if case==data.GCM_name:
              ms=11
              marker='*'  #ensmDict[name]["marker"]
            # color1='black' #ensmDict[name]["color"]   #ensmDict[name]["color"]
            # color2='black'  #ensmDict[name]["color"]
            else:
              morder+= 1  #(i-3)%24 #(int((name.replace("run_",""))))%24
              #marker='$%s$' % chr( ord('a')+i*(data.nregs+1)+ireg)
              marker='$%s$' % chr( ord('a')+i)
            color1=tableau20[2*i] if i<10 else 'b'
            #color1=tableau20[2*ireg] if ireg<10 else 'b'
            labelname= sim_nicename[case] if case in sim_nicename else case
            labelname= regname+"  "+labelname if ireg >0 else labelname
            dia.add_sample(stddev, corrcoef,
                           marker=marker, markersize=ms, ls='',
                           mfc=color1, mec=color1, # Colors
                           label=labelname,zorder=zorder)
  
      # Add RMS contours, and label them
      contours = dia.add_contours(levels=5,  colors='0.5') # 5 levels
      dia.ax.clabel(contours, inline=1, fontsize=5, fmt='%.1f')
      # Tricky: ax is the polar ax (used for plots), _ax is the
      # container (used for layout)
      dia._ax.set_title(season.capitalize(),loc='right',fontsize=12,  fontweight='bold')
  
  # Add a figure legend and title. For loc option, place x,y tuple inside [ ].
  # Can also use special options here:
  # http://matplotlib.sourceforge.net/users/legend_guide.html
  fig.legend(dia.samplePoints,
             [ p.get_label() for p in dia.samplePoints ],
             numpoints=1, prop=dict(size=6),loc='center')
  plt.savefig(vname+"_"+data.plotname+".png", dpi=500)

def combinedtaylor(data):
  cases=data.cases
  colors = plt.matplotlib.cm.Set1(np.linspace(0,1,len(cases)))
  
  # Here set placement of the points marking 95th and 99th significance
  # levels. For more than 102 samples (degrees freedom > 100), critical
  # correlation levels are 0.195 and 0.254 for 95th and 99th
  # significance levels respectively. Set these by eyeball using the
  # standard deviation x and y axis.
  rects={} 
  for ivname,vname in enumerate(data.vnames):
    rects[vname]=str(len(data.vnames))+'1'+str(ivname+1)
  
  fig = plt.figure(figsize=(8,15))
  plt.style.use(['seaborn-paper'])
  mpl.rcParams['grid.linewidth'] = 0.01
  mpl.rcParams['axes.linewidth'] = 0.6
  mpl.rcParams['font.size'] = 1
  mpl.rcParams['font.sans-serif'] = "Arial Narrow"
  mpl.rcParams['xtick.labelsize'] = "xx-large"
  zorder=1
  
  stdrefs=1
  
  colorseason={"DJF":tableau20[18],"MAM":tableau20[5],"JJA":tableau20[6],"SON":tableau20[8]}
  #colorseason={"DJF":"blue","MAM":"green","JJA":"red","SON":"purple"}
  dia ={} 
  for ivname,vname in enumerate(data.vnames):
    dia[vname] = td.TaylorDiagram(stdrefs, fig=fig, rect=rects[vname] ,
                          label='Obs')
    ph=[]
    for i,case in  enumerate(data.cases):
      for iseason, season in enumerate(seasonname):
        zorder=1
        if case!=data.obsname:
          stddev, corrcoef=data.plotdata[case][vname][iseason]
          if case==data.GCM_name:
            ms=8
            marker="^"
          elif "RegCM" in case:
            marker="s"
            ms =8
          else:
            ms=12
            zorder=100
            marker="*"
          color1=colorseason[season]
          labelname=season if i==3 else " "
          ph.append(dia[vname].add_sample(stddev, corrcoef,
                       marker=marker, markersize=ms, ls='',
                       mfc=color1, mec=color1, # Colors
                         label=labelname,zorder=zorder))

    
        contours = dia[vname].add_contours(levels=5,  colors='0.5') # 5 levels
        dia[vname].ax.clabel(contours, inline=1, fontsize=5, fmt='%.1f')
        dia[vname]._ax.set_ylabel("Normalized STD",fontsize=12,  fontweight='bold')
        plt.text(0.85, 0.03, sim_nicename.get(vname,vname),transform = dia[vname]._ax.transAxes,zorder=1000,fontsize=12)
    
  leg=dia[data.vnames[1]]._ax.legend( ph, [ p.get_label() for p in ph], 
             frameon=True, mode="expand",fancybox=True, framealpha=1,numpoints=1, 
             loc="upper right",bbox_to_anchor=(0.6, 0.95,0.4,0.2), ncol=3)
  plt.setp(leg.texts, family="monospace")
             #frameon=True, mode=None,fancybox=True, framealpha=1,numpoints=1, loc="upper right",bbox_to_anchor=(1.25, 1.3), ncol=3)
  leg.set_title("ERI   CWRF   RegCM4", prop = {'size':10})
# plt.show()
  plt.savefig(vname+"_"+data.plotname+".pdf")

def writedata(data,vname):
  import pandas as pd
  outputlist=[case for case in data.cases if case!=data.obsname]
  writer = pd.ExcelWriter('Std-Cor_'+vname+'.xlsx')
  outputstd=np.zeros((len(outputlist)*(data.nregs+1),len(seasonname)))
  outputcor=np.zeros((len(outputlist)*(data.nregs+1),len(seasonname)))
  for iseason, season in enumerate(seasonname):
    idex=0
    for icase,case in  enumerate(outputlist):
      for ireg in range(data.nregs+1):
        stddev, corrcoef=data.plotdata[case][vname][ireg,iseason,:]
        outputstd[idex,iseason]=stddev
        outputcor[idex,iseason]=corrcoef
        idex+=1

  outputindex=[]
  for icase,case in  enumerate(outputlist):
    for ireg in range(data.nregs+1):
      regname=str("".join(data.regnames[ireg-1])) if ireg>0 else "whole"
      outputindex.append(sim_nicename[case]+":"+regname)
  dfstd = pd.DataFrame(outputstd, index=outputindex,columns=seasonname)
  dfcor = pd.DataFrame(outputcor, index=outputindex,columns=seasonname)
  dfstd.to_excel(writer,'std')
  dfcor.to_excel(writer,'cor')
  writer.save()
