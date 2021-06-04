import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Adafruit import ADS1x15
import pickle
import collections
from analysis_tools import get_power_spectrum, get_rms_voltage, get_brain_wave
import pygame #modulo for playing audio
from multiprocessing import Process, Queue

def update_timeseries(time_series, volt_diff):
    """
    Adds a new voltage difference measurement to the end of timeseries while deleting the first element to keep the same size.

    :param timeseries: Numpy array containing the most recent ADC voltage difference measurements
    """
    time_series = np.roll(time_series, -1)
    time_series[-1] = volt_diff
    return time_series

def init_plot(xmax):
    ax.set_xlim(0,xmax)
    ax.set_ylim(0,2)
    return ln,

def update_plot(frame):
    global time_series
    t0 = time.perf_counter()
    update_timeseries()
    fft_power=get_fourier_transform(time_series, sps)
    ln.set_data(time_series_freq, fft_power)
    #ln.set_data(np.arange(0,time_series.size), time_series)
    while (time.perf_counter() -t0 <= sinterval):
        pass
    return ln,

print()
print('Initializing')
print()

adc = ADS1x15() #Instantiate Analog Digital Converter
VRANGE = 4096 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sps = 64 # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
sinterval = 1.0/sps
sampletime = 3 # how long to look back in time for current alpha waves

pygame.init()
clock = pygame.time.Clock()

#ask for session length
while True:
    try:
        exptimem = float(input('Please enter session length in minutes (eg: 30)'))#ask session length in minutes
        exptime = int(60*exptimem)#convert to seconds
        print('Session time =', exptimem, 'minutes.')
        break
    except ValueError:
        print('Please enter a valid input. The input should be a number.')
            
print('Experiment time in seconds', exptime)
time_series_len = sampletime*sps
nsamples=exptime*sps
time_series = np.zeros(time_series_len)
freq = np.fft.fftfreq(time_series.size, d=1/sps) #Gets frequencies in Hz/sec for time_series
freq_min = 8 #minimum freq in Hz for alpha waves
freq_max = 12 #maximum freq in Hz for alpha waves

'''Calibration function should be called and run here'''

input('Press <Enter> to start %.1f minutes session...' % exptimem)
print()

times = [] #fills with time values
rms_values = [] #fills with rms values

#Initialize plot to be updated in real time
fig, ax = plt.subplots()
line, = ax.plot([],[], lw=3)
ax.set_xlim(0, exptime)
ax.set_ylim(0,50)
fig.canvas.draw()
plt.show(block=False)

adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps) #Returns the voltage difference in millivolts between port 2 and 3 on the ADC.
t0 = time.perf_counter()
for i in range(nsamples):
    st = time.perf_counter()
    volt_diff = 0.001*adc.getLastConversionResults()-3.3 #0.001 to convert mV -> V, adc ground is 3.3 volts above circuit ground 
    time_series = update_timeseries(time_series, volt_diff)
    ps = get_power_spectrum(time_series)
    rms = get_rms_voltage(ps, freq_min, freq_max, freq, time_series_len)
    #Plotting real time stuff
    times.append(i*sinterval)
    rms_values.append(rms)
    line.set_data(times,rms_values)
    ax.draw_artist(line)
    fig.canvas.blit(ax.bbox)
    clock.tick(sps)
    #while (time.perf_counter() - st <= sinterval):
    #    pass
    
t = time.perf_counter() - t0
adc.stopContinuousConversion()
print('Time elapsed: %.9f s.' % t)
print()
print("Time perf counter: ", time.perf_counter())
                                                                                                         
                                                                                                 
                                                                                                         