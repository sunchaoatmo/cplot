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
  print(np.corrcoef(data.plotdata["RegCM"][vname],data.plotdata["ERI"][vname]))
  print(np.corrcoef(data.plotdata["new_ERI_albedo"][vname],data.plotdata["ERI"][vname]))
  for casenumber,case in enumerate(data.plotlist):
    #units_cur=data.time[case][vname].units
    #calendar_cur=data.time[case][vname].calendar
    legname = sim_nicename.get(case,case)
    color1=tableau20[2*(casenumber)] 
    plt.plot(data.plotdata[case][vname][:],label=legname,color=color1,lw=0.8)
    print(np.argmin(data.plotdata[case][vname][:]))
    leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)

  plt.ylim([0.8,1.0])
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

def meanplot(data,vname):
  import numpy as np
  from math import ceil 
  filename=data.plotname+"_"+"".join(vname)
  outputformat="pdf"
  if outputformat=="pdf":
    pp = PdfPages(filename+'.pdf')
  else:
    page=0
  fig = plt.figure(figsize=(8.5,12))
  gs0 = gridspec.GridSpec(1,1 )
  ax1 = plt.subplot(gs0[0])
  Setting={}
  Setting["PRAVG"]={}
  Setting["PRAVG"]["interval_h"]=3
  Setting["PRAVG"]["und"]=0
  Setting["PRAVG"]["upp"]=2
  Setting["PRAVG"]["interval"]=7
  Setting["PRAVG"]["yadd"]=9
  Setting["AT2M"]={}
  Setting["AT2M"]["interval_h"]=3
  Setting["AT2M"]["und"]=0
  Setting["AT2M"]["upp"]=2
  Setting["AT2M"]["interval"]=7
  Setting["AT2M"]["yadd"]=9

  interval_h=Setting[vname]["interval_h"]
  interval=Setting[vname]["interval"]

  months=(data.ye-data.yb+1)*12
  for casenumber,case in enumerate(data.plotlist):
    legname = sim_nicename.get(case,case)
    color=data.casecolors[case]  #tableau20[2*(casenumber-1)] 
    zorder=data.casezorders[case]  #tableau20[2*(casenumber-1)] 
    sidename = sim_nicename.get(case,case)
    for yloc,regname in enumerate(data.plotregnames):
      ireg=data.regnames.index(regname)
      plt.axhline(interval*ireg, color='black',lw=0.1,ls=":")
      if ireg==0:
        plt.plot(interval*yloc+data.plotdata[case][vname][0][ireg],label=sidename,lw=0.5,color=color,zorder=zorder)
        #plt.plot(xdate,interval*yloc+data.plotdata[case][vname][0][ireg],label=sidename,lw=0.5,color=color,zorder=zorder)
      else:
        plt.plot(interval*yloc+data.plotdata[case][vname][0][ireg],lw=0.5,color=color,zorder=zorder)
      if casenumber==0:
        cc1=float(np.corrcoef(data.plotdata["new_ERI_albedo"][vname][0][ireg],data.plotdata[data.obsname][vname][0][ireg])[0,1])
        cc2=float(np.corrcoef(data.plotdata["RegCM"][vname][0][ireg],data.plotdata[data.obsname][vname][0][ireg])[0,1])
        ax1.text(-5, interval*yloc, regname,fontsize=6,
           verticalalignment='center', horizontalalignment='right',
           rotation="vertical")
        ax1.text(10, interval_h+interval*yloc, "$CC=%0.3f$"%cc1,fontsize=6,
           verticalalignment='center', horizontalalignment='left',
           color=data.casecolors["new_ERI_albedo"])
        ax1.text(50, interval_h+interval*yloc,"$CC=%0.3f$"%cc2,fontsize=6,
           verticalalignment='center', horizontalalignment='left',
           color=data.casecolors["RegCM"])

  yshifts=[x for x in range(-int(interval_h),int(interval_h)+1)]
  print(yshifts)
  tickloc_y=[]
  for yloc,regname in enumerate(data.plotregnames):
    for yshift in yshifts:
      y=yloc*interval+yshift
      ax1.text(-0, y, yshift,fontsize=5,rotation="vertical",
      verticalalignment='center', horizontalalignment='right') #,
      tickloc_y.append(y)
  #ax1.yaxis.set_minor_locator(minorLocator)
  ax1.set_yticks(tickloc_y)



  tickloc=[x for x  in range(0,int(months),12)]
  ax1.set_xticks(tickloc)
  ticklabels=[]
  for year in range(data.yb,data.ye+1):
    ticklabels.append("%s"%(year))
  ax1.set_xticklabels(ticklabels,fontsize=5,rotation="vertical")
  tickloc=[x for x  in range(0,int(months))]
  ax1.set_xticks(tickloc,minor=True)
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



  #leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)
  ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 0.99),
            ncol=4, fancybox=True,  fontsize=6)
  for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(0.01)
  #plt.ylim([0.,50.0])
  plt.ylim([-1-int(len(yshifts)/2),3+int((len(data.plotregnames)-1)*interval+len(yshifts)/2)])
  plt.xlim([0.,data.plotdata[case][vname][0].shape[1]])

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
def monthlystdfillplot(data,vname):
  from constant import monthname 
  import numpy as np
  from math import ceil 
  filename=data.plotname+"_"+"".join(vname)+"_std"
  if data.outputformat=="pdf":
    pp = PdfPages(filename+'.pdf')
  else:
    page=0
  fig = plt.figure(figsize=(6.,20))
  gs0 = gridspec.GridSpec(1,1 )
  ax1 = plt.subplot(gs0[0])

  Setting={}
  Setting["PRAVG"]={}
  Setting["PRAVG"]["interval_h"]=6
  Setting["PRAVG"]["und"]=0
  Setting["PRAVG"]["upp"]=2
  Setting["PRAVG"]["ytcik_interval"]=2
  Setting["PRAVG"]["yadd"]=9
  Setting["PRAVG"]["shiftylabel"]=1
  Setting["PRAVG"]["y_down"]=0
  Setting["PRAVG"]["y_up"]=int((len(data.plotregnames)-1)*(2*Setting["PRAVG"]["interval_h"]+1))+Setting["PRAVG"]["yadd"]

  Setting["AT2M"]={}
  Setting["AT2M"]["interval_h"]=10
  Setting["AT2M"]["und"]=-1
  Setting["AT2M"]["upp"]=1
  Setting["AT2M"]["ytcik_interval"]=2
  Setting["AT2M"]["yadd"]=9
  Setting["AT2M"]["shiftylabel"]=0
  Setting["AT2M"]["y_down"]=-3# -Setting["AT2M"]["interval_h"]
  Setting["AT2M"]["y_up"]=int((len(data.plotregnames)-1)*(2*Setting["AT2M"]["interval_h"]+1))+Setting["AT2M"]["yadd"]
  shiftylabel=Setting[vname]["shiftylabel"]

  interval_h=Setting[vname]["interval_h"]
  interval=interval_h*2+1
  y_down,y_up=Setting[vname]["y_down"],Setting[vname]["y_up"]

  for casenumber,case in enumerate(data.plotlist):
    legname = sim_nicename.get(case,case)
    color=data.casecolors[case]  #tableau20[2*(casenumber-1)] 
    zorder=data.casezorders[case]  #tableau20[2*(casenumber-1)] 
    sidename = sim_nicename.get(case,case)
    for yloc,regname in enumerate(data.plotregnames):
      ireg=data.regnames.index(regname)
      plt.axhline(interval*ireg, color='black',lw=0.1,ls=":")
      std=data.plotdata[case][vname][2][ireg]
      if vname=="AT2M":
        y=data.plotdata[case][vname][1][ireg]-data.plotdata[data.obsname][vname][1][ireg]
      else:
        y=data.plotdata[case][vname][1][ireg]
      if ireg==0:
        plt.plot(interval*yloc+y,label=sidename,lw=0.5,color=color,zorder=zorder)
      else:
        plt.plot(interval*yloc+y,lw=0.5,color=color,zorder=zorder)
      plt.fill_between( range(len(monthname)),
                        interval*yloc+y-std,
                        interval*yloc+y+std,
                        alpha=0.3,lw=0.5,color=color,zorder=zorder)
      if casenumber==0:
        ax1.text(-0.3, shiftylabel*interval_h+interval*yloc, regname,fontsize=6,
           verticalalignment='center', horizontalalignment='right',
           rotation="vertical")
        """
        cc1=float(np.corrcoef(data.plotdata["new_ERI_albedo"][vname][1][ireg],data.plotdata[data.obsname][vname][1][ireg])[0,1])
        cc2=float(np.corrcoef(data.plotdata["RegCM"][vname][1][ireg],data.plotdata[data.obsname][vname][1][ireg])[0,1])
        ax1.text(0.2, 7+interval*yloc, "$CC=%0.3f$"%cc1,fontsize=6,
           verticalalignment='center', horizontalalignment='left',
           color=data.casecolors["new_ERI_albedo"])
        ax1.text(1.3, 7+interval*yloc,"$CC=%0.3f$"%cc2,fontsize=6,
           verticalalignment='center', horizontalalignment='left',
           color=data.casecolors["RegCM"])
        """
  yshifts=[x for x in range(int(interval_h)*Setting[vname]["und"]
                            ,int(interval_h)*Setting[vname]["upp"]+2
                            ,Setting[vname]["ytcik_interval"])]
  print(yshifts)
  tickloc_y=[]
  for yloc,regname in enumerate(data.plotregnames):
    for yshift in yshifts:
      y=yloc*interval+yshift
      if y>y_down and y<y_up:
        ax1.text(-0, y, yshift,fontsize=5,rotation="vertical",
        verticalalignment='center', horizontalalignment='right') #,
        tickloc_y.append(y)
  ax1.set_yticks(tickloc_y)

  tickloc=[x for x  in range(0,len(monthname))]
  ax1.set_xticks(tickloc)
  ax1.set_xticklabels(monthname,fontsize=5)  #,rotation="vertical")
  ax1.set_xticks(tickloc,minor=True)
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

  ax1.legend(loc='upper center', bbox_to_anchor=(0.5, 0.99),
            ncol=4, fancybox=True,  fontsize=6)
  for axis in ['top','bottom','left','right']:
    ax1.spines[axis].set_linewidth(0.01)
  plt.ylim([y_down,y_up])
  plt.xlim([0.,11])

  if data.outputformat=="pdf":
    pp.savefig()
  else:
    print(outputformat)
    figurename=filename+str(page)+"."+outputformat
    page+=1
    fig.savefig(figurename,format=outputformat,dpi=300) #,dpi=300)
  fig.clf()
  if data.outputformat=="pdf":
    pp.close()
  print("finished plot climate monthly data!")
