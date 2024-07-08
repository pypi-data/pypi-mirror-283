"""
DPS Sensor Library

This library provides functions to interface with the Infineon DPS310 pressure sensor.

Author: Powen Ko
Email: powenkoads@gmail.com

Note: I am seeking a programming job in the US. If you have any opportunities, please contact me at the above email.

Copyright (c) 2024 Powen Ko

GPT License v3:

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import smbus2

I2C_BUS = 1  # I2C bus number
DPS310_ADDRESSES = [0x77, 0x76]  # Possible I2C addresses for the DPS310 sensor

class dps:
    def __init__(self):
        self.bus = smbus2.SMBus(I2C_BUS)  # Initialize the I2C bus
        self.addr = self.find_address()  # Find the I2C address of the sensor
        self.__correctTemperature()  # Correct temperature calibration
        self.__setOversamplingRate()  # Set oversampling rate

    def find_address(self):
        # Try to find the sensor on known addresses
        for address in DPS310_ADDRESSES:
            try:
                self.bus.read_byte(address)
                return address
            except IOError:
                continue
        raise Exception("DPS310 sensor not found on any known address")

    def getTwosComplement(self, raw_val, length):
        # Calculate two's complement for signed integer representation
        val = raw_val
        if raw_val & (1 << (length - 1)):
            val = raw_val - (1 << length)
        return val

    def __correctTemperature(self):
        # Correct the temperature readings
        self.bus.write_byte_data(self.addr, 0x0E, 0xA5)
        self.bus.write_byte_data(self.addr, 0x0F, 0x96)
        self.bus.write_byte_data(self.addr, 0x62, 0x02)
        self.bus.write_byte_data(self.addr, 0x0E, 0x00)
        self.bus.write_byte_data(self.addr, 0x0F, 0x00)

    def __setOversamplingRate(self):
        # Set the oversampling rate for temperature and pressure readings
        self.bus.write_byte_data(self.addr, 0x06, 0x26)
        self.bus.write_byte_data(self.addr, 0x07, 0xA6)
        self.bus.write_byte_data(self.addr, 0x08, 0x07)
        self.bus.write_byte_data(self.addr, 0x09, 0x0C)

    def __getRawTemperature(self):
        # Read raw temperature data from the sensor
        t1 = self.bus.read_byte_data(self.addr, 0x03)
        t2 = self.bus.read_byte_data(self.addr, 0x04)
        t3 = self.bus.read_byte_data(self.addr, 0x05)
        t = (t1 << 16) | (t2 << 8) | t3
        t = self.getTwosComplement(t, 24)
        return t

    def __getRawPressure(self):
        # Read raw pressure data from the sensor
        p1 = self.bus.read_byte_data(self.addr, 0x00)
        p2 = self.bus.read_byte_data(self.addr, 0x01)
        p3 = self.bus.read_byte_data(self.addr, 0x02)
        p = (p1 << 16) | (p2 << 8) | p3
        p = self.getTwosComplement(p, 24)
        return p

    def calcScaledTemperature(self):
        # Calculate scaled temperature
        raw_t = self.__getRawTemperature()
        scaled_t = raw_t / 1040384  # __kT = 1040384
        return scaled_t

    def calcCompTemperature(self, scaled_t):
        # Calculate compensated temperature
        c0, c1 = self.__getTemperatureCalibrationCoefficients()
        comp_t = c0 * 0.5 + scaled_t * c1
        return comp_t

    def calcScaledPressure(self):
        # Calculate scaled pressure
        raw_p = self.__getRawPressure()
        scaled_p = raw_p / 1040384  # __kP = 1040384
        return scaled_p

    def calcCompPressure(self, scaled_p, scaled_t):
        # Calculate compensated pressure
        c00, c10, c20, c30, c01, c11, c21 = self.__getPressureCalibrationCoefficients()
        comp_p = (c00 + scaled_p * (c10 + scaled_p * (c20 + scaled_p * c30))
                  + scaled_t * (c01 + scaled_p * (c11 + scaled_p * c21)))
        return comp_p

    def __getTemperatureCalibrationCoefficients(self):
        # Get temperature calibration coefficients from the sensor
        src10 = self.bus.read_byte_data(self.addr, 0x10)
        src11 = self.bus.read_byte_data(self.addr, 0x11)
        src12 = self.bus.read_byte_data(self.addr, 0x12)
        c0 = (src10 << 4) | (src11 >> 4)
        c0 = self.getTwosComplement(c0, 12)
        c1 = ((src11 & 0x0F) << 8) | src12
        c1 = self.getTwosComplement(c1, 12)
        return c0, c1

    def __getPressureCalibrationCoefficients(self):
        # Get pressure calibration coefficients from the sensor
        src13 = self.bus.read_byte_data(self.addr, 0x13)
        src14 = self.bus.read_byte_data(self.addr, 0x14)
        src15 = self.bus.read_byte_data(self.addr, 0x15)
        src16 = self.bus.read_byte_data(self.addr, 0x16)
        src17 = self.bus.read_byte_data(self.addr, 0x17)
        src18 = self.bus.read_byte_data(self.addr, 0x18)
        src19 = self.bus.read_byte_data(self.addr, 0x19)
        src1A = self.bus.read_byte_data(self.addr, 0x1A)
        src1B = self.bus.read_byte_data(self.addr, 0x1B)
        src1C = self.bus.read_byte_data(self.addr, 0x1C)
        src1D = self.bus.read_byte_data(self.addr, 0x1D)
        src1E = self.bus.read_byte_data(self.addr, 0x1E)
        src1F = self.bus.read_byte_data(self.addr, 0x1F)
        src20 = self.bus.read_byte_data(self.addr, 0x20)
        src21 = self.bus.read_byte_data(self.addr, 0x21)

        c00 = (src13 << 12) | (src14 << 4) | (src15 >> 4)
        c00 = self.getTwosComplement(c00, 20)

        c10 = ((src15 & 0x0F) << 16) | (src16 << 8) | src17
        c10 = self.getTwosComplement(c10, 20)

        c20 = (src1C << 8) | src1D
        c20 = self.getTwosComplement(c20, 16)

        c30 = (src20 << 8) | src21
        c30 = self.getTwosComplement(c30, 16)

        c01 = (src18 << 8) | src19
        c01 = self.getTwosComplement(c01, 16)

        c11 = (src1A << 8) | src1B
        c11 = self.getTwosComplement(c11, 16)

        c21 = (src1E << 8) | src1F
        c21 = self.getTwosComplement(c21, 16)

        return c00, c10, c20, c30, c01, c11, c21

    def read_temperature(self):
        # Read and return the compensated temperature
        scaled_t = self.calcScaledTemperature()
        temperature = self.calcCompTemperature(scaled_t)
        return temperature

    def read_pressure(self):
        # Read and return the compensated pressure
        scaled_t = self.calcScaledTemperature()
        scaled_p = self.calcScaledPressure()
        pressure = self.calcCompPressure(scaled_p, scaled_t)
        return pressure
    
