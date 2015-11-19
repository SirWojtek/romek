from datetime import time
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial

days_map = {
    'M' : 0,
    'TU' : 1,
    'W' : 2,
    'TH' : 3,
    'F' : 4,
    'SA' : 5,
    'SU' : 6 }

class Task:
    def __init__(self, task, start_function, end_function):
        self._init_task_data(task)
        self._init_scheduler(start_function, end_function)

    def _init_task_data(self, task):
        self.start_day = task[0]
        self.start_time = time(hour = task[1][0], minute = task[1][1])
        self.end_day = task[2]
        self.end_time = time(hour = task[3][0], minute = task[3][1])
        self.status = task[4]

    def _init_scheduler(self, start_function, end_function):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(partial(start_function, self.status), 'cron',
            day_of_week = days_map[self.start_day],
            hour = self.start_time.hour,
            minute = self.start_time.minute)
        self.scheduler.add_job(partial(end_function, self.status), 'cron',
            day_of_week = days_map[self.end_day],
            hour = self.end_time.hour,
            minute = self.end_time.minute)
        self.scheduler.start()

    def raw(self):
        return ( self.start_day, (self.start_time.hour, self.start_time.minute),
            self.end_day, (self.end_time.hour, self.end_time.minute), self.status)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.start_day == other.start_day and self.start_time == other.start_time
            and self.end_day == other.end_day and self.end_time == self.end_time)

    def __ne__(self, other):
        return not self.__eq__(other)
