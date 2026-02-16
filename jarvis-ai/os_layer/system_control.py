import subprocess

def shutdown():
    subprocess.run(["sudo", "shutdown", "now"])

def restart():
    subprocess.run(["sudo", "reboot"])
