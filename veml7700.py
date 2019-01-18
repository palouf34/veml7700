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


# These settings will provide the all range for the sensor (0-120Klx)
# but at the lowest precision:
#                       LSB   MSB
# 1/8 gain, 25ms IT (Integration Time)
confValues25_18 = bytearray([0x00, 0x13])
# 1/4 gain, 25ms IT (Integration Time)
confValues25_14 = bytearray([0x00,0x1B])
# 1 gain, 25ms IT (Integration Time)
confValues25_1 = bytearray([0x00, 0x01])
# 2 gain, 25ms IT (Integration Time)
confValues25_2 = bytearray([0x00, 0x0B])

# 1/8 gain, 50ms IT (Integration Time)
confValues50_18 = bytearray([0x00, 0x12])
# 1/4 gain, 50ms IT (Integration Time)
confValues50_14 = bytearray([0x00, 0x1A])
# 1 gain, 50ms IT (Integration Time)
confValues50_1 = bytearray([0x00, 0x02])
# 2 gain, 50ms IT (Integration Time)
confValues50_2 = bytearray([0x00, 0x0A])

# 1/8 gain, 100ms IT (Integration Time)
confValues100_18 = bytearray([0x00, 0x10])
# 1/4 gain, 100ms IT (Integration Time)
confValues100_14 = bytearray([0x00, 0x18])
# 1 gain, 100ms IT (Integration Time)
confValues100_1 = bytearray([0x00, 0x00])
# 2 gain, 100ms IT (Integration Time)
confValues100_2 = bytearray([0x00, 0x08])

# 1/8 gain, 200ms IT (Integration Time)
confValues200_18 = bytearray([0x40, 0x10])
# 1/4 gain, 200ms IT (Integration Time)
confValues200_14 = bytearray([0x40, 0x18])
# 1 gain, 200ms IT (Integration Time)
confValues200_1 = bytearray([0x40, 0x00])
# 2 gain, 200ms IT (Integration Time)
confValues200_2 = bytearray([0x40, 0x08])

# 1/8 gain, 400ms IT (Integration Time)
confValues400_18 = bytearray([0x80, 0x10])
# 1/4 gain, 400ms IT (Integration Time)
confValues400_14 = bytearray([0x80, 0x18])
# 1 gain, 400ms IT (Integration Time)
confValues400_1 = bytearray([0x80, 0x00])
# 2 gain, 400ms IT (Integration Time)
confValues400_2 = bytearray([0x80, 0x08])

# 1/8 gain, 800ms IT (Integration Time)
confValues800_18 = bytearray([0xC0, 0x10])
# 1/4 gain, 800ms IT (Integration Time)
confValues800_14 = bytearray([0xC0, 0x18])
# 1 gain, 800ms IT (Integration Time)
confValues800_1 = bytearray([0xC0, 0x00])
# 2 gain, 800ms IT (Integration Time)
confValues800_2 = bytearray([0xC0, 0x08])


# These settings will provide the max light level for the sensor (0-120Klx)
# but at the lowest precision:

# 1/8 gain, 25ms IT (Integration Time)
gain25_18 = 1.8432
# 1/4 gain, 25ms IT (Integration Time)
gain25_14 = 0.9216
# 1 gain, 25ms IT (Integration Time)
gain25_1 = 0.2304
# 2 gain, 25ms IT (Integration Time)
gain25_2 = 0.1152

# 1/8 gain, 50ms IT (Integration Time)
gain50_18 = 0.9216
# 1/4 gain, 50ms IT (Integration Time)
gain50_14 = 0.4608
# 1 gain, 50ms IT (Integration Time)
gain50_1 = 0.1152
# 2 gain, 50ms IT (Integration Time)
gain50_2 = 0.0576

# 1/8 gain, 100ms IT (Integration Time)
gain100_18 = 0.4608
# 1/4 gain, 100ms IT (Integration Time)
gain100_14 = 0.2304
# 1 gain, 100ms IT (Integration Time)
gain100_1 = 0.0288
# 2 gain, 100ms IT (Integration Time)
gain100_2 = 0.0144

# 1/8 gain, 200ms IT (Integration Time)
gain200_18 = 0.2304
# 1/4 gain, 200ms IT (Integration Time)
gain200_14 = 0.1152
# 1 gain, 200ms IT (Integration Time)
gain200_1 = 0.0288
# 2 gain, 200ms IT (Integration Time)
gain200_2 = 0.0144

# 1/8 gain, 400ms IT (Integration Time)
gain400_18 = 0.1152
# 1/4 gain, 400ms IT (Integration Time)
gain400_14 = 0.0576
# 1 gain, 400ms IT (Integration Time)
gain400_1 = 0.0144
# 2 gain, 400ms IT (Integration Time)
gain400_2 = 0.0072

# 1/8 gain, 800ms IT (Integration Time)
gain800_18 = 0.0876
# 1/4 gain, 800ms IT (Integration Time)
gain800_14 = 0.0288
# 1 gain, 800ms IT (Integration Time)
gain800_1 = 0.0072
# 2 gain, 800ms IT (Integration Time)
gain800_2 = 0.0036

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
                 confValues=confValues100_18,
                 gain=gain100_18,
                 **kwargs):
       
        self.address = address
        if i2c is None:
            raise ValueError('An I2C object is required.')
        self.i2c = i2c
        if confValues == "confValues800_2":
            self.confValues = confValues800_2
        elif confValues == "confValues800_1":
            self.confValues = confValues800_1
        elif confValues == "confValues800_14":
            self.confValues = confValues800_14
        elif confValues == "confValues800_18":
            self.confValues = confValues800_18
        elif confValues == "confValues400_2":
            self.confValues = confValues400_2
        elif confValues == "confValues400_1":
            self.confValues = confValues400_1
        elif confValues == "confValues400_14":
            self.confValues = confValues400_14
        elif confValues == "confValues400_18":
            self.confValues = confValues400_18
        elif confValues == "confValues200_2":
                self.confValues = confValues200_2
        elif confValues == "confValues200_1":
            self.confValues = confValues200_1
        elif confValues == "confValues200_14":
            self.confValues = confValues200_14
        elif confValues == "confValues200_18":
            self.confValues = confValues200_18
        elif confValues == "confValues100_2":
                self.confValues = confValues100_2
        elif confValues == "confValues100_1":
            self.confValues = confValues100_1
        elif confValues == "confValues100_14":
            self.confValues = confValues100_14
        elif confValues == "confValues100_18":
            self.confValues = confValues100_18
        elif confValues == "confValues50_2":
                self.confValues = confValues50_2
        elif confValues == "confValues50_1":
            self.confValues = confValues50_1
        elif confValues == "confValues50_14":
            self.confValues = confValues50_14
        elif confValues == "confValues50_18":
            self.confValues = confValues50_18
        elif confValues == "confValues25_2":
                self.confValues = confValues25_2
        elif confValues == "confValues25_1":
            self.confValues = confValues25_1
        elif confValues == "confValues25_14":
            self.confValues = confValues25_14
        elif confValues == "confValues25_18":
            self.confValues = confValues25_18
        else :
            self.confValues = confValues100_18


        #self.confValues = confValues
        if gain == "gain800_2":
            self.gain=gain800_2
        elif gain == "gain800_1":
            self.gain=gain800_1
        elif gain == "gain800_14":
            self.gain=gain800_14
        elif gain == "gain800_18":
            self.gain=gain800_18
        elif gain == "gain400_2":
            self.gain=gain400_2
        elif gain == "gain400_1":
            self.gain=gain400_1
        elif gain == "gain400_14":
            self.gain=gain400_14
        elif gain == "gain400_18":
            self.gain=gain400_18
        elif gain == "gain200_2":
            self.gain=gain200_2
        elif gain == "gain200_1":
            self.gain=gain200_1
        elif gain == "gain200_14":
            self.gain=gain200_14
        elif gain == "gain200_18":
            self.gain=gain200_18
        elif gain == "gain100_2":
            self.gain=gain100_2
        elif gain == "gain100_1":
            self.gain=gain100_1
        elif gain == "gain100_14":
            self.gain=gain100_14
        elif gain == "gain100_18":
            self.gain=gain100_18
        elif gain == "gain50_2":
            self.gain=gain50_2
        elif gain == "gain50_1":
            self.gain=gain800_1
        elif gain == "gain50_14":
            self.gain=gain50_14
        elif gain == "gain50_18":
            self.gain=gain50_18
        elif gain == "gain25_2":
            self.gain=gain25_2
        elif gain == "gain25_1":
            self.gain=gain25_1
        elif gain == "gain25_14":
            self.gain=gain25_14
        elif gain == "gain25_18":
            self.gain=gain25_18
        else :
            self.gain=gain100_18

        #self.gain = gain
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

        self.i2c.readfrom_mem_into(self.address, als,self.lux)
        self.lux= self.lux[0]+self.lux[1]
        self.lux=self.lux*self.gain
        return(int(self.lux))
        
    

