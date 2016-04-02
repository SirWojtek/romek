import observable

class CurrentSettings:
    def __init__(self):
        self.manual_mode = ManualModeSetting()
        self.temperature = TemperatureSetting(self.manual_mode)

class TemperatureSetting(observable.Observable):
    def __init__(self, manual_mode):
        self.manual_mode = manual_mode
        observable.Observable.__init__(self)

    def update_temperature_manual(self, temperature):
        self.manual_mode.update(True)
        self.update(temperature)

class ManualModeSetting(observable.Observable):
    def __init__(self):
        observable.Observable.__init__(self)

