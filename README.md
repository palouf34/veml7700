# veml7700
this library dedicated to micropython is used to communicate with  the VEML7700 light sensor
in a simple and fast way, while controlling the usage parameters

usage: 
```python
from machine import Pin, I2C
import veml7700

i2c = I2C(0)
i2c = I2C(1, scl=Pin(22), sda=Pin(21), freq=10000)

veml = veml7700.VEML7700(address=0x10, i2c=i2c, it=100, gain=1/8)

lux_val = veml.read_lux()
```

Parameters:

`address`: The I2C address of the sensor, standard is `0x10`

`i2c`: The I2C bus object

`it`: The integration time of the sensor, standard is `25 ms`
Available times are: `25, 50, 100, 200, 400, 800 ms`

`gain`: The gain of the sensor, standard is `1/8`
Available gains are: `1/8, 1/4, 1, 2`
