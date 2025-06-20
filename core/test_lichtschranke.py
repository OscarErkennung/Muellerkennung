import RPi.GPIO as GPIO
import time
 
RECEIVER_PIN = 5  # GPIO-Pin, an dem der LDR hängt
 
def callback_func(channel):
    if GPIO.input(channel):
        print("Laser erkannt (nicht unterbrochen)")
    else:
        print("Lichtschranke wurde unterbrochen!")
 
if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
 
    # Setze GPIO23 als Eingang, kein Pullup nötig, da Spannung von außen kommt
    GPIO.setup(RECEIVER_PIN, GPIO.IN)
 
    # Erkenne beide Flanken (Laser trifft / wird unterbrochen)
    GPIO.add_event_detect(RECEIVER_PIN, GPIO.BOTH, callback=callback_func, bouncetime=200)
 
    try:
        print("Lichtschranke läuft. Drücke Strg+C zum Beenden.")
        while True:
            time.sleep(1)
            print("GPIO-Wert:", GPIO.input(RECEIVER_PIN))
            time.sleep(0.5)
    except KeyboardInterrupt:
        GPIO.remove_event_detect(RECEIVER_PIN)
        GPIO.cleanup()
        print("Beendet.")