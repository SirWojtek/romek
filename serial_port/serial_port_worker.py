import serial
import threading

class SerialPortWorker(threading.Thread):
    _timeout = 0.1

    def __init__(self, receive_callback):
        threading.Thread.__init__(self)
        self._serial = serial.Serial(0, timeout = self._timeout)
        self._messages_to_send = []
        self._send_event = threading.Event()
        self._send_lock = threading.Lock()
        self._receive_callback = receive_callback

    def add_message(self, message):
        self._send_lock.acquire()
        self._messages_to_send.append(message)
        self._send_lock.release()
        self._send_event.set()

    def run(self):
        while True:
            if self._send_event.wait(self._timeout):
                self._send_lock.acquire()
                self._send_message()
                self._send_event.clear()
                self._send_lock.release()
            self._receive_message()

    # thread safe must be ensured by caller
    def _send_message(self):
        for message in self._messages_to_send:
            self._serial.write(message.get())
            self._serial.flush()

    def _receive_message(self):
        message = self._serial.readline()
        if message:
            self._receive_callback(message)
