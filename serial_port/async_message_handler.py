from printer.Printer import Printer

class AsyncMessageHandler:
    _message_to_callback_map = {
        "LOG_" : lambda message: Printer.write(message) }

    @classmethod
    def handle_async_message(cls, message):
        callbacks = (
            call for pattern, call in cls._message_to_callback_map.iteritems()
                if message.find(pattern) != -1)
        called = False
        for callback in callbacks:
            callback(message)
            called = True
        if not called:
            Printer.write("Unhandled async message: " + message)

