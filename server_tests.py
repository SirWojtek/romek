#!/bin/python2
import dbus
import unittest
import subprocess
import threading
import gobject
import socket
from datetime import date, time
from time import sleep
from dbus.mainloop.glib import DBusGMainLoop
from defaults import defaults

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

class ATMessage:
    Ok = 'AT+OK'
    Error = 'AT+ERROR'

    @staticmethod
    def ir_status(status):
        return 'AT+IR=' + status

    @staticmethod
    def lcd_status(status):
        return 'AT+LCD_BKT=' + status

    @staticmethod
    def temperature_status(temperature):
        strTemp = ('%.2f' % temperature).replace('.', ':')
        return 'AT+TEMPERATURE=' + strTemp

    @staticmethod
    def time_status(time):
        return 'AT+TIME=' + time.__str__()

    @staticmethod
    def date_status(date):
        return "AT+DATE=" + date.strftime('%d:%m:%y')

class TestServerSchedule(unittest.TestCase):
    _test_port = 7777

    def setUp(self):
        global test_port
        global sock

        self.server = subprocess.Popen(['./server_main.py', '--test_mode_port', str(test_port)])
        self.connection, addr = sock.accept()
        self.bus = dbus.SessionBus()
        self.interface = 'org.romek.interface'
        self.obj = init_object(self.bus)

        self.task1 = ('M', (12, 0), 'M', (13, 0), 13)
        self.task2 = ('F', (14, 30), 'SA', (6, 15), 21)
        self.task3 = ('SU', (9, 30), 'TU', (9, 30), 28)

        self.temp = 23

    def write_serial_message(self, message):
        sleep_time = .1
        self.connection.send(message + '\n')
        sleep(sleep_time)

    def write_serial_temp_change(self, new_temp):
        self.write_serial_message('temp_change %d' % (new_temp))

    def tearDown(self):
        self.server.kill()
        self.server.communicate()
        self.connection.shutdown(socket.SHUT_RDWR)

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

    def test_set_and_get_temperature_settings(self):
        self.assertTrue(self.obj.set_temperature_settings(self.temp, dbus_interface = self.interface))
        self.assertEqual(self.obj.get_temperature_settings(dbus_interface = self.interface), self.temp)

    def test_set_and_get_manual_mode(self):
        self.assertTrue(self.obj.set_manual_mode(True, dbus_interface = self.interface))
        self.assertTrue(self.obj.get_manual_mode(dbus_interface = self.interface))

    def test_set_temperature_settings_and_get_manual_mode(self):
        self.assertFalse(self.obj.get_manual_mode(dbus_interface = self.interface))
        self.assertTrue(self.obj.set_temperature_settings(self.temp, dbus_interface = self.interface))
        self.assertTrue(self.obj.get_manual_mode(dbus_interface = self.interface))

    def test_at_ok_message(self):
        self.write_serial_message(ATMessage.Ok)
        self.assertTrue(self.obj.get_driver_status(dbus_interface = self.interface))

    def test_at_error_message(self):
        self.write_serial_message(ATMessage.Error)
        self.assertFalse(self.obj.get_driver_status(dbus_interface = self.interface))

    def test_get_temperature_status_after_change(self):
        # TODO: replace when AT message interface will be ready
        self.write_serial_temp_change(self.temp)
        self.assertEqual(self.obj.get_temperature_status(dbus_interface = self.interface), self.temp)

    def test_get_temperature_history(self):
        history = self.obj.get_temperature_history(dbus_interface = self.interface)
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0][0], defaults['temperature_status'])

    def test_get_temperature_history_after_change(self):
        temps = [ 22, 21, 20, 21, 23, 25 ]
        for temp in temps:
            self.write_serial_temp_change(temp)
        temps_with_timestamp = self.obj.get_temperature_history(dbus_interface = self.interface)
        # because of default value at begining of history
        self.assertEqual(len(temps) + 1, len(temps_with_timestamp))
        for i in range(1, len(temps_with_timestamp)):
            self.assertEqual(temps_with_timestamp[i][0], temps[i - 1])

if __name__ == '__main__':
    unittest.main()
