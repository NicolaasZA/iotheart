import logging
import signal
import sys

import mysql.connector
from bottle import Bottle, request, abort

app = Bottle()

sql = """
update heartbeat
set
    beat_datetime_utc = now(),
    mem_total = %s,
    mem_used = %s,
    mem_free = %s,
    disk_total = %s,
    disk_used = %s,
    disk_free = %s
where device_id = %s;
"""


def connect_db():
    return mysql.connector.connect(host="server_ip_here", user="iotheart_server", database="iotheart", password="75#fGh3Xc&mf254")


def add_heartbeat_to_db(device_id: str, mt, mu, mf, dt, du, df):
    db = connect_db()
    cur = db.cursor()

    cur.execute(sql, (mt, mu, mf, dt, du, df, device_id))

    db.commit()
    cur.close()
    db.close()


def optional(value: object, fallback=0):
    return value if (value != '' and value is not None) else fallback


def receive_heartbeat():
    device_id: str = request.params.device_id
    mem_total: int = optional(request.params.mem_total)
    mem_used: int = optional(request.params.mem_used)
    mem_free: int = optional(request.params.mem_free)
    disk_total: int = optional(request.params.disk_total)
    disk_used: int = optional(request.params.disk_used)
    disk_free: int = optional(request.params.disk_free)

    if not device_id:
        abort(400, 'missing device_id')
        return
    add_heartbeat_to_db(device_id, mem_total, mem_used, mem_free, disk_total, disk_used, disk_free)


def stop(sig=0, frame=None):
    logging.getLogger().info(f"Stopping application with sig={sig}")
    app.close()
    sys.exit(sig)


# Register listeners for termination signals so the app can be gracefully stopped
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

try:
    app.route(path='/api/beat', method='POST', callback=receive_heartbeat)
    app.run(host='0.0.0.0', port=1111)
except Exception as exc:
    logging.getLogger().exception("Stopping app due to exception", exc_info=True)
    stop()
