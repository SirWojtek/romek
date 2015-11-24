
class SerialPortManager:
    def __init__(self, current_settings, status):
        current_settings.register(self.update)
        self._status = status

    # callback function
    def update(self, settings):
        # TODO: write serial port send implementation
        pass
