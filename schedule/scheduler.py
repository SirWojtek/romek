from task import Task


class TemperatureUpdater:
    def __init__(self, settings):
        self._settings = settings
        self._temperature = self._settings.temperature

    def start_update_temperature(self, temperature):
        self._temperature = self._settings.temperature
        self._settings.update_temperature(temperature)

    def end_update_temperature(self, temperature):
        self._settings.update_temperature(self._temperature)

class Scheduler:
    def __init__(self, settings):
        self._tasks = []
        self._temperature_updater = TemperatureUpdater(settings)

    def add_task(self, raw_task):
        self._tasks.append(self._create_temperature_task(raw_task))

    def update_task(self, raw_tasks):
        old_task = self._create_temperature_task(raw_tasks[0])
        new_task = self._create_temperature_task(raw_tasks[1])
        self._tasks = [ new_task if x == old_task else x for x in self._tasks ]

    def remove_task(self, raw_task):
        self._tasks.remove(self._create_temperature_task(raw_task))

    def list_tasks(self):
        return [ x.raw() for x in self._tasks ]

    def _create_temperature_task(self, raw_task):
        return Task(raw_task, self._temperature_updater.start_update_temperature,
            self._temperature_updater.end_update_temperature)
