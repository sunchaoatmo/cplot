#!/usr/bin/env python
import seaborn as sns
import matplotlib.pyplot as plt
from cstoolkit import tableau20 
import matplotlib as mpl
import taylorDiagram as td
import numpy as np
import numpy.ma as ma
from matplotlib.backends.backend_pdf import PdfPages
from constant  import *
from plotset import *
def seasonaltaylor(data,vname):
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
          stddev, corrcoef=data.plotdata[case][vname][iseason]
          ms=10
          if case==data.GCM_name:
            ms=11
            marker='*'  #ensmDict[name]["marker"]
            color1='black' #ensmDict[name]["color"]   #ensmDict[name]["color"]
            color2='black'  #ensmDict[name]["color"]
          else:
            morder+= 1  #(i-3)%24 #(int((name.replace("run_",""))))%24
            marker='$%s$' % chr( ord('a')+i)
            color1=tableau20[2] 
          labelname= sim_nicename[case] if case in sim_nicename else case
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
             numpoints=1, prop=dict(size=13),loc='center')
  plt.savefig(vname+"_"+data.plotname+".png", dpi=500)
