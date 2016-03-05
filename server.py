import dbus.service
from schedule.scheduler import Scheduler
from settings.current_settings import CurrentSettings
from settings.current_status import CurrentStatus
from serial_port.serial_port_manager import SerialPortManager
from serial_port.messages.ATMessage import ATErrorException
from serial_port.messages.StatusMessage import StatusMessage
from serial_port.messages.TemperatureMessages import TemperatureGetMessage
from history.TemperatureHistory import TemperatureHistory
from printer.Printer import Printer
from defaults import defaults
from functools import partial


def safe_schedule_call(method):
    try:
        method()
    except Exception as e:
        Printer.write(e)
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
    temperature_history_signature = 'a(uuuuuuu)'

    def __init__(self, bus):
        self._bus_name = dbus.service.BusName(self.service_name, bus)
        self._current_settings = CurrentSettings()
        self._current_status = CurrentStatus()
        self._scheduler = Scheduler(self._current_settings)
        self._serial_port_manager = SerialPortManager(
            self._current_settings.temperature, self._current_status)
        self._temp_history = TemperatureHistory(self._current_status)
        self._set_defaults()
        dbus.service.Object.__init__(self, bus, self.service_object)

    def _set_defaults(self):
        self._current_settings.temperature.value = defaults['temperature_settings']
        self._current_settings.manual_mode.value = defaults['manual_mode']
        self._current_status.temperature = defaults['temperature_status']

    ###################### dbus methods ###########################################

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 's')
    def hello_world(self):
        return 'Hello World!'

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = task_tuple_signature, out_signature = 'b')
    def add_schedule_task(self, task):
        Printer.write('add_schedule_task: ')
        Printer.write(task)
        return safe_schedule_call(partial(self._scheduler.add_task, task))

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = edit_task_signature, out_signature = 'b')
    def update_schedule_task(self, tasks):
        Printer.write('update_schedule_task: ')
        Printer.write(tasks)
        return safe_schedule_call(partial(self._scheduler.update_task, tasks))

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = task_tuple_signature, out_signature = 'b')
    def remove_schedule_task(self, task):
        Printer.write('remove_schedule_task: ')
        Printer.write(task)
        return safe_schedule_call(partial(self._scheduler.remove_task, task))

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = task_list_signature)
    def list_schedule_task(self):
        Printer.write('list_schedule_task')
        return self._scheduler.list_tasks()

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 'b')
    def get_driver_status(self):
        try:
            self._serial_port_manager.send_and_receive(StatusMessage())
            return True
        except ATErrorException:
            Printer.write('Received AT+ERROR')
            return False

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = 'u', out_signature = 'b')
    def set_temperature_settings(self, temperature):
        Printer.write('set_temperature_settings: ')
        Printer.write(temperature)
        try:
            self._current_settings.temperature.update_temperature_manual(temperature)
            return True
        except ATErrorException:
            Printer.write('Received AT+ERROR')
            return False

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 'u')
    def get_temperature_settings(self):
        Printer.write('get_temperature_settings')
        return self._current_settings.temperature.value

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 'b')
    def get_manual_mode(self):
        Printer.write('get_manual_mode')
        return self._current_settings.manual_mode.value

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = 'b', out_signature = 'b')
    def set_manual_mode(self, manual_mode):
        Printer.write('set_manual_mode')
        self._current_settings.manual_mode.update(manual_mode)
        return True

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = 'u')
    def get_temperature_status(self):
        Printer.write('get_temperature_status')
        temp_status = self._serial_port_manager.send_and_receive(
            TemperatureGetMessage())
        self._current_status.update(temp_status)
        return temp_status

    @dbus.service.method(dbus_interface = interface_name,
        in_signature = '', out_signature = temperature_history_signature)
    def get_temperature_history(self):
        Printer.write('get_temperature_history')
        return self._temp_history.get_list()
