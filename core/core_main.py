#!/bin/python
from http.client import REQUEST_URI_TOO_LONG
import os, time, threading, core.interface, core.logger, core.robot_control, core.sound

autonomous_mode_enabled = False
stop_flag = threading.Event()
trash_count = 0


class RobotStatus:
    status = {}  
    def __init__(self):
        self.status['trash_detected'] = 0
        self.status['distance'] = 0
        self.status['battery_level'] = 100  # Beispielwert
        self.status['is_autonomous'] = False
        self.status['message'] = ""
        self.status['total'] = 1000  # Beispielwert
        self.lock = threading.Lock()  # Lock for thread-safe access to status
    def update_status(self, new_status): 
        with self.lock:
            self.status.update(new_status)
    
    def getstate(self):
        with self.lock:
            return self.status.copy()
    def increase_trash_count(self):
        with self.lock:
            self.status['trash_detected'] += 1
            self.status['message'] = f"Trash detected: {self.status['trash_detected']} items"


our_status = RobotStatus()

def get_system_status():
    """
    Returns the current system status as a dictionary.
    """
    return our_status.getstate()

def app_main(): 
    """
    executed after djangos ready hook is triggered. should not block too long.
    """
    #perform startup sequences.
    core.sound.play_sound_safecast("START")
    # start subthread....
    worker_thread = threading.Thread(target=app_worker, args={our_status})
    worker_thread.daemon = True
    worker_thread.start()
    # TODO start subthread for camera
    #camera_thread = threading.Thread(target=camera_worker, args={})
    #camera_thread.daemon = True
    #camera_thread.start
    
    #amd set callback for beam: 


def lightbar_callback(shared_status: RobotStatus): 
    core.play_sound_safecast("thanks") #thank user when throwing something in
    shared_status.increase_trash_count()


def app_worker(shared_status: RobotStatus):
    #since some of the movement functions include blocking features, 
    #they should be called from this seperate thread. 
    core.robot_control.gpio_setup()
    core.robot_control.set_lightbar_callback(lightbar_callback)  # Set the callback for the lightbar
    print("Worker thread started.") 
    while not stop_flag.is_set(): 
        while shared_status.getstate()['is_autonomous']: #TODO should be a view.
            #drive autonomously.
            core.robot_control.move_autonomous()
        else:
            #do nothing. 
            time.sleep(1) #sleep to avoid busy waiting
    print("Worker thread stopping.")
    worker_cleanup()
    return

def sensor_worker(shared_status: RobotStatus, stop_flag: threading.Event):
    """
    This worker thread is responsible for reading sensors and updating the shared status.
    """
    while not stop_flag.is_set():
        # Read sensors and update shared_status
        distance = core.robot_control.get_ultrasound_distance(round2n=True)
        
        # Update the shared status with the new distance
        shared_status.update_status({'distance': distance})
        # Sleep for a short duration to avoid busy waiting
        time.sleep(1)  # Adjust the sleep duration as needed


def worker_cleanup():
    core.robot_control.cleanup() 
    core.logger.log("Worker thread cleaned up and stopped.", lvl=20)
    core.sound.play_sound_safecast("STOP")
    pass