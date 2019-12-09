# simple time clock
import time

class clock:
    def __init__(self):
        self._now_time = None

    def tic(self):
        self._now_time = time.time()

    def toc(self):
        return time.time() - self._now_time