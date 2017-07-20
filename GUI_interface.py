
#!/usr/bin/env/python
from appJar import gui
import Tkinter
import weather_DAQ
import air_quality_DAQ
import adc_DAQ

app = gui("Adafruit Weather Sensor", "800x400")

wdaq = weather_DAQ.weather_DAQ()
aqdaq = air_quality_DAQ.air_quality_DAQ()
adcdaq = adc_DAQ.adc_DAQ()

top = Tkinter.Tk()
varAir = Tkinter.BooleanVar()
varAir.set(True)
varCO2 = Tkinter.BooleanVar()
varCO2.set(True)
varWeather = Tkinter.BooleanVar()
varWeather.set(True)    


def weather_test(btn):
    if varCO2.get(): 
        adcdaq.create_file()
    if varAir.get(): 
        aqdaq.create_file()
    if varWeather.get(): 
        wdaq.create_file() 
    if varWeather.get(): 
        top = Tkinter.Tk()
        global job1
        global jobpress
        global jobhumid
        global jobtemp
        job1 = None
        jobpress = None
        jobhumid = None
        jobtemp = None
        def start():
            global job1
            wdaq.start()
            job1=top.after(1000,start)
        def stop():
            global job1
            top.after_cancel(job1)
        def press():
            global jobpress
            global jobhumid
            global jobtemp
            if jobhumid is not None:
                top.after_cancel(jobhumid)
                jobhumid = None
                wdaq.close(2)
            if jobtemp is not None:
                top.after_cancel(jobtemp)
                jobtemp = None
                wdaq.close(1)
            wdaq.press()
            jobpress=top.after(1000,press)
        
        def temp():
            global jobpress
            global jobhumid
            global jobtemp
            if jobhumid is not None:
                top.after_cancel(jobhumid)
                jobhumid = None
                wdaq.close(2)
            if jobpress is not None:
                top.after_cancel(jobpress)
                jobpress = None
                wdaq.close(3)
            wdaq.temp()
            jobtemp=top.after(1000,temp)
        
        def humid():
            global jobpress
            global jobhumid
            global jobtemp
            if jobpress is not None:
                top.after_cancel(jobpress)
                jobpress = None
                wdaq.close(3)
            if jobtemp is not None:
                top.after_cancel(jobtemp)
                jobtemp = None
                wdaq.close(1)
            wdaq.humid()
            jobhumid=top.after(1000,humid)
    
    startButton = Tkinter.Button(top, height=2, width=20, text ="Start", command = start)
    stopButton = Tkinter.Button(top, height=2, width=20, text ="Stop", command = stop)
    PressureButton = Tkinter.Button(top, height=2, width=20, text = "Pressure", command = press)
    TempButton = Tkinter.Button(top, height=2, width=20, text = "Temperature", command = temp)
    HumidButton = Tkinter.Button(top, height=2, width=20, text = "Humidity", command = humid)
    
    startButton.pack()
    stopButton.pack()
    PressureButton.pack()
    TempButton.pack()
    HumidButton.pack()

    top.mainloop()
  

AirButton = Tkinter.Checkbutton(top, text="Air Quality", onvalue=True, offvalue=False, variable=varAir)     
WeatherButton = Tkinter.Checkbutton(top, text='Weather Sensor', onvalue=True, offvalue=False, variable=varWeather)
CO2Button = Tkinter.Checkbutton(top, text="CO2 Sensor", onvalue=True, offvalue=False, variable=varCO2)  
RecordButton = Tkinter.Button(top, height=2, width=20, text ="Record Data", command = weather_test)

AirButton.pack()   
WeatherButton.pack()
CO2Button.pack()
RecordButton.pack()

top.mainloop()
    

'''
def air_quality_test(btn):
    aqdaq.create_file()
    top = Tkinter.Tk()
    def start():
        global job2
        aqdaq.start()
        job2=top.after(1000,start)
    def stop():
        global job2
        top.after_cancel(job2)

    startButton = Tkinter.Button(top, height=2, width=20, text ="Start", command = start)
    stopButton = Tkinter.Button(top, height=2, width=20, text ="Stop", command = stop)

    startButton.pack()
    stopButton.pack()

    top.mainloop()

def CO2_test(btn):
    adcdaq.create_file()
    top = Tkinter.Tk()
    def start():
        global job3
        adcdaq.start()
        job3=top.after(1000,start)
    def stop():
        global job3
        top.after_cancel(job3)
    
    startButton = Tkinter.Button(top, height=2, width=20, text ="Start", command = start)
    stopButton = Tkinter.Button(top, height=2, width=20, text ="Stop", command = stop)

    startButton.pack()
    stopButton.pack()

    top.mainloop()

def weather_plot(btn):

    wdaq.plotdata()  
    '''

