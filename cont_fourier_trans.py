import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from Adafruit import ADS1x15
import pickle
import collections

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
    #time_series_tapered = time_series*window(time_series.size)
    time_series_tapered = time_series-np.mean(time_series)
    time_series_fft = np.fft.rfft(time_series_tapered)
    time_series_fft_power = np.abs(time_series_fft)**2 #Gets magnitude of complex number
    return time_series_fft_power

adc = ADS1x15() #Instatiate Analog Digital Converter
VRANGE = 4096
sps = 920
sinterval = 1.0/sps
ACQTIME = 5
measuretime = 20
time_series_len = ACQTIME*sps
time_series = np.zeros(time_series_len)
time_series_freq = np.fft.rfftfreq(time_series.size, d=1/sps) #Gets frequencies in Hz/sec

"""
Returns the voltage difference in millivolts between port 0 and 1 on the ADC.

:param VRANGE: Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
:param sps: Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
"""
adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps)

t_start = time.perf_counter()
while (time.perf_counter() - t_start < measuretime):
    t0 = time.perf_counter()
    update_timeseries()
    fft_power=get_fourier_transform(time_series, sps)
    print("Max Frequency: " + str(time_series_freq[np.argmax(fft_power)]))
    while (time.perf_counter() -t0 <= sinterval):
        pass
print(fft_power)
t = time.perf_counter() - t_start
adc.stopContinuousConversion()
print('Time elapsed: %.9f s.' % t)
print()
    
    
    
    
    
    