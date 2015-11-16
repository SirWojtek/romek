import dbus.service

class RomekServer(dbus.service.Object):
    service_name = 'org.romek.service'
    service_object = '/org/romek/service'
    interface_name = 'org.romek.interface'

    def __init__(self, bus):
        self._bus_name = dbus.service.BusName(self.service_name, bus)
        dbus.service.Object.__init__(self, bus, self.service_object)

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 's')
    def hello_world(self):
        return 'Hello World!'
