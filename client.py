#!/bin/python2
import dbus

bus = dbus.SessionBus()

obj = bus.get_object('org.romek.service', '/org/romek/service')

reply = obj.hello_world(dbus_interface = 'org.romek.interface')

print reply
