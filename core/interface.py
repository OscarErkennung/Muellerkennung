import serial, time
from enum import Enum
import core.logger as logger

ser = None

DEBUG_FLAG:bool = False  # Set to True for debugging, False for production


#interface A,B,C,D = <uint_8t speed>

#A   B
#C   D

class Direction(Enum):
    forward = 'forward'
    backward = 'backward'
    left = 'left'
    right = 'right'
    stop = 'stop'

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
    Direction.stop: {Motor.A: 0, Motor.B: 0, Motor.C: 0, Motor.D: 0}   
}
    
def interface_setup(): 
    global ser
    try: 
        if not DEBUG_FLAG: 
            ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
            time.sleep(4)
            if not ser.is_open: 
                 ser.open()
        else:
            ser = None  # For debugging, we don't open a real serial port
        print("Serial port opened successfully.")
    except serial.SerialException as e: 
        logger.log(f"Error opening serial port: {e}", lvl=40)

def interface_cleanup():
    try:
        if ser.is_open:
            ser.close()
            print("Serial port closed successfully.")
    except serial.SerialException as e:
        logger.log(f"Error closing serial port: {e}", lvl=40)

def move_robot_safecast(maybe_dir:str, speed:int=70):
    """
    Safely cast the direction and move the robot.
    """
    try:
        dir = Direction(maybe_dir)
        move_robot(dir, speed)
    except ValueError as e:
        logger.log(f"Invalid direction: {maybe_dir}. Error: {e}", lvl=40)


def move_robot(dir:Direction , speed:int=70): 
    """

    """    
    try: 
        assert 0<=speed<=100, "Speed must be between 0 and 100"
        assert type(dir)==Direction, "Invalid direction"
        if not DEBUG_FLAG:
            assert ser.is_open, "Serial port is not open"
    except AssertionError as e:
        logger.log(f"Assertion Error: {e}", lvl=40)
        return
    
    for i in Motor:
          # Get the speed for the motor in the specified direction
        to_send = f'{i}{lookup_directions.get(dir, {}).get(i, 0)}'
        
        if not DEBUG_FLAG: 
            ser.write(to_send.encode('utf-8'))
            ser.flush()
        print(f'Sent command: {i}={lookup_directions[dir][i]}')

if __name__ == "__main__":
    interface_setup()
    move_robot(Direction.forward, 70)
    time.sleep(1)
    move_robot(Direction.backward, 70)
    time.sleep(1)
    move_robot(Direction.left, 70)
    time.sleep(1)
    move_robot(Direction.right, 70)
    time.sleep(1)
    move_robot(Direction.stop, 0)
    time.sleep(1)
    interface_cleanup()
else: 
    DEBUG_FLAG = False # never debug as module.
    interface_setup()
    logger.log("module init for interface complete")


