
class SerialPortManager:
    def __init__(self, current_settings):
        current_settings.register(self)

    # callback function
    def update(self, settings):
        # TODO: write serial port send implementation
        pass

