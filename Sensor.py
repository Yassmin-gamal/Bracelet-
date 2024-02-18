# this file for High | Low heart rate

from machine import    SoftI2C, Pin
from machine import Pin, Timer
import machine
import time
import utime
from servo import Servo
from time import sleep
import boost
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
from max30102 import hrcalc
from ulab import numpy as np
 
import ulab


def mean(arr, n):
    sum = 0
    
    for i in range(0, n):
        sum = sum + arr[i]
    
    return sum / n


def covariance(arr1, arr2, n):
    sum = 0
    mean_arr1 = mean(arr1, n)
    mean_arr2 = mean(arr2, n)
    
    for i in range(0, n):
        sum = sum + (arr1[i] - mean_arr1) * (arr2[i] - mean_arr2)

    return sum / (n - 1)


def variance(time, n):
    sum = 0
    sumsqr = 0
    mean = 0
    value = 0
    variance = 0.0

    for i in range(0, 10):
        sum = sum + time[i]

    mean = sum / 10

    for i in range(0, 10):
        value = time[i] - mean
        sumsqr = sumsqr + value * value

    variance = sumsqr / n

    return variance


def get_time_array():
    time_array = []
    for i in range(10):
        time_milliseconds = round(time.time() /1000)
        time_array.append(time_milliseconds)
        #utime.sleep_ms(10000)
        utime.sleep_ms(1000)  # Add a small delay to avoid getting the same time repeatedly
    print(time_array)    
    return time_array

    

'''
pwm = PWM(Pin(15))
pwm.freq(50)
res =0
    # Sensor instance
sensor = MAX30102(i2c=i2c)  # An I2C instance is required
    # Configure interrupt pin in MAX30102 sensor
interrupt_pin = machine.Pin(14, machine.Pin.IN)
interrupt_pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=handle_interrupt)
def handle_interrupt(pin):
         global res
         res = 1
 
         for position in range(1000,9000,50):
             pwm.duty_u16(position)
             sleep(0.01)
         for position in range(9000,1000,-50):
             pwm.duty_u16(position)
             sleep(0.01)
        
'''
 
def sensor ():
     # I2C software instance
    i2c = SoftI2C(sda=Pin(16),  # Here, use your I2C SDA pin
                  scl=Pin(17),  # Here, use your I2C SCL pin
                  freq=100000)  # Fast: 400kHz, slow: 100kHz
    led_pin = machine.Pin(14, machine.Pin.OUT)



    # Examples of working I2C configurations:
    # Board             |   SDA pin  |   SCL pin
    # ------------------------------------------
    # ESP32 D1 Mini     |   22       |   21
    # TinyPico ESP32    |   21       |   22
    # Raspberry Pi Pico |   16       |   17
    # TinyS3			|	 8		 |    9
    sensor = MAX30102(i2c=i2c)  # An I2C instance is required
 
    # Scan I2C bus to ensure that the sensor is connected
    if sensor.i2c_address not in i2c.scan():
        print("Sensor not found.")
        return
    elif not (sensor.check_part_id()):
        # Check that the targeted sensor is compatible
        print("I2C device ID not corresponding to MAX30102 or MAX30105.")
        return
    else:
        print("Sensor connected and recognized.")

    # It's possible to set up the sensor at once with the setup_sensor() method.
    # If no parameters are supplied, the default config is loaded:
    # Led mode: 2 (RED + IR)
    # ADC range: 16384
    # Sample rate: 400 Hz
    # Led power: maximum (50.0mA - Presence detection of ~12 inch)
    # Averaged samples: 8
    # pulse width: 411
    print("Setting up sensor with default configuration.", '\n')
    sensor.setup_sensor()

    # It is also possible to tune the configuration parameters one by one.
    # Set the sample rate to 400: 400 samples/s are collected by the sensor
    sensor.set_sample_rate(400)
    # Set the number of samples to be averaged per each reading
    sensor.set_fifo_average(8)
    # Set LED brightness to a medium value
    sensor.set_active_leds_amplitude(MAX30105_PULSE_AMP_MEDIUM)

    sleep(1)

    # The readTemperature() method allows to extract the die temperature in °C    
    print("Reading temperature in °C.", '\n')
    print(sensor.read_temperature())

    # Select whether to compute the acquisition frequency or not
    compute_frequency = True

    print("Starting data acquisition from RED & IR registers...", '\n')
    sleep(1)


    t_start = ticks_us()  # Starting time of the acquisition
    samples_n = 0  # Number of samples that have been collected
    flag=0
    k=0
    ir_buf = []
    red_buf = []
    beats=[0]*61
    spo2=[0]*10
    HR=[0]*10
    beats_low=[0]*10
    HRUnsorted=[0]*10
    slopes=[0]*10
    time = [1193559, 1195559, 1197598, 1199598, 1201617, 1203617, 1205617, 1207645, 1209676, 1211672]
    #time=get_time_array()
    #spo2 = [98.69, 98.69, 99.04, 99.18, 98.67, 98.59, 98.59, 98.03, 98.47, 99.12]
     
    IRQ =0.0
    SPo2lower =0.0
    SPo2upper=0.0
    var=0.0
    covar=0.0
    slope=0.0
    varHR=0.0
    time_counter=0
    covarHR=0.0
    slopeHR=0.0
    slopeThreshold=0.0
    i=0
    n=0
    j=0
    m=0
    counter=0
    alarm=0
    while True:
        flag=flag+1
        # The check() method has to be continuously polled, to check if
        # there are new readings into the sensor's FIFO queue. When new
        # readings are available, this function will put them into the storage.
        sensor.check()

        # Check if the storage contains available samples
        if sensor.available():
            # Access the storage FIFO and gather the readings (integers)
            red_reading = sensor.pop_red_from_storage()
            ir_reading = sensor.pop_ir_from_storage()
            #print("red2  ",red_reading)
            #print("ir2  ",ir_reading)
            # Print the acquired data (so that it can be plotted with a Serial Plotter)
            #print(red_reading, ",", ir_reading)
            red_buf.append(red_reading)
            ir_buf.append(ir_reading)
            #print("red  ",red_buf)
            #print("ir  ",ir_buf)
            #print("flag  ",flag)
            #red, ir = read_sequential(100)
            if (len(red_buf)==100):
                flag=0
                hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir_buf, red_buf)

                print("hr detected:",hrb)
                print("sp detected:",spb)
                if(hrb == True and hr != -999):
                    hr2 = int(hr)
                    for i in range(59,-1,-1):
                        print(beats[59])
                        beats[i]=beats[i+1]               
                    
                    beats[60]=hr2
                    sum =0  
                    HRMAD10=0
                    HRMAD30=0
                    HRMAD60 =0
                    j=0
                    if (beats[0]!=0):
                      for i in range(59,-1,-1):
                          sum+=beats[i]
                          
                          if (i<10):
                              beats_low[j]=beats[i]
                               
                              j=j+1
                          if(i==50):
                              HRMAD10=(beats[60]-(sum/10))             
                          
                          if(i==30):
                              HRMAD30=(beats[60]-(sum/30))             
                          
                          if(i==0):
                              HRMAD60=(beats[60]-(sum/60))
                              
                              
 
                          
                        
                                        
                            
                    
                    irisSample = [beats[60],HRMAD10,HRMAD30,HRMAD60]
                        #float irisSample[4] = {186,1,4,15};
                    
                    

                    print("Predicted label (you should see '2': ")
                    print("\n ")
                     
                    #print("hr = ",beats[60])
                   # print("\n ");
 
                    prediction=boost.score(irisSample)
                    print("score =  ",prediction);
                    res = prediction.index(max(prediction))
                    print("pred =  ",res);
            
                    #print("Heart Rate : ",hr2)
                    if(m<10):
                        if (hr2>100 ):
                              HR[m]=75
                        if(hr2 <60):
                           HR[m]=hr2+50
                        
                        m=m+1
                if(spb == True and sp != -999):
                    sp2 = int(sp)
                    #print(sp2)
                    #spo2.append(sp2)
                    spo2[k]=sp2
                    #print("SPO2 : ",spo2)
                    k=k+1
                    #m=m+1
                    
                    #spo2[k-1]=sp2
                      
                    #HRUnsorted[i]=readHR(); 
                    #slopes[i]=slope;

                        
                    #print( "ana da5l el if  ")       
                    if(spo2[9]!=0):
                        #print( "ana fe el if  ")
                         
                        print("SPO2 : " ,spo2)
                        print("HR : " ,HR)
                        print("Time : " ,time)
                        var= variance(time,10)
                        print( "var is  ",var)
                        covar= covariance(time,spo2,10)
                        print( "covar is  ",covar)
                        slope= (covar/var)*time[n-1]*0.001                     
                        print( "slope is  ",slope)    
                        print(" \n")
                        
                        
                        varHR= variance(time,10)
                        print( "varHR is  ",varHR)
                        covarHR= covariance(time, HR,10)
                        print( "covar isHR  ",covarHR)
                        slopeHR= (covarHR/varHR)*time[n-1]*0.001                     
                        print( "slopeHR is  ",slopeHR)    
                        print(" \n")
                        
                        #time=time[1:] + [0]
                        #print(time)
                         
                        
                        spo2=spo2[1:] + [0]
                        time=time[1:] + [0]
                        time[9]=time[8]+200
                        k=9
                        m=9
                        HR=HR[1:] +[0]
                        #print(spo2)
                        #print(HR)
 
                        

                    
                    #print("SPO2       : ",sp)
                    if (slope < -0.05  ):
                      if (slopeHR <-0.2):
                         time_counter +=1
                         if time_counter == 5:
                            Servo()
                      elif(time_counter >0):
                         time_counter -=1
                    elif(time_counter >0):
                         time_counter -=1      
                         
                    if (res==1  ):
                        led_pin.on()
                        utime.sleep_ms(2000)
                        led_pin.off()
                        print( "EMERGENCY !! ")
                        print(" \n")
                        print(" INFLATABLE DEVICE WILL OPEN !! ")
                        
                        Servo()
                        

                ir_buf = []
                red_buf = []

            # Compute the real frequency at which we receive data
            if compute_frequency:
                if ticks_diff(ticks_us(), t_start) >= 999999:
                    f_HZ = samples_n
                    samples_n = 0
                    #print("acquisition frequency = ", f_HZ)
                    t_start = ticks_us()
                else:
                    samples_n = samples_n + 1
           
