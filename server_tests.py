#!/bin/python2
import dbus
import unittest
import subprocess
import threading
import gobject
from time import sleep
from functools import partial
from dbus.mainloop.glib import DBusGMainLoop

############# Daemon setup ######################################

class DBusMainLoopThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        gobject.MainLoop().run()

gobject.threads_init()

main_loop_thread = DBusMainLoopThread()
main_loop_thread.setDaemon(True)
main_loop_thread.start()

#################################################################

def init_object(bus):
    iterations = 10
    sleep_time = 0.1
    for i in range(iterations):
        try:
            return bus.get_object('org.romek.service', '/org/romek/service')
        except dbus.DBusException:
            sleep(sleep_time)
    raise Exception('Could not get server object')

def signal_handler(was_called, sender):
    was_called.value = True

class BoleeanWrapper:
    def __init__(self):
        self.value = False

class TestServerSchedule(unittest.TestCase):
    def setUp(self):
        self.server = subprocess.Popen(['./server_main.py'])
        self.dbus_loop = DBusGMainLoop(set_as_default = True)
        self.bus = dbus.SessionBus(mainloop = self.dbus_loop)
        self.interface = 'org.romek.interface'
        self.obj = init_object(self.bus)

        self.task1 = ('M', (12, 0), 'M', (13, 0), 13)
        self.task2 = ('F', (14, 30), 'SA', (6, 15), 21)
        self.task3 = ('SU', (9, 30), 'TU', (9, 30), 28)

    def tearDown(self):
        self.server.kill()
        self.server.communicate()

    def test_add_multiple_tasks(self):
        self.assertTrue(self.obj.add_schedule_task(self.task1, dbus_interface = self.interface))
        self.assertTrue(self.obj.add_schedule_task(self.task2, dbus_interface = self.interface))
        self.assertListEqual(self.obj.list_schedule_task(), [ self.task1, self.task2 ])

    def test_add_multiple_tasks_and_remove_task(self):
        self.assertTrue(self.obj.add_schedule_task(self.task1, dbus_interface = self.interface))
        self.assertTrue(self.obj.add_schedule_task(self.task2, dbus_interface = self.interface))
        self.assertTrue(self.obj.remove_schedule_task(self.task1, dbus_interface = self.interface))
        self.assertListEqual(self.obj.list_schedule_task(), [ self.task2 ])

    def test_add_multiple_tasks_and_update_task(self):
        self.assertTrue(self.obj.add_schedule_task(self.task1, dbus_interface = self.interface))
        self.assertTrue(self.obj.add_schedule_task(self.task2, dbus_interface = self.interface))
        self.assertTrue(self.obj.update_schedule_task((self.task1, self.task3), dbus_interface = self.interface))
        self.assertListEqual(self.obj.list_schedule_task(), [ self.task3, self.task2 ])

    def test_set_and_get_temperature(self):
        temp = 23

        self.assertTrue(self.obj.set_temperature(temp, dbus_interface = self.interface))
        self.assertEqual(self.obj.get_temperature(dbus_interface = self.interface), temp)

    def test_set_temperature_and_get_manual_mode(self):
        temp = 23

        self.assertFalse(self.obj.get_manual_mode(dbus_interface = self.interface))
        self.assertTrue(self.obj.set_temperature(temp, dbus_interface = self.interface))
        self.assertTrue(self.obj.get_manual_mode(dbus_interface = self.interface))

    def test_set_temperature_and_get_temperature_change_signal(self):
        temp = 23
        was_handler_called = BoleeanWrapper()

        self.obj.connect_to_signal("temperature_change", partial(signal_handler, was_handler_called))
        self.assertTrue(self.obj.set_temperature(temp, dbus_interface = self.interface))
        self.assertTrue(was_handler_called)

if __name__ == '__main__':
    unittest.main()
