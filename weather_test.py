import datetime
import csv
from Adafruit_BME280 import *

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

file_time= time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
filename = "weather_test_results_"+file_time+".csv"
results=csv.writer(open(filename, "ab+"), delimiter = ",")

metadata=["Time", "Temp (C)","Pressure (hPa)", "Humidity %"]
results.writerow(metadata)

time_of_program=input("Enter the number of seconds the program will last: ")
time_passed=0

while time_passed<time_of_program:
    date_time = datetime.datetime.now()
    degrees = sensor.read_temperature()
    pascals = sensor.read_pressure()
    hectopascals = pascals / 100
    humidity = sensor.read_humidity()

    print ('Temp     = {0:0.3f} deg C'.format(degrees))
    print ('Pressure  = {0:0.2f} hPa'.format(hectopascals))
    print ('Humidity = {0:0.2f} %'.format(humidity))
    
    data=[]
    data.append(date_time)
    data.append(degrees)
    data.append(hectopascals)
    data.append(humidity)
    
    results.writerow(data)
    
    time.sleep(1)
    
    time_passed+=1
    