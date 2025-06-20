import cv2
import time
import os
import ai_edge_litert.interpreter as tflite
import numpy as np
from datetime import datetime
 
# Maximal erlaubte Anzahl von Bildern
MAX_BILDER = 100
 
MODEL_PATH = "mobile_net_v2_2025-06-19_15:30:28.718971_quantized.tflite"
output_dir = "tmp"
os.makedirs(output_dir, exist_ok=True)
 
labels = ["notrash", "trash"]

interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
 
input_index = input_details[0]['index']
output_index = output_details[0]['index']
input_shape = input_details[0]['shape']
height, width = input_shape[1], input_shape[2]

# Webcam starten (0 = /dev/video0)
cap = cv2.VideoCapture(0)
 
if not cap.isOpened():
    print("Fehler: Webcam konnte nicht geöffnet werden.")
    exit()
 
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fehler beim Lesen des Kamerabilds.")
            continue
 
        # Zeitstempel für Dateinamen
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(output_dir, f"webcam_{timestamp}.jpg")
 
        # Bild speichern
        cv2.imwrite(filename, frame)

	    # Bild vorbereiten
        img = cv2.resize(frame, (width, height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_data = np.expand_dims(img.astype(np.float32), axis=0)
              
        # Modell ausführen
        interpreter.set_tensor(input_index, input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_index) 

        predicted_index = int(round(output_data[0][0]))
        label = labels[predicted_index]
        print(f"[{timestamp}]  {output_data[0][0]:.4f}  |  {label}")
 
        # Bilderliste neu laden und nach Änderungszeit sortieren
        bilder = sorted(
            [f for f in os.listdir(output_dir) if f.endswith(".jpg")],
            key=lambda f: os.path.getmtime(os.path.join(output_dir, f))
        )
 
        # Alte Bilder löschen, wenn über MAX_BILDER
        while len(bilder) > MAX_BILDER:
            zu_loeschen = bilder.pop(0)
            os.remove(os.path.join(output_dir, zu_loeschen))

        time.sleep(0.5)
 
except KeyboardInterrupt:
    print("Aufnahme manuell gestoppt mit STRG+C.")
 
finally:
    cap.release()
    print("Kamera freigegeben.")
