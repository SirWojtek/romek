
class Observable:
    def __init__(self):
        self.observers = []
 
    def register(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)
 
    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)
 
    def unregister_all(self):
        if self.observers:
            del self.observers[:]
 
    def update_notification(self):
        for observer in self.observers:
            observer.update(self)


def update_decorator(func):
    def func_wrapper(self, value):
        func(self, value)
        self.update_notification()
    return func_wrapper
