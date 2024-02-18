import utime
import time 
from machine import Pin, Timer


def time2 ():
    time_array = []
    for i in range(10):
        
        time_milliseconds = round(time.time() /1000)
        time_array.append(time_milliseconds)
        utime.sleep_ms(10000)
    return time_array    
        
    

t=time2 ()
print(t)



 
led = Pin(15, Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
 

 
