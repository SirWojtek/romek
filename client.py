#!/bin/python2
import dbus

bus = dbus.SessionBus()

obj = bus.get_object('org.romek.service', '/org/romek/service')

print obj.add_schedule_task(('MO', (12,0), 'MO', (13,0), 13), dbus_interface = 'org.romek.interface')

print obj.list_schedule_task(dbus_interface = 'org.romek.interface')
