#!/usr/bin/env python3

import time
import smbus

class Gy21():
    'SI7021 (gy-21) sensor'
    addr = 0x40
    bus_n = 1
    command_t = 0xF3
    command_h = 0xF5
    bus = smbus.SMBus(bus_n)

    def read(self):
        "Reading data from sensor"
        data1 = self.bus.read_byte(Gy21.addr)
        data2 = self.bus.read_byte(Gy21.addr)
        result = data1 * 256 + data2
        return result

    def write(self, command):
        "Sending command to sensor"
        self.bus.write_byte(Gy21.addr, command)
        time.sleep(0.2)

    def get_temperature(self):
        "Getting temperature from sensor"
        self.write(Gy21.command_t)
        data = self.read()
        cels_temp = (data * 175.72 / 65536.0) - 46.85

        return cels_temp

    def get_humidity(self):
        "Getting humidity from sensor"
        self.write(Gy21.command_h)
        data = self.read()
        humidity = (data * 125 / 65536.0) - 6

        return humidity

    def get_tmpr_and_hmdt(self):
        "Getting temperature and humidity from sensor"
        data = [0, 0]
        data[0] = self.get_temperature()
        data[1] = self.get_humidity()

        return data
