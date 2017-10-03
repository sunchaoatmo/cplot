import matplotlib.pyplot as plt
from constant  import *
from matplotlib.backends.backend_pdf import PdfPages
from plotset import sim_nicename,tableau20
import matplotlib.gridspec as gridspec
def setmonthlyticklabe(yb,ye,units_cur,calendar_cur):
  x_tickloc_major=[]
  labels_major   =[]
  x_tickloc_major=[0]
  begdate=datetime.datetime(yb,1 , 1, 0,0,0)                
  enddate=datetime.datetime(ye,12 , 1, 0,0,0)                
  T0=date2num( curdate,units=units_cur,calendar=calendar_cur)
  labels_major=[curdate.strftime("%m-%d")]
  for imonth,month in enumerate(range(LLJ_sm+1,LLJ_em+2)):
    curdate=datetime.datetime(years[0],month , 1, 0,0,0)                
    T_loc=date2num( curdate,units=units_cur,calendar=calendar_cur)-T0
    ax.plot([T_loc,T_loc],[0,len(xlat)-1], lw=1, c="r",linestyle="--")
    x_tickloc_major.append(T_loc)
    labels_major.append(curdate.strftime("%m/%d"))
  ax.set_xticks( x_tickloc_major )
  ax.set_xticklabels(labels_major,color='brown')
 
def corplot(data,vname):
  filename=data.plotname+"_"+"".join(vname)
  outputformat="pdf"
  if outputformat=="pdf":
    pp = PdfPages(filename+'.pdf')
  else:
    page=0
  fig = plt.figure()
  gs0 = gridspec.GridSpec(1,1 )
  ax1 = plt.subplot(gs0[0])
  import numpy as np
  for casenumber,case in enumerate(data.plotlist):
    #units_cur=data.time[case][vname].units
    #calendar_cur=data.time[case][vname].calendar
    legname = sim_nicename.get(case,case)
    color1=tableau20[2*(casenumber)] 
    plt.plot(data.plotdata[case][vname][:],label=legname,color=color1,lw=0.8)
    leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)

  plt.ylim([0.8,1.0])
  #plt.xlim([0.,150])
  
  if outputformat=="pdf":
    pp.savefig()
  else:
    figurename=filename+str(page)+"."+outputformat
    page+=1
    fig.savefig(figurename,format=outputformat,dpi=300) #,dpi=300)
  fig.clf()
  if outputformat=="pdf":
    pp.close()

def meanplot(data,vname):
  import numpy as np
  from math import ceil 
  filename=data.plotname+"_"+"".join(vname)
  outputformat="pdf"
  if outputformat=="pdf":
    pp = PdfPages(filename+'.pdf')
  else:
    page=0
  #fig = plt.figure(figsize=(15,12))
  fig = plt.figure(figsize=(11.69,8.27))
  gs0 = gridspec.GridSpec(12,60 )
  ax1 = plt.subplot(gs0[:,12:])
  #gs0 = gridspec.GridSpec(12,16 )
  #ax1 = plt.subplot(gs0[:,3:16])
  Setting={}
  Setting["PRAVG"]={}
  Setting["PRAVG"]["interval_h"]=3
  Setting["PRAVG"]["und"]=0
  Setting["PRAVG"]["upp"]=2
  Setting["PRAVG"]["interval"]=6
  Setting["PRAVG"]["yadd"]=9
  Setting["AT2M"]={}
  Setting["AT2M"]["interval_h"]=3
  Setting["AT2M"]["und"]=0
  Setting["AT2M"]["upp"]=2
  Setting["AT2M"]["interval"]=6
  Setting["AT2M"]["yadd"]=6

  interval_h=Setting[vname]["interval_h"]
  interval=Setting[vname]["interval"]
  x_up=data.plotdata[data.cases[0]][vname][0].shape[1]
  x_extra=10
  yloc_regname=-1

  months=(data.ye-data.yb+1)*12
  suptitle="%s %s*std markers"%(data.title[vname],data.nstd)
  fontsizetitle=16
  fontsizetick=9
  fontsizereg=9
  fontsizeleg=15
  fontsizeCC=9
  fig.suptitle(suptitle, fontsize=fontsizetitle, fontweight='bold')
  for casenumber,case in enumerate(data.cases):
    legname = sim_nicename.get(case,case)
    color=data.casecolors[case]  
    zorder=data.casezorders[case] 
    ls=data.caselinestyles[case]
    sidename = sim_nicename.get(case,case)
    for yloc,regname in enumerate(data.plotregnames):
      print(yloc,regname)
      ireg=data.regnames.index(regname)
      plt.axhline(interval*yloc, color='black',lw=0.1,ls=":")
      y_org=data.plotdata[case][vname][0][ireg]
      y_obs=data.plotdata["CN_OBS"][vname][0][ireg]
      y_shift=interval*yloc
      yplot=y_shift+y_org
      if "OBS" not in case:
        abnormal=list(np.where(np.abs(y_org-y_obs)>data.nstd))
      else:
        abnormal=[]
      if yloc==0:
        plt.plot(yplot,label=sidename,lw=0.5,color=color,zorder=zorder,ls=ls,marker="o",markevery=abnormal,markerfacecolor="None",ms=4.5)
      else:
        plt.plot(yplot,lw=0.5,color=color,zorder=zorder,ls=ls,marker="o",markevery=abnormal,markerfacecolor="None",ms=4.5)
      if casenumber==0:
        cc1=float(np.corrcoef(data.plotdata["new_ERI_albedo"][vname][0][ireg],data.plotdata[data.obsname][vname][0][ireg])[0,1])
        cc2=float(np.corrcoef(data.plotdata["RegCM"][vname][0][ireg],data.plotdata[data.obsname][vname][0][ireg])[0,1])
        #ax1.text(-5, interval*yloc, sim_nicename.get(regname,regname),fontsize=12,
        #   verticalalignment='center', horizontalalignment='right',
        #   rotation="vertical")
        ax1.text(10, interval_h+interval*yloc, "$Cor=%0.2f$"%cc1,fontsize=fontsizeCC,
           verticalalignment='center', horizontalalignment='left',
           color=data.casecolors["new_ERI_albedo"])
        ax1.text(50, interval_h+interval*yloc,"$Cor=%0.2f$"%cc2,fontsize=fontsizeCC,
           verticalalignment='center', horizontalalignment='left',
           color=data.casecolors["RegCM"])

  yshifts=data.yshifts
  #yshifts=[int(y) if y.is_integer() else y for y in data.yshifts]
  #yshifts=[x for x in range(-int(interval_h),int(interval_h)+1)]
  tickloc_y=[]
  for ireg,regname in enumerate(data.plotregnames):
    for yshift in yshifts:
      y=ireg*interval+yshift
      ylab=yshift if yshift<yshifts[-1] else ''
      #ax1.text(-0, y, ylab,fontsize=fontsizetick,#rotation="vertical",
      ax1.text(x_up+x_extra, y, ylab,fontsize=fontsizetick,#rotation="vertical",
      verticalalignment='center', horizontalalignment='right') #,
      tickloc_y.append(y)
  #ax1.yaxis.set_minor_locator(minorLocator)
  ax1.set_yticks(tickloc_y)



  tickloc=[x for x  in range(0,int(months),12)]
  ax1.set_xticks(tickloc)
  ticklabels=[]
  for year in range(data.yb,data.ye+1):
    ticklabels.append("%s"%(year))
  ax1.set_xticklabels(ticklabels,fontsize=fontsizetick,rotation="vertical")
  tickloc=[x for x  in range(0,int(months),6)]
  ax1.set_xticks(tickloc,minor=True)
  plt.tick_params(
        which='both',      # both major and minor ticks are affected
        direction="in",
        right='on',         # ticks along the top edge are off
        bottom='on',         # ticks along the top edge are off
        left='on',         # ticks along the top edge are off
        labelleft='off',         # ticks along the top edge are off
        top='on',         # ticks along the top edge are off
        length=4,width=0.6)
  plt.tick_params(
        which='minor',      # both major and minor ticks are affected
        direction="in",
        bottom='on',         # ticks along the top edge are off
        top='on',         # ticks along the top edge are off
        length=2,width=0.6
        ) 



  #leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)
  ax1.legend(loc='upper center',frameon=False, bbox_to_anchor=(0.5, 1.0),
            ncol=4,  fontsize=fontsizeleg,markerscale=0)
  for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(0.01)
  #plt.ylim([0.,50.0])
  plt.ylim([-int(len(yshifts)/2),1+int((len(data.plotregnames)-1)*interval+len(yshifts)/2)])
  plt.xlim([0.,x_up])
  #plt.xlim([0.,data.plotdata[case][vname][0].shape[1]])

  from constant import monthname 
  import numpy as np
  from math import ceil 
  ax2 = plt.subplot(gs0[:,1:11])

  Setting={}
  Setting["PRAVG"]={}
  Setting["PRAVG"]["interval_h"]=6
  Setting["PRAVG"]["und"]=0
  Setting["PRAVG"]["upp"]=2
  Setting["PRAVG"]["ytcik_interval"]=2
  Setting["PRAVG"]["yadd"]=-3
  Setting["PRAVG"]["shiftylabel"]=1
  Setting["PRAVG"]["y_down"]=0
  Setting["PRAVG"]["extra"]=2
  Setting["PRAVG"]["y_up"]=int((len(data.plotregnames)-1)*(2*Setting["PRAVG"]["interval_h"]+1)) +5#+Setting["PRAVG"]["yadd"]

  Setting["AT2M"]={}
  Setting["AT2M"]["interval_h"]=5
  Setting["AT2M"]["und"]=-1
  Setting["AT2M"]["upp"]=1
  Setting["AT2M"]["ytcik_interval"]=2
  Setting["AT2M"]["yadd"]=2.5
  Setting["AT2M"]["shiftylabel"]=0
  Setting["AT2M"]["y_down"]=-5# -Setting["AT2M"]["interval_h"]
  #Setting["AT2M"]["y_down"]=-3# -Setting["AT2M"]["interval_h"]
  Setting["AT2M"]["extra"]=1
  Setting["AT2M"]["y_up"]=int((len(data.plotregnames)-1)*(2*Setting["AT2M"]["interval_h"]+1))+Setting["AT2M"]["yadd"]
  #Setting["AT2M"]["y_up"]=int((len(data.plotregnames)-1)*(2*Setting["AT2M"]["interval_h"]+1))+Setting["AT2M"]["yadd"]
  shiftylabel=Setting[vname]["shiftylabel"]
  frameshifts={}
  frameshifts["AT2M"]={"ST":4,"WT":4,"SX":2}
  frameshifts["PRAVG"]={}

  interval_h=Setting[vname]["interval_h"]
  interval=interval_h*2#+1
  y_down,y_up=Setting[vname]["y_down"],Setting[vname]["y_up"]

  for casenumber,case in enumerate(data.cases):
    legname = sim_nicename.get(case,case)
    ls=data.caselinestyles[case]
    color=data.casecolors[case]  
    zorder=data.casezorders[case]
    sidename = sim_nicename.get(case,case)
    for yloc,regname in enumerate(data.plotregnames):
      ireg=data.regnames.index(regname)
      std=data.plotdata[case][vname][2][ireg]
      if vname=="AT2M":
        y=data.plotdata[case][vname][1][ireg]-data.plotdata[data.obsname][vname][1][ireg]
      else:
        plt.axhline(interval*yloc, color='black',lw=0.1,ls=":")
        y=data.plotdata[case][vname][1][ireg]
      y_real=interval*yloc+y+frameshifts[vname].get(regname,0) 
      #y_real=interval*ireg+y
      if yloc==0:
        plt.plot(y_real,label=sidename,lw=0.5,color=color,zorder=zorder,ls=ls)
      else:
        plt.plot(y_real,lw=0.5,color=color,zorder=zorder,ls=ls)
      plt.fill_between( range(len(monthname)),
                        y_real-std,
                        y_real+std,
                        alpha=0.3,lw=0.5,color=color,zorder=zorder)
      """
      if casenumber==0:
        ax2.text(6, interval*yloc+1, regname,fontsize=fontsizetick,
           verticalalignment='center', horizontalalignment='right' ) #,
           #rotation="vertical")
      """
      textloc=interval*yloc if vname=="AT2M" else interval*(yloc+0.5)
      ax2.text(yloc_regname, textloc, sim_nicename.get(regname,regname),fontsize=fontsizereg,
           verticalalignment='center', horizontalalignment='right',
           rotation="vertical")
  yshifts=[x for x in range(int(interval_h)*Setting[vname]["und"]+Setting[vname]["extra"]
                            ,int(interval_h)*Setting[vname]["upp"]+Setting[vname]["extra"]
                            ,Setting[vname]["ytcik_interval"])]

  tickloc_y=[]
  for yloc,regname in enumerate(data.plotregnames):
    for yshift in yshifts:
      y=yloc*interval+yshift
      if y>y_down and y<y_up:
        ylab=yshift-frameshifts[vname].get(regname,0)
        ax2.text(-0, y, ylab,fontsize=fontsizetick, #rotation="vertical",
        verticalalignment='center', horizontalalignment='right') #,
        tickloc_y.append(y)
  ax2.set_yticks(tickloc_y)

  tickloc=[x for x  in range(0,len(monthname))]
  ax2.set_xticks(tickloc)
  ax2.set_xticklabels(monthname,fontsize=fontsizetick,rotation="vertical")
  ax2.set_xticks(tickloc,minor=True)
  plt.tick_params(
        which='both',      # both major and minor ticks are affected
        direction="in",
        right='on',         # ticks along the top edge are off
        bottom='on',         # ticks along the top edge are off
        left='on',         # ticks along the top edge are off
        labelleft='off',         # ticks along the top edge are off
        top='off',         # ticks along the top edge are off
        length=2,width=0.6)
  plt.tick_params(
        which='minor',      # both major and minor ticks are affected
        direction="in",
        bottom='on',         # ticks along the top edge are off
        top='on',         # ticks along the top edge are off
        length=1,width=0.6
        ) 

  for axis in ['top','bottom','left','right']:
    ax2.spines[axis].set_linewidth(0.01)
  plt.ylim([y_down,y_up])
  plt.xlim([0.,11])

  if data.outputformat=="pdf":
    pp.savefig()
    #pp.savefig(bbox_inches='tight')
  else:
    figurename=filename+str(page)+"."+outputformat
    page+=1
    fig.savefig(figurename,format=outputformat,dpi=300) #,dpi=300)
  if data.outputformat=="pdf":
    pp.close()
  print("finished plot climate monthly data!")
