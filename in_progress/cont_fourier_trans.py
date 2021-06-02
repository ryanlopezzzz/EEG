import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from Adafruit import ADS1x15
import pickle
import collections

def update_timeseries(time_series, volt_diff):
    """
    Adds a new voltage difference measurement to the end of timeseries while deleting the first element to keep the same size.

    :param timeseries: Numpy array containing the most recent ADC voltage difference measurements
    """
    time_series = np.roll(time_series, -1)
    time_series[-1] = volt_diff
    return time_series
    
def get_power_spectrum(time_series):
    """
    Applies window function and fourier transform to time_series data and returns power spectrum of FFT: ps[freq]=|FFT(x)|^2[freq]

    :param time_series: Numpy array containing the most recent ADC voltage difference measurements.
    """
    time_series_zero_mean = time_series-np.mean(time_series)
    time_series_fft = np.fft.fft(time_series_zero_mean)
    ps = np.abs(time_series_fft)**2 #Gets square of complex number
    return ps

def get_rms_voltage(ps, freq_min, freq_max):
    """
    Gets the Root-Mean-Square (RMS) voltage of waves with frequency between freq_min and freq_max. Parseval's Theorem says:
    \sum_{i=0}^{N-1} x[i]^2 = \frac{1}{N} \sum_{i=-(N-1)}^{N-1} |FFT(x)[i]|^2
    Using this, the RMS voltage is (first formula is definition, second is implemented evaluation):
    \sqrt{ \frac{1}{N} \sum_{i=0}^{N-1} x[i]^2 } = \frac{1}{N} \sqrt{ \sum_{freq in range} |FFT(x)[freq]|^2}
    
    :param ps: FFT power spectrum of time_series, ps[freq] = |FFT(x)|^2[freq]
    """
    freq_abs = np.abs(freq) 
    ps_in_range = ps[(freq_abs <= freq_max) & (freq_abs >= freq_min)] #Gets power spectrum for freq in range [freq_min, freq_max]
    rms = (1/time_series_len) * np.sqrt(np.sum(ps_in_range))
    return rms

adc = ADS1x15() #Instantiate Analog Digital Converter
VRANGE = 4096 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sps = 250 # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
sinterval = 1.0/sps
sampletime = 3 # how long to look back in time for current alpha waves
exptime = 40 #total experiment time
time_series_len = sampletime*sps
time_series = np.zeros(time_series_len)
freq = np.fft.fftfreq(time_series.size, d=1/sps) #Gets frequencies in Hz/sec
freq_min = 8 #minimum freq in Hz for alpha waves
freq_max = 12 #maximum freq in Hz for alpha waves

raw_data = []
rms_values = []

input('Press <Enter> to start %.1f s data acquisition...' % exptime)
print()

adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps) #Returns the voltage difference in millivolts between port 2 and 3 on the ADC.

t_start = time.perf_counter()
while (time.perf_counter() - t_start < exptime):
    t0 = time.perf_counter()
    volt_diff = 0.001*adc.getLastConversionResults()-3.3 #0.001 to convert mV -> V, adc ground is 3.3 volts above circuit ground 
    time_series = update_timeseries(time_series, volt_diff)
    raw_data.append(volt_diff)
    ps = get_power_spectrum(time_series)
    rms = get_rms_voltage(ps, freq_min, freq_max)
    rms_values.append(rms)
    #print("Alpha Wave RMS: ", rms)
    while (time.perf_counter() - t0 <= sinterval):
        pass
t = time.perf_counter() - t_start
adc.stopContinuousConversion()
print('Time elapsed: %.9f s.' % t)
print()

fig1, ax1 = plt.subplots()
times = np.linspace(0, exptime, num=exptime*sps)


print(len(times))
print(len(rms_values))
print(len(raw_data))
times = times[:len(rms_values)]

ax1.plot(times, rms_values)
ax1.set(xlabel='RMS of Voltage (V)', ylabel='Time (s)', title='Alpha Wave Magnitude')

fig2, ax2 = plt.subplots()
ax2.plot(times, raw_data)
ax2.set(xlabel='Voltage (V)', ylabel='Time (s)', title='Raw Data')

plt.show()
input('Press <Enter> to end program')
plt.close('all')


    
    
    
    
    
    