#!/usr/bin/env python
import ConfigParser 
def readini():
  config = ConfigParser.ConfigParser()
  config.read('plot.ini')
  cases=config.get('MAIN','cases')
  cases=[x.strip() for x in cases.split(',')]
  vnames=config.get('MAIN','vnames')
  vnames=[x.strip() for x in vnames.split(',')]
  try:
    shapefile=config.get('MAIN','shapefile')
    shapefile=[x.strip() for x in shapefile.split(',')]
  except:
    shapefile=None
  CTL_name=config.get('MAIN','CTL_name')
  period=config.get('MAIN','period')
  datapath=config.get('MAIN','datapath')
  nlevel=int(config.get('MAIN','nlevel'))
  cutpoints=[int(x) for x in config.get('MAIN','cutpoints').split(',')]
  neof    =int(config.get('MAIN','neof'))
  masktype=int(config.get('MAIN','masktype'))
  method=config.get('MAIN','method')
  plottype=config.get('MAIN','plottype')
  obsname=config.get('MAIN','obsname')
  GCM_name=config.get('MAIN','GCM_name')
  regmapfile=config.get('MAIN','regmapfile')
  Hovmoller={}
  section="Hovmoller"
  for option in config.options(section):
    Hovmoller[option]=config.getfloat(section, option)
  section="PDF"
  PDF={}
  for option in config.options(section):
    PDF[option]=config.getint(section, option)

  section="PLOT"
  PLOT={}
  for option in config.options(section):
    PLOT[option]=config.get(section,option)
    PLOT[option]=[float(x.strip()) for x in PLOT[option].split(',')]

  Time_control={}
  section="Time_control"
  for option in config.options(section):
    Time_control[option]=config.getint(section, option)
  return (period,vnames,cases,nlevel,datapath,cutpoints,neof,masktype,method,plottype,shapefile,obsname,GCM_name,Hovmoller,Time_control,PDF,PLOT,regmapfile)
