#!/bin/python

import os, subprocess
from enum import Enum
import core.logger as logger
##asume launching from "Muellerkennung"
#Sound_dir = os.getcwd() + '/core/sounds/'
##asume sound is in predifined path 
sound_dir = '/home/oscar/audiostuff/'


class Sound(Enum): 
    START = {'file':'sm64_mario_lets_go.mp3'}
    STOP = {'file':'halt_stop.mp3'}
    ERROR = {'file':'mario_fail_sound.mp3'}
    light_beam = {'file':'applepay.mp3'}
    help_me = {'file':'Hilfe.mp3'}
    thanks = {'file':'Danke.mp3'}
    trash_detected = {'file':'Muellentdeckt.mp3'}

def play_sound_safecast(mysound:str): 
    try: 
        sound = Sound[mysound]
        play_sound(sound)
    except ValueError as e:
        print(f"Invalid sound: {mysound}. Error: {e}")



def play_sound(mysound:Sound):
    """
    Play a sound using the system's default media player.
    """
    sound_file = sound_dir + mysound.value.get('file', '')  
    if os.path.exists(sound_file):
        try:
            subprocess.Popen(['mpg123', sound_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            logger.log(f"Error playing sound {sound_file}: {e}")
    else:
        logger.log(f"Sound file {sound_file} does not exist.")


if __name__ == "__main__":
    for i in Sound: 
        print(f"Playing sound: {i.name}")
        play_sound(i)
        input("Press Enter to continue...") 
else: 
    #imported as module
    pass
