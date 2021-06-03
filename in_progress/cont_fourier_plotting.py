import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from Adafruit import ADS1x15
import pickle
import collections
from multiprocessing import Process, Queue

def update_timeseries():
    """
    Adds a new voltage difference measurement to the end of timeseries while deleting the first element to keep the same size.

    :param timeseries: Numpy array containing the most recent ADC voltage difference measurements
    """
    global time_series #allows function to alter global time_series variable
    volt_diff = 0.001*adc.getLastConversionResults()
    time_series = np.roll(time_series, -1)
    time_series[-1] = volt_diff

def get_fourier_transform(time_series, sps, window=np.hamming):
    """
    Applies window function and fourier transform to time_series data, then plots the frequencies in units Hz/sec.

    :param time_series: Numpy array containing the most recent ADC voltage difference measurements.
    :param sps: Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300
    :param window: Window function with input integer M, default: Hamming function w(x) = 0.54 - 0.46cos(2 \pi n / (M-1)
    """
    time_series_tapered = time_series*window(time_series.size)
    time_series_fft = np.fft.rfft(time_series_tapered)
    time_series_fft_power = np.abs(time_series_fft)**2 #Gets magnitude of complex number
    return time_series_fft_power

def init_plot():
    ax.set_xlim(0,1000)
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

adc = ADS1x15() #Instatiate Analog Digital Converter

"""
Returns the voltage difference in millivolts between port 0 and 1 on the ADC.

:param VRANGE: Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
:param sps: Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
"""
VRANGE = 4096
sps = 920
sinterval = 1.0/sps
ACQTIME = 1
measuretime = 2
time_series_len = ACQTIME*sps
time_series = np.zeros(time_series_len)
time_series_freq = np.fft.rfftfreq(time_series.size, d=1/sps) #Gets frequencies in Hz/sec

adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps)
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([],[],'ro')

t_start = time.perf_counter()

ani = FuncAnimation(fig, update_plot, frames=np.linspace(0,measuretime, measuretime*sps),
                    interval = 0, repeat=False, init_func=init_plot, blit=True)
plt.show()
"""
while (time.perf_counter() - t_start < measuretime):
    t0 = time.perf_counter()
    update_timeseries()
    fft_power=get_fourier_transform(time_series, sps)
    while (time.perf_counter() -t0 <= sinterval):
        pass
"""
t = time.perf_counter() - t_start
adc.stopContinuousConversion()
print('Time elapsed: %.9f s.' % t)
print()
    
    
    
    
    
    