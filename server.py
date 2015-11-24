import dbus.service
from schedule.scheduler import Scheduler
from settings.current_settings import CurrentSettings
from settings.current_status import CurrentStatus
from serial_port.serial_port_manager import SerialPortManager
from signals.signal_emitter import SignalEmitter
from functools import partial

def safe_schedule_call(method):
    try:
        method()
    except Exception as e:
        print e
        return False
    return True

class RomekServer(dbus.service.Object):
    service_name = 'org.romek.service'
    service_object = '/org/romek/service'
    interface_name = 'org.romek.interface'

    task_signature = 's(uu)s(uu)u'
    task_tuple_signature = '(%s)' % task_signature
    edit_task_signature = '(%s%s)' % (task_tuple_signature, task_tuple_signature)
    task_list_signature = 'a%s' % task_tuple_signature

    def __init__(self, bus):
        signal_map = {
            'temperature_change' : self.temperature_change,
            'temperature_status' : self.temperature_status
        }

        self._bus_name = dbus.service.BusName(self.service_name, bus)
        self._current_settings = CurrentSettings()
        self._current_status = CurrentStatus()
        self._scheduler = Scheduler(self._current_settings)
        self._serial_port_manager = SerialPortManager(self._current_settings, self._current_status)
        self._signal_emitter = SignalEmitter(self._current_settings, self._current_status, signal_map)
        dbus.service.Object.__init__(self, bus, self.service_object)

    ###################### dbus methods ###########################################

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 's')
    def hello_world(self):
        return 'Hello World!'

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = task_tuple_signature, out_signature = 'b')
    def add_schedule_task(self, task):
        return safe_schedule_call(partial(self._scheduler.add_task, task))

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = edit_task_signature, out_signature = 'b')
    def update_schedule_task(self, task):
        return safe_schedule_call(partial(self._scheduler.update_task, task))

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = task_tuple_signature, out_signature = 'b')
    def remove_schedule_task(self, task):
        return safe_schedule_call(partial(self._scheduler.remove_task, task))

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = task_list_signature)
    def list_schedule_task(self):
        return self._scheduler.list_tasks()

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = 'u', out_signature = 'b')
    def set_temperature(self, temperature):
        self._current_settings.update_temperature_manual(temperature)
        return True

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 'u')
    def get_temperature(self):
        return self._current_settings.temperature

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 'b')
    def get_manual_mode(self):
        return self._current_settings.manual_mode

    ####################### dbus signals ########################################

    @dbus.service.signal(dbus_interface = interface_name, signature = 'u')
    def temperature_change(self, new_temperature):
        pass

    @dbus.service.signal(dbus_interface = interface_name, signature = 'u')
    def temperature_status(self, new_temperature):
        pass
