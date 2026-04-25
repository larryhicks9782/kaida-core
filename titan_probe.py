import requests
import time
import datetime
import threading

class AdaptiveProbe:
    """Adaptive Conduit Probe Protocol [ACPP v1.0]"""
    def __init__(self, target_url='http://www.google.com/generate_204', max_backoff=3600):
        self.target = target_url
        self.max_backoff = max_backoff
        self.attempt_count = 0
        self.backoff_time = 1 
        self.conduit_live = False
        self._thread = None
        self._stop_event = threading.Event()

    def log(self, message, status):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        # Internal silent logging for the OS logs
        with open("probe_logs.txt", "a") as f:
            f.write(f"[{timestamp}] [{status}] {message}\n")

    def _probe_loop(self):
        while not self._stop_event.is_set():
            try:
                response = requests.head(self.target, timeout=5)
                if response.ok:
                    self.conduit_live = True
                    self.log("SUCCESS: Conduit is open.", "ESTABLISHED")
                    break # Stop probing once restored
            except Exception as e:
                self.conduit_live = False
                self.attempt_count += 1
                self.log(f"Attempt {self.attempt_count}: Signal failed.", "FAILURE")
                
                time.sleep(self.backoff_time)
                self.backoff_time = min(self.backoff_time * 2, self.max_backoff)

    def start(self):
        """Launches the probe as a background process."""
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._probe_loop, daemon=True)
            self._thread.start()

    def status(self):
        return "LIVE" if self.conduit_live else "PROBING"
