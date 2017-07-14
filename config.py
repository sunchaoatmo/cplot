#!/usr/bin/env python
import ConfigParser 
def retrivesetting(config,section,setting):
  for option in config.options(section):
    setting[option]=config.get(section, option)
    if "," in setting[option]:
      setting[option]=[x.strip() for x in setting[option].split(',')]
      if setting[option][0].lstrip("-+")[0].isdigit():
        try:
          setting[option]=[int(x.strip()) for x in setting[option]]
        except:
          setting[option]=[float(x.strip()) for x in setting[option]]
    elif setting[option].lstrip("-+")[0].isdigit():
      try:
        setting[option]=int(setting[option])
      except:
        setting[option]=float(setting[option])
    elif option.endswith('s'):
      setting[option]=[setting[option]]
    elif setting[option]=="False":
      setting[option]=False
    elif setting[option]=="True":
      setting[option]=True



def readini():
  from collections import defaultdict
  settings=defaultdict(dict)
  config = ConfigParser.ConfigParser()
  config.read('plot.ini')
  sections=["MAIN","Timeserial","EOF","Parameter","Hovmoller","PDF","PLOT","Taylor","Time_control","ETS","Regional"]
  for section in sections:
    retrivesetting(config,section,settings[section])
  return settings
