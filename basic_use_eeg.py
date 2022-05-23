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
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.ads1x15 import Mode
from adafruit_ads1x15.analog_in import AnalogIn
import board
import busio
from analysis_tools import get_power_spectrum, get_rms_voltage, get_brain_wave, gaussian_eval, get_cutoff

i2c = busio.I2C(board.SCL, board.SDA, frequency=1000000)

indata = np.zeros(nsamples, 'float')
print()
print('Initializing ADC...')
print()

ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0, ADS.P1) # This puts ADC in differential mode which reads the voltage difference between pin 0 and pin 1
ads.mode = Mode.CONTINUOUS #This puts ADC in continuous mode
ads.data_rate = 860 # Change actual value of data rate
data1 = chan.voltage

input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
print()

t0 = time.perf_counter()
for i in range(nsamples): #loops and records data
    st = time.perf_counter()
    indata[i] = 0.001*adc.getLastConversionResults() #Gets voltage in volts
    indata[i] -= 3.3 #adc ground is 3.3 volts below circuit ground 
    while (time.perf_counter() - st) <= sinterval:
            pass

t = time.perf_counter() - t0

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t) #Want to check that this time is reasonable
print()

#Plots raw input data to the ADC
f1, ax1 = plt.subplots()
ax1.plot(xpoints, indata)
ax1.set(xlabel='Time (s)', ylabel='Voltage', title='Raw Signal')    
f1.show()

#Plots power spectrum of data (not normalized)
ps = get_power_spectrum(indata)
freq = np.fft.fftfreq(nsamples, d=1.0/SPS) #frequencies for FFT of data
f2, ax2 = plt.subplots()
ax2.plot(freq, ps)
ax2.set(xlabel='Frequency (Hz)', ylabel='Power', title='Power Spectrum')    
f2.show()

#Plots brain wave (raw data with frequencies outside 8 to 12 Hz filtered out)
brain_wave = get_brain_wave(indata, freq_min, freq_max, freq)
f3, ax3 = plt.subplots()
ax3.plot(xpoints, brain_wave)
ax3.set(xlabel='Time (s)', ylabel='Voltage', title='Alpha Wave')    
f3.show()

rms = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)
print('Alpha wave root mean square (rms) voltage is: ',rms)
input('\nPress <Enter> to exit...\n')

