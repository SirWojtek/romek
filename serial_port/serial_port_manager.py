from serial_port_worker import SerialPortWorker

class SerialPortManager:
    def __init__(self, current_settings, status):
        current_settings.register(self.update)
        self._status = status
        self._worker = SerialPortWorker(self.message_received)
        self._worker.setDaemon(True)
        self._worker.start()

    # settings change callback
    def update(self, settings):
        # TODO: write serial port send implementation
        pass

    # received message callback
    def message_received(self, message):
        if message.find('temp_change') != -1:
            a = message.split(' ')
            if (len(a) > 1):
                self._status.update_temperature(int(a[1]))
