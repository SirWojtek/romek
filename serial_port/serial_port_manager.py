from serial_port_worker import SerialPortWorker
import threading

class SerialPortManager:
    def __init__(self, current_settings, status):
        current_settings.register(self.update)
        self._status = status
        self._worker = SerialPortWorker(self.message_received)
        self._worker.setDaemon(True)
        self._worker.start()
        self._answer_received = threading.Event()
        self._answer = ''

    # settings change callback
    def update(self, settings):
        # TODO: write serial port send implementation
        pass

    def send_and_receive(self, message):
        self._worker.add_message(message)
        self._wait_for_answer(message)
        return message.translate_answer(self._return_and_clear_answer())

    # received message callback
    def message_received(self, message):
        # TODO: remove 'temp_change' implementation
        if message.find('temp_change') != -1:
            a = message.split(' ')
            if (len(a) > 1):
                self._status.update_temperature(int(a[1]))
        else:
            self._write_answer(message)

    def _write_answer(self, message):
        self._answer = message.replace('\n', '')
        self._answer_received.set()

    def _wait_for_answer(self, message):
        while not message.isAnswer(self._answer):
            self._answer_received.wait()

    def _return_and_clear_answer(self):
        answer, self._answer = self._answer, ''
        self._answer_received.clear()
        return answer

