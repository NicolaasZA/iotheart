import mysql.connector
import logging
import signal
import sys

from bottle import Bottle, request, abort

app = Bottle()


def connect_db():
    return mysql.connector.connect(host="192.168.50.10", user="iotheart_server", database="iotheart", password="75#fGh3Xc&mf254")


def add_heartbeat_to_db(device_id: str):
    db = connect_db()
    cur = db.cursor()

    cur.execute('update heartbeat set beat_datetime_utc = now() where device_id = %s;', (device_id,))

    db.commit()
    cur.close()
    db.close()


def receive_heartbeat():
    device_id: str = request.params.get('device_id')
    if not device_id:
        abort(400, 'missing device_id')
        return
    add_heartbeat_to_db(device_id)


def stop(sig=0, frame=None):
    logging.getLogger().info(f"Stopping application with sig={sig}")
    app.close()
    sys.exit(sig)


# Register listeners for termination signals so the app can be gracefully stopped
signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)


try:
    app.route(path='/api/beat', method='POST', callback=receive_heartbeat)
    app.run(port=1111)
except Exception as exc:
    logging.getLogger().exception("Stopping app due to exception", exc_info=True)
    stop()
