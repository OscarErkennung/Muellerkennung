import subprocess


def set_image(name: str):
    subprocess.run(f"feh --fullscreen --auto-zoom ../images/{name}.png")
