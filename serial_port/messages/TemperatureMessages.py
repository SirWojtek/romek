from ATMessage import ATMessage

class TemperatureGetMessage(ATMessage):
    temp_message_core = 'AT+TEMPERATURE'

    def get(self):
        return self.temp_message_core + '?'

    def translate_answer(self, message):
        temp = message.split('=')[1]
        return float(temp.replace(':', '.'))

    def isAnswer(self, message):
        return message.find(self.temp_message_core) != -1

class TemperatureSetMessage(ATMessage):
    temp_message_core = 'AT+TEMPERATURE='

    def __init__(self, temp):
        self._temp = temp

    def get(self):
        return "%s%d:0" % (self.temp_message_core, self._temp)

