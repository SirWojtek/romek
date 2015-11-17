from task import Task

class Scheduler:
    def __init__(self):
        self._tasks = []

    def add_task(self, raw_task):
        self._tasks.append(Task(raw_task))

    def update_task(self, raw_tasks):
        old_task = Task(raw_tasks[0])
        new_task = Task(raw_tasks[1])
        self._tasks = [ new_task if x == old_task else x for x in self._tasks ]

    def remove_task(self, raw_task):
        self._tasks.remove(Task(raw_task))

    def list_tasks(self):
        return [ x.raw() for x in self._tasks ]
