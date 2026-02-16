import subprocess

def list_processes():
    return subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout
