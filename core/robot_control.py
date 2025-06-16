# robot_control.py
# import serial
# Beispiel: Serieller Port
arduino = None #serial.Serial('/dev/ttyUSB0', 9600)
def move_robot(direction):
   command_map = {
       'forward': 'F',
       'backward': 'B',
       'left': 'L',
       'right': 'R',
       'stop': 'S'
   }
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