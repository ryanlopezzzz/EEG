"""
Program Description:

Simple code which takes EEG data for fixed interval in time, then plots a number of graphs related to this data.
"""

ACQTIME = 5
SPS = 920 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS
freq_min = 8 #minimum frequency for alpha waves
freq_max = 12 #maximum frequency for alpha waves

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from Adafruit import ADS1x15
from analysis_tools import get_power_spectrum, get_rms_voltage, get_brain_wave, gaussian_eval, get_cutoff

indata = np.zeros(nsamples, 'float')
print()
print('Initializing ADC...')
print()

adc = ADS1x15()
adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)

input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
print()

t0 = time.perf_counter()
for i in range(nsamples): #loops and records data
    st = time.perf_counter()
    time_series[i] = 0.001*adc.getLastConversionResults() #Gets voltage in volts
    time_series[i] -= 3.3 #adc ground is 3.3 volts below circuit ground 
    while (time.perf_counter() - st) <= sinterval:
            pass

t = time.perf_counter() - t0
adc.stopContinuousConversion()

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t) #Want to check that this time is reasonable
print()

#Plots raw input data to the ADC
f1, ax1 = plt.subplots()
ax1.plot(xpoints, time_series)
ax1.set(xlabel='Time (s)', ylabel='Voltage', title='Raw Signal')    
f1.show()

#Plots power spectrum of data (not normalized)
ps = get_power_spectrum(time_series)
freq = np.fft.fftfreq(nsamples, d=1.0/SPS) #frequencies for FFT of data
f2, ax2 = plt.subplots()
ax2.plot(xpoints, time_series)
ax2.set(xlabel='Frequency (Hz)', ylabel='Voltage', title='Power Spectrum')    
f2.show()

#Plots brain wave (raw data with frequencies outside 8 to 12 Hz filtered out)
brain_wave = get_brain_wave(time_series, freq_min, freq_max, freq)
f3, ax3 = plt.subplots()
ax3.plot(xpoints, time_series)
ax3.set(xlabel='Time (s)', ylabel='Voltage', title='Alpha Wave')    
f3.show()

rms = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)
print('Alpha wave root mean square (rms) voltage is: ',rms)
input('\nPress <Enter> to exit...\n')

