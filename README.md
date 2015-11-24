# romek
DBus server for serial communication with ATMega

## Dependencies
- dbus
- python-dbus
- pygtk
- apscheduler (pip)
- pyserial (pip)

## How to allow not-root user access serial port?
Serial ports in Linux are mapped as device in /dev folder as ttyS*.
By default all devs are owned by root, and not-root user cannot access it.
To allow user control serial port you can:
- change owner of /dev/ttyS*,
- add your user to serial ports owner group (recomended way).

To add user to right group you need:

1. Get know what group owns ttyS*:
`ls -l /dev | grep ttyS`

2. Add user to group:
`usermod -a -G group_name user_name`

Don't forget about logout and login again after this operation!

