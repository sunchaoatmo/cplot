#!/usr/bin/env python
import matplotlib.pyplot as plt
import numpy as np# reshape
import cs_stat
from plotset import sim_nicename,plotres,tableau20
from constant  import *

import cs_stat  #.cs_stat.fit_3d
import numpy.ma as ma
plotmethodlist=[plt.plot]
#plotmethodlist=[plt.semilogy,plt.loglog]
def pdfplot(data,vname):
  from matplotlib.backends.backend_pdf import PdfPages
  import seaborn as sns
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
  bin_size=(float(data.x_max)-float(data.x_min))/(float(data.n_bin))
  x_axis=np.arange(data.x_min,data.x_max,bin_size)
  gs1 = gridspec.GridSpec(data.nregs,len(seasonname) )
  gs1.update(wspace=0.0, hspace=0.0)
  pp = PdfPages('%s_sptd.pdf'%vname)
  plt.style.use('seaborn-bright')
  sns.set_style("darkgrid")
  sns.set_context("paper")
  LINEstyel=[':','None','None','-']
  Marker=['None','v',"^","None"]
  
  fig=plt.figure(figsize=(6, 8))
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  sns.set_style("ticks", {"xtick.major.size": 3, "ytick.major.size": 3})
  locx=0.7  #bin[-1]*0.9
  locy=17.0 #1e-1.6 #0.5
  linewidth=0.5
  linestyle='-'   #LINEstyel[k1//6]  #'-'
  ms=1;ms0=2
  for plotmethod in plotmethodlist:
    for ireg,regname in enumerate(data.regnames): 
      for iseason,season in enumerate(seasonname):
        ax1 = plt.subplot(gs1[iseason+ireg*4])
        ax1.grid(True)
        gridlines = ax1.get_ygridlines()+ ax1.get_xgridlines()
        for line in gridlines:
          line.set_linewidth(0.1)
          line.set_linestyle('-')
        for axis in ['top','bottom','left','right']:
          ax1.spines[axis].set_linewidth(0.01)
        if ireg==0:
          ax1.text(locx, locy, season, color='black', fontsize=6, bbox=props,ha='center',weight='bold',family='monospace')
        for icase,case in enumerate( data.plotlist):
          if case==data.obsname:
            color='k'
            label="Obs"
          else:
            linestyle="-"
            linewidth=0.8
          plotmethod(x_axis,data.plotdata["all"][vname][:,ireg,iseason,icase]*100,linewidth=linewidth, linestyle=linestyle,
                   color=tableau20[2+2*icase],markersize=ms0,label=sim_nicename[case])
        if ireg==0 and iseason==3:
          print("plot legend")
          ax1.legend(fontsize=4.2,bbox_to_anchor=(1.03,1),loc=2,borderaxespad=0.)
        plt.xticks(rotation='vertical',fontsize=4)
        ax1.set_ylim([0,20])
        if iseason==0:
          ax1.set_ylabel("".join(regname), fontsize=6)
          plt.setp(ax1.get_yticklabels(), fontsize=4)
        if iseason!=0:
          plt.setp(ax1.get_yticklabels(), visible=False)
          plt.tick_params(
          axis='y',          # changes apply to the x-axis
          which='both',      # both major and minor ticks are affected
          left='off',      # ticks along the bottom edge are off
          ) # labels along the bottom edge are off 
        BOTTICK='off' if ireg!=len(data.plotlist)-1 else 'on'
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            top='off',         # ticks along the top edge are off
            bottom=BOTTICK,      # ticks along the bottom edge are off
            labeltop='off') # labels along the bottom edge are off

    pp.savefig()
    fig=plt.figure(figsize=(6, 8))
  pp.close()

