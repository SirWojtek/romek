from task import Task

class Scheduler:
    def __init__(self):
        self._tasks = []

    def add_task(self, raw_task):
        self._tasks.append(Task(raw_task))

    def update_task(self, raw_tasks):
        old_task = Task(raw_tasks[0])
        found = next(x for x in self._tasks if x == old_task)
        found = Task(raw_tasks[0])

    def remove_task(self, raw_task):
        self._tasks.remove(Task(raw_tasks[0]))

    def list_tasks(self):
        return [ x.raw() for x in self._tasks ]
