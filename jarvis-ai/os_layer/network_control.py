import subprocess

def wifi_off():
    subprocess.run(["nmcli", "radio", "wifi", "off"])

def wifi_on():
    subprocess.run(["nmcli", "radio", "wifi", "on"])
