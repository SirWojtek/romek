from serial_port_worker import SerialPortWorker

class SerialPortManager:
    def __init__(self, current_settings, status):
        current_settings.register(self.update)
        self._status = status
        self._worker = SerialPortWorker(self.message_received)

    # settings change callback
    def update(self, settings):
        # TODO: write serial port send implementation
        pass

    # received message callback
    def message_received(self, message):
        print message
        if message.find('temp_change') != -1:
            a = message.split(' ')
            self._status.update_temperature(int(a[1]))
