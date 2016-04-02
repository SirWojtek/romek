from task import Task

class TemperatureUpdater:
    def __init__(self, settings):
        self._settings = settings
        self._temperature = self._settings.temperature

    def start_function(self, temperature):
        if  not self._settings.manual_mode:
            self._temperature = self._settings.temperature
            self._settings.update_temperature(temperature)

    def end_function(self, temperature):
        if  not self._settings.manual_mode:
            self._settings.update_temperature(self._temperature)

class TaskBuilder:
    @staticmethod
    def build_temperature_task(settings, raw_task):
        updater = TemperatureUpdater(settings)
        return Task(raw_task, updater)

    @staticmethod
    def build_another_task(settings, raw_task):
        # TODO: write another builders for different updaters
        pass
