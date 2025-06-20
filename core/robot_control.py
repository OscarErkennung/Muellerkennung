# robot_control.py
# import serial
# Beispiel: Serieller Port
from bdb import Breakpoint
from random import randint
from turtle import forward
from typing import Callable
import RPi.GPIO as GPIO
#from gpiozero import Device, DistanceSensor
#from gpiozero.pins.native import NativeFactory
from core import logger, interface
import time 

RECEIVER_PIN = 15 # gpio pin for photoresistive divider. 
MIN_DISTANCE = 80 #dm
TIME_THRESHOLD = 10 #secs

def gpio_setup(): 
   # GPIO Setup
   GPIO.setmode(GPIO.BCM)
   GPIO.setup(RECEIVER_PIN, GPIO.IN)
   distance_front_sensor = DistanceSensor(echo=19, trigger=26)

#Device.pin_factory = NativeFactory()

#distance_back_sensor = DistanceSensor(echo=XXX, trigger=YYY)
#distance_left_sensor = DistanceSensor(echo=XXX, trigger=YYY)
#distance_right_sensor = DistanceSensor(echo=XXX, trigger=YYY)


def set_lightbar_callback(func:Callable):
   GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH, callback=func, bouncetime=200)


def cleanup():
   GPIO.cleanup()
   #test

def detect_trash():
   # TODO: Anbindung an CV-Modul
   return False

def get_ultrasound_distance(round2n=True):#currently front only.
   # TODO: Werte vom Sensor lesen
   distance = 0
   #distance = distance_front_sensor.distance * 100  # Umwandlung in cm
   logger.log(f"Measured Distance: {distance:.2f} cm")
   if round2n:
      return round(distance, 2)  # cm
   else:
      return distance  # cm

def move_autonomous():
   while(True): # -> only call in a breakable loop. 
      #setup
      interface.move_robot_linear(interface.Direction.forward)
      start_time = time.now()
      reason =""
      #move forward until we have to do something. 
      while True: 
         if(get_ultrasound_distance()<=MIN_DISTANCE): 
            reason="distance"
            break 
         if(time.now()-start_time)>=TIME_THRESHOLD:#cm 
            reason="time" 
            break
      ##stop
      interface.move_robot_linear(interface.Direction.stop)
      ## Change direction
      match reason: 
         case "time":
            # turn randomly to cover free area.
            interface.rotate_robot(30, 50)
            break
         case "distance":
            #we see a wall, turn roomba style. 
            random_direction = randint(-60, 60)
            interface.move_robot_linear(random_direction)
            break          
   
if __name__ == "__main__": 
   try:
       while True:
           distance = distance_front_sensor.distance * 100  # Umwandlung in cm
           print(f"Distance: {distance:.2f} cm")
           time.sleep(1)
   except KeyboardInterrupt:
       print("Measurement stopped by User")
       GPIO.cleanup()
   except Exception as e:
       print(f"An error occurred: {e}")
       GPIO.cleanup()
   else: 
      #we are a module. 
      pass