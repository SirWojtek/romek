from datetime import time

class Task:
    def __init__(self, task):
        self.start_day = task[0]
        self.start_time = time(hour = task[1][0], minute = task[1][1])
        self.end_day = task[2]
        self.end_time = time(hour = task[3][0], minute = task[3][1])
        self.status = task[4]

    def raw(self):
        return ( self.start_day, (self.start_time.hour, self.start_time.minute),
            self.end_day, (self.end_time.hour, self.end_time.minute), self.status)
