import subprocess

def run_with_sudo(command):
    return subprocess.run(["sudo"] + command)
