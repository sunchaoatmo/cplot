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
    plt.plot(data.plotdata[case][vname][:150],label=legname,color=color1,lw=0.8)
    print(np.argmin(data.plotdata[case][vname][:150]))
    leg=ax1.legend(loc=1,borderaxespad=0.,frameon=False, fontsize=6)

  for imonth in range(150):
    print("month=%s,cwrf=%s,regcm=%s"%(imonth,data.plotdata["new_ERI_albedo"][vname][imonth],data.plotdata["RegCM"][vname][imonth]))
  plt.ylim([0.8,1.0])
  plt.xlim([0.,150])
  
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
