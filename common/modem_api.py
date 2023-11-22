#!/usr/bin/python3
import common_api
import dbus


class Ofono_Modem(object):
    'Ofono Modem'

    def __init__(self,bus,path):
        self.interface = dbus.Interface(bus.get_object('org.ofono', path),
						'org.ofono.Modem')


# Methods		dict GetProperties()

# 			    Returns properties for the modem object. See
# 			    the properties section for available properties.
    def GetProperties(self):
       return self.interface.GetProperties()


# Methods       SetProperty(string property, variant value)

# 	            Changes the value of the specified property. Only
# 	            properties that are listed as readwrite are
# 	            changeable. On success a PropertyChanged signal
# 	            will be emitted.
    def SetProperty(self, property, value):
       return self.interface.SetProperty(property, value)

# Function     def modem_powerd(self, powerd):
    def modem_powerd(self, powerd):
        try:
            self.SetProperty("Powered", dbus.Boolean(powerd))
        except:
            print("modem Powered={} fail".format(powerd))


    def modem_online(self, online):
        try:
            self.SetProperty("Online",dbus.Boolean(online))
        except:
            print("modem Online={} fail".format(online))


# Signals		PropertyChanged(string name, variant value)

# 			    This signal indicates a changed value of the given
# 			    property.
    def PropertyChanged(self, isMornitor, func):
        if isMornitor:
            self.interface.connect_to_signal("PropertyChanged", func)






