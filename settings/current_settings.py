import observable

class CurrentSettings(observable.Observable):
    def __init__(self, temperature = 20, manual_mode = False):
        self.temperature = temperature
        self.manual_mode = manual_mode
        observable.Observable.__init__(self)

    @observable.update_decorator
    def update_temperature(self, temperature):
        self.temperature = temperature

    @observable.update_decorator
    def update_manual_mode(self, manual_mode):
        self._manual_mode = manual_mode
