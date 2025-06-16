import cv2
import time
import numpy as np
import pygame
import os

from tflite_runtime.interpreter import Interpreter

# === Einstellungen ===
MODEL_PATH = 'model.tflite'
LABEL_PATH = 'labels.txt'
SOUND_DIR = 'sounds'
IMAGE_SIZE = (224, 224)  # anpassen je nach Modell
INFERENCE_INTERVAL = 1  # Sekunden

# === Audio-Setup (pygame) ===
pygame.mixer.init()

def play_audio(label):
    filepath = os.path.join(SOUND_DIR, f"{label}.mp3")
    if os.path.exists(filepath):
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    else:
        print(f"[WARN] Keine Audiodatei für: {label}")

# === Labels laden ===
with open(LABEL_PATH, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# === Modell laden ===
interpreter = Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# === Kamera starten ===
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise RuntimeError("Kamera konnte nicht geöffnet werden.")

print("[INFO] Starte Müllklassifikation...")

try:
    while True:
        start = time.time()

        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Kein Kamerabild.")
            continue

        # Bild vorbereiten
        resized = cv2.resize(frame, IMAGE_SIZE)
        input_data = np.expand_dims(resized, axis=0).astype(np.float32) / 255.0

        # Modell ausführen
        interpreter.set_tensor(input_details[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(output_details[0]['index'])[0]

        # Höchste Wahrscheinlichkeit
        top_idx = int(np.argmax(output_data))
        label = labels[top_idx]
        confidence = output_data[top_idx]

        print(f"[INFO] Erkannt: {label} ({confidence:.2f})")

        if confidence > 0.6:  # Schwelle zur Sicherheit
            play_audio(label)

        # Warte bis zur nächsten Aufnahme
        time.sleep(max(0, INFERENCE_INTERVAL - (time.time() - start)))

except KeyboardInterrupt:
    print("\n[INFO] Beende Programm...")

finally:
    cap.release()
    pygame.mixer.quit()
