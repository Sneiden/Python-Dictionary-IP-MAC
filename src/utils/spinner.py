import sys
import threading
import itertools
import time

class Spinner:
    """
    Displays an animated CLI spinner in a background thread
    while a blocking task is running.
    """

    def __init__(self, message: str = "Loading..."):
        self.message = message
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin)

    def _spin(self):
        for frame in itertools.cycle(["|", "/", "—", "\\"]):
            if self._stop_event.is_set():
                break
            sys.stdout.write(f"\r{frame} {self.message}")
            sys.stdout.flush()
            time.sleep(0.1)
        sys.stdout.write("\r" + " " * (len(self.message) + 2) + "\r")
        sys.stdout.flush()

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()