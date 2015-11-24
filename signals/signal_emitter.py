
class SignalEmitter:
    def __init__(self, settings, status, signals):
        self._signals = signals
        settings.register(self.update_settings)
        status.register(self.update_status)

    # callback functions
    def update_settings(self, settings):
        self._signals['temperature_change'](settings.temperature)

    def update_status(self, status):
        self._signals['temperature_status'](status.temperature)
