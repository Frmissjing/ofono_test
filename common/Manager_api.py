#!/usr/bin/python3
import common_api
import dbus


class ofono_Manager(object):
    'Ofono Manager'
    interface = None
    ModemNum = 0

    def __init__(self,bus):
        self.interface = dbus.Interface(bus.get_object('org.ofono', '/'),
                        'org.ofono.Manager')

# Methods	array{object,dict} GetModems()

# 		    Get an array of modem objects and properties
# 		    that represents the currently attached modems.

# 		    This method call should only be used once when an
# 		    application starts up.  Further modem additions
# 		    and removal shall be monitored via ModemAdded and
# 		    ModemRemoved signals.
    def GetModems(self):
        return self.interface.GetModems()


# Signals	ModemAdded(object path, dict properties)

# 			Signal that is sent when a new modem is added.  It
# 			contains the object path of new modem and also its
# 			properties.
    def AddModem(self, isMonitor = False, func = None):
        if(isMonitor):
            self.interface.connect_to_signal("AddModem", func)


# Signals	ModemRemoved(object path)

# 			Signal that is sent when a modem has been removed.
# 			The object path is no longer accessible after this
# 			signal and only emitted for reference
    def ModemRemoved(self, isMonitor = False, func = None):
        if(isMonitor):
            self.interface.connect_to_signal("ModemRemoved", func)



