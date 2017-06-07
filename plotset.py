#!/usr/bin/env python
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import  cm
import numpy as np# reshape
from cstoolkit import drange
from matplotlib.colors import LinearSegmentedColormap
"""
cmap_cs_precp = [ (242, 242, 242), (191, 239, 255), (178, 223, 238), 
            (154, 192, 205), (  0, 235, 235), (  0, 163, 247), 
            (153, 255, 51),(  0, 255,   0), (  0, 199,   0), (  0, 143,   0), 
            (  0,  63,   0), (255, 255,   0),(255, 204, 0) ,   (255, 143,   0),
            (255,   0,   0), (215,   0,   0), 
            (255,   0, 255) ] #, (155,  87, 203)]
"""
cmap_cs_precp = [ (242, 242, 242),  (178, 223, 238),(154, 192, 205),(68, 176, 213),
              (  0, 163, 247), (  0, 235, 235),
            (153, 255, 51),(  0, 255,   0), (  0, 199,   0), (  0, 143,   0), 
            (  0,  63,   0), (255, 255,   0),(255, 204, 0) ,   (255, 143,   0),
            (255,   0,   0), (215,   0,   0), 
            (255,   0, 255) ] #, (155,  87, 203)]

tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
 
def buildcmp(cmaplist):
  for i in range(len(cmaplist)):    
      r, g, b = cmaplist[i]    
      cmaplist[i] = (r / 255., g / 255., b / 255.) 
  return LinearSegmentedColormap.from_list( "precip", cmaplist,N=len(cmaplist))
cmap_cs_precp=buildcmp(cmap_cs_precp)
cmap_cs_precp.set_over('purple')
tableau20=buildcmp(tableau20)
sim_nicename={"ERI":"ERI",
             "RegCM":"RegCM4.6",
             "PRAVG":"PR",
             "SDII":"DI",
             "RAINYDAYS":"RD",
             "run_RegCM4.6":"RegCM\n4.6",
             "run_RegCM4.5":"RegCM\n4.5",
             "ERI_run_0":"old CWRF",
             "new_ERI_run_0":"CWRF\nMor",
             "new_ERI_gsfc":"CWRF",
             "new_ERI_albedo":"Albedo",
#             "new_ERI_gsfc":"CWRF\nGSFC",
             "new_ERI_morr":"Mor",
             "run_00":"CWRF",
             "xoml":"new_xoml",
             "run_01":"BMJ",
             "run_02":"NKF",
             "run_03":"NSAS",
             "run_04":"TDK",
             "run_06":"MB",
             "run_06":"THO",
             "run_07":"MOR",
             "run_08":"WD6",
             "run_09":"AER",
            "run_10": "XR",   # "Radall",
            "run_11":"CCCMA",
            "run_12":"FLG",
            "run_13":"RRTMG",
            "run_14":"MYNN",
            "run_15":"ACM",
            "run_16":"UW",
            "run_17":"NOAH",
            "run_18":"XOML",
            "run_19":"F-M",
            "run_20":"FMBMJ",
            "run_21":"FMNKF",
            "run_22":"FMNSAS",
            "run_23":"FMTDK",
            "run_24":"FMMB",#"scheme_cst_2",
            "run_25":"FMTHO",#"scheme_cst_3",
            "run_26":"FMMOR",#"scheme_cst_3",
            "run_27":"boulac",#"scheme_ccb_1",
            "run_28":"gfs",#"scheme_ccb_4",
            "run_29":"mynn2",#"scheme_ccb_5",
            "run_30":"new cloud",#"scheme_ccs_3",
            "run_31":"boulac",      #"NewTHO",
            "run_32":"gfs2",      #"NewMOR",
            "run_33":"",      #"NewMOR",
            "run_34":"New Melt",      #"NewMOR",
            "run_35":"old CAM",      #"NewMOR",
            "run_36":"NewSW",      #"NewMOR",
            "run_37":"ACM",      #"NewMOR",
            "run_38":"bedrock",      #"NewMOR",
            "run_39":"CF",      #"NewMOR",
            "run_40":"NewDrain V0",      #"NewMOR",
            "run_41":"Warm start V1",      #"NewMOR",
            "run_42":"Cold start V1",      #"NewMOR",
            "run_43":"inflx ",      #"NewMOR",
            "run_44":"om ",      #"NewMOR",
            "run_45":"New Soil Water",      #"NewMOR",
            "run_46":"New Reff",      #"NewMOR",
            "run_47":"OISST",      #"NewMOR",
            "run_48":"NOoml",      #"NewMOR",
            "run_49":"NOocean",      #"NewMOR",
            "run_50":"MSA_newSW",    #"ERIsst"
            "run_51":"NoMSA ipf0",      #"NewMOR",
            "run_52":"new UWCAM",      #"NewMOR",
            "run_53":"NoMSA ipf2",      #"NewMOR",
            "run_54":"AERO_MSAon",      #"NewMOR",
            "run_55":"AERO_MSAold",      #"NewMOR",
            "run_56":"noAERO",      #"NewMOR",
            "run_57":"OBC_V0",     #"SVNcode",      #"NewMOR",
            "run_58":"OBClg100",      #"NewMOR",
            "run_59":"OBClg111",      #"NewMOR",
            "run_60":"WRF",      #"NewMOR",
            "run_61":"ALBfix",      #"NewMOR",
            "run_62":"PSFC4_NSW",      #"NewMOR",
            "run_63":"PSFC4_OSW",      #"NewMOR",
            "run_64":"psfc4_osw_CAMUW",      #"NewMOR",
            "run_65":"git558faed",      #"NewMOR",
            "run_66":"psfc4morr",      #"NewMOR",
            "run_67":"newsw_morr",      #"NewMOR",
            "run_68":"psfc4_osw_v2",      #"NewMOR",
            "run_69":"WRFRUN",      #
            "run_70":"PSFC4_NSW",   #oldini0     
            "run_71":"PSFC4_V0",    #"PSFC4_SVNCODE"
            "run_72":"OBC_OSW" ,    #"oldBC_osw"
            "run_73":"PSFC4_br_OSW" ,    #"oldBC_osw"
            "run_74":"OLDini_br_NSW" ,    #"oldBC_osw"
            "run_75":"OLDini_br_V0" ,    #"oldBC_osw"
            "run_76":"OLDini_br_558faed" ,    #"oldBC_osw"
            "run_77":"OVEG_NSW" ,    #"oldBC_osw"
            "run_78":"OVEG_OSW" ,    #"oldBC_osw"
            "run_79":"OVEG_V0" ,    #"oldBC_osw"
            "run_80":"HydRED" ,    #"oldBC_osw"
            "run_81":"CTL" ,    #"oldBC_osw"
            "run_82":"newcam" ,    #"oldBC_osw"
            "run_oldSW_flw8_new":"CWRF",
            "ERI_run_1":"CWRF/CLM4.5",
            "CESM_run_0":"CWRF/CSSP",
            "CESM_run_1":"CWRF/CLM4.5",
            "PCR85-CESM_run_0":"CWRF/CSSP",
            "PCR85-CESM_run_1":"CWRF/CLM4.5",
            "run_CTL":"CTL ",
            "CESM":"CESM",
            "run_CLM4.5":"CLM4.5Hyd ",
            "run_Red":"HydRed ",
            "run_noxoml":"NO xoml ",
            "run_nolake":"NO lake ",
            "run_oldrad" :"Old Alb ",
            "run_oldveg":"Old LAI ",
            "run_noforzen":"Old frozen ",
              "Mean":"Mean",
              "Mean_Sub":"Mean_Sub",
               "Med":"Med",
               "P85":"P85",
               "P80":"P80",
               "P70":"P70",
               "P10":"P10",
               "P20":"P20",
               "Obs":"OBS",
               "OBS":"OBS",
               "Max":"Max",
              "run_1":"MY/MO/W1.5/MC0.5/TD0",
              "run_2":"CAM/GSFC/W1.5/MC0.75/TD0",
              "run_3":"MY/MO/W1.5/MC0.75/TD0",
              "run_4":"MY/MO/W1/MC0.75/TD0",
              "run_5":"MY/MO/W1/MC0.75/TD0.5",
              "run_6":"MY/MO/W1/MC1/TD0",
              "run_7":"MY/MO/W1/MC1/TD1"}
#plotres={'PRAVG':{},'PCT':{},'CDD':{},'RAINYDAYS':{},'AT2M':{},'ASWUPT':{}}

from collections import defaultdict
plotres= defaultdict(dict)

##########################set the plot related parameters#####################
plotres['XRSUR']['cleve1']=[x*1e-6 for x in range(31)]
plotres['XRSUR']['cleve2']=[x*1e-6*3*2 for x in range(-5,6) ]#np.linspace(-5,5,21)
plotres['XRSUR']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['XRSUR']['cmp2']=cmp
plotres['XRSUR']['eri_name']=None
plotres['XRSUR']['eri_vname']=None
plotres['XRSUR']['obs_name']="XRSUR_isccp.nc"
plotres['XRSUR']['obs_vname']="XRSUR_seasonal_daily"
plotres['XRSUR']['sim_name']="XRSUR" #"  #seasonal.bin" 
#plotres['XRSUR']['convertcoef']=0.001
plotres['XRSUR']['sim_vname']="XRSUR" #"  #seasonal.bin" 
plotres['XRSUR']['unit']="kg/m2/day"
plotres['XRSUR']['mask']=True
plotres['XRSUR']['biasplot']=True
plotres['XRSUR']['ETS']=False
plotres['XRSUR']['Taylor']=True
plotres['XRSUR']['violion']=False

plotres['XRBAS']['cleve1']=[x*1e-6 for x in range(31)]
plotres['XRBAS']['cleve2']=[x*1e-6*3*2 for x in range(-5,6) ]#np.linspace(-5,5,21)
plotres['XRBAS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['XRBAS']['cmp2']=cmp
plotres['XRBAS']['eri_name']=None
plotres['XRBAS']['eri_vname']=None
plotres['XRBAS']['sim_name']="XRBAS" #"  #seasonal.bin" 
plotres['XRBAS']['sim_vname']="XRBAS" #"  #seasonal.bin" 
plotres['XRBAS']['unit']="kg/m2/day"
plotres['XRBAS']['mask']=True
plotres['XRBAS']['biasplot']=True
plotres['XRBAS']['ETS']=False
plotres['XRBAS']['Taylor']=True
plotres['XRBAS']['violion']=False


plotres['SFROFF']['cleve1']=[x*10000 for x in range(31)]
plotres['SFROFF']['cleve2']=range(-30,31) #np.linspace(-5,5,21)
plotres['SFROFF']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['SFROFF']['cmp2']=cmp
plotres['SFROFF']['eri_name']=None
plotres['SFROFF']['eri_vname']=None
plotres['SFROFF']['obs_name']="SFROFF_isccp.nc"
plotres['SFROFF']['obs_vname']="SFROFF_seasonal_daily"
plotres['SFROFF']['sim_name']="SFROFF" #"  #seasonal.bin" 
#plotres['SFROFF']['convertcoef']=0.001
plotres['SFROFF']['sim_vname']="SFROFF" #"  #seasonal.bin" 
plotres['SFROFF']['unit']="kg/m2"
plotres['SFROFF']['mask']=True
plotres['SFROFF']['biasplot']=True
plotres['SFROFF']['ETS']=False
plotres['SFROFF']['Taylor']=True
plotres['SFROFF']['violion']=False



plotres['XSMTg']['cleve1']=[x*20 for x in range(1,20)] #range(0, 1,0.05)
plotres['XSMTg']['cleve2']=[x*10*2 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['XSMTg']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['XSMTg']['cmp2']=cmp
plotres['XSMTg']['eri_name']=None
plotres['XSMTg']['eri_vname']=None
plotres['XSMTg']['obs_name']="XSMTg_isccp.nc"
plotres['XSMTg']['obs_vname']="XSMTg_seasonal_daily"
plotres['XSMTg']['sim_name']="XSMTg" #"  #seasonal.bin" 
plotres['XSMTg']['sim_vname']="XSMTg" #"  #seasonal.bin" 
plotres['XSMTg']['unit']="kg/m2"
plotres['XSMTg']['mask']=True
plotres['XSMTg']['biasplot']=True
plotres['XSMTg']['ETS']=False
plotres['XSMTg']['Taylor']=True
plotres['XSMTg']['violion']=False
plotres['XSMTg']['vlevel']=4

plotres['AODNIR']['cleve0']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
plotres['AODNIR']['cleve1']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
plotres['AODNIR']['cleve2']=[x*0.1 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['AODNIR']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['AODNIR']['cmp2']=cmp
plotres['AODNIR']['eri_name']=None
plotres['AODNIR']['eri_vname']=None
plotres['AODNIR']['obs_name']="AODNIR_isccp.nc"
plotres['AODNIR']['obs_vname']="AODNIR_seasonal_daily"
plotres['AODNIR']['sim_name']="AODNIR" #"  #seasonal.bin" 
plotres['AODNIR']['sim_vname']="AODNIR" #"  #seasonal.bin" 
#plotres['AODNIR']['convertcoef']=0.01
plotres['AODNIR']['unit']=""
plotres['AODNIR']['mask']=True
plotres['AODNIR']['biasplot']=False
plotres['AODNIR']['ETS']=False
plotres['AODNIR']['Taylor']=True


plotres['AODVIS']['cleve0']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
plotres['AODVIS']['cleve1']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
plotres['AODVIS']['cleve2']=[x*0.1 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['AODVIS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['AODVIS']['cmp2']=cmp
plotres['AODVIS']['eri_name']=None
plotres['AODVIS']['eri_vname']=None
plotres['AODVIS']['obs_name']="AODVIS_isccp.nc"
plotres['AODVIS']['obs_vname']="AODVIS_seasonal_daily"
plotres['AODVIS']['sim_name']="AODVIS" #"  #seasonal.bin" 
plotres['AODVIS']['sim_vname']="AODVIS" #"  #seasonal.bin" 
#plotres['AODVIS']['convertcoef']=0.01
plotres['AODVIS']['unit']=""
plotres['AODVIS']['mask']=True
plotres['AODVIS']['biasplot']=False
plotres['AODVIS']['ETS']=False
plotres['AODVIS']['Taylor']=True


plotres['CLDFRAh']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRAh']['cleve2']=[x*0.1 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['CLDFRAh']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRAh']['cmp2']=cmp
plotres['CLDFRAh']['eri_name']=None
plotres['CLDFRAh']['eri_vname']=None
plotres['CLDFRAh']['obs_name']="CLDFRAh_isccp.nc"
plotres['CLDFRAh']['obs_vname']="CLDFRAh_seasonal_daily"
plotres['CLDFRAh']['sim_name']="CLDFRAg" #"  #seasonal.bin" 
plotres['CLDFRAh']['sim_vname']="CLDFRAg" #"  #seasonal.bin" 
#plotres['CLDFRAh']['convertcoef']=0.01
plotres['CLDFRAh']['unit']=""
plotres['CLDFRAh']['mask']=True
plotres['CLDFRAh']['biasplot']=True
plotres['CLDFRAh']['ETS']=False
plotres['CLDFRAh']['Taylor']=True
plotres['CLDFRAh']['violion']=False
plotres['CLDFRAh']['vlevel']=3



plotres['CLDFRAm']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRAm']['cleve2']=[x*0.1 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['CLDFRAm']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRAm']['cmp2']=cmp
plotres['CLDFRAm']['eri_name']=None
plotres['CLDFRAm']['eri_vname']=None
plotres['CLDFRAm']['obs_name']="CLDFRAm_isccp.nc"
plotres['CLDFRAm']['obs_vname']="CLDFRAm_seasonal_daily"
plotres['CLDFRAm']['sim_name']="CLDFRAg" #"  #seasonal.bin" 
plotres['CLDFRAm']['sim_vname']="CLDFRAg" #"  #seasonal.bin" 
#plotres['CLDFRAm']['convertcoef']=0.01
plotres['CLDFRAm']['unit']=""
plotres['CLDFRAm']['mask']=True
plotres['CLDFRAm']['biasplot']=True
plotres['CLDFRAm']['ETS']=False
plotres['CLDFRAm']['Taylor']=True
plotres['CLDFRAm']['violion']=False
plotres['CLDFRAm']['vlevel']=2




plotres['CLDFRAl']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRAl']['cleve2']=[x*0.1 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['CLDFRAl']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRAl']['cmp2']=cmp
plotres['CLDFRAl']['eri_name']=None
plotres['CLDFRAl']['eri_vname']=None
plotres['CLDFRAl']['obs_name']="CLDFRAl_isccp.nc"
plotres['CLDFRAl']['obs_vname']="CLDFRAl_seasonal_daily"
plotres['CLDFRAl']['sim_name']="CLDFRAg" #"  #seasonal.bin" 
plotres['CLDFRAl']['sim_vname']="CLDFRAg" #"  #seasonal.bin" 
#plotres['CLDFRAl']['convertcoef']=0.01
plotres['CLDFRAl']['unit']=""
plotres['CLDFRAl']['mask']=True
plotres['CLDFRAl']['biasplot']=True
plotres['CLDFRAl']['ETS']=False
plotres['CLDFRAl']['Taylor']=True
plotres['CLDFRAl']['violion']=False
plotres['CLDFRAl']['vlevel']=1


plotres['CLDFRA']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRA']['cleve2']=[x*0.1 for x in range(-10,11)] #np.linspace(-5,5,21)
plotres['CLDFRA']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRA']['cmp2']=cmp
plotres['CLDFRA']['eri_name']=None
plotres['CLDFRA']['eri_vname']=None
plotres['CLDFRA']['obs_name']="CLDFRA_isccp.nc"
plotres['CLDFRA']['obs_vname']="CLDFRA_seasonal_daily"
plotres['CLDFRA']['sim_name']="CLDFRAg" #"  #seasonal.bin" 
plotres['CLDFRA']['sim_vname']="CLDFRAg" #"  #seasonal.bin" 
#plotres['CLDFRA']['convertcoef']=0.01
plotres['CLDFRA']['unit']=""
plotres['CLDFRA']['mask']=True
plotres['CLDFRA']['biasplot']=True
plotres['CLDFRA']['ETS']=False
plotres['CLDFRA']['Taylor']=True
plotres['CLDFRA']['violion']=False
plotres['CLDFRA']['vlevel']=0



plotres['QVAPOR']['cleve1']=range(0, 20,1)
plotres['QVAPOR']['cleve2']=range(-20,22,2) #np.linspace(-5,5,21)
plotres['QVAPOR']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['QVAPOR']['cmp2']=cmp
plotres['QVAPOR']['obs_name']=None
plotres['QVAPOR']['obs_vname']=None
plotres['QVAPOR']['eri_name']=None
plotres['QVAPOR']['eri_vname']=None
plotres['QVAPOR']['sim_name']="QVAPOR" #"  #seasonal.bin" 
plotres['QVAPOR']['sim_vname']="QVAPOR" #"  #seasonal.bin" 
plotres['QVAPOR']['convertcoef']=1000
plotres['QVAPOR']['unit']="$g/kg$"
plotres['QVAPOR']['mask']=False
plotres['QVAPOR']['biasplot']=False
plotres['QVAPOR']['ETS']=False
plotres['QVAPOR']['Taylor']=True
plotres['QVAPOR']['violion']=False
plotres['QVAPOR']['vlevel']=21



plotres['TCWPC']['cleve1']=range(0, 200,10)
plotres['TCWPC']['cleve2']=range(-60,62,2) #np.linspace(-5,5,21)
plotres['TCWPC']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['TCWPC']['cmp2']=cmp
plotres['TCWPC']['obs_name']="tcwpc_isccp.nc"
plotres['TCWPC']['obs_vname']="tcwpc_seasonal_daily"
plotres['TCWPC']['eri_name']=None
plotres['TCWPC']['eri_vname']=None
plotres['TCWPC']['sim_name']="TCWPC" #"  #seasonal.bin" 
plotres['TCWPC']['sim_vname']="TCWPC" #"  #seasonal.bin" 
plotres['TCWPC']['unit']="$g/m^{2}$"
plotres['TCWPC']['mask']=True
plotres['TCWPC']['biasplot']=True
plotres['TCWPC']['ETS']=False
plotres['TCWPC']['Taylor']=True
plotres['TCWPC']['violion']=False



plotres['V']['cleve1']=range(-10, 10,1)
plotres['V']['cleve2']=range(-20,22,2) #np.linspace(-5,5,21)
plotres['V']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['V']['cmp2']=cmp
plotres['V']['obs_name']=None
plotres['V']['obs_vname']=None
plotres['V']['eri_name']=None
plotres['V']['eri_vname']=None
plotres['V']['sim_name']="V" #"  #seasonal.bin" 
plotres['V']['sim_vname']="V" #"  #seasonal.bin" 
plotres['V']['unit']="$m/s$"
plotres['V']['mask']=False
plotres['V']['biasplot']=False
plotres['V']['ETS']=False
plotres['V']['Taylor']=True
plotres['V']['violion']=False
plotres['V']['vlevel']=21


plotres['U']['cleve1']=range(-10, 10,1)
plotres['U']['cleve2']=range(-20,22,2) #np.linspace(-5,5,21)
plotres['U']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['U']['cmp2']=cmp
plotres['U']['obs_name']=None
plotres['U']['obs_vname']=None
plotres['U']['eri_name']=None
plotres['U']['eri_vname']=None
plotres['U']['sim_name']="U" #"  #seasonal.bin" 
plotres['U']['sim_vname']="U" #"  #seasonal.bin" 
plotres['U']['unit']="$m/s$"
plotres['U']['mask']=False
plotres['U']['biasplot']=False
plotres['U']['ETS']=False
plotres['U']['Taylor']=True
plotres['U']['violion']=False
plotres['U']['vlevel']=21


plotres['PSL']['cleve1']=range(1000, 1024,1)
plotres['PSL']['cleve2']=range(-20,22,2) #np.linspace(-5,5,21)
plotres['PSL']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['PSL']['cmp2']=cmp
plotres['PSL']['obs_name']=None
plotres['PSL']['obs_vname']=None
plotres['PSL']['eri_name']=None
plotres['PSL']['eri_vname']=None
plotres['PSL']['sim_name']="PSL" #"  #seasonal.bin" 
plotres['PSL']['sim_vname']="PSL" #"  #seasonal.bin" 
plotres['PSL']['unit']="$\%$"
plotres['PSL']['convertcoef']=0.01
plotres['PSL']['mask']=False
plotres['PSL']['biasplot']=False
plotres['PSL']['ETS']=False
plotres['PSL']['Taylor']=True
plotres['PSL']['violion']=False

plotres['PS']['cleve1']=range(700, 1030,5)
plotres['PS']['cleve2']=range(-20,22,2) #np.linspace(-5,5,21)
plotres['PS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['PS']['cmp2']=cmp
plotres['PS']['obs_name']=None
plotres['PS']['obs_vname']=None
plotres['PS']['eri_name']=None
plotres['PS']['eri_vname']=None
plotres['PS']['sim_name']="PS" #"  #seasonal.bin" 
plotres['PS']['sim_vname']="PS" #"  #seasonal.bin" 
plotres['PS']['unit']="$\%$"
plotres['PS']['convertcoef']=0.01
plotres['PS']['mask']=False
plotres['PS']['biasplot']=False
plotres['PS']['ETS']=False
plotres['PS']['Taylor']=True
plotres['PS']['violion']=False


plotres['ALBEDO']['cleve1']=range(0, 60,5)
plotres['ALBEDO']['cleve2']=range(-20,22,2) #np.linspace(-5,5,21)
plotres['ALBEDO']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALBEDO']['cmp2']=cmp
plotres['ALBEDO']['obs_name']="SAL_albe_seasonal.nc"
plotres['ALBEDO']['obs_vname']="sal"
plotres['ALBEDO']['eri_name']=None
plotres['ALBEDO']['eri_vname']=None
plotres['ALBEDO']['sim_name']="ALBEDO" #"  #seasonal.bin" 
plotres['ALBEDO']['sim_vname']="ALBEDO" #"  #seasonal.bin" 
plotres['ALBEDO']['unit']="$\%$"
plotres['ALBEDO']['convertcoef']=100
plotres['ALBEDO']['mask']=False
plotres['ALBEDO']['biasplot']=True
plotres['ALBEDO']['ETS']=False
plotres['ALBEDO']['Taylor']=True
plotres['ALBEDO']['violion']=False


#plotres['ASWUPT']['cleve0']=list(drange(0.2,8,0.2))  #np.linspace(1,10,num=20) #range(1,11)
plotres['ASWUPT']['cleve1']=range(80,160,10)
plotres['ASWUPT']['cleve2']=range(-30,30,5) #np.linspace(-5,5,21)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['ASWUPT']['cmp1']=plt.get_cmap('jet')
#plotres['ASWUPT']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ASWUPT']['cmp2']=cmp
plotres['ASWUPT']['obs_name']="srb_rel3.0_shortwave_seasonal.nc"
plotres['ASWUPT']['obs_vname']="sw_toa_up"
plotres['ASWUPT']['eri_name']=None
plotres['ASWUPT']['eri_vname']=None
plotres['ASWUPT']['sim_name']="ASWUPT" #"  #seasonal.bin" 
plotres['ASWUPT']['sim_vname']="ASWUPT" #"  #seasonal.bin" 
plotres['ASWUPT']['unit']="$W m^{-2}$"
#plotres['ASWUPT']['convertcoef']=*60*24
plotres['ASWUPT']['mask']=True
plotres['ASWUPT']['biasplot']=True
plotres['ASWUPT']['ETS']=False
plotres['ASWUPT']['Taylor']=True
plotres['ASWUPT']['violion']=False

plotres['ASWUPS']['cleve1']=range(0,210,10)
plotres['ASWUPS']['cleve2']=range(-30,30,5) #np.linspace(-5,5,21)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['ASWUPS']['cmp1']=plt.get_cmap('jet')
#plotres['ASWUPS']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ASWUPS']['cmp2']=cmp
plotres['ASWUPS']['obs_name']="srb_rel3.0_shortwave_seasonal.nc"
plotres['ASWUPS']['obs_vname']="sw_sfc_up"
plotres['ASWUPS']['eri_name']=None
plotres['ASWUPS']['eri_vname']=None
plotres['ASWUPS']['sim_name']="ASWUPS" #"  #seasonal.bin" 
plotres['ASWUPS']['sim_vname']="ASWUPS" #"  #seasonal.bin" 
plotres['ASWUPS']['unit']="$W m^{-2}$"
#plotres['ASWUPS']['convertcoef']=*60*24
plotres['ASWUPS']['mask']=True
plotres['ASWUPS']['biasplot']=True
plotres['ASWUPS']['ETS']=False
plotres['ASWUPS']['Taylor']=True
plotres['ASWUPS']['violion']=False

plotres['ALWDNS']['cleve1']=range(20,410,50)
plotres['ALWDNS']['cleve0']=range(20,410,10)
plotres['ALWDNS']['cleve2']=range(-65,65,5) #np.linspace(-5,5,21)
plotres['ALWDNS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWDNS']['cmp2']=cmp
plotres['ALWDNS']['obs_name']="srb_rel3.0_shortwave_seasonal.nc"
plotres['ALWDNS']['obs_vname']="sw_sfc_dn"
plotres['ALWDNS']['eri_name']=None
plotres['ALWDNS']['eri_vname']=None
plotres['ALWDNS']['sim_name']="ALWDNS" #"  #seasonal.bin" 
plotres['ALWDNS']['sim_vname']="ALWDNS" #"  #seasonal.bin" 
plotres['ALWDNS']['unit']="$W m^{-2}$"
#plotres['ALWDNS']['convertcoef']=*60*24
plotres['ALWDNS']['mask']=True
plotres['ALWDNS']['biasplot']=True
plotres['ALWDNS']['ETS']=False
plotres['ALWDNS']['Taylor']=True
plotres['ALWDNS']['violion']=False


plotres['ASWDNS']['cleve1']=range(20,410,50)
plotres['ASWDNS']['cleve0']=range(20,410,10)
plotres['ASWDNS']['cleve2']=range(-65,65,5) #np.linspace(-5,5,21)
plotres['ASWDNS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ASWDNS']['cmp2']=cmp
plotres['ASWDNS']['obs_name']="srb_rel3.0_shortwave_seasonal.nc"
plotres['ASWDNS']['obs_vname']="sw_sfc_dn"
plotres['ASWDNS']['eri_name']=None
plotres['ASWDNS']['eri_vname']=None
plotres['ASWDNS']['sim_name']="ASWDNS" #"  #seasonal.bin" 
plotres['ASWDNS']['sim_vname']="ASWDNS" #"  #seasonal.bin" 
plotres['ASWDNS']['unit']="$W m^{-2}$"
#plotres['ASWDNS']['convertcoef']=*60*24
plotres['ASWDNS']['mask']=True
plotres['ASWDNS']['biasplot']=True
plotres['ASWDNS']['ETS']=False
plotres['ASWDNS']['Taylor']=True
plotres['ASWDNS']['violion']=False

plotres['ALWUPS']['cleve1']=range(200,510,10)
plotres['ALWUPS']['cleve2']=range(-30,30,5) #np.linspace(-5,5,21)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['ALWUPS']['cmp1']=plt.get_cmap('jet')
#plotres['ALWUPS']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWUPS']['cmp2']=cmp
plotres['ALWUPS']['obs_name']="srb_rel3.1_longwave_seasonal.nc"
plotres['ALWUPS']['obs_vname']="lw_sfc_up"
plotres['ALWUPS']['eri_name']=None
plotres['ALWUPS']['eri_vname']=None
plotres['ALWUPS']['sim_name']="ALWUPS" #"  #seasonal.bin" 
plotres['ALWUPS']['sim_vname']="ALWUPS" #"  #seasonal.bin" 
plotres['ALWUPS']['unit']="$W m^{-2}$"
#plotres['ALWUPS']['convertcoef']=*60*24
plotres['ALWUPS']['mask']=True
plotres['ALWUPS']['biasplot']=True
plotres['ALWUPS']['ETS']=False
plotres['ALWUPS']['Taylor']=True
plotres['ALWUPS']['violion']=False

plotres['ALWDNS']['cleve1']=range(150,450,10)
plotres['ALWDNS']['cleve2']=range(-30,30,5) #np.linspace(-5,5,21)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['ALWDNS']['cmp1']=plt.get_cmap('jet')
#plotres['ALWDNS']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWDNS']['cmp2']=cmp
plotres['ALWDNS']['obs_name']="srb_rel3.1_longwave_seasonal.nc"
plotres['ALWDNS']['obs_vname']="lw_sfc_dn"
plotres['ALWDNS']['eri_name']=None
plotres['ALWDNS']['eri_vname']=None
plotres['ALWDNS']['sim_name']="ALWDNS" #"  #seasonal.bin" 
plotres['ALWDNS']['sim_vname']="ALWDNS" #"  #seasonal.bin" 
plotres['ALWDNS']['unit']="$W m^{-2}$"
#plotres['ALWDNS']['convertcoef']=*60*24
plotres['ALWDNS']['mask']=True
plotres['ALWDNS']['biasplot']=True
plotres['ALWDNS']['ETS']=False
plotres['ALWDNS']['Taylor']=True
plotres['ALWDNS']['violion']=False

plotres['ALWUPT']['cleve1']=range(150,360,10)
plotres['ALWUPT']['cleve2']=range(-30,30,5) #np.linspace(-5,5,21)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['ALWUPT']['cmp1']=plt.get_cmap('jet')
#plotres['ALWUPT']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWUPT']['cmp2']=cmp
plotres['ALWUPT']['obs_name']="srb_rel3.1_longwave_seasonal.nc"
plotres['ALWUPT']['obs_vname']="lw_toa_up"
plotres['ALWUPT']['eri_name']=None
plotres['ALWUPT']['eri_vname']=None
plotres['ALWUPT']['sim_name']="ALWUPT" #"  #seasonal.bin" 
plotres['ALWUPT']['sim_vname']="ALWUPT" #"  #seasonal.bin" 
plotres['ALWUPT']['unit']="$W m^{-2}$"
#plotres['ALWUPT']['convertcoef']=*60*24
plotres['ALWUPT']['mask']=True
plotres['ALWUPT']['biasplot']=True
plotres['ALWUPT']['ETS']=False
plotres['ALWUPT']['Taylor']=True
plotres['ALWUPT']['violion']=False

plotres['PrMAX']['cleve0']=range(1,35)
plotres['PrMAX']['cleve1']=range(0,51,5)
plotres['PrMAX']['cleve2']=np.linspace(-10,10,21)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['PrMAX']['cmp1']=plt.get_cmap('jet')
#plotres['PrMAX']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['PrMAX']['cmp2']=cmp
plotres['PrMAX']['obs_name']="Pr_obs_ana.nc"
plotres['PrMAX']['obs_vname']="obs_max"
plotres['PrMAX']['eri_name']="Pr_eri_ana.nc"
plotres['PrMAX']['eri_vname']="eri_max"
plotres['PrMAX']['sim_name']="PRMAX" #"  #seasonal.bin" 
plotres['PrMAX']['sim_vname']="PRMAX" #"  #seasonal.bin" 
plotres['PrMAX']['unit']="mm/day"
plotres['PrMAX']['convertcoef']=60*60*24
plotres['PrMAX']['mask']=True
plotres['PrMAX']['biasplot']=True
plotres['PrMAX']['ETS']=True
plotres['PrMAX']['Taylor']=True
plotres['PrMAX']['violion']=True


nws_precip_colors = [
    "#04e9e7",  # 0.01 - 0.10 inches
    "#019ff4",  # 0.10 - 0.25 inches
    "#0300f4",  # 0.25 - 0.50 inches
    "#02fd02",  # 0.50 - 0.75 inches
    "#01c501",  # 0.75 - 1.00 inches
    "#008e00",  # 1.00 - 1.50 inches
    "#fdf802",  # 1.50 - 2.00 inches
    "#e5bc00",  # 2.00 - 2.50 inches
    "#fd9500",  # 2.50 - 3.00 inches
    "#fd0000",  # 3.00 - 4.00 inches
    "#d40000",  # 4.00 - 5.00 inches
    "#bc0000",  # 5.00 - 6.00 inches
    "#f800fd",  # 6.00 - 8.00 inches
    "#9854c6",  # 8.00 - 10.00 inches
    "#653700",  # 8.00 - 10.00 inches
    "#fdfdfd"   # 10.00+
]
"""
cmap = [ (242, 242, 242), (191, 239, 255), (178, 223, 238), 
            (154, 192, 205), (  0, 235, 235), (  0, 163, 247), 
            (  0, 255,   0), (  0, 199,   0), (  0, 143,   0), 
            (  0,  63,   0), (255, 255,   0), (255, 143,   0),
            (255,   0,   0), (215,   0,   0), (191,   0,   0),
            (255,   0, 255), (155,  87, 203), ( 92,  52, 176) ,]
"""
import matplotlib
plotres['PRAVG']['cleve1']=[1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10,11,12,13,14,15,16,17,18]
plotres['PRAVG']['cleve1']=range(1,19)
plotres['PRAVG']['cleve1']=[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5,6,7,8,9,10,11,12,13,14]
plotres['PRAVG']['cleve2']=np.linspace(-5,5,21)
plotres['PRAVG']['cleve3']=range(10)
plotres['PRAVG']['cmp1']=cmap_cs_precp
plotres['PRAVG']['cmp2']='RdBu_r'
cmp   =plt.get_cmap('Spectral_r');cmp.set_over('maroon');cmp.set_under('w')
plotres['PRAVG']['cmp3']=cmp #plt.get_cmap('jet')
plotres['PRAVG']['obs_name']="OBS_PRAVG_seasonal.nc"
plotres['PRAVG']['obs_name_month']="OBS_PRAVG_monthly.nc"
plotres['PRAVG']['obs_vname']="obs_mean"
plotres['PRAVG']['eri_name']="ERI_PRAVG_seasonal.nc"
plotres['PRAVG']['eri_name_month']="ERI_PRAVG_monthly.nc"
plotres['PRAVG']['eri_vname']="obs_mean"
plotres['PRAVG']['cesm_name']="CESM_PRAVG_seasonal.nc"
plotres['PRAVG']['cesm_name_month']="CESM_PRAVG_monthly.nc"
plotres['PRAVG']['cesm_vname']="obs_mean"
plotres['PRAVG']['sim_name']="PRAVG" #"  #seasonal.bin" 
plotres['PRAVG']['sim_vname']="PRAVG" #"  #seasonal.bin" 
plotres['PRAVG']['unit']="mm/day"
#plotres['PRAVG']['convertcoef']=60*60*24
plotres['PRAVG']['maskland']=False
plotres['PRAVG']['maskocean']=True
plotres['PRAVG']['biasplot']=False
plotres['PRAVG']['ETS']=True
plotres['PRAVG']['Taylor']=True
plotres['PRAVG']['violion']=True

plotres['R95T']['cleve1']=[x*0.04 for x in range(0,21)] #range(0, 1,0.05)
plotres['R95T']['cleve0']=[x*0.04 for x in range(0,21)] #range(0, 1,0.05)
plotres['R95T']['cleve2']=np.linspace(-10,10,21)
plotres['R95T']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['R95T']['cmp2']=cmp
plotres['R95T']['obs_name']="pr_obs_ana.nc"
plotres['R95T']['obs_vname']="obs_pct"
plotres['R95T']['eri_name']="pr_eri_ana.nc"
plotres['R95T']['eri_vname']="eri_pct"
plotres['R95T']['sim_name']="R95T"  #seasonal.bin" 
plotres['R95T']['sim_vname']="R95T"  #seasonal.bin" 
plotres['R95T']['unit']=""
plotres['R95T']['convertcoef']=1
plotres['R95T']['maskland']=False
plotres['R95T']['maskocean']=True
plotres['R95T']['biasplot']=False
plotres['R95T']['ETS']=True
plotres['R95T']['Taylor']=True


plotres['PCT']['cleve0']=[0,2,4,6,8,10,15,20,25,30,40,50,60]
plotres['PCT']['cleve1']=[0,2,4,6,8,10,15,20,25,30,40,50,60]
plotres['PCT']['cleve1']=[2,4,6,8,10,12,14,16,18,20,25,30,35,40,45,50,55,60]
plotres['PCT']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['PCT']['cleve2']=np.linspace(-10,10,21)
plotres['PCT']['cmp1']=cmap_cs_precp
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('w')
plotres['PCT']['cmp2']=cmp
plotres['PCT']['obs_name']="pr_obs_ana.nc"
plotres['PCT']['obs_vname']="obs_pct"
plotres['PCT']['eri_name']="pr_eri_ana.nc"
plotres['PCT']['eri_vname']="eri_pct"
plotres['PCT']['sim_name']="PCT"  #seasonal.bin" 
plotres['PCT']['sim_vname']="PCT"  #seasonal.bin" 
plotres['PCT']['unit']="mm/day"
plotres['PCT']['convertcoef']=1
plotres['PCT']['maskland']=False
plotres['PCT']['maskocean']=True
plotres['PCT']['biasplot']=False
plotres['PCT']['ETS']=True
plotres['PCT']['Taylor']=True

plotres['CDD']['cleve0']=range(2,40,2)
plotres['CDD']['cleve1']=[4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['CDD']['cleve2']=None
plotres['CDD']['cmp1']=cmap_cs_precp
plotres['CDD']['cmp2']=None
plotres['CDD']['obs_name']="Pr_obs_ana.nc"
plotres['CDD']['obs_vname']="obs_cdd"
plotres['CDD']['eri_name']="Pr_eri_ana.nc"
plotres['CDD']['eri_vname']="eri_cdd"
plotres['CDD']['sim_name']="CDD"   #seasonal.bin.cdd"
plotres['CDD']['sim_vname']="CDD"   #seasonal.bin.cdd"
plotres['CDD']['unit']="day"
plotres['CDD']['convertcoef']=1
plotres['CDD']['mask']=True
plotres['CDD']['biasplot']=False
plotres['CDD']['ETS']=True
plotres['CDD']['Taylor']=True

plotres['SDII']['cleve0']=range(1,15)
plotres['SDII']['cleve1']=range(1,20)
plotres['SDII']['cleve2']=None
plotres['SDII']['cmp1']=cmap_cs_precp
plotres['SDII']['cmp2']=None
plotres['SDII']['sim_name']="SDII"  #seasonal.bin.SDII"
plotres['SDII']['sim_vname']="SDII"  #seasonal.bin.SDII"
plotres['SDII']['unit']="mm/day"
plotres['SDII']['convertcoef']=1
plotres['SDII']['mask']=True
plotres['SDII']['biasplot']=False
plotres['SDII']['ETS']=True
plotres['SDII']['Taylor']=True

plotres['R5D']['cleve0']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['R5D']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['R5D']['cleve2']=None
plotres['R5D']['cmp1']=cmap_cs_precp
plotres['R5D']['cmp2']=None
plotres['R5D']['sim_name']="R5D"  #seasonal.bin.R5D"
plotres['R5D']['sim_vname']="R5D"  #seasonal.bin.R5D"
plotres['R5D']['unit']="mm/day"
plotres['R5D']['convertcoef']=1 # divided by 5 days
plotres['R5D']['mask']=True
plotres['R5D']['biasplot']=False
plotres['R5D']['ETS']=True
plotres['R5D']['Taylor']=True

plotres['R10']['cleve0']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['R10']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['R10']['cleve2']=None
plotres['R10']['cmp1']=cmap_cs_precp
#plotres['R10']['cmp1']=plt.get_cmap('YlGnBu')
plotres['R10']['cmp2']=None
plotres['R10']['sim_name']="R10"  #seasonal.bin.R10"
plotres['R10']['sim_vname']="R10"  #seasonal.bin.R10"
plotres['R10']['unit']="day"
plotres['R10']['convertcoef']=1
plotres['R10']['mask']=True
plotres['R10']['biasplot']=False
plotres['R10']['ETS']=True
plotres['R10']['Taylor']=True

plotres['RAINYDAYS']['cleve0']=range(5,95,5)
plotres['RAINYDAYS']['cleve1']=range(5,95,5)
plotres['RAINYDAYS']['cleve2']=None
#plotres['RAINYDAYS']['cmp1']=plt.get_cmap('jet');cmp.set_over('maroon');cmp.set_under('w')
plotres['RAINYDAYS']['cmp1']=cmap_cs_precp
plotres['RAINYDAYS']['cmp2']=None
plotres['RAINYDAYS']['sim_name']="RAINYDAYS"  #seasonal.bin.RAINYDAYS"
plotres['RAINYDAYS']['sim_vname']="RAINYDAYS"  #seasonal.bin.RAINYDAYS"
plotres['RAINYDAYS']['unit']="day"
plotres['RAINYDAYS']['convertcoef']=1
plotres['RAINYDAYS']['mask']=True
plotres['RAINYDAYS']['biasplot']=False
plotres['RAINYDAYS']['ETS']=True
plotres['RAINYDAYS']['Taylor']=True

plotres['TMAX']['cleve1']=range(-10,41)
plotres['TMAX']['cleve0']=np.linspace(-10,30,num=20) #range(1,11)
plotres['TMAX']['cleve2']=range(-6,7)
plotres['TMAX']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['TMAX']['cmp2']=cmp
plotres['TMAX']['obs_name']="Tmax_obs_ana.nc"
plotres['TMAX']['obs_vname']="obs_max"
plotres['TMAX']['eri_name']=None
plotres['TMAX']['eri_vname']=None
plotres['TMAX']['sim_name']="T2MAX"  #seasonal.bin" 
plotres['TMAX']['sim_vname']="T2MAX"  #seasonal.bin" 
plotres['TMAX']['unit']="$^\circ$C"
plotres['TMAX']['convertcoef']=1
plotres['TMAX']['mask']=True
plotres['TMAX']['valuemask']=True
plotres['TMAX']['biasplot']=True
plotres['TMAX']['shift']=-273.15
plotres['TMAX']['Taylor']=True
plotres['TMAX']['ETS']=True

plotres['TMIN']['cleve1']=range(-10,41)
plotres['TMIN']['cleve0']=np.linspace(-10,30,num=20) #range(1,11)
plotres['TMIN']['cleve2']=range(-10,11)
plotres['TMIN']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['TMIN']['cmp2']=cmp
plotres['TMIN']['obs_name']="Tmin_obs_ana.nc"
plotres['TMIN']['obs_vname']="obs_min"
plotres['TMIN']['eri_name']=None
plotres['TMIN']['eri_vname']=None
plotres['TMIN']['sim_name']="T2MIN"  #seasonal.bin" 
plotres['TMIN']['sim_vname']="T2MIN"  #seasonal.bin" 
plotres['TMIN']['unit']="$^\circ$C"
plotres['TMIN']['convertcoef']=1
plotres['TMIN']['mask']=True
plotres['TMIN']['valuemask']=True
plotres['TMIN']['biasplot']=True
plotres['TMIN']['shift']=-273.15
plotres['TMIN']['Taylor']=True
plotres['TMIN']['ETS']=True



plotres['AT2M']['cleve1']=range(-10,31,2)
plotres['AT2M']['cleve0']=range(-10,31,2) #np.linspace(-10,30,num=20) #range(1,11)
plotres['AT2M']['cleve2']=range(-6,7)
plotres['AT2M']['cleve3']=range(10)
plotres['AT2M']['cleve2'].remove(0)
plotres['AT2M']['cmp1']=plt.get_cmap('jet')
cmp   = plt.get_cmap('PuOr_r') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['AT2M']['cmp2']=cmp
plotres['AT2M']['obs_name']="OBS_AT2M_seasonal.nc"
plotres['AT2M']['obs_vname']="obs_mean"
plotres['AT2M']['obs_name_month']="OBS_AT2M_monthly.nc"
plotres['AT2M']['obs_vname']="obs_mean"
plotres['AT2M']['eri_name']="ERI_AT2M_seasonal.nc"
plotres['AT2M']['eri_vname']="obs_mean"
plotres['AT2M']['cesm_name']="CESM_AT2M_seasonal.nc"
plotres['AT2M']['cesm_vname']="obs_mean"
plotres['AT2M']['eri_name_month']="ERI_AT2M_monthly.nc"
plotres['AT2M']['sim_name']="AT2M"  #seasonal.bin" 
plotres['AT2M']['sim_vname']="AT2M"  #seasonal.bin" 
plotres['AT2M']['unit']="$^\circ$C"
plotres['AT2M']['convertcoef']=1
plotres['AT2M']['maskland']=False
plotres['AT2M']['maskocean']=True
plotres['AT2M']['valuemask']=True
plotres['AT2M']['biasplot']=True
plotres['AT2M']['shift']=-273.15
plotres['AT2M']['Taylor']=True
plotres['AT2M']['ETS']=True

########################## FINISH SET parameters#####################
########################## constant value for US##############
#REG_WIN  = [[ 20,  85,  36, 121]     
REG_WIN  ={}
REG_NAME = {}
REG_WIN["US"]  = [
           [ 16,  85,  36, 121]     
       ,   [ 42,  89,  62, 117]  
       ,   [ 51,  16,  70,  70]
       ,   [139,  80, 166, 116]  
       ,   [ 74,  55,  91,  90]  
       ,   [104,  66, 133,  93]  
       ,   [134,  28, 155,  69]  
       ,   [ 94,  39, 128,  63]  
       ]
REG_NAME['US'] = [
            "Cascade", 
            "North Rockies", 
            "NAM",
            "Northeast", 
            "Central Great Plain",  
            "Midwest", 
            "Southeast", 
            "Coast States"
            ] 
REG_NAME['CN'] = [
             "Xinjiang", "Northwest", "Sichuan", "Southwest", 
            "Northeast", "North",    "Yangtze", "Southeast", 
            "EastTibet", "WestTibet"] 
REG_WIN["CN"]  = [
           [ 22, 123,  81 , 141]  
       ,   [ 90,  83, 115 , 106]  
       ,   [ 90,  64,  115,  82]  
       ,   [ 72,  37,  115,  60]  
       ,   [145, 104,  168, 153]  
       ,   [116,  85,  147, 103]  
       ,   [116,  52,  157,  84]  
       ,   [116,  20,  156,  51]   
       ,   [ 55,  64,   89,  94]  
       ,   [ 24,  64,   54,  94] 
       ]

from collections import OrderedDict
DOMAIN_reg={}
DOMAIN_reg['US'] = OrderedDict(zip(REG_NAME['US'], REG_WIN['US']))
DOMAIN_reg['CN'] = OrderedDict(zip(REG_NAME['CN'], REG_WIN['CN']))
#US_reg = dict(zip(REG_NAME, REG_WIN))
