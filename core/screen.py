import subprocess, os

last_process = None

def set_image(name: str):
    global last_process
    if last_process:
        last_process.terminate()
        last_process.wait()


    last_process = subprocess.Popen(["feh", "--fullscreen", "--auto-zoom", f"./images/{name}.png"])
