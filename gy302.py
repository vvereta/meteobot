#!/usr/bin/env python3

import time
import smbus

class Gy302():
    'BH1715 (gy-302) sensor'
    addr = 0x23
    bus_n = 1
    command_on = 0x01
    command_read = 0x10
    bus = smbus.SMBus(bus_n)

    def write(self):
        "Sending command to sensor"
        self.bus.write_byte(Gy302.addr, Gy302.command_on)
        self.bus.write_byte(Gy302.addr, Gy302.command_read)
        time.sleep(0.2)

    def read(self):
        "Reading data from sensor"
        data = self.bus.read_i2c_block_data(Gy302.addr, 2)
        result = (data[0] * 256 + data[1])
        return result

    def get_luminance(self):
        "Getting luminance from sensor"
        self.write()
        data = self.read()
        luminance = data / 1.2
        return luminance
