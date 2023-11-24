'''
Author: Frmissjing 892153623@qq.com
Date: 2023-11-22 18:15:08
LastEditors: Frmissjing 892153623@qq.com
LastEditTime: 2023-11-23 14:08:55
FilePath: /ofono_test/common/modem_api.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
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


# Signals		PropertyChanged(string name, variant value)

# 			    This signal indicates a changed value of the given
# 			    property.
    def PropertyChanged(self, isMornitor, func):
        if isMornitor:
            self.interface.connect_to_signal("PropertyChanged", func)


# Function     def modem_powerd(self, powerd):
    def modem_powerd(self, powerd):
        return self.SetProperty("Powered", dbus.Boolean(powerd))


    def modem_online(self, online):
        return self.SetProperty("Online",dbus.Boolean(online))



