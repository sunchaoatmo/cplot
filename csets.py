import matplotlib.pyplot as plt
from constant  import *
from matplotlib.backends.backend_pdf import PdfPages
from plotset import sim_nicename,tableau20,cmap_hotcold18
import matplotlib.gridspec as gridspec
 
axes_bar={5:[0.15, 0.04, 0.7, 0.1],4:[0.15, 0.03, 0.7, 0.1],3:[0.15, 0.01, 0.7, 0.1],2:[0.15, 0.02, 0.7, 0.1]}
figsizes={5:(8.5,9.0),4:(8.25,7.0),3:(8.5,7.0),2:(8.5,3.61)}
def etscontourf(data,vname):
  data.plotlist.remove("ERI")
  for ireg in range(int(data.nregs)):
    regname=data.regnames[ireg]
    filename=data.plotname+"_"+"".join(vname)+regname
    outputformat="pdf"
    if outputformat=="pdf":
      pp = PdfPages(filename+'.pdf')
    else:
      page=0
    fig = plt.figure(figsize=figsizes[len(data.plotlist)])
    suptitle=data.title[vname]+" "+regname
    fig.suptitle(suptitle, fontsize=12, fontweight='bold')
    #plt.style.use('ggplot')
    plt.style.use(['ggplot','seaborn-paper'])
    gs0 = gridspec.GridSpec(len(data.plotlist),1 )
    gs0.update(hspace=0.1, wspace=0.0)
    import numpy as np
    for casenumber,case in enumerate(data.plotlist):
      ax1 = plt.subplot(gs0[casenumber])
      legname = sim_nicename.get(case,case)
      cax=plt.contourf(data.plotdata[case][vname][ireg]-data.plotdata['ERI'][vname][ireg],
                       levels=data.ets_level,
                       extend="both",
                       cmap=cmap_hotcold18 ) #plt.get_cmap('Spectral_r')) #,norm=norm,cmap=cmp,extend='max')
      sidename = sim_nicename.get(case,case)
      ax1.set_ylabel(sidename, fontsize=6, fontweight='bold')
      if case!=data.plotlist[-1]:
        plt.tick_params(
          which='both',      # both major and minor ticks are affected
          right='off', labelright='off',   # ticks along the top edge are off
          bottom='off',labelbottom='off',         # ticks along the top edge are off
          left='on', labelleft='on',        # ticks along the top edge are off
          top='off',         # ticks along the top edge are off
          length=1
          ) 
      else:
        plt.tick_params(
          which='both',      # both major and minor ticks are affected
          right='off',         # ticks along the top edge are off
          bottom='on',  labelbottom='on',       # ticks along the top edge are off
          left='on',         # ticks along the top edge are off
          top='off',         # ticks along the top edge are off
          length=1
          ) 


    ax2 = fig.add_axes(axes_bar[len(data.plotlist)],aspect=0.02)
    cbar=fig.colorbar(cax, cax=ax2,orientation="horizontal",drawedges=False)
    cbar.set_ticks(data.ets_level)

    #plt.ylim([0.8,1.0])
    #plt.xlim([0.,150])
    
    if outputformat=="pdf":
      pp.savefig()
    else:
      print(outputformat)
      figurename=filename+str(page)+"."+outputformat
      page+=1
      fig.savefig(figurename,format=outputformat,dpi=300) #,dpi=300)
    fig.clf()
    if outputformat=="pdf":
      pp.close()
