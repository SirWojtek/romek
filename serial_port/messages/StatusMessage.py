from ATMessage import ATMessage

class StatusMessage(ATMessage):
    def get(self):
        return 'AT'

