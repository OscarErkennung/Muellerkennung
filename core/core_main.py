#!/bin/python
import signal
from http.client import REQUEST_URI_TOO_LONG
import os
import json
import time
import threading
import core.interface
import core.logger
import core.robot_control
import core.sound
import core.screen

TRASH_CONSUMPTION_TIMEOUT = 10

autonomous_mode_enabled = False

stop_flag = threading.Event()
trash_count = 0
last_lightbar_callback = 0
last_trash = 0

def stop_signal_handler(sig, frame):
    if os.environ.get("RUN_MAIN") == "true":
        print("Stopping CORE")
    global stop_flag
    core.sound.play_sound_safecast("STOP")
    stop_flag.set()
    exit()


signal.signal(signal.SIGINT, stop_signal_handler)


class RobotStatus:
    status = {}

    def __init__(self):
        self._trash_detected = False
        self._distance = -1
        self._battery_level = 100
        self._is_autonomous = False
        self._message = ""
        self._trash_found_count = 0
        self._trash_consumed_count = 0
        self._lock = threading.Lock()
        self.lock = threading.Lock()  # Lock for thread-safe access to status

    def set_trash_detected(self, value):
        with self._lock:
            self._trash_detected = value

    def get_trash_detected(self):
        return self._trash_detected

    def set_battery_level(self, value):
        with self._lock:
            self._battery_level = value

    def get_battery_level(self):
        return self._battery_level

    def set_distance(self, value):
        with self._lock:
            self._distance = value

    def get_distance(self):
        return self._distance

    def set_is_autonomous(self, value):
        with self._lock:
            self._is_autonomous = value
        if not self._is_autonomous:
            core.sound.play_sound_safecast("ERROR")

    def get_is_autonomous(self):
        return self._is_autonomous

    def set_message(self, value):
        with self._lock:
            self._message = value

    def get_message(self):
        return self._message

    def _set_trash_found_count(self, value):
        with self._lock:
            self._trash_found_count = value

    def get_trash_found_count(self):
        return self._trash_found_count

    def get_trash_consumed_count(self):
        return self._trash_consumed_count

    def handle_trash_found(self, label: str):

        def clear_trash_detected():
            """ Helper method to clear trash detected after 10 seconds """
            thrash_consumed = self._trash_consumed_count
            time.sleep(TRASH_CONSUMPTION_TIMEOUT)

            with self._lock:
                if self._trash_detected and self._trash_consumed_count == thrash_consumed:
                    self._trash_detected = False
            core.screen.set_image("face")

        with self.lock:
            self._trash_found_count += 1
            self._message = f"Trash #{self._trash_found_count} detected"
            self._trash_detected = True
        core.screen.set_image(label)
        threading.Thread(target=clear_trash_detected).start()
        global last_trash
        if time.time() - last_trash > 5:
            core.sound.play_sound_safecast("help_me")
        last_trash = time.time()

    def handle_trash_thrown(self):
        with self.lock:
            self._message = f"Trash #{self._trash_consumed_count} has been consumed"
            self._trash_consumed_count += 1
            self._trash_detected = False
        core.screen.set_image("face")

    def to_json(self):
        status = {
            "trash_detected": self._trash_detected,
            "distance": self._distance,
            "battery_level": self._battery_level,
            "is_autonomous": self._is_autonomous,
            "message": self._message,
            "trash_found_count": self._trash_found_count,
            "trash_consumed_count": self._trash_consumed_count
        }
        return json.dumps(status)

our_status = RobotStatus()


def get_system_status():
    """
    Returns the current system status as a dictionary.
    """
    global our_status
    return our_status


def app_main():
    """
    executed after djangos ready hook is triggered. should not block too long.
    """
    # perform startup sequences.
    core.sound.play_sound_safecast("START")
    # start subthreads....
    core.screen.set_image("face")
    # start subthread....
    worker_thread = threading.Thread(target=app_worker)
    worker_thread.daemon = True
    worker_thread.start()

    sensor_thread = threading.Thread(target=sensor_worker)
    sensor_thread.daemon = True
    sensor_thread.start()

    # TODO start subthread for camera
    from core.webcam import camera_worker
    camera_thread = threading.Thread(target=camera_worker, args={})
    camera_thread.daemon = True
    camera_thread.start()

    # amd set callback for beam:
    # camera_thread.start()



def lightbar_callback(shared_status: RobotStatus, channel): 
    global last_lightbar_callback
    if time.time()-last_lightbar_callback <  TRASH_CONSUMPTION_TIMEOUT:
        print("ignoring recent callback.")
        return
    print("interrupt from lightbar detected.")
    last_lightbar_callback = time.time()
    core.sound.play_sound_safecast("thanks") #thank user when throwing something in
    shared_status.handle_trash_thrown()


def app_worker():
    # since some of the movement functions include blocking features,
    # they should be called from this seperate thread.
    core.robot_control.gpio_setup()
    time.sleep(2)  # Wait for GPIO setup to complete
    core.robot_control.set_lightbar_callback(lightbar_callback, our_status)  # Set the callback for the lightbar
    
    print("Worker thread started.")
    while not stop_flag.is_set():
        print(f"App worker heartbeat <3 {our_status.get_is_autonomous()}")
        while our_status.get_is_autonomous() and not our_status.get_trash_detected():  # TODO: should be a view
            # drive autonomously.
            core.robot_control.move_autonomous()
        else:
            # do nothing.
            time.sleep(1)  # sleep to avoid busy waiting
    print("Worker thread stopping.")
    worker_cleanup()
    return


def sensor_worker():
    """
    This worker thread is responsible for reading sensors and updating the shared status.
    """
    while not stop_flag.is_set():
        # Read sensors and update shared_status
        distance = core.robot_control.get_ultrasound_distance(round2n=True)

        # Update the shared status with the new distance
        our_status.set_distance(distance)
        # Sleep for a short duration to avoid busy waiting
        time.sleep(1)  # Adjust the sleep duration as needed


def worker_cleanup():
    core.robot_control.cleanup()
    core.logger.log("Worker thread cleaned up and stopped.", lvl=20)
    core.sound.play_sound_safecast("STOP")
    pass
