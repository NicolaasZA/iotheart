from scheduling import RepeatedTimer
import requests
import logging
import time

# Properties
target_ip = 'server_ip_here'
device_id = 'device_id_here'
beat_frequency_seconds = 10


def send_heartbeat(*args, **kwargs):
    result = requests.post(f'http://{target_ip}:1111/api/beat?device_id={device_id}', data={}, timeout=20000).status_code
    if result != 200:
        print(f'Failed to send heartbeat. Response code is {result}')
    else:
        print('Heartbeat sent')


# Set a timer
timers = [
    RepeatedTimer(beat_frequency_seconds, send_heartbeat, [], {})
]

try:
    while True:
        time.sleep(60)
except KeyboardInterrupt:
    logging.info("Service is being stopped by the user.")
except Exception:
    logging.error("Service is stopping because of error.", exc_info=True)
finally:
    for timer in timers:
        timer.stop()
