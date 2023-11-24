'''
Author: Frmissjing 892153623@qq.com
Date: 2023-11-22 18:15:08
LastEditors: Frmissjing 892153623@qq.com
LastEditTime: 2023-11-23 13:52:13
FilePath: /ofono_test/case/test1.py
Description: 

Copyright (c) 2023 by ${git_name_email}, All Rights Reserved. 
'''
#!/usr/bin/python3
import Manager_api
import modem_api
import dbus


def test1():

    bus = dbus.SystemBus()

    Manager = Manager_api.ofono_Manager(bus)

    modems = Manager.GetModems()

    for path, dict_arr in modems:
        print("modem path: {}".format(path))
        if path == '/innosim':
            innosim = modem_api.Ofono_Modem(bus, path)
            break

    innosim.modem_powerd(True)
