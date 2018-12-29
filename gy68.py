#!/usr/bin/env python3

import ctypes
import time
import smbus

def get_short(data, index):
    return ctypes.c_short((data[index] << 8) + data[index + 1]).value


def get_ushort(data, index):
    return (data[index] << 8) + data[index + 1]


class Gy68():
    'BMP180 (gy-68) sensor'
    addr = 0x77
    bus_n = 1
    bus = smbus.SMBus(bus_n)

    def read_cal_data(self):
        "Reading calibration data from sensor"
        REG_CALIB = 0xAA
        BYTES = 22

        return self.bus.read_i2c_block_data(Gy68.addr, REG_CALIB, BYTES)

    def read_data(self):
        "Reading data from sensor"
        REG_MEAS = 0xF4
        CRV_TEMP = 0x2E
        REG_MSB = 0xF6
        self.bus.write_byte_data(Gy68.addr, REG_MEAS, CRV_TEMP)
        time.sleep(0.005)
        data = self.bus.read_i2c_block_data(Gy68.addr, REG_MSB, 2)
        result = (data[0] << 8) + data[1]
        return result

    def get_temperature(self):
        "Getting temperature from sensor"
        cal = self.read_cal_data()
        UT = self.read_data()

        AC5 = get_ushort(cal, 8)
        AC6 = get_ushort(cal, 10)
        MC = get_short(cal, 18)
        MD = get_short(cal, 20)

        X1 = ((UT - AC6) * AC5) >> 15
        X2 = (MC << 11) / (X1 + MD)
        B5 = X1 + X2
        temperature = (int(B5 + 8) >> 4) / 10.0

        return temperature

    def get_pressure(self):
        "WIP"
        return 42
