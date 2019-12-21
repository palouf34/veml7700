#standard libraries
from machine import Pin, I2C

#this library
import veml7700

#setup i2c bus
i2c = I2C(0)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=10000)

#setup sensor with intergartion time 100 ms and gain 1/8
veml = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

#read the ambient light brightness
lux_val = veml.read_lux()

