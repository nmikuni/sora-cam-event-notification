import datetime
import json
import os
import subprocess
import time

import requests

SORACOM_AUTH_KEY_ID = os.environ.get("SORACOM_AUTH_KEY_ID")
SORACOM_AUTH_KEY = os.environ.get("SORACOM_AUTH_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
COMMON_ARG = ' --auth-key-id ' + SORACOM_AUTH_KEY_ID + ' --auth-key ' + SORACOM_AUTH_KEY

LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

def lambda_handler(event, context):
    print("Get the motion events list with SORACOM API")
    motion_events = list_events()
    if motion_events == []:
        print("There was no event.")
        return
    for motion_event in motion_events:
        event_detected_time = motion_event["time"]
        image_url = motion_event["eventInfo"]["atomEventV1"]["picture"]
        image_bytes = download_image(image_url)
        print("Notify the image")
        notify_to_line(event_detected_time, image_bytes)
    return


def run_cmd(cmd):
    cmd = cmd + COMMON_ARG
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return res


def list_events():
    """Get the list of motion detection events from Soracom Cloud Camera Service using Soracom API"""
    current_unix_time_ms = int(time.time() * 1000)
    delta_ms = 60000 # 1 minutes
    from_unix_time_ms = current_unix_time_ms - delta_ms
    list_sora_cam_events_cmd = "soracom sora-cam devices events list-for-device --device-id " + DEVICE_ID + " --from " + str(from_unix_time_ms)
    event_list = json.loads(run_cmd(list_sora_cam_events_cmd).stdout.decode())
    return event_list


def download_image(image_url):
    image_data_bytes = requests.get(image_url).content
    return image_data_bytes


def notify_to_line(event_detected_time, image_bytes):
    """Notify the result to LINE"""
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + LINE_NOTIFY_TOKEN}

    event_detected_time_dt = datetime.datetime.utcfromtimestamp(int(event_detected_time) / 1000)
    event_detected_time_iso = event_detected_time_dt.isoformat() + 'Z'

    message = 'There was an event at ' + event_detected_time_iso

    data = {'message': 'message: ' + message}
    files = {'imageFile': image_bytes}
    response = requests.post(line_notify_api, headers=headers, data=data, files=files)
    print(response)
    