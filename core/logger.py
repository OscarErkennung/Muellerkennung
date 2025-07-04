#!/usr/bin/env python
import os
import yaml
import logging
logger = logging.getLogger(__name__)


flags=[1,1,1,1,1,1]

news = False

def load_logs():
    path =  os.getcwd()+"/general.log" # Open Django Log
    data=""
    textfile=open(path)
    for line in textfile.readlines():
        if ("DEBUG" in line and not flags[1]) or ("INFO" in line and not flags[2]) or ("ERROR" in line and not flags[3])  or ("WARNING" in line and not flags[4]) or ("CRITICAL" in line and not flags[5]):
            #Nothing happens, catches every line which is to be ignored
            pass
        elif flags[0]:
            data+=line 
    textfile.close()
    return data

def log(msg, lvl=10):
    global news
    # Evaluate Logging level, valid options are: DEBUG=10; INFO=20; WARNING=30; ERROR=40; CRITICAL=50
    if (lvl not in [10, 20, 30, 40, 50]):
        lvl=30
    
    #print("logging\t"+str(msg)+"\t as \t"+str(lvl)) 
    logger.log(lvl, msg) # parse to django Handler and Logger
    news=True
    return 0 

def clear_logs(): 
    # Delete the current log and create an empty one...
    os.system("truncate ./general.log -s 0")
    return 0
def check_new():
    global news
    if news:
        news = False
        return True
    return False