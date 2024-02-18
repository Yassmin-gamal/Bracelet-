# main.py
# Some ports need to import 'sleep' from 'time' module
from machine import    SoftI2C, Pin
from time import sleep
import boost
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM
import hrcalc
import ulab
from ulab import numpy as np
i2c = SoftI2C(sda=Pin(16),  # Here, use your I2C SDA pin
                  scl=Pin(17),  # Here, use your I2C SCL pin
                  freq=100000)  # Fast: 400kHz, slow: 100kHz
sensor = MAX30102(i2c=i2c)  # An I2C instance is required



# def read_sequential(self, amount=100):
#         """
#         This function will read the red-led and ir-led `amount` times.
#         This works as blocking function.
#         """
#         
#         red_buf = []
#         ir_buf = []
#         for i in range(amount):
#             red = sensor.pop_red_from_storage()
#             ir = sensor.pop_ir_from_storage()
#             print("red  ",red)
#             print("ir  ",ir)
#             red_buf.append(red)
#             ir_buf.append(ir)
# 
#         return red_buf, ir_buf

def mean( arr,  n):

    sum = 0.0;
    for i in range(0,n-1,1): 
        sum = sum + arr[i]
    return sum / n

def covariance(arr1, arr2, n):

    sum = 0
    i=0
    mean_arr1 = mean(arr1, n)
    mean_arr2 = mean(arr2, n)
    for i in range(0,n-1,1):
        sum = sum + (arr1[i] - mean_arr1) * (arr2[i] - mean_arr2)
    return sum / (n - 1)

def variance(time,n):
        i=0
        sum=0
        sumsqr=0
        mean=0
        value=0
        variance=0.0

        for i in range(0,10,1):
        
            sum=sum+time[i]
        
        mean=sum/10
        for i in range(0,10,1):
        
            value=time[i]-mean
            sumsqr=sumsqr+value*value
        
        variance=sumsqr/n
        return variance
    


def main():
    # I2C software instance
    i2c = SoftI2C(sda=Pin(16),  # Here, use your I2C SDA pin
                  scl=Pin(17),  # Here, use your I2C SCL pin
                  freq=100000)  # Fast: 400kHz, slow: 100kHz

    # Examples of working I2C configurations:
    # Board             |   SDA pin  |   SCL pin
    # ------------------------------------------
    # ESP32 D1 Mini     |   22       |   21
    # TinyPico ESP32    |   21       |   22
    # Raspberry Pi Pico |   16       |   17
    # TinyS3			|	 8		 |    9

    # Sensor instance
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
    beats_low=[0]*10
    HRUnsorted=[0]*10
    slopes=[0]*10
    spo2=[98.62
,
99.03
,
99.28
,
98.72
,
98.1
,
98.29
,
98.22
,
98.05
,
98.79
,
98
]
    time=[1806.969,
              1809.035,
              1811.031,
              1813.028,
                1815.067,
                1817.090,
                1819.086,
                1821.086,
                1823.114,
                1825.141]
    IRQ =0.0
    SPo2lower =0.0
    SPo2upper=0.0
    var=0.0
    covar=0.0
    slope=0.0
    slopeThreshold=0.0
    i=0
    n=0
    j=0
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
                     
                    print("hr = ",beats[60])
                    print("\n ");


                    prediction=boost.score(irisSample)
                    print("score =  ",prediction);
                    res = prediction.index(max(prediction))
                    print("pred =  ",res);
            
                    print("Heart Rate : ",hr2)
                if(spb == True and sp != -999):
                    sp2 = int(sp)
                    k=k+1
                    #spo2[k-1]=sp2
                      
                      #HRUnsorted[i]=readHR(); 
                      #slopes[i]=slope;

                        
                    print( "ana da5l el if  ")       
                    if(spo2[9]!=0):
                        print( "ana fe el if  ")  
                        k=0
                        var= variance(time,10)
                        print( "var is  ",var)
                        covar= covariance(time,spo2,10)
                        print( "covar is  ",covar)
                        slope= (covar/var)*time[n-1]*0.001                     
                        print( "slope is  ",slope)    
                        print(" \n")

                    
                    print("SPO2       : ",sp2)
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
           

if __name__ == '__main__':
    main()

