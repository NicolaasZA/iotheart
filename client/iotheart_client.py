from scheduling import RepeatedTimer
import psutil
import requests
import logging
import time

# Properties
target_ip = 'server_ip_here'
device_id = 'device_id_here'
beat_frequency_seconds = 10

# Calculated
beat_timeout = (beat_frequency_seconds - 1) * 1000
beat_url = f'http://{target_ip}:1111/api/beat'

def send_heartbeat(*args, **kwargs):

    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    payload = {
        'device_id': device_id,
        'mem_total': memory_info.total,
        'mem_used': memory_info.used,
        'mem_free': memory_info.available,
        'disk_total': disk_info.total,
        'disk_used': disk_info.used,
        'disk_free': disk_info.free,
    }
    try:
        result = requests.post(url=beat_url, data=payload, timeout=beat_timeout).status_code
        if result != 200:
            print(f'Failed to send heartbeat. Response code is {result}')
        else:
            print('Heartbeat sent')
    except Exception as exc:
        print(f'Failed to send heartbeat: {exc}')


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
