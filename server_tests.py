#!/bin/python2
import dbus
import unittest
import subprocess
import threading
import gobject
import socket
from time import sleep
from dbus.mainloop.glib import DBusGMainLoop

############# Daemon setup ######################################

class DBusMainLoopThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        gobject.MainLoop().run()

gobject.threads_init()
dbus.mainloop.glib.threads_init()

main_loop_thread = DBusMainLoopThread()
main_loop_thread.setDaemon(True)
main_loop_thread.start()

#################################################################

sock = None
test_port = 7777

def setUpModule():
    global sock
    global test_port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', test_port))
    sock.listen(1)

def tearDownModule():
    global sock
    sock.close()

def init_object(bus):
    iterations = 100
    sleep_time = .1
    for i in range(iterations):
        try:
            return bus.get_object('org.romek.service', '/org/romek/service')
        except dbus.DBusException:
            sleep(sleep_time)
    raise Exception('Could not get server object')

class SignalWrapper:
    _timeout = .1

    def __init__(self):
        self.value = None
        self.event = threading.Event()

    # called from dbus thread
    def signal_handler(self, received_value):
        self.value = received_value
        self.event.set()

    def wait_for_signal(self):
        self.event.wait(self._timeout)

class TestServerSchedule(unittest.TestCase):
    _test_port = 7777

    def setUp(self):
        global test_port
        global sock

        self.server = subprocess.Popen(['./server_main.py', '--test_mode_port', str(test_port)])
        self.connection, addr = sock.accept()
        self.dbus_loop = DBusGMainLoop(set_as_default = True)
        self.bus = dbus.SessionBus(mainloop = self.dbus_loop)
        self.interface = 'org.romek.interface'
        self.obj = init_object(self.bus)

        self.task1 = ('M', (12, 0), 'M', (13, 0), 13)
        self.task2 = ('F', (14, 30), 'SA', (6, 15), 21)
        self.task3 = ('SU', (9, 30), 'TU', (9, 30), 28)

    def write_serial_message(self, message):
        self.connection.send(message + '\n')

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
        wrapper = SignalWrapper()

        self.obj.connect_to_signal("temperature_change", wrapper.signal_handler)
        self.assertTrue(self.obj.set_temperature(temp, dbus_interface = self.interface))
        wrapper.wait_for_signal()
        self.assertEqual(wrapper.value, temp)

    # @unittest.skip('skipping because of lacking feature')
    def test_get_temperature_status_after_change(self):
        change_temp = 23
        wrapper = SignalWrapper()

        self.obj.connect_to_signal("temperature_status", wrapper.signal_handler)
        self.write_serial_message('temp_change %d' % (change_temp))
        wrapper.wait_for_signal()
        self.assertEqual(wrapper.value, change_temp)

if __name__ == '__main__':
    unittest.main()
