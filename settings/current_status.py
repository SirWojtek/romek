import observable

class CurrentStatus(observable.Observable):
    def __init__(self, temperature = -1):
        self.temperature = temperature
        observable.Observable.__init__(self)

    @observable.update_decorator
    def update_temperature(self, temperature):
        self.temperature = temperature