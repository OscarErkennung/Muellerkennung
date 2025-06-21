import traceback

try:
    import serial
except ImportError:
    import rpi_mockups as serial
import time
from enum import Enum
import math
import core.logger as logger

ser = None

DEBUG_FLAG:bool = False  # Set to True for debugging, False for production
CALIBRATION_VALUE = 105
DEFAULT_SPEED = 30

#interface A,B,C,D = <uint_8t speed>

#B   C
#A   D

# C&D inverted

class Direction(Enum):
    forward = 'forward'
    backward = 'backward'
    left = 'left'
    right = 'right'
    stop = 'stop'
    rotate_cw = 'rotate_cw'
    rotate_ccw = 'rotate_ccw'

class Motor(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    __str__ = lambda self: self.value  # Ensure enum values are strings

lookup_directions = {
    Direction.forward: {Motor.A: 255, Motor.B: 255, Motor.C: -255, Motor.D: -255},
    Direction.backward: {Motor.A: -255, Motor.B: -255, Motor.C: 255, Motor.D: 255},
    Direction.stop: {Motor.A: 0, Motor.B: 0, Motor.C: 0, Motor.D: 0},
    Direction.left: {Motor.A: -255, Motor.B: -255, Motor.C: -255, Motor.D: -255},
    Direction.right: {Motor.A: 255, Motor.B: 255, Motor.C: 255, Motor.D: 255}, 
    Direction.stop: {Motor.A: 0, Motor.B: 0, Motor.C: 0, Motor.D: 0},
    Direction.rotate_cw: {Motor.A: 255, Motor.B: 0, Motor.C: 0, Motor.D: 255},
    Direction.rotate_ccw: {Motor.A: -255, Motor.B: 0, Motor.C: 0, Motor.D: -255}
}

def is_between(a, x, b):
    return min(a, b) < x < max(a, b)

def dir_from_angle(deg:float) -> dict: 
    """
    Convert x and y coordinates to a Direction.
    """
    # catch simple
    if deg==0:
       return lookup_directions.get(Direction.forward)
    try:
        assert is_between(0, deg,360)
    except AssertionError as e: 
        logger.log(f"Assertion Error: {e}", lvl=40)
        return Direction.stop
    x_component = math.cos(math.radians(deg))
    y_component = math.sin(math.radians(deg))
    
    output:dict = {}# lookup_directions.get(Direction.stop, {})  #init empty
    dummy:dict = lookup_directions.get(Direction.stop, {})  #init empty
    for index, (key, value) in enumerate(dummy.items()):
        #index, key, value
        value = x_component * lookup_directions[Direction.forward][key] + y_component * lookup_directions[Direction.right][key]
        output[key] = round(value)  # Initialize all motors to 0
        print(f"Index: {index}, Key: {key}, Value: {value}")
    print(f"Direction from angle {deg}: {output}")
    ## do vector scaling to fit the range of -255 to 255
    max_value = max(abs(v) for v in output.values())
    ##scale down or up, should always return one or all motors at 255
    if max_value > 255:
        scale_factor = 255 / max_value
        for key in output:
            output[key] = int(output[key] * scale_factor)
    print(f"Scaled direction: {output}")
    return output

def interface_setup(usb_port=0): 
    global ser
    try: 
        if not DEBUG_FLAG: 
            ser = serial.Serial(f'/dev/ttyUSB{usb_port}', 9600, timeout=1)#can be ttyUSB0 or ttyUSB1
            time.sleep(4)
            if not ser.is_open: 
                 ser.open()
        else:
            ser = None  # For debugging, we don't open a real serial port
    except serial.SerialException as e: 
        logger.log(f"Error opening serial port: {e}", lvl=40)
        if usb_port < 10:
            logger.log(f"Trying again using USB{usb_port + 1}", lvl=40)
            interface_setup(usb_port + 1)
    if usb_port == 0:
        print("Serial port opened successfully.")

def interface_cleanup():
    try:
        if ser.is_open:
            ser.close()
            print("Serial port closed successfully.")
    except serial.SerialException as e:
        logger.log(f"Error closing serial port: {e}", lvl=40)

def move_robot_safecast_linear(maybe_dir:str, speed:int=DEFAULT_SPEED):
    """
    Safely cast the direction and move the robot.
    """
    try:
        dir = Direction(maybe_dir)
        move_robot_linear(dir, speed)
    except ValueError as e:
        logger.log(f"Invalid direction: {maybe_dir}. Error: {e}", lvl=40)


def move_robot_linear(dir:Direction , speed:int=DEFAULT_SPEED): 
    """

    """
    print(f"Moving robot linear in direction {dir} to speed {speed}")
    try: 
        assert 0<=speed<=100, "Speed must be between 0 and 100"
        assert type(dir)==Direction, "Invalid direction"
        if not DEBUG_FLAG:
            assert ser.is_open, "Serial port is not open"
    except AssertionError as e:
        logger.log(f"Assertion Error: {e}", lvl=40)
        return
    except AttributeError:
        # traceback.print_exc()
        return
    
    for i in Motor:
          # Get the speed for the motor in the specified direction
        to_send = f'{i}{lookup_directions.get(dir, {}).get(i, 0)}\n'
        
        if not DEBUG_FLAG: 
            ser.write(to_send.encode('utf-8'))
        print(f'Sent command: {i}={lookup_directions[dir][i]}')
    time.sleep(0.3)  # Allow time for the command to be processed   
    ser.flush()

def move_robot_angular_safecast(deg:float, speed:int=DEFAULT_SPEED):
    """
    Move the robot in a direction based on an angle.
    """
    try:
        assert 0 <= speed <= 100, "Speed must be between 0 and 100"
        assert type(deg) == float, "Angle must be a float"
        if not DEBUG_FLAG:
            assert ser.is_open, "Serial port is not open"
    except AssertionError as e:
        logger.log(f"Assertion Error: {e}", lvl=40)
        return

    motor_values = dir_from_angle(deg)
    print(f"{motor_values=}")
    for i in Motor:
          # Get the speed for the motor in the specified direction
        to_send = f'{i}{motor_values[i]}\n'
        
        if not DEBUG_FLAG: 
            ser.write(to_send.encode('utf-8'))
        print(f'Sent command: {i}={motor_values[i]}')
    time.sleep(round(), 2)  # Allow time for the command to be processed
    ser.flush()

def rotate_robot(deg:int, speed:int=DEFAULT_SPEED):
    """
    Rotate the robot clockwise.

    1 sec is 124deg°
    -> 
    """
    print(f"Rotating roboto in direction {deg} to speed {speed}")
    try:
        assert 0 <= speed <= 100, "Speed must be between 0 and 100"
        assert -360 <= deg <=+360, "Angle should not exceed +/-360°."
        if not DEBUG_FLAG:
            assert ser.is_open, "Serial port is not open"
    except AssertionError as e:
        logger.log(f"Assertion Error: {e}", lvl=40)
        return
    except AttributeError:
        return
    
    move_robot_linear(Direction.rotate_cw, 100) if deg>0 else move_robot_linear(Direction.rotate_ccw, 100)
    time.sleep(abs(deg/CALIBRATION_VALUE)) #drehe über steuerbord.
    move_robot_linear(Direction.stop, 0)
    return
if __name__ == "__main__":
    interface_setup()
    rotate_robot(360, 70)
    #move_robot(Direction.forward, 70)
    #time.sleep(1)
    #move_robot(Direction.backward, 70)
    #time.sleep(1)
    #move_robot(Direction.left, 70)
    #time.sleep(1)
    #move_robot(Direction.right, 70)
    #time.sleep(1)
    #move_robot(Direction.stop, 0)
    #time.sleep(1)
    interface_cleanup()
else: 
    DEBUG_FLAG = False # never debug as module.
    interface_setup()
    logger.log("module init for interface complete")


