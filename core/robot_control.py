# robot_control.py
# import serial
# Beispiel: Serieller Port
import RPi.GPIO as GPIO
from gpiozero import DistanceSensor
from core import logger
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)

distance_front_sensor = DistanceSensor(echo=19, trigger=26)
#distance_back_sensor = DistanceSensor(echo=XXX, trigger=YYY)
#distance_left_sensor = DistanceSensor(echo=XXX, trigger=YYY)
#distance_right_sensor = DistanceSensor(echo=XXX, trigger=YYY)


def cleanup():
   GPIO.cleanup()
   #test

def set_autonomous_mode(enabled):
   #arduino.write(b'A1' if enabled else b'A0')
   pass
def get_status():
   # Hier könnt ihr Sensoren lesen – als Platzhalter:
   return {
       'trash_detected': detect_trash(),
       'distance': get_ultrasound_distance(),
       'battery_level': 76  # Beispielwert
   }
def detect_trash():
   # TODO: Anbindung an CV-Modul
   return False
def get_ultrasound_distance(round2n=True):#currently front only.
   # TODO: Werte vom Sensor lesen
   distance = distance_front_sensor.distance * 100  # Umwandlung in cm
   logger.log(f"Measured Distance: {distance:.2f} cm")
   if round2n:
      return round(distance, 2)  # cm
   else:
      return distance  # cm


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