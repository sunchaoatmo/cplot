#!/usr/bin/env python
import numpy as np# reshape
import cs_stat
from plotset import sim_nicename,plotres
from constant  import *

import cs_stat  #.cs_stat.fit_3d
import numpy.ma as ma
plotmethodlist=[plt.semilogy,plt.loglog]
def plotdist(data,domain):
  spatial_stat=data.
  from matplotlib.backends.backend_pdf import PdfPages
  import seaborn as sns
  import matplotlib.pyplot as plt
  import matplotlib.gridspec as gridspec
                       n_bin=self.n_bin,x_min=self.x_min,x_max=self.x_max)
  bin_size=(self.x_max-self.x_min)/(self.n_bin)
  y_axis=np.arange(self.x_min,self.x_max,bin_size)
  gs1 = gridspec.GridSpec(data.nregs,len(seasonname) )
  gs1.update(wspace=0.0, hspace=0.0)
  pp = PdfPages('%s_sptd.pdf'%data.vname)
  plt.style.use('seaborn-bright')
  sns.set_style("darkgrid")
  sns.set_context("paper")
  LINEstyel=[':','None','None','-']
  Marker=['None','v',"^","None"]
  
  fig=plt.figure(figsize=(6, 8))
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  sns.set_style("ticks", {"xtick.major.size": 3, "ytick.major.size": 3})
  locx=0.1  #bin[-1]*0.9
  locy=5.0 #1e-1.6 #0.5
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
        for icase,case in enumerate( data.cases):
          if case==data.obsname:
            color=black
            label="Obs"
          else:
            linestyle="-"
            linewidth=0.4
          plotmethod(y_axis,data.plotdata["all"][:,ireg,iseason,icase],linewidth=linewidth, linestyle=linestyle,
                   color=tableau20[3+2*icase],markersize=ms0,marker=marker,zorder=0,label=sim_nicename[case])
        if ireg==0 and iseason==3:
          print("plot legend")
          ax1.legend(fontsize=4.2,bbox_to_anchor=(1.03,1),loc=2,borderaxespad=0.)
        plt.xticks(rotation='vertical',fontsize=4)
        ax1.set_ylim([0,10])
        if iseason==0:
          ax1.set_ylabel(regname, fontsize=6)
          plt.setp(ax1.get_yticklabels(), fontsize=4)
        if iseason!=0:
          plt.setp(ax1.get_yticklabels(), visible=False)
          plt.tick_params(
          axis='y',          # changes apply to the x-axis
          which='both',      # both major and minor ticks are affected
          left='off',      # ticks along the bottom edge are off
          ) # labels along the bottom edge are off 
        if ireg!=len(DOMAIN_reg[domain])-1:
          plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='off',      # ticks along the bottom edge are off
            labelbottom='off') # labels along the bottom edge are off
        plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            top='off',         # ticks along the top edge are off
            labeltop='off') # labels along the bottom edge are off

    pp.savefig()
    fig=plt.figure(figsize=(6, 8))
  pp.close()

