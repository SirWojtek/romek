
class ATErrorException(Exception):
    pass

class ATMessage:
    ok = 'AT+OK'
    error = 'AT+ERROR'

    def get(self):
        raise NotImplementedError()

    def translate_answer(self, message):
        if message == ATMessage.ok:
            return True
        elif message == ATMessage.error:
            raise ATErrorException()
        raise Exception('Reveived incorrect message')

    def isAnswer(self, message):
        return message == ATMessage.ok or message == ATMessage.error

