import observable

class CurrentStatus(observable.Observable):
    def __init__(self):
        observable.Observable.__init__(self)

