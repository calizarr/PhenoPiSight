#!/usr/bin/python
import pdb
import time
import picamera
import socket
import json
import itertools
import subprocess
import socket

from fractions import Fraction
from datetime import datetime, timedelta

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

def convert_ip(ip, width, height):
    octet = int(ip.split('.')[-1])
    formula = abs(octet-(width*height)-10)
    x = (formula / width) + 1
    y = (formula % width) + 1
    return [x, y]

def make_metadata(experiment, hostname, ip, camera):
    metadata = {}
    metadata['experiment'] = {
        "experiment": experiment
        }
    metadata['fixed_camera_data'] = {
        "hostname": hostname,
        "ip_address": ip,
        "grid_coord": convert_ip(ip, width, height)
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
    for key, value in metadata['variable_camera_settings'].items():
        if isinstance(value, Fraction):
            metadata['variable_camera_settings'][key] = str(value)
        elif isinstance(value, tuple) and isinstance(value[0], Fraction):
            metadata['variable_camera_settings'][key] = [str(x) for x in value]
    return metadata

def wait():
    # Calculate the delay to the start of the next hour
    next_hour = (datetime.now() + timedelta(minutes=2)).replace(
        second=0, microsecond=0)
#        minute=0, second=0, microsecond=0)
    print("This is the next hour: {0}".format(next_hour))
    delay = (next_hour - datetime.now()).seconds
    print("This is the delay time: {0}".format(delay))
    time.sleep(delay)

with picamera.PiCamera() as camera:
    width = 6
    height = 30
    hostname = socket.gethostname()
    print("The hostname is {0}".format(hostname))
    camera.resolution = (2592, 1944)
    camera.start_preview()
    wait()
    for filename in camera.capture_continuous(hostname+"_"+'{timestamp:%Y-%m-%d-%H-%M}.png'):
        print("Captured %s" % filename)
        # ip = "".join("".join(x) for is_number, x in itertools.groupby(hostname, key=str.isdigit) if is_number is True)
        # For multi-platform ip getting
        # ip = get_ip()
        ip = subprocess.check_output("hostname -I", shell=True).strip()
        # Getting all the metadata that will be going into the json file.
        metadata_name = filename.split('.')[0]
        experiment = "To be determined later..."
        metadata = make_metadata(experiment, hostname, ip, camera)
        json_filename = metadata_name + ".json"
        with open(json_filename, "w") as fp:
            json.dump(metadata, fp, sort_keys=True, indent=4)
        wait()
