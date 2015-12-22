import observable

class CurrentSettings(observable.Observable):
    def __init__(self):
        self.temperature = None
        self.manual_mode = None
        observable.Observable.__init__(self)

    def update_temperature_manual(self, temperature):
        self.update_manual_mode(True)
        self.update_temperature(temperature)

    @observable.update_decorator
    def update_temperature(self, temperature):
        self.temperature = temperature

    @observable.update_decorator
    def update_manual_mode(self, manual_mode):
        self.manual_mode = manual_mode
