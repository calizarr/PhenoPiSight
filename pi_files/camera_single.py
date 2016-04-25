#!/usr/bin/python
import pdb
import time
import picamera
import socket
import json
import itertools
import subprocess
import socket
import os
import tarfile
import zipfile
import shutil

from fractions import Fraction
from datetime import datetime, timedelta
from contextlib import contextmanager
from glob import glob

# Function to switch directories so as to make tarballing a little easier.
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

# Platform-independent method to get the ip of the current host.
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 0))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def convert_ip(ip, width, height, offset):
    octet = int(ip.split('.')[-1])
    formula = abs(octet-(width*height)-offset)
    y = (formula / width) + 1
    x = (formula % width) + 1
    if width > height:
        pad = len(str(width))
    else:
        pad = len(str(height))
    x = str(x).zfill(pad)
    y = str(y).zfill(pad)
    return [y, x]

# Make the medata for the current Raspberry Pi Camera.
def make_metadata(experiment, hostname, ip, camera, grid):
    metadata = {}
    metadata['experiment'] = {
        "experiment": experiment
        }
    metadata['fixed_camera_data'] = {
        "hostname": hostname,
        "ip_address": ip,
        "grid_coord": grid
    }
    metadata['variable_camera_settings'] = {
        "zoom": camera.zoom,
        "vflip": camera.vflip,
        "hflip": camera.hflip,
        "still_stats": camera.still_stats,
        "shutter_speed": camera.shutter_speed,
        "sharpness": camera.sharpness,
        "sensor_mode": camera.sensor_mode,
        "saturation": camera.saturation,
        "rotation": camera.rotation,
        "resolution": camera.resolution,
        "meter_mode": camera.meter_mode,
        "iso": camera.iso,
        "image_effect": camera.image_effect,
        "image_effect_params": camera.image_effect_params,
        "image_denoise": camera.image_denoise,
        "framerate": camera.framerate,
        "analog_gain": camera.analog_gain,
        "digital_gain": camera.digital_gain,
        "awb_gains": camera.awb_gains,
        "awb_mode": camera.awb_mode,
        "brightness": camera.brightness,
        "color_effects": camera.color_effects,
        "contrast": camera.contrast,
        "crop": camera.crop,
        "drc_strength": camera.drc_strength,
        "exposure_compensation": camera.exposure_compensation,
        "exposure_mode": camera.exposure_mode,
        "exposure_speed": camera.exposure_speed,
        "flash_mode": camera.flash_mode
    }

    # Setting values that are Fractions to their string representations i.e. "3/4" instead of Fraction(3, 4)
    for key, value in metadata['variable_camera_settings'].items():
        if isinstance(value, Fraction):
            metadata['variable_camera_settings'][key] = str(value)
        elif isinstance(value, tuple) and isinstance(value[0], Fraction):
            metadata['variable_camera_settings'][key] = [str(x) for x in value]
    return metadata

# Here begins the proper process of taking the pictures
with picamera.PiCamera() as camera:
    # Getting the image directory for all of the rPIs. Should become a passable parameter.
    image_dir = os.path.join("/home", "pi", "Images")
    # Switching into the directory where the folders and tarballs exist.
    with cd(image_dir):
        # Testing if the switch was proper
        print(os.getcwd())
        # Getting the hostname of the rPI
        hostname = socket.gethostname()
        print("The hostname is {0}".format(hostname))
        # Setting the camera resolution to max, and letting the camera adjust settings.
        camera.resolution = (2592, 1944)
        camera.start_preview()
        time.sleep(2)

        # Getting the current timestamp
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        hour = now.strftime("%Y-%m-%d-%H")
        # Full path directories.
        date_directory = os.path.join(image_dir, now.strftime("%Y-%m-%d"))
        hour_directory = os.path.join(date_directory, now.strftime("%Y-%m-%d-%H"))
        # Creating directories if they do not exist.
        if not os.path.exists(date_directory):
            os.makedirs(date_directory)
            # Hour directory will not exist for time point IF the date directory does not exist.
            # Frankly, they all get removed so they shouldn't exist at all
            os.makedirs(hour_directory)
        elif not os.path.exists(hour_directory):
            os.makedirs(hour_directory)

        # Making the filename for the capture of the image.
        width = 6
        height = 30
        offset = 10
        grid = convert_ip(get_ip(), width, height, offset)
        filename = "{hostname}_Y{y}_X{x}_{now}.png".format(hostname=hostname, x=grid[1], y=grid[0], now=now.strftime("%Y-%m-%d-%H-%M"))
        # filename = hostname+"_"+now.strftime("%Y-%m-%d-%H-%M")+".png"
        filename = os.path.join(hour_directory, filename)
        camera.capture(filename)
        print("Captured %s" % filename)
        
        # For multi-platform ip getting
        ip = get_ip()

        # Getting all the metadata that will be going into the json file.
        metadata_name = filename.split('.')[0]
        experiment = "To be determined later..."
        metadata = make_metadata(experiment, hostname, ip, camera, grid)
        json_filename = metadata_name + ".json"
        json_filename = os.path.join(hour_directory, json_filename)
        with open(json_filename, "w") as fp:
            json.dump(metadata, fp, sort_keys=True, indent=4)

        # Creating directory structure tar
        dir_join = hostname+"_"+now.strftime("%Y-%m-%d")
        with tarfile.open(dir_join+".tar", "w") as tar:
            tar.add(date_directory, arcname=date)
        shutil.rmtree(date_directory)
