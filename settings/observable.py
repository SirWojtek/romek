
class Observable:
    def __init__(self):
        self.value = None
        self.observers = []

    def register(self, func):
        if not func in self.observers:
            self.observers.append(func)

    def unregister(self, func):
        if func in self.observers:
            self.observers.remove(func)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def update(self, value):
        self.update_notification(value)
        self.value = value

    def update_notification(self, new_value):
        for observer in self.observers:
            observer(new_value)

