# robot_control.py
# import serial
# Beispiel: Serieller Port
import RPi.GPIO as GPIO
import time
# 🧠 Genaue GPIO-Nummern eintragen!
SPEED_LEFT = 24      # PWM für linke Seite
DIR_LEFT = 25        # Richtung für linke Seite
SPEED_RIGHT = 23     # PWM für rechte Seite
DIR_RIGHT = 22       # Richtung für rechte Seite
PWM_FREQ = 100       # PWM-Frequenz in Hz
# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([SPEED_LEFT, DIR_LEFT, SPEED_RIGHT, DIR_RIGHT], GPIO.OUT)
# PWM initialisieren
pwm_left = GPIO.PWM(SPEED_LEFT, PWM_FREQ)
pwm_right = GPIO.PWM(SPEED_RIGHT, PWM_FREQ)
pwm_left.start(0)
pwm_right.start(0)
def move_robot(direction, speed=70):
   """
   Steuert den Roboter in eine bestimmte Richtung
   direction: 'forward', 'backward', 'left', 'right', 'stop'
   speed: PWM-Stärke (0–100)
   """
   if direction == "forward":
       GPIO.output(DIR_LEFT, GPIO.HIGH)
       GPIO.output(DIR_RIGHT, GPIO.HIGH)
       pwm_left.ChangeDutyCycle(speed)
       pwm_right.ChangeDutyCycle(speed)
   elif direction == "backward":
       GPIO.output(DIR_LEFT, GPIO.LOW)
       GPIO.output(DIR_RIGHT, GPIO.LOW)
       pwm_left.ChangeDutyCycle(speed)
       pwm_right.ChangeDutyCycle(speed)
   elif direction == "left":
       GPIO.output(DIR_LEFT, GPIO.LOW)
       GPIO.output(DIR_RIGHT, GPIO.HIGH)
       pwm_left.ChangeDutyCycle(speed)
       pwm_right.ChangeDutyCycle(speed)
   elif direction == "right":
       GPIO.output(DIR_LEFT, GPIO.HIGH)
       GPIO.output(DIR_RIGHT, GPIO.LOW)
       pwm_left.ChangeDutyCycle(speed)
       pwm_right.ChangeDutyCycle(speed)
   elif direction == "stop":
       pwm_left.ChangeDutyCycle(0)
       pwm_right.ChangeDutyCycle(0)
def cleanup():
   pwm_left.stop()
   pwm_right.stop()
   GPIO.cleanup()
   #arduino.write(command_map[direction].encode())
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
def get_ultrasound_distance():
   # TODO: Werte vom Sensor lesen
   return 45  # cm