#!/bin/python2

from dbus.mainloop.glib import DBusGMainLoop
import dbus
import gobject
import server

def main():
    dbus_loop = DBusGMainLoop(set_as_default = True)
    bus = dbus.SessionBus(mainloop = dbus_loop)
    romek = server.RomekServer(bus)

    gobject.MainLoop().run()

if __name__ == '__main__':
    main()
