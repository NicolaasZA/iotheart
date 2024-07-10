"""
Async timer for repeated function calls.
by Rodrigo Silva [https://github.com/MestreLion]
"""

import threading
import time


class RepeatedTimer():
    """Creates a separate thread that acts as a daemon, spawning a new thread every 'interval' seconds and calling 'function'."""

    def __init__(self, interval, function, *args, **kwargs):
        threading.current_thread().setName(f"RepeatedTimer_{function.__name__}") 
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.next_call = time.time()
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        try:
            self.function(*self.args, **self.kwargs)
        except KeyboardInterrupt:
            self.stop()

    def start(self):
        if not self.is_running:
            self.next_call += self.interval
            self._timer = threading.Timer(self.next_call - time.time(), self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

    def __str__(self):
        return f"RepeatedTimer <{self.function.__name__} every {self.interval} seconds>"
