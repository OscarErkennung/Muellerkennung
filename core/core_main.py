#!/bin/python
from http.client import REQUEST_URI_TOO_LONG
import os
import threading
import core.interface
import core.logger
import core.robot_control
import core.sound
from core.webcam import camera_worker

autonomous_mode_enabled = False
stop_flag = threading.Event()
trash_count = 0


def app_main():
    """
    executed after djangos ready hook is triggered. should not block too long.
    """
    # perform startup sequences.
    core.sound.play_sound_safecast("START")
    # start subthread....
    worker_thread = threading.Thread(target=app_worker, args={})
    worker_thread.daemon = True
    worker_thread.start
    camera_thread = threading.Thread(
        target=camera_worker, args={detected_callback})
    camera_thread.daemon = True
    camera_thread.start

    # amd set callback for beam:

    core.robot_control.set_lightbar_callback(lightbar_callback)


def lightbar_callback():
    core.play_sound_safecast("thanks")  # thank user when throwing something in
    global trash_count
    trash_count += 1


def app_worker():
    # since some of the movement functions include blocking features,
    # they should be called from this seperate thread.

    while not stop_flag.is_set():
        while autonomous_mode_enabled:
            # drive autonomously.
            core.robot_control.move_autonomous()
        else:
            # do nothing.
            pass
    worker_cleanup()
    return


def worker_cleanup():
    pass


def detected_callback():
    core.play_sound_safecast("trash_detected")
