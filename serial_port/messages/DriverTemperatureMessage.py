from ATMessage import ATMessage

class DriverTemperatureMessage(ATMessage):
    temp_message_core = 'AT+TEMPERATURE'

    def get(self):
        return self.temp_message_core + '?'

    def translate_answer(self, message):
        temp = message.split('=')[1]
        return float(temp.replace(':', '.'))

    def isAnswer(self, message):
        return message.find(self.temp_message_core) != -1

