#!/usr/bin/python3
import common_api
import Manager_api
import modem_api
import dbus


def test1():

    common_api.test_init()

    bus = dbus.SystemBus()

    Manager = Manager_api.ofono_Manager(bus)

    modems = Manager.GetModems()

    for path, dict_arr in modems:
        print("modem path: {}".format(path))
        if path == '/innosim':
            innosim = modem_api.Ofono_Modem(bus, path)
            break

    innosim.modem_powerd(True)

    common_api.test_deinit()
