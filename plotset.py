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
haxby= [ (37,57,175) ,
(37,68,187) ,
(38,79,199) ,
(38,90,211) ,
(39,101,223) ,
(39,113,235) ,
(40,124,247) ,
(41,134,251) ,
(43,144,252) ,
(44,154,253) ,
(46,164,253) ,
(47,174,254) ,
(49,184,255) ,
(54,193,255) ,
(62,200,255) ,
(71,207,255) ,
(80,214,255) ,
(89,221,255) ,
(98,229,255) ,
(107,235,254) ,
(112,235,241) ,
(117,235,228) ,
(122,235,215) ,
(127,236,202) ,
(132,236,189) ,
(137,236,177) ,
(147,238,172) ,
(157,241,171) ,
(168,244,169) ,
(178,247,167) ,
(189,250,165) ,
(200,253,163) ,
(208,253,159) ,
(213,250,152) ,
(219,247,146) ,
(224,244,139) ,
(230,241,133) ,
(236,238,126) ,
(240,235,120) ,
(243,227,115) ,
(245,220,109) ,
(248,212,104) ,
(250,205,98) ,
(252,197,93) ,
(255,190,88) ,
(255,185,84) ,
(255,181,81) ,
(255,176,78) ,
(255,172,75) ,
(255,167,72) ,
(255,163,69) ,
(255,163,74) ,
(255,167,85) ,
(255,171,95) ,
(255,175,105) ,
(255,179,115) ,
(255,183,126) ,
(255,189,139) ,
(255,200,158) ,
(255,211,178) ,
(255,222,197) ,
(255,233,216) ,
(255,244,236) ,
(255,255,255) ] 

BWR=[ ( 36    ,   0 ,    216), 
(   24    ,  28 ,    247), 
(   40    ,  87 ,    255), 
(   61    , 135 ,    255), 
(   86    , 176 ,    255), 
(  117    , 211 ,    255), 
(  153    , 234 ,    255), 
(  188    , 249 ,    255), 
(  234    , 255 ,    255), 
(  255    , 255 ,    255), 
(  255    , 241 ,    188), 
(  255    , 214 ,    153), 
(  255    , 172 ,    117), 
(  255    , 120 ,     86), 
#(  255    ,  61 ,     61), 
(  247    ,  39 ,     53), 
(  165    ,   0 ,     33)]
"""
(  216    ,  21 ,     47), 
(  165    ,   0 ,     33)]
"""
BWR=[ #( 0    ,   0 ,    0), 
(   16    ,  78 ,    139), 
(   23    ,  116 ,    205), 
#(   24    ,  28 ,    247), 
#(   40    ,  87 ,    255), 
(   61    , 135 ,    255), 
(   86    , 176 ,    255), 
(  117    , 211 ,    255), 
(  153    , 234 ,    255), 
(  188    , 249 ,    255), 
(  234    , 255 ,    255), 
(  255    , 255 ,    255), 
(  255    , 241 ,    188), 
(  255    , 214 ,    153), 
(  255    , 172 ,    117), 
(  255    , 120 ,     86), 
(  255    ,  61 ,     61), 
(  247    ,  39 ,     53)] 



tableau20 = [(31, 119, 180), (174, 199, 232), (255, 127, 14), (255, 187, 120),    
             (44, 160, 44), (152, 223, 138), (214, 39, 40), (255, 152, 150),    
             (148, 103, 189), (197, 176, 213), (140, 86, 75), (196, 156, 148),    
             (227, 119, 194), (247, 182, 210), (127, 127, 127), (199, 199, 199),    
             (188, 189, 34), (219, 219, 141), (23, 190, 207), (158, 218, 229)]    
 
def buildcmp(cmaplist):
  for i in range(len(cmaplist)):    
      r, g, b = cmaplist[i]    
      cmaplist[i] = (r / 255., g / 255., b / 255.) 
  return LinearSegmentedColormap.from_list( "precip", cmaplist,N=len(cmaplist)),cmaplist
cmap_cs_precp,cs_precp_list=buildcmp(cmap_cs_precp)
cmap_haxby,haxby_list=buildcmp(haxby[::5])
cmap_BWR,BWR_list=buildcmp(BWR)
cmap_BWR.set_over('maroon')
cmap_BWR.set_under('blue')
cmap_cs_precp.set_over('purple')
cmap_tableau20,tableau20=buildcmp(tableau20)
sim_nicename={"ERI":"ERI",
             "RegCM":"RegCM4.6",
             "PRAVG":"PR",
             "AT2M97":"A97",
             "SDII":"DI",
             "CN_OBS":"OBS",
             "RAINYDAYS":"RD",
             "run_RegCM4.6":"RegCM\n4.6",
             "run_RegCM4.5":"RegCM\n4.5",
             "ERI_run_0":"old CWRF",
             "new_ERI_run_0":"CWRF\nMor",
             "new_ERI_gsfc":"CWRF",
             "new_ERI_albedo":"CWRF",
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
#plotres['XRSUR']['cleve1']=[x*1e-6 for x in range(31)]
plotres['XRSUR']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['XRSUR']['cmp2']=cmp
#plotres['XRSUR']['convertcoef']=0.001
plotres['XRSUR']['unit']="kg/m2/day"
plotres['XRSUR']['mask']=True
plotres['XRSUR']['violion']=False

#plotres['XRBAS']['cleve1']=[x*1e-6 for x in range(31)]
plotres['XRBAS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['XRBAS']['cmp2']=cmp
plotres['XRBAS']['unit']="kg/m2/day"
plotres['XRBAS']['mask']=True
plotres['XRBAS']['violion']=False


#plotres['SFROFF']['cleve1']=[x*10000 for x in range(31)]
plotres['SFROFF']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['SFROFF']['cmp2']=cmp
#plotres['SFROFF']['convertcoef']=0.001
plotres['SFROFF']['unit']="kg/m2"
plotres['SFROFF']['mask']=True
plotres['SFROFF']['violion']=False



#plotres['XSMTg']['cleve1']=[x*20 for x in range(1,20)] #range(0, 1,0.05)
plotres['XSMTg']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['XSMTg']['cmp2']=cmp
plotres['XSMTg']['unit']="kg/m2"
plotres['XSMTg']['mask']=True
plotres['XSMTg']['violion']=False
plotres['XSMTg']['vlevel']=4

#plotres['AODNIR']['cleve0']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
#plotres['AODNIR']['cleve1']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
plotres['AODNIR']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['AODNIR']['cmp2']=cmp
#plotres['AODNIR']['convertcoef']=0.01
plotres['AODNIR']['unit']=""
plotres['AODNIR']['mask']=True


#plotres['AODVIS']['cleve0']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
#plotres['AODVIS']['cleve1']=[x*0.05 for x in range(0,11)] #range(0, 1,0.05)
plotres['AODVIS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['AODVIS']['cmp2']=cmp
#plotres['AODVIS']['convertcoef']=0.01
plotres['AODVIS']['unit']=""
plotres['AODVIS']['mask']=True


#plotres['CLDFRAh']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRAh']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRAh']['cmp2']=cmp
#plotres['CLDFRAh']['convertcoef']=0.01
plotres['CLDFRAh']['unit']=""
plotres['CLDFRAh']['mask']=True
plotres['CLDFRAh']['violion']=False
plotres['CLDFRAh']['vlevel']=3



#plotres['CLDFRAm']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRAm']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRAm']['cmp2']=cmp
#plotres['CLDFRAm']['convertcoef']=0.01
plotres['CLDFRAm']['unit']=""
plotres['CLDFRAm']['mask']=True
plotres['CLDFRAm']['violion']=False
plotres['CLDFRAm']['vlevel']=2




#plotres['CLDFRAl']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRAl']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRAl']['cmp2']=cmp
#plotres['CLDFRAl']['convertcoef']=0.01
plotres['CLDFRAl']['unit']=""
plotres['CLDFRAl']['mask']=True
plotres['CLDFRAl']['violion']=False
plotres['CLDFRAl']['vlevel']=1


#plotres['CLDFRA']['cleve1']=[x*0.05 for x in range(0,21)] #range(0, 1,0.05)
plotres['CLDFRA']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['CLDFRA']['cmp2']=cmp
#plotres['CLDFRA']['convertcoef']=0.01
plotres['CLDFRA']['unit']=""
plotres['CLDFRA']['mask']=True
plotres['CLDFRA']['violion']=False
plotres['CLDFRA']['vlevel']=0



#plotres['QVAPOR']['cleve1']=range(0, 20,1)
plotres['QVAPOR']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['QVAPOR']['cmp2']=cmp
plotres['QVAPOR']['convertcoef']=1000
plotres['QVAPOR']['unit']="$g/kg$"
plotres['QVAPOR']['mask']=False
plotres['QVAPOR']['violion']=False
plotres['QVAPOR']['vlevel']=21



#plotres['TCWPC']['cleve1']=range(0, 200,10)
plotres['TCWPC']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['TCWPC']['cmp2']=cmp
plotres['TCWPC']['unit']="$g/m^{2}$"
plotres['TCWPC']['mask']=True
plotres['TCWPC']['violion']=False



#plotres['V']['cleve1']=range(-10, 10,1)
plotres['V']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['V']['cmp2']=cmp
plotres['V']['unit']="$m/s$"
plotres['V']['mask']=False
plotres['V']['violion']=False
plotres['V']['vlevel']=21


#plotres['U']['cleve1']=range(-10, 10,1)
plotres['U']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['U']['cmp2']=cmp
plotres['U']['unit']="$m/s$"
plotres['U']['mask']=False
plotres['U']['violion']=False
plotres['U']['vlevel']=21


#plotres['PSL']['cleve1']=range(1000, 1024,1)
plotres['PSL']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['PSL']['cmp2']=cmp
plotres['PSL']['unit']="$\%$"
plotres['PSL']['convertcoef']=0.01
plotres['PSL']['mask']=False
plotres['PSL']['violion']=False

#plotres['PS']['cleve1']=range(700, 1030,5)
plotres['PS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['PS']['cmp2']=cmp
plotres['PS']['unit']="$\%$"
plotres['PS']['convertcoef']=0.01
plotres['PS']['mask']=False
plotres['PS']['violion']=False


#plotres['ALBEDO']['cleve1']=range(0, 60,5)
plotres['ALBEDO']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALBEDO']['cmp2']=cmp
plotres['ALBEDO']['unit']="$\%$"
plotres['ALBEDO']['convertcoef']=100
plotres['ALBEDO']['mask']=False
plotres['ALBEDO']['violion']=False


#plotres['ASWUPT']['cleve1']=range(80,160,10)
plotres['ASWUPT']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ASWUPT']['cmp2']=cmp
plotres['ASWUPT']['unit']="$W m^{-2}$"
plotres['ASWUPT']['mask']=True
plotres['ASWUPT']['violion']=False

#plotres['ASWUPS']['cleve1']=range(0,210,10)
plotres['ASWUPS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ASWUPS']['cmp2']=cmp
plotres['ASWUPS']['unit']="$W m^{-2}$"
plotres['ASWUPS']['mask']=True
plotres['ASWUPS']['violion']=False

#plotres['ALWDNS']['cleve1']=range(20,410,50)
#plotres['ALWDNS']['cleve0']=range(20,410,10)
plotres['ALWDNS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWDNS']['cmp2']=cmp
plotres['ALWDNS']['unit']="$W m^{-2}$"
plotres['ALWDNS']['mask']=True
plotres['ALWDNS']['violion']=False


#plotres['ASWDNS']['cleve1']=range(20,410,50)
#plotres['ASWDNS']['cleve0']=range(20,410,10)
plotres['ASWDNS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ASWDNS']['cmp2']=cmp
plotres['ASWDNS']['unit']="$W m^{-2}$"
plotres['ASWDNS']['mask']=True
plotres['ASWDNS']['violion']=False

#plotres['ALWUPS']['cleve1']=range(200,510,10)
plotres['ALWUPS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWUPS']['cmp2']=cmp
plotres['ALWUPS']['unit']="$W m^{-2}$"
plotres['ALWUPS']['mask']=True
plotres['ALWUPS']['violion']=False

#plotres['ALWDNS']['cleve1']=range(150,450,10)
plotres['ALWDNS']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWDNS']['cmp2']=cmp
plotres['ALWDNS']['unit']="$W m^{-2}$"
plotres['ALWDNS']['mask']=True
plotres['ALWDNS']['violion']=False

#plotres['ALWUPT']['cleve1']=range(150,360,10)
plotres['ALWUPT']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['ALWUPT']['cmp2']=cmp
plotres['ALWUPT']['unit']="$W m^{-2}$"
plotres['ALWUPT']['mask']=True
plotres['ALWUPT']['violion']=False

#plotres['PrMAX']['cleve0']=range(1,35)
#plotres['PrMAX']['cleve1']=range(0,51,5)
#  import colormaps as cmaps
#  cmp=cmap=cmaps.viridis
plotres['PrMAX']['cmp1']=plt.get_cmap('jet')
#plotres['PrMAX']['cmp1']=cm.s3pcpn
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['PrMAX']['cmp2']=cmp
plotres['PrMAX']['unit']="mm/day"
plotres['PrMAX']['convertcoef']=60*60*24
plotres['PrMAX']['mask']=True
plotres['PrMAX']['violion']=True



#plotres['PRAVG']['cleve1']=[0.5,1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5,6,7,8,9,10,11,12,13,14]
#plotres['PRAVG']['cleve3']=range(10)
plotres['PRAVG']['cmp1']=cmap_cs_precp
plotres['PRAVG']['cmp2']='RdBu_r'
cmp   =plt.get_cmap('Spectral_r');cmp.set_over('maroon');cmp.set_under('w')
plotres['PRAVG']['cmp3']=cmap_haxby #plt.get_cmap('jet')
plotres['PRAVG']['unit']="mm/day"
plotres['PRAVG']['violion']=True

#plotres['R95T']['cleve1']=[x*0.04 for x in range(0,21)] #range(0, 1,0.05)
#plotres['R95T']['cleve0']=[x*0.04 for x in range(0,21)] #range(0, 1,0.05)
plotres['R95T']['cmp1']=plt.get_cmap('jet')
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['R95T']['cmp2']=cmp
plotres['R95T']['unit']=""
plotres['R95T']['convertcoef']=1


#plotres['PCT']['cleve0']=[0,2,4,6,8,10,15,20,25,30,40,50,60]
#plotres['PCT']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['PCT']['cmp1']=cmap_cs_precp
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('w')
plotres['PCT']['cmp2']=cmp
plotres['PCT']['unit']="mm/day"
plotres['PCT']['convertcoef']=1

#plotres['PCT99']['cleve0']=[0,2,4,6,8,10,15,20,25,30,40,50,60]
#plotres['PCT99']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['PCT99']['cmp1']=cmap_cs_precp
cmp   =plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('w')
plotres['PCT99']['cmp2']=cmp
plotres['PCT99']['unit']="mm/day"
plotres['PCT99']['convertcoef']=1


#plotres['CDD']['cleve0']=[-20,-18,-16,-14,-10,-8,-6,-4,-2,2,4,6,8,10,12,14,16,18,20,22]
#plotres['CDD']['cleve1']=[4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['CDD']['cmp1']=cmap_cs_precp
plotres['CDD']['cmp2']=None
plotres['CDD']['unit']="day"
plotres['CDD']['convertcoef']=1
plotres['CDD']['mask']=True

#plotres['SDII']['cleve0']=range(1,15)
#plotres['SDII']['cleve1']=range(1,20)
plotres['SDII']['cmp1']=cmap_cs_precp
plotres['SDII']['cmp2']=None
plotres['SDII']['unit']="mm/day"
plotres['SDII']['convertcoef']=1
plotres['SDII']['mask']=True

#plotres['R5D']['cleve0']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
#plotres['R5D']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['R5D']['cmp1']=cmap_cs_precp
plotres['R5D']['cmp2']=None
plotres['R5D']['unit']="mm/day"
plotres['R5D']['convertcoef']=1 # divided by 5 days
plotres['R5D']['mask']=True

#plotres['R10']['cleve0']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
#plotres['R10']['cleve1']=[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,35,40,45,50]
plotres['R10']['cmp1']=cmap_cs_precp
plotres['R10']['cmp2']=None
plotres['R10']['unit']="day"
plotres['R10']['convertcoef']=1
plotres['R10']['mask']=True

#plotres['RAINYDAYS']['cleve0']=range(5,95,5)
#plotres['RAINYDAYS']['cleve1']=range(5,95,5)
plotres['RAINYDAYS']['cmp1']=cmap_cs_precp
plotres['RAINYDAYS']['cmp2']=None
plotres['RAINYDAYS']['unit']="day"
plotres['RAINYDAYS']['convertcoef']=1
plotres['RAINYDAYS']['mask']=True

#plotres['T2MAX']['cleve1']=range(-10,41)
#plotres['T2MAX']['cleve0']=[-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]
plotres['T2MAX']['cmp1']=plt.get_cmap('jet')
cmp   =cmap_BWR
plotres['T2MAX']['cmp2']=cmp
plotres['T2MAX']['unit']="$^\circ$C"
plotres['T2MAX']['convertcoef']=1
plotres['T2MAX']['mask']=True
plotres['T2MAX']['valuemask']=True
plotres['T2MAX']['shift']=-273.15

#plotres['T2MIN']['cleve1']=range(-10,41)
#plotres['T2MIN']['cleve0']=[-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]
plotres['T2MIN']['cmp1']=plt.get_cmap('jet')
cmp   =cmap_BWR
plotres['T2MIN']['cmp2']=cmp
plotres['T2MIN']['unit']="$^\circ$C"
plotres['T2MIN']['convertcoef']=1
plotres['T2MIN']['mask']=True
plotres['T2MIN']['valuemask']=True
plotres['T2MIN']['shift']=-273.15


#plotres['AT2M']['cleve0']=[-9,-8,-7,-6,-5,-4,-3,-2,-1,1,2,3,4,5,6,7]
#plotres['AT2M']['cleve1']=range(-10,31,2)
#plotres['AT2M']['cleve3']=range(10)
plotres['AT2M']['cmp1']=plt.get_cmap('jet')
cmp   =cmap_BWR
plotres['AT2M']['cmp2']=cmp
plotres['AT2M']['unit']="$^\circ$C"
plotres['AT2M']['convertcoef']=1
plotres['AT2M']['valuemask']=True
plotres['AT2M']['shift']=-273.15

#plotres['AT2M97']['cleve0']=[-10, -9, -8, -7, -6, -5, -4, -3, -2, -1,  1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#plotres['AT2M97']['cleve1']=range(-15,35,2)
#plotres['AT2M97']['cleve3']=range(10)
plotres['AT2M97']['cmp1']=plt.get_cmap('gist_rainbow_r')
cmp   = plt.get_cmap('PuOr_r') #plt.get_cmap('seismic');cmp.set_over('maroon');cmp.set_under('b')
plotres['AT2M97']['cmp2']=cmp
plotres['AT2M97']['unit']="$^\circ$C"
plotres['AT2M97']['convertcoef']=1
plotres['AT2M97']['valuemask']=True
plotres['AT2M97']['shift']=-273.15

plotres['DTR']['cmp1']=cmap_cs_precp
cmp   =cmap_BWR
plotres['DTR']['cmp2']=cmp
plotres['DTR']['unit']="$^\circ$C"
plotres['DTR']['convertcoef']=1
plotres['DTR']['valuemask']=True

plotres['RH']['cmp1']=plt.get_cmap('viridis_r')
cmp   =cmap_BWR
plotres['RH']['cmp2']=cmp
plotres['RH']['unit']="$\%$"
plotres['RH']['convertcoef']=1
plotres['RH']['valuemask']=True

plotres['WIN']['cmp1']=cmap_haxby
cmp   =cmap_BWR
plotres['WIN']['cmp2']=cmp
plotres['WIN']['unit']="$m/s$"
plotres['WIN']['convertcoef']=1
plotres['WIN']['valuemask']=True

plotres['GUST']['cmp1']=cmap_haxby
cmp   =cmap_BWR
plotres['GUST']['cmp2']=cmp
plotres['GUST']['unit']="$m/s$"
plotres['GUST']['convertcoef']=1
plotres['GUST']['valuemask']=True
