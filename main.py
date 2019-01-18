#import standard library
import machine
import time

from ustruct import unpack, unpack_from, calcsize
from array import array

import ubinascii

# import special library
import veml7700


# address  of external captor
vmle7700_addr = 0x10

# activate i2c port
i2c = machine.I2C(scl=machine.Pin(5),sda=machine.Pin(4))

capteur_lumiere = veml7700.VEML7700(vmle7700_addr,
                                     i2c,
                                     "confValues25_18",
                                     "gain25_18")

#start software

#start scan i2c buss
print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))

#end scan i2c bus

print("start reading")
i=0
while i<4:
  
  #read the coptor values   
  
  
  mesure_lux = capteur_lumiere.read_lux()
  print("Values of  VLME7700 : ")
  print("The value is  ", mesure_lux, " lux")
  time.sleep(1)
  i=i+1


