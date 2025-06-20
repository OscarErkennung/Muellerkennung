
class GPIO:
    BCM = "BCM"
    IN = "IN"
    BOTH = "BOTH"
    @staticmethod
    def setmode(mode):
        pass

    @staticmethod
    def setup(pin, mode):
        pass

    @staticmethod
    def add_event_detect(a, b, callback=None, bouncetime=None):
        pass


class DistanceSensor:
    def __init__(self, echo, trigger):
        self.echo = echo
        self.trigger = trigger
        self.distance = 1000

class Serial:
    def __init__(self, port, baudrate, timeout):
        self.is_open = True
        pass

    def open(self):
        pass

    def close(self):
        self.is_open = False

    def write(self, string):
        pass

    def flush(self):
        pass


class SerialException(Exception):
    def __init__(self):
        pass