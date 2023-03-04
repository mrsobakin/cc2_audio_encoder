import platform
import subprocess


USE_WINE = platform.system() != "Windows"


def run(exe, args):
    if USE_WINE:
        return subprocess.run(["wine", exe, *args], check=True)

    return subprocess.run([exe, *args], check=True)
