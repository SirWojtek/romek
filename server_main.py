#!/bin/python2

from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject
import server
import argparse
from printer.Printer import Printer

parser = argparse.ArgumentParser(description = 'Runs romek d-bus server')
parser.add_argument('--test_mode_port', '-t', type = int, help = 'Run server in serial port test mode on TCP socket')
parser.add_argument('--verbose', '-v', action = 'store_true', help = 'Produces additional prints')

def main():
    gobject.threads_init()
    dbus.mainloop.glib.threads_init()

    dbus_loop = DBusGMainLoop(set_as_default = True)
    bus = dbus.SessionBus(mainloop = dbus_loop)
    romek = server.RomekServer(bus)
    args = parser.parse_args()
    _mock_serial_port_for_test_mode(romek, args)
    _verbose(args)

    gobject.MainLoop().run()

def _mock_serial_port_for_test_mode(server, args):
    if args.test_mode_port:
        import serial
        server._serial_port_manager._worker._serial =serial.serial_for_url(
            'socket://localhost:%d' % (parser.parse_args().test_mode_port), timeout = 0.1)

def _verbose(args):
    Printer.set_print(args.verbose)

if __name__ == '__main__':
    main()
