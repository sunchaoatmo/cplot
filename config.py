#!/usr/bin/env python
import ConfigParser 
def readini():
  config = ConfigParser.ConfigParser()
  config.read('plot.ini')
  cases=config.get('PLOT','cases')
  cases=[x.strip() for x in cases.split(',')]
  vnames=config.get('PLOT','vnames')
  vnames=[x.strip() for x in vnames.split(',')]
  try:
    shapefile=config.get('PLOT','shapefile')
    shapefile=[x.strip() for x in shapefile.split(',')]
  except:
    shapefile=None
  CTL_name=config.get('PLOT','CTL_name')
  period=config.get('PLOT','period')
  datapath=config.get('PLOT','datapath')
  nlevel=int(config.get('PLOT','nlevel'))
  cutpoints=int(config.get('PLOT','cutpoints'))
  neof    =int(config.get('PLOT','neof'))
  masktype=int(config.get('PLOT','masktype'))
  method=config.get('PLOT','method')
  plottype=config.get('PLOT','plottype')
  obsname=config.get('PLOT','obsname')
  GCM_name=config.get('PLOT','GCM_name')
  Hovmoller={}
  section="Hovmoller"
  for option in config.options(section):
    Hovmoller[option]=config.getfloat(section, option)
  Time_control={}
  section="Time_control"
  for option in config.options(section):
    Time_control[option]=config.getint(section, option)
  return (period,vnames,cases,nlevel,datapath,cutpoints,neof,masktype,method,plottype,shapefile,obsname,GCM_name,Hovmoller,Time_control)
