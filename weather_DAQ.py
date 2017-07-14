# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 11:32:41 2017

@author: Ludi Cao
"""
import time
import datetime
import csv
from Adafruit_BME280 import *
import os
from appJar import gui
import numpy as np
import dateutil
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
from collections import deque

sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)

class weather_DAQ(object):
    def __init__(self):
        self.sensor = sensor
        self.running=False
        self.time_queue=deque()
        self.temp_queue=deque()
        self.humid_queue=deque()
        self.press_queue=deque()
        self.maxdata=10
        self.n_merge=10
        self.temp_list=[]
        self.temp_array = np.asarray(self.temp_list)
        
    def create_file(self):
        global results
        file_time= time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())
        filename = "weather_test_results_"+file_time+".csv"
        results=csv.writer(open(filename, "ab+"), delimiter = ",")
        metadata=["Time", "Temp (C)","Pressure (hPa)", "Humidity (%)"]
        results.writerow(metadata)

    def start(self):
        
        if self.running==False:
            self.running=True
            plt.ion()

           
            plt.ion()
            self.humidfig = plt.figure(2)
            plt.xlabel("Time")
            plt.ylabel("Humidity(%)")
            plt.title("Humdity")

            plt.ion()
            self.pressfig = plt.figure(3)
            plt.xlabel("Time")
            plt.ylabel("Pressure(hPa)")
            plt.title("Pressure")


        global results
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

        self.add_data(self.temp_queue, degrees)
        self.add_data(self.humid_queue,humidity)
        self.add_data(self.press_queue,hectopascals)
        self.add_data(self.time_queue, date_time)


        self.update_plot(1,self.time_queue,self.temp_queue,"Time","Temperature(C)","Temperature vs. time")
        plt.figure(2)
        plt.clf()
        ax=self.humidfig.add_subplot(111)
        plt.plot(self.time_queue, self.humid_queue,"r.")
        self.humidfig.autofmt_xdate()
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        self.humidfig.show()
        plt.pause(0.0005)
       
        plt.figure(3)
        plt.clf()
        ax=self.pressfig.add_subplot(111)
        plt.plot(self.time_queue, self.press_queue, "r.")
        self.pressfig.autofmt_xdate()
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        self.pressfig.show()
        plt.pause(0.0005)

    def add_data(self, queue, data):
        self.temp_array.append(data)
        if len(self.temp_array)<self.n_merge:
            number_count=False
        if len(self.temp_array)>self.n_merge:
            number_count=True
        if number_count==True:
            queue.append(np.mean(self.temp_array))
            self.temp_array = []
        if len(queue)>self.maxdata:
            queue.popleft()
    
    def update_plot(self,plot_id,xdata,ydata,xlabel,ylable,title):
        fig = plt.figure(plot_id)
        plt.clf()
        ax=fig.add_subplot(111)
        plt.xlabel(xlabel)
        plt.ylabel(ylable) 
        plt.title(title)
        plt.plot(xdata,ydata,"r.")
        fig.autofmt_xdate()
        ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
        fig.show()
        plt.pause(0.0005)


    def plotdata(self):
        
        times=[]
        degrees_list=[]
        pressure_list=[]
        humidity_list=[]
        temp_ave=[]
        temp_unc = []
        pressure_ave=[]
        pressure_unc=[]
        humidity_ave=[]
        humidity_unc=[]
        merge_times = []
        
        app=gui("Weather Plot","800x400")   
        app.addLabel("1","Please choose a following .csv file")
        file_name=[]
        for filename in os.listdir('.'):
            if filename.endswith(".csv"):
                file_name.append(os.path.join('.', filename))
        app.setFont(20)
        app.addOptionBox("Files",file_name)
        app.setOptionBoxHeight("Files","4")
        app.addLabel("2","Enter the number of data points to merge:")
        app.setLabelFont("20","Heletica")
        app.addNumericEntry("n")
        app.setFocus("n")     
    
        def ok(btn):
            user_file=app.getOptionBox("Files") 
            n_merge=int(app.getEntry("n"))
            row_counter=0
            results = csv.reader(open(user_file), delimiter=',')

            for r in results:
                if row_counter>0:
                    times.append(dateutil.parser.parse(r[0]))
                    degrees_list.append(float(r[1]))
                    pressure_list.append(float(r[2]))
                    humidity_list.append(float(r[3]))
        
                row_counter+=1

            ndata = int(len(degrees_list))
            nsum_data = int(ndata/n_merge)

            for i in range(nsum_data):
                itemp = degrees_list[i*n_merge:(i+1)*n_merge]
                itemp_array = np.asarray(itemp)
                temp_mean = np.mean(itemp_array)
                temp_sigma = np.sqrt(np.var(itemp_array))
                temp_ave.append(temp_mean)
                temp_unc.append(temp_sigma)
    
            for i in range(nsum_data):
                ipressure = pressure_list[i*n_merge:(i+1)*n_merge]   
                ipressure_array = np.asarray(ipressure)
                pressure_mean = np.mean(ipressure_array)
                pressure_sigma = np.sqrt(np.var(ipressure_array))
                pressure_ave.append(pressure_mean)
                pressure_unc.append(pressure_sigma)
    
            for i in range(nsum_data):
                ihumid = humidity_list[i*n_merge:(i+1)*n_merge]
                ihumid_array = np.asarray(ihumid)
                humid_mean = np.mean(ihumid_array)
                humid_sigma = np.sqrt(np.var(ihumid_array))
                humidity_ave.append(humid_mean)
                humidity_unc.append(humid_sigma)

            for i in range(nsum_data):
                itimes = times[i*n_merge:(i+1)*n_merge]
                itime = itimes[int(len(itimes)/2)]
                merge_times.append(itime)
       
            fig=plt.figure()
            ax=fig.add_subplot(111)   
            plt.plot(merge_times, temp_ave, "b.")
            plt.errorbar(merge_times, temp_ave, yerr = temp_unc)
            plt.title("Temperature")
            plt.xlabel("Time(s)")
            plt.ylabel("Temperature(C)")
            fig.autofmt_xdate()
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))

            fig=plt.figure()
            ax=fig.add_subplot(111)
            plt.plot(merge_times, pressure_ave,"g." )
            plt.errorbar(merge_times, pressure_ave, yerr = pressure_unc)
            plt.title("Pressure")
            plt.xlabel("Time(s)")
            plt.ylabel("Pressure(hPa)")
            fig.autofmt_xdate()
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
            
            fig=plt.figure()
            ax=fig.add_subplot(111)
            plt.plot(merge_times, humidity_ave,"r." )
            plt.errorbar(merge_times, humidity_ave, yerr = humidity_unc)
            plt.title("Humidity")
            plt.xlabel("Time(s)")
            plt.ylabel("Humidity(%)")
            fig.autofmt_xdate()
            ax.xaxis.set_major_formatter(DateFormatter('%H:%M:%S'))
            plt.show()
    
        app.addButton("OK",ok)
        app.setButtonWidth("OK","20")
        app.setButtonHeight("OK","4")
        app.setButtonFont("20","Helvetica")
        app.go()
    


    


        