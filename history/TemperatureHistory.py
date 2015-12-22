from collections import deque
from time import time
from datetime import datetime

class TemperatureHistory:
    max_results = 100

    def __init__(self, current_status):
        self._temperature_list = deque(maxlen = TemperatureHistory.max_results)
        current_status.register(self.update_notification)

    def update_notification(self, status):
        self.add(status.temperature)

    def add(self, temperature):
        timestamp = datetime.fromtimestamp(time())
        self._temperature_list.append((temperature, timestamp))

    def get_list(self):
        return [ (x, y.year, y.month, y.day, y.hour, y.minute, y.second)
            for x, y in self._temperature_list ]

    def clear(self):
        self._temperature_list.clear()
