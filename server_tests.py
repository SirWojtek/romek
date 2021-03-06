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
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    StatusQuery = 'AT'
    Ok = 'AT+OK'
    Error = 'AT+ERROR'
    TemperatureQuery = 'AT+TEMPERATURE?'

    @staticmethod
    def ir_status(status):
        return 'AT+IR=' + status

    @staticmethod
    def lcd_status(status):
        return 'AT+LCD_BKT=' + status

    @staticmethod
    def temperature_status(temperature):
        strTemp = ('%.1f' % temperature).replace('.', ':')
        return 'AT+TEMPERATURE=' + strTemp

    @staticmethod
    def time_status(time):
        return 'AT+TIME=' + time.__str__()

    @staticmethod
    def date_status(date):
        return "AT+DATE=" + date.strftime('%d:%m:%y')

    @staticmethod
    def log(message):
        return "LOG_" + message

class SocketCommunitator(threading.Thread):
    def __init__(self, connection, to_receive, to_send):
        self._connection = connection
        self._to_receive = to_receive
        self._to_send = to_send
        self.received = None
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.received = self._connection.recv(128)
        # print (received, self._to_receive)
        self._connection.send(self._to_send + '\n')
        # print self._to_send
        # sleep(.1)  # performance reasons

    def join(self):
        join_timeout = .5
        threading.Thread.join(self, join_timeout)

class TestServerSchedule(unittest.TestCase):
    _test_port = 7777

    def setUp(self):
        global test_port
        global sock

        self.server = subprocess.Popen(['./server_main.py' ,'--test_mode_port', str(test_port)])
        self.connection, addr = sock.accept()
        self.bus = dbus.SessionBus()
        self.interface = 'org.romek.interface'
        self.obj = init_object(self.bus)

        self.task1 = ('M', (12, 0), 'M', (13, 0), 13)
        self.task2 = ('F', (14, 30), 'SA', (6, 15), 21)
        self.task3 = ('SU', (9, 30), 'TU', (9, 30), 28)

        self.temp = 23
        self.communicator_timeout = .5

        self.temp_message = ATMessage.temperature_status(self.temp)

    def tearDown(self):
        self.server.kill()
        self.server.communicate()
        self.connection.close()

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

    def test_set_and_get_temperature_settings_ok(self):
        com = SocketCommunitator(self.connection, self.temp_message, ATMessage.Ok)
        self.assertTrue(self.obj.set_temperature_settings(self.temp, dbus_interface = self.interface))
        self.assertEqual(self.obj.get_temperature_settings(dbus_interface = self.interface), self.temp)
        com.join()
        self.assertEqual(com.received, self.temp_message)

    def test_set_and_get_temperature_settings_nok(self):
        com = SocketCommunitator(self.connection, self.temp_message,
            ATMessage.Error)
        self.assertFalse(self.obj.set_temperature_settings(self.temp, dbus_interface = self.interface))
        self.assertNotEqual(self.obj.get_temperature_settings(dbus_interface = self.interface), self.temp)
        com.join()
        self.assertEqual(com.received, self.temp_message)

    def test_set_and_get_manual_mode(self):
        self.assertTrue(self.obj.set_manual_mode(True, dbus_interface = self.interface))
        self.assertTrue(self.obj.get_manual_mode(dbus_interface = self.interface))

    def test_set_temperature_settings_and_get_manual_mode(self):
        com = SocketCommunitator(self.connection, self.temp_message, ATMessage.Ok)
        self.assertFalse(self.obj.get_manual_mode(dbus_interface = self.interface))
        self.assertTrue(self.obj.set_temperature_settings(self.temp, dbus_interface = self.interface))
        self.assertTrue(self.obj.get_manual_mode(dbus_interface = self.interface))
        com.join()
        self.assertEqual(com.received, self.temp_message)

    def test_at_ok_message(self):
        com = SocketCommunitator(self.connection, ATMessage.StatusQuery, ATMessage.Ok)
        self.assertTrue(self.obj.get_driver_status(dbus_interface = self.interface))
        com.join()
        self.assertEqual(com.received, ATMessage.StatusQuery)

    def test_at_error_message(self):
        com = SocketCommunitator(self.connection, ATMessage.StatusQuery, ATMessage.Error)
        self.assertFalse(self.obj.get_driver_status(dbus_interface = self.interface))
        com.join()
        self.assertEqual(com.received, ATMessage.StatusQuery)

    def test_get_temperature_status_after_change(self):
        com = SocketCommunitator(self.connection, ATMessage.TemperatureQuery,
            ATMessage.temperature_status(self.temp))
        self.assertEqual(self.obj.get_temperature_status(dbus_interface = self.interface), self.temp)
        com.join()
        self.assertEqual(com.received, ATMessage.TemperatureQuery)

    def test_get_temperature_history_after_change(self):
        temps = [ 22, 21, 20, 21, 23, 25 ]
        for temp in temps:
            con = SocketCommunitator(self.connection, ATMessage.TemperatureQuery,
                    ATMessage.temperature_status(temp))
            self.assertEqual(self.obj.get_temperature_status(dbus_interface = self.interface), temp)
            con.join()
            self.assertEqual(con.received, ATMessage.TemperatureQuery)
        temps_with_timestamp = self.obj.get_temperature_history(dbus_interface = self.interface)
        self.assertEqual(len(temps_with_timestamp), len(temps))
        for i in range(len(temps_with_timestamp)):
            self.assertEqual(temps_with_timestamp[i][0], temps[i])

    def test_async_log_message_receive(self):
        # received log message can not be checked here
        self.connection.send(ATMessage.log("test") + '\n')
        self.test_get_temperature_status_after_change()

    # TODO: write async serial message send test

if __name__ == '__main__':
    unittest.main()
