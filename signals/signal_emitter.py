
class SignalEmitter:
    def __init__(self, settings, signals):
        self._signals = signals
        settings.register(self)

    # callback function
    def update(self, settings):
        self._signals['temperature_change'](settings.temperature)