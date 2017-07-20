
#!/usr/bin/env/python
from appJar import gui
import Tkinter
import weather_DAQ
import air_quality_DAQ
import adc_DAQ

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

def make_run_gui():
    top1 = Tkinter.Tk()
    global job1
    global jobpress
    global jobhumid
    global jobtemp
    global jobco2
    global jobaq
    job1 = None
    jobpress = None
    jobhumid = None
    jobtemp = None
    jobco2 = None
    jobaq = None

    def start():
        global job1
        if varWeather.get(): 
            wdaq.start()
        if varAir.get():
            aqdaq.start()
        if varCO2.get():
            adcdaq.start()
        job1=top1.after(1000,start)

    def stop():
        global job1
        top1.after_cancel(job1)

    def press():
        global jobpress
        global jobhumid
        global jobtemp
        if jobhumid is not None:
            top1.after_cancel(jobhumid)
            jobhumid = None
            wdaq.close(2)
        if jobtemp is not None:
            top1.after_cancel(jobtemp)
            jobtemp = None
            wdaq.close(1)
        wdaq.press()
        jobpress=top.after(1000,press)
        
    def temp():
        global jobpress
        global jobhumid
        global jobtemp
        if jobhumid is not None:
            top1.after_cancel(jobhumid)
            jobhumid = None
            wdaq.close(2)
        if jobpress is not None:
            top1.after_cancel(jobpress)
            jobpress = None
            wdaq.close(3)
        wdaq.temp()
        jobtemp=top.after(1000,temp)
        
    def humid():
        global jobpress
        global jobhumid
        global jobtemp
        if jobpress is not None:
            top1.after_cancel(jobpress)
            jobpress = None
            wdaq.close(3)
        if jobtemp is not None:
            top1.after_cancel(jobtemp)
            jobtemp = None
            wdaq.close(1)
        wdaq.humid()
        jobhumid=top.after(1000,humid)

    startButton1 = Tkinter.Button(top1, height=2, width=20, text ="Start", command = start)
    stopButton1 = Tkinter.Button(top1, height=2, width=20, text ="Stop", command = stop)
    startButton1.pack()
    stopButton1.pack()

    if varWeather.get():
        PressureButton = Tkinter.Button(top1, height=2, width=20, text = "Pressure", command = press)
        PressureButton.pack()
        TempButton = Tkinter.Button(top1, height=2, width=20, text = "Temperature", command = temp)
        TempButton.pack()
        HumidButton = Tkinter.Button(top1, height=2, width=20, text = "Humidity", command = humid)
        HumidButton.pack()

    top1.mainloop()

def weather_test():
    if varCO2.get(): 
        print("create CO2 file")
        adcdaq.create_file()
    if varAir.get(): 
        print("create Air file")
        aqdaq.create_file()
    if varWeather.get(): 
        print("create weather file")
        wdaq.create_file()

    make_run_gui()

def print_check():
    print("varAir = {}, varCO2 = {}, varWeather = {}".format(varAir.get(),varCO2.get(),varWeather.get()))    


AirButton = Tkinter.Checkbutton(top, text="Air Quality", variable=varAir, command = print_check)     
WeatherButton = Tkinter.Checkbutton(top, text='Weather Sensor', variable=varWeather, command = print_check)
CO2Button = Tkinter.Checkbutton(top, text="CO2 Sensor", variable=varCO2, command = print_check)
RecordButton = Tkinter.Button(top, text="Record Data", height=2, width=20, command = weather_test)  

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

    '''

