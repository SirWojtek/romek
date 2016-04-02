from serial_port_worker import SerialPortWorker
from async_message_handler import AsyncMessageHandler
from messages.TemperatureMessages import TemperatureSetMessage
import threading

class SerialPortManager:
    def __init__(self, temperature_setting, status):
        temperature_setting.register(self.update_temperature)
        self._status = status
        self._worker = SerialPortWorker(self.message_received)
        self._worker.setDaemon(True)
        self._worker.start()
        self._waiting_for_answer_event = threading.Event()
        self._answer_received_event = threading.Event()
        self._answer = ''

    # settings change callback
    def update_temperature(self, temperature):
        self.send_and_receive(TemperatureSetMessage(temperature))

    def send_and_receive(self, message):
        self._waiting_for_answer_event.set()
        self._worker.add_message(message)
        self._wait_for_answer(message)
        self._waiting_for_answer_event.clear()
        return message.translate_answer(self._return_and_clear_answer())

    # received message callback
    def message_received(self, message):
        message = message.replace('\n', '')
        if self._waiting_for_answer_event.is_set():
            self._answer = message
            self._answer_received_event.set()
        else:
            AsyncMessageHandler.handle_async_message(message)

    def _wait_for_answer(self, message):
        self._answer_received_event.wait()
        while not message.isAnswer(self._answer):
            AsyncMessageHandler.handle_async_message(self._answer)
            self._answer_received_event.clear()
            self._answer_received_event.wait()

    def _return_and_clear_answer(self):
        answer, self._answer = self._answer, ''
        self._answer_received_event.clear()
        return answer

