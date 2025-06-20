#!/bin/python
from http.client import REQUEST_URI_TOO_LONG
import os, threading, core.interface, core.logger, core.robot_control, core.sound

autonomous_mode_enabled = False
stop_flag = threading.Event()
trash_count = 0

def app_main(): 
    """
    executed after djangos ready hook is triggered. should not block too long.
    """
    #perform startup sequences.
    core.sound.play_sound_safecast("START")
    # start subthread....
    worker_thread = threading.Thread(target=app_worker, args={})
    worker_thread.daemon = True
    worker_thread.start
    # TODO start subthread for camera
    #camera_thread = threading.Thread(target=camera_worker, args={})
    #camera_thread.daemon = True
    #camera_thread.start
    
    #amd set callback for beam: 

    core.robot_control.set_lightbar_callback(lightbar_callback)

def lightbar_callback(): 
    core.play_sound_safecast("thanks") #thank user when throwing something in
    global trash_count
    trash_count +=1


def app_worker():
    #since some of the movement functions include blocking features, 
    #they should be called from this seperate thread. 
    
    while not stop_flag.is_set(): 
        while autonomous_mode_enabled:
            #drive autonomously.
            core.robot_control.move_autonomous()
        else:
            #do nothing. 
            pass
    worker_cleanup()
    return

def worker_cleanup(): 
    pass