# Copyright (c) 2019 Joseph Hopfmüller
# This module is a fork of Christophe Rousseaus module. 
# see: https://github.com/palouf34/veml7700.git
# 
# Original coypright notices are reproduced below.
# Changes:
#   - fixed critical error in value calculation
#   - restructured the constants into dictionaries
#       -> with this you have to pass the integration time and gain when initializing the module
# 
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# 
# 
# Original copyright notices:
# 
# Authors: Christophe ROUSSEAU, 2019
#
# This module borrows from the DFROBOT VEML7700 Python library. Original
# Copyright notices are reproduced below.
#
# Those libraries were written for the NODEMCU(LOLIN). This modification is
# intended for the MicroPython and esp8266 boards.
#
#
# Based on the BH1750 driver with VMEL7700 changes provided by
# Auteur : iTechnoFrance
#
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from machine import I2C, Pin
import time
from micropython import const

#start const
# default address
addr = const(0x10)

# Write registers
als_conf_0 = const(0x00)
als_WH = const(0x01)
als_WL = const(0x02)
pow_sav = const(0x03)

# Read registers
als = const(0x04)
white = const(0x05)
interrupt = const(0x06)

#gain            0.125                    0.25                    1                        2                         integration time
confValues = {  25: {1/8: bytearray([0x00, 0x13]), 1/4: bytearray([0x00,0x1B]), 1: bytearray([0x00, 0x01]), 2: bytearray([0x00, 0x0B])}, #25
                50: {1/8: bytearray([0x00, 0x12]), 1/4: bytearray([0x00,0x1A]), 1: bytearray([0x00, 0x02]), 2: bytearray([0x00, 0x0A])}, #50
                100:{1/8: bytearray([0x00, 0x10]), 1/4: bytearray([0x00,0x18]), 1: bytearray([0x00, 0x00]), 2: bytearray([0x00, 0x08])}, #100
                200:{1/8: bytearray([0x40, 0x10]), 1/4: bytearray([0x40,0x18]), 1: bytearray([0x40, 0x00]), 2: bytearray([0x40, 0x08])}, #200
                400:{1/8: bytearray([0x80, 0x10]), 1/4: bytearray([0x80,0x18]), 1: bytearray([0x80, 0x00]), 2: bytearray([0x80, 0x08])}, #400
                800:{1/8: bytearray([0xC0, 0x10]), 1/4: bytearray([0xC0,0x18]), 1: bytearray([0xC0, 0x00]), 2: bytearray([0xC0, 0x08])}} #800

#gain               0.125,  0.25,   1,      2       integration time
gainValues = {  25: {1/8: 1.8432, 1/4: 0.9216, 1: 0.2304, 2: 0.1152}, #25
                50: {1/8: 0.9216, 1/4: 0.4608, 1: 0.1152, 2: 0.0576}, #50
                100:{1/8: 0.4608, 1/4: 0.2304, 1: 0.0288, 2: 0.0144}, #100
                200:{1/8: 0.2304, 1/4: 0.1152, 1: 0.0288, 2: 0.0144}, #200
                400:{1/8: 0.1152, 1/4: 0.0576, 1: 0.0144, 2: 0.0072}, #400
                800:{1/8: 0.0876, 1/4: 0.0288, 1: 0.0072, 2: 0.0036}} #800


# fin des constante

# Reference data sheet Table 1 for configuration settings

interrupt_high = bytearray([0x00, 0x00]) # Clear values
# Reference data sheet Table 2 for High Threshold

interrupt_low = bytearray([0x00, 0x00]) # Clear values
# Reference data sheet Table 3 for Low Threshold

power_save_mode= bytearray([0x00, 0x00]) # clear values
# Reference data sheet Table 4 for Power Saving Modes


class VEML7700:

    def __init__(self,
                 address=addr,
                 i2c=None,
                 it=25,
                 gain=1/8,
                 **kwargs):
       
        self.address = address
        if i2c is None:
            raise ValueError('An I2C object is required.')
        self.i2c = i2c

        confValuesForIt = confValues.get(it)
        gainValuesForIt = gainValues.get(it)
        if confValuesForIt is not None and gainValuesForIt is not None:
            confValueForGain = confValuesForIt.get(gain)
            gainValueForGain = gainValuesForIt.get(gain)
            if confValueForGain is not None and gainValueForGain is not None:
                self.confValues = confValueForGain
                self.gain = gainValueForGain
            else:
                raise ValueError('Wrong gain value. Use 1/8, 1/4, 1, 2')
        else:
            raise ValueError('Wrong integration time value. Use 25, 50, 100, 200, 400, 800')

        self.init()

    def init(self):
       
        # load calibration data
        #self.i2c.writeto_mem(self.address, als_conf_0, bytearray([0x00,0x13]) )
        self.i2c.writeto_mem(self.address, als_conf_0, self.confValues )
        self.i2c.writeto_mem(self.address, als_WH, interrupt_high )
        self.i2c.writeto_mem(self.address, als_WL, interrupt_low)
        self.i2c.writeto_mem(self.address, pow_sav, power_save_mode)
        
    def detect(self):
        """ Functions is  verified is  module has detecedself.

        this function not implemented for this time
        """
        None
        
    def read_lux(self):
        """ Reads the data from the sensor and returns the data.
            
            Returns:
               the number of lux detect by this captor.
        """
       	#The frequency to read the sensor should be set greater than
        # the integration time (and the power saving delay if set).
        # Reading at a faster frequency will not cause an error, but
        # will result in reading the previous data

        self.lux = bytearray(2)
        
        time.sleep(.04)  # 40ms

        self.i2c.readfrom_mem_into(self.address, als, self.lux)
        self.lux= self.lux[0]+self.lux[1]*256
        self.lux=self.lux*self.gain
        return(int(round(self.lux,0)))
        
    

