#!/bin/python2

from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject
import server
import argparse

parser = argparse.ArgumentParser(description='Runs romek d-bus server')
parser.add_argument('--test_mode', '-t', action = 'store_true', help='Run server in serial port test mode')

def main():
    dbus_loop = DBusGMainLoop(set_as_default = True)
    bus = dbus.SessionBus(mainloop = dbus_loop)
    romek = server.RomekServer(bus)
    _mock_serial_port_for_test_mode(romek)

    gobject.MainLoop().run()

def _mock_serial_port_for_test_mode(server):
    if parser.parse_args().test_mode:
        import serial
        server._serial_port_manager._worker._serial = serial.serial_for_url('loop://', timeout=1)

if __name__ == '__main__':
    main()
