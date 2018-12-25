#!/usr/bin/env python3

import smbus
import time

class Gy21():
    'SI7021 (gy-21) sensor'
    addr = 0x40
    bus_n = 1
    command_t = 0xF3
    command_h = 0xF5
    bus = smbus.SMBus(bus_n)

    def read(self):
        data = Gy21.bus.read_byte(Gy21.addr)
        data = data * 256 + data
        return data

    def write(self, command):
        Gy21.bus.write_byte(Gy21.addr, command)
        time.sleep(0.2)

    def get_temperature(self):
        self.write(Gy21.command_t)
        data = self.read()
        celsTemp = (data * 175.72 / 65536.0) - 46.85

        return celsTemp

    def get_humidity(self):
        self.write(Gy21.command_h)
        data = self.read()
        humidity = (data * 125 / 65536.0) - 6

        return humidity

    def get_tmpr_and_hmdt(self):
        data = [0, 0]
        data[0] = self.get_temperature()
        data[1] = self.get_humidity()

        return data