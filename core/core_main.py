#!/bin/python
from http.client import REQUEST_URI_TOO_LONG
import os, threading, core.interface, core.logger, core.robot_control, core.sound

autonomous_mode_enabled = False
stop_flag = threading.Event()
trash_count = 0


def get_system_status():
   # Hier könnt ihr Sensoren lesen – als Platzhalter:
   return {
       'trash_detected': 0,
       'distance': core.robot_control.get_ultrasound_distance(round2n=True),  # Beispielwert
       'battery_level': 76,  # Beispielwert
       'is_autonomous': 0,
       'message': "", 
        'total': 1000, 
   }


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


def lightbar_callback(): 
    core.play_sound_safecast("thanks") #thank user when throwing something in
    global trash_count
    trash_count +=1


def app_worker():
    #since some of the movement functions include blocking features, 
    #they should be called from this seperate thread. 
    core.robot_control.setup_gpio()
    core.robot_control.set_lightbar_callback(lightbar_callback)
    print("Worker thread started.") 
    while not stop_flag.is_set(): 
        while autonomous_mode_enabled:
            #drive autonomously.
            core.robot_control.move_autonomous()
        else:
            #do nothing. 
            pass
    print("Worker thread stopping.")
    worker_cleanup()
    return

def worker_cleanup():
    core.robot_control.cleanup() 
    core.logger.log("Worker thread cleaned up and stopped.", lvl=20)
    core.sound.play_sound_safecast("STOP")
    pass