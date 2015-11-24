
class Observable:
    def __init__(self):
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

    def update_notification(self):
        for observer in self.observers:
            observer(self)


def update_decorator(func):
    def func_wrapper(self, value):
        func(self, value)
        self.update_notification()
    return func_wrapper
