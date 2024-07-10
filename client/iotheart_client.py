from scheduling import RepeatedTimer
import requests

# Properties
target_ip = 'server_ip_here'
device_id = 'device_id_here'
beat_frequency_seconds = 10


def send_heartbeat(*args, **kwargs):
    result = requests.get(f'http://{target_ip}:1111/api/beat?device_id={device_id}', timeout=20000).status_code
    if result != 200:
        print(f'Failed to send heartbeat. Response code is {result}')
    print('Heartbeat sent')


# Set a timer
timers = [
    RepeatedTimer(beat_frequency_seconds, send_heartbeat, [], {})
]
