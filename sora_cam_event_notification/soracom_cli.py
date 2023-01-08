import json
import subprocess
import time


def run_cmd(cmd, arg):
    cmd = cmd + arg
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return res


def list_events(device_id, delta_sec, arg):
    """Get the list of motion detection events from Soracom Cloud Camera Service using Soracom API"""
    current_unix_time_ms = int(time.time() * 1000)
    delta_ms = int(delta_sec) * 1000
    from_unix_time_ms = current_unix_time_ms - delta_ms
    list_sora_cam_events_cmd = "soracom sora-cam devices events list-for-device --device-id " + \
        device_id + " --from " + str(from_unix_time_ms)
    event_list = json.loads(
        run_cmd(cmd=list_sora_cam_events_cmd, arg=arg).stdout.decode())
    return event_list
