#!/usr/bin/env python
import numpy as np# reshape
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec
import matplotlib
from plotset import DOMAIN_reg,sim_nicename,plotres
from constant  import *

def plothist(hist_data,bin,caseList,ensmDict,Vname,domain):
  gs1 = gridspec.GridSpec(2,2)
#  gs1.update(wspace=0.0, hspace=0.0)
  plotPDF= True
  if plotPDF:
    pp = PdfPages('pr_pdf.pdf')
  else:
    pp = PdfPages('pr_cdf.pdf')
  plt.style.use('seaborn-bright')
# sns.set_style("darkgrid")
  sns.set_context("paper")
  LINEstyel=[':','None','None','-']
  Marker=['None','v',"^","None"]
  #####################HIST setting
  
  fig=plt.figure()
  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  sns.set_style("ticks", {"xtick.major.size": 3, "ytick.major.size": 3})
  plotmethodlist=[plt.semilogy,plt.loglog]
  ms=1;ms0=2
  for plotmethod in plotmethodlist:
    for ireg,(regname,reg) in enumerate(DOMAIN_reg[domain].iteritems()): 
      for iseason,season in enumerate(seasonname):
        ax1 = plt.subplot(gs1[iseason])
        for axis in ['top','bottom','left','right']:
          ax1.spines[axis].set_linewidth(0.01)
        locx=bin[-1]*0.9
        locy=0.03 #1e-1.6 #0.5
        if ireg==0:
          ax1.text(locx, locy, season, color='black', fontsize=6, bbox=props,ha='center',weight='bold',family='monospace')
        zorderE=len(caseList)+1
        plotmethod(bin[0:-1],hist_data[(season,case,regname)],linewidth=linewidth, linestyle=linestyle,
                     color=ensmDict[case]["color"],markersize=ms0,marker=marker,zorder=0,label=sim_nicename[case])
        if ireg==0 and iseason==3:
          print("plot legend")
          ax1.legend(fontsize=4.2,bbox_to_anchor=(1.03,1),loc=2,borderaxespad=0.)
        plt.xlabel(plotres[Vname]['unit'])
        if plotmethod==plt.semilogy: 
          xticks=range(10,100,10)
          yticks=[0.01,0.1]
        else:
          xticks=[10, 20, 50,100,200,500] #range(10,500,50)
        plt.xticks(xticks,rotation='vertical',fontsize=4)
        plt.yticks(yticks,fontsize=4)
        ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        ax1.set_ylim([1e-6,0.1])
        ax1.set_xlim([10,100])
        if iseason==0:
          ax1.set_ylabel(regname, fontsize=6)
          plt.setp(ax1.get_yticklabels(), fontsize=4)
        if iseason%2 !=0:
          plt.setp(ax1.get_yticklabels(), visible=False)
          plt.tick_params(
          axis='y',          # changes apply to the x-axis
          which='both',      # both major and minor ticks are affected
          left='off',      # ticks along the bottom edge are off
          ) # labels along the bottom edge are off 
        #if ireg!=len(DOMAIN_reg[domain])-1:
        if iseason%2 !=1:
          plt.tick_params(
            axis='x',          # changes apply to the x-axis
            which='both',      # both major and minor ticks are affected
            bottom='on',      # ticks along the bottom edge are off
            labelbottom='off') # labels along the bottom edge are off
      pp.savefig()
      fig=plt.figure() #figsize=(6, 8))
  pp.close()
