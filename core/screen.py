import subprocess, os


def set_image(name: str):
    return
    subprocess.run(f"feh --fullscreen --auto-zoom ./images/{name}.png")
