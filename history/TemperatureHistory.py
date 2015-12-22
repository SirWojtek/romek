from collections import deque

class TemperatureHistory:
    max_results = 100

    def __init__(self, current_status):
        self._temperature_list = deque(maxlen = TemperatureHistory.max_results)
        current_status.register(self.update_notification)

    def update_notification(self, status):
        self.add(status.temperature)

    def add(self, temperature):
        self._temperature_list.append(temperature)

    def get_list(self):
        return list(self._temperature_list)

    def clear(self):
        self._temperature_list.clear()
