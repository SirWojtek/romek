import serial
import threading

class SerialPortWorker(threading.Thread):
    _timeout = 0.1

    def __init__(self, receive_callback):
        threading.Thread.__init__(self)
        self._serial = serial.Serial(0, timeout = self._timeout)
        self._message_to_send = None
        self._send_event = threading.Event()
        self._send_lock = threading.Lock()
        self._receive_callback = receive_callback

    def add_message(self, message):
        self._send_lock.acquire()
        if self._message_to_send:
            raise Exception('Previous message not handled')
        self._message_to_send = message
        self._send_lock.release()
        self._send_event.set()

    def run(self):
        while True:
            if self._send_event.wait(self._timeout):
                self._send_message()
            self._receive_message()

    # thread safe must be ensured by caller
    def _send_message(self):
        self._send_lock.acquire()
        self._serial.write(self._message_to_send.get())
        self._message_to_send = None
        self._send_event.clear()
        self._send_lock.release()

    def _receive_message(self):
        message = self._serial.readline()
        if message:
            self._receive_callback(message)
