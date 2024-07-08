"""
PA_CO2 Sensor Library

This library provides functions to interface with the Infineon PA_CO2 sensor.

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
import time

class paco2:
    def __init__(self, device_address=0x28, period=10000):
        self.device_address = device_address  # I2C address of the PA_CO2 sensor
        self.period = period  # Measurement period in milliseconds
        self.bus = smbus2.SMBus(1)  # Initialize the I2C bus

    def read_byte(self, command):
        # Read a byte from the specified command register
        return self.bus.read_byte_data(self.device_address, command)

    def write_byte(self, command, value):
        # Write a byte to the specified command register
        self.bus.write_byte_data(self.device_address, command, value)

    def check_sensor_status(self):
        # Check the status of the sensor
        status = self.read_byte(0x01)
        return status

    def set_idle_mode(self):
        # Set the sensor to idle mode
        self.write_byte(0x04, 0x00)
        time.sleep(0.4)

    def set_pressure(self, high_byte=0x03, low_byte=0xF5):
        # Set the pressure for the sensor
        self.write_byte(0x0B, high_byte)
        self.write_byte(0x0C, low_byte)

    def trigger_measurement(self):
        # Trigger a single measurement
        self.write_byte(0x04, 0x01)
        time.sleep(1.15)

    def get_ppm_value(self):
        # Get the CO2 concentration in parts per million (ppm)
        value1 = self.read_byte(0x05)
        time.sleep(0.005)
        value2 = self.read_byte(0x06)
        time.sleep(0.005)
        result = (value1 << 8) | value2
        return result

    def measure_co2(self):
        # Measure the CO2 concentration
        self.set_idle_mode()
        self.set_pressure()
        self.trigger_measurement()
        ppm = self.get_ppm_value()
        return ppm
