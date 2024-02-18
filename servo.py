from time import sleep
from machine import Pin, PWM
# this file for High | Low heart rate

from machine import    SoftI2C, Pin
from machine import Pin, Timer
import machine
import time
import utime

from time import sleep
import boost
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from max30102 import hrcalc
from ulab import numpy as np
 
import ulab


pwm = PWM(Pin(15))
pwm.freq(50)
time = [1193559, 1195559, 1197598, 1199598, 1201617, 1203617, 1205617, 1207645, 1209676, 1211672]
spo2 = [98.69, 98.69, 99.04, 99.18, 98.67, 98.59, 98.59, 98.03, 98.47, 99.12]
HreatRate = [70, 71.69, 68.04, .18, 98.67, 98.59, 98.59, 98.03, 98.47, 99.12]
led_pin = machine.Pin(14, machine.Pin.OUT)


def Servo():
         for position in range(1000,9000,50):
             pwm.duty_u16(position)
             sleep(0.01)
#              print("568")
         for position in range(9000,1000,-50):
             pwm.duty_u16(position)
             sleep(0.01)
             
        
          
def main():
                        
                        led_pin.on()
                        utime.sleep_ms(3000)
                        led_pin.off()
                        print( "EMERGENCY !! ")
                        print(" \n")
                        print(" INFLATABLE DEVICE WILL OPEN !! ")
                        Servo()
    
     
if __name__ == '__main__':
    main()
   
