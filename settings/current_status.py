import observable

class CurrentStatus(observable.Observable):
    def __init__(self, temperature = 10):
        self.temperature = temperature
        observable.Observable.__init__(self)

    @observable.update_decorator
    def update_temperature(self, temperature):
        self.temperature = temperature
