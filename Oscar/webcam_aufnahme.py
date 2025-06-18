import cv2
import time
import os
from datetime import datetime

MAX_BILDER = 100
# Zielordner für die Bilder
output_dir = "tmp/"
os.makedirs(output_dir, exist_ok=True)
 
# Kamera öffnen (0 = /dev/video0)
cap = cv2.VideoCapture(0)
 
# Prüfen, ob die Kamera erfolgreich geöffnet wurde
if not cap.isOpened():
    print("Fehler: Webcam konnte nicht geöffnet werden.")
    exit()
    
bilder = sorted([f for f in os.listdir(output_dir) if f.endswith(".jpg")])

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Lesen des Kamerabilds.")
            break
 
        # Zeitstempel für Dateinamen
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"webcam_{timestamp}.jpg")
 
        # Bild speichern
        cv2.imwrite(filename, frame)
        print(f"Bild gespeichert: {filename}")
        bilder.append(f"webcam_{timestamp}.jpg")
        if len(bilder) > MAX_BILDER:
            os.remove(os.path.join(output_dir, bilder[0]))
            print(f"{bilder[0]} wurde gelöscht (ältestes Bild)")
            bilder = bilder[1:]

        time.sleep(0.5)
 
except KeyboardInterrupt:
    print("Aufnahme manuell gestoppt.")
 
finally:
    cap.release()
    print("Kamera freigegeben.")

