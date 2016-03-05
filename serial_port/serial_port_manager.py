from serial_port_worker import SerialPortWorker
from messages.TemperatureMessages import TemperatureSetMessage
import threading

class SerialPortManager:
    def __init__(self, temperature_setting, status):
        temperature_setting.register(self.update_temperature)
        self._status = status
        self._worker = SerialPortWorker(self.message_received)
        self._worker.setDaemon(True)
        self._worker.start()
        self._answer_received = threading.Event()
        self._answer = ''

    # settings change callback
    def update_temperature(self, temperature):
        self.send_and_receive(TemperatureSetMessage(temperature))

    def send_and_receive(self, message):
        self._worker.add_message(message)
        self._wait_for_answer(message)
        return message.translate_answer(self._return_and_clear_answer())

    # received message callback
    def message_received(self, message):
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

