from task_builder import TaskBuilder

class Scheduler:
    def __init__(self, settings):
        self._tasks = []
        self._settings = settings

    def add_task(self, raw_task):
        self._tasks.append(TaskBuilder.build_temperature_task(self._settings, raw_task))

    def update_task(self, raw_tasks):
        old_task = TaskBuilder.build_temperature_task(self._settings, raw_tasks[0])
        new_task = TaskBuilder.build_temperature_task(self._settings, raw_tasks[1])
        self._tasks = [ new_task if x == old_task else x for x in self._tasks ]

    def remove_task(self, raw_task):
        self._tasks.remove(TaskBuilder.build_temperature_task(self._settings, raw_task))

    def list_tasks(self):
        return [ x.raw() for x in self._tasks ]
