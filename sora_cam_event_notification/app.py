import datetime
import os

import requests
import line_notify
import soracom_cli

SORACOM_AUTH_KEY_ID = os.environ.get("SORACOM_AUTH_KEY_ID")
SORACOM_AUTH_KEY = os.environ.get("SORACOM_AUTH_KEY")
DEVICE_ID = os.environ.get("DEVICE_ID")
COMMON_ARG = ' --auth-key-id ' + SORACOM_AUTH_KEY_ID + \
    ' --auth-key ' + SORACOM_AUTH_KEY
LINE_NOTIFY_TOKEN = os.environ.get("LINE_NOTIFY_TOKEN")

EVENT_RETRIEVE_INTERVAL_SEC = int(
    os.environ.get("EVENT_RETRIEVE_INTERVAL_SEC"))


def lambda_handler(event, context):
    print("Get the motion events list with SORACOM API")
    motion_events = soracom_cli.list_events(
        device_id=DEVICE_ID, delta_sec=EVENT_RETRIEVE_INTERVAL_SEC, arg=COMMON_ARG)
    if motion_events == []:
        print("There was no event.")
        return
    for motion_event in motion_events:
        event_detected_time = motion_event["time"]
        image_url = motion_event["eventInfo"]["atomEventV1"]["picture"]
        image_bytes = download_image(image_url)
        notify_message = create_event_detection_message(event_detected_time)
        print("Notify the image")
        line_notify.notify_to_line_with_image(
            token=LINE_NOTIFY_TOKEN, message=notify_message, image_bytes=image_bytes)
    return


def download_image(image_url):
    image_data_bytes = requests.get(image_url).content
    return image_data_bytes


def create_event_detection_message(event_detected_time):
    event_detected_time_dt = datetime.datetime.utcfromtimestamp(
        int(event_detected_time) / 1000)
    event_detected_time_iso = event_detected_time_dt.isoformat() + 'Z'

    message = 'There was an event at ' + event_detected_time_iso

    return message
