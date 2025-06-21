# robot_control.py
# import serial
# Beispiel: Serieller Port
from random import randint
from typing import Callable
try:
    import RPi.GPIO as GPIO
    from gpiozero import DistanceSensor
except ImportError:
    from rpi_mockups import GPIO
    from rpi_mockups import DistanceSensor
from core import logger, interface, core_main
import time
from functools import partial

RECEIVER_PIN1 = 17  # gpio pin for photoresistive divider.
RECEIVER_PIN2 = 27  # gpio pin for photoresistive divider.
RECEIVER_PIN3 = 22  # gpio pin for photoresistive divider.
MIN_DISTANCE = 80  # dm
TIME_THRESHOLD = 2  # secs

distance_front_sensor = None
gpio_is_setup = False

def gpio_setup(): 
   global gpio_is_setup
   global distance_front_sensor 
   if gpio_is_setup:
      logger.log("GPIO already set up, skipping setup.", lvl=20)
      return
   gpio_is_setup = True
   # GPIO Setup
   GPIO.setmode(GPIO.BCM)
   GPIO.setup([RECEIVER_PIN1, RECEIVER_PIN2, RECEIVER_PIN3], GPIO.IN)

   #Device.pin_factory = NativeFactory()  # Use native GPIO pins 
   global distance_front_sensor
   distance_front_sensor = DistanceSensor(echo=19, trigger=26)


# Device.pin_factory = NativeFactory()
# distance_back_sensor = DistanceSensor(echo=XXX, trigger=YYY)
# distance_left_sensor = DistanceSensor(echo=XXX, trigger=YYY)
# distance_right_sensor = DistanceSensor(echo=XXX, trigger=YYY)


def set_lightbar_callback(func:Callable, args=None):
   partial_func = partial(func, args) if args else func
   if not gpio_is_setup:
      gpio_setup()
   GPIO.add_event_detect(RECEIVER_PIN1, GPIO.BOTH, callback=partial_func, bouncetime=200)
   GPIO.add_event_detect(RECEIVER_PIN2, GPIO.BOTH, callback=partial_func, bouncetime=200)
   GPIO.add_event_detect(RECEIVER_PIN3, GPIO.BOTH, callback=partial_func, bouncetime=200)


def cleanup():
    GPIO.cleanup()
    # test


def get_ultrasound_distance(round2n=True):  # currently front only.
   # TODO: Werte vom Sensor lesen
   global distance_front_sensor
   try: 
      distance = distance_front_sensor.distance * 100  # Umwandlung in cm
   except AttributeError as e:
      logger.log("Distance sensor not initialized, please call gpio_setup() first.", lvl=50)
      return -1
   logger.log(f"Measured Distance: {distance:.2f} cm")
   if round2n:
      return round(distance, 2)  # cm
   else:
      return distance  # cm


def move_autonomous():
    # setup
    interface.move_robot_linear(interface.Direction.forward)
    start_time = time.time()
    # move forward until we have to do something.
    while True:
        if get_ultrasound_distance() == -1:
            reason = "uninitialized"
            break
        if get_ultrasound_distance() <= MIN_DISTANCE:
            reason = "distance"
            break
        if (time.time() - start_time) >= TIME_THRESHOLD:  # cm
            reason = "time"
            break
        if core_main.our_status.get_trash_detected():
            reason = "trash"
            break
    ##stop
    interface.move_robot_linear(interface.Direction.stop)
    ## Change direction
    match reason:
        case "time":
            # turn randomly to cover free area.
            random_direction = randint(-130, 130)
            interface.rotate_robot(random_direction, 50)
        case "distance":
            # we see a wall, turn roomba style.
            interface.move_robot_linear(interface.Direction.backward, speed=50)
            time.sleep(0.25)
            random_direction = randint(90, 180)
            random_vorzeichen = randint(90, 180)
            if random_vorzeichen % 2 == 0:
                interface.rotate_robot(random_direction)
            else:
                interface.rotate_robot(-random_direction)
        case "trash":
            # Do nothing
            pass
        case "uninitialized":
            print("Unitialized distance sensor, cannot move autonomously!")
            logger.log("Distance sensor has not yet been read, preventing sensorless autonomous mode!")

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
        # we are a module.
        pass
