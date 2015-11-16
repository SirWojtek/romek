#!/bin/python2
import dbus
from dbus.mainloop.glib import DBusGMainLoop
import dbus.service
import gobject

dbus_loop = DBusGMainLoop(set_as_default = True)

class RomekServer(dbus.service.Object):
    def __init__(self, bus, object_path):
        dbus.service.Object.__init__(self, bus, object_path)

    @dbus.service.method(dbus_interface = 'org.romek.interface',
        in_signature = '', out_signature = 's')
    def hello_world(self):
        return 'Hello World!'

def main():
    bus = dbus.SessionBus(mainloop = dbus_loop)
    name = dbus.service.BusName("org.romek.service", bus)
    romek = RomekServer(bus, '/org/romek/service')

    gobject.MainLoop().run()


if __name__ == '__main__':
    main()
