#!/bin/python2
import dbus
import unittest
import subprocess
from time import sleep

server = None

def init_object(bus):
    iterations = 10
    sleep_time = 0.01

    for i in range(iterations):
        try:
            return bus.get_object('org.romek.service', '/org/romek/service')
        except dbus.DBusException:
            sleep(sleep_time)   

class TestServerSchedule(unittest.TestCase):
    def setUp(self):
        global server
        server = subprocess.Popen(['./server_main.py'])
        self.bus = dbus.SessionBus()
        self.interface = 'org.romek.interface'
        self.obj = init_object(self.bus)

        self.task1 = ('MO', (12,0), 'MO', (13,0), 13)
        self.task2 = ('F', (14,30), 'SA', (6,15), 21)

    def tearDown(self):
        global server
        server.kill()

    def test_add_single_task(self):
        self.assertTrue(self.obj.add_schedule_task(self.task1, dbus_interface = self.interface))
        self.assertListEqual(self.obj.list_schedule_task(), [ self.task1 ])

    def test_add_multiple_tasks(self):
        self.assertTrue(self.obj.add_schedule_task(self.task1, dbus_interface = self.interface))
        self.assertTrue(self.obj.add_schedule_task(self.task2, dbus_interface = self.interface))
        self.assertListEqual(self.obj.list_schedule_task(), [ self.task1, self.task2 ])

if __name__ == '__main__':
    unittest.main()
