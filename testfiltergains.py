ACQTIME = 2.0
SPS = 920
VRANGE = 4096
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
import collections
from Adafruit import ADS1x15

print()
print('Initializing ADC...')
print()

adc = ADS1x15()

def get_freq_power():
    indata = np.zeros(nsamples, 'float')
    
    adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)

    input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
    print()

    t0 = time.perf_counter()

    for i in range(nsamples):
        st = time.perf_counter()
        indata[i] = 0.001*adc.getLastConversionResults()
        while (time.perf_counter() - st) <= sinterval:
                pass

    t = time.perf_counter() - t0

    adc.stopContinuousConversion()

    xpoints = np.arange(0, ACQTIME, sinterval)

    print('Time elapsed: %.9f s.' % t)
    print()

    f1, ax1 = plt.subplots()
    ax1.plot(xpoints, indata)
    f1.show()

    ave=np.mean(indata)
    newdata=indata-ave
    ft = np.fft.fft(newdata)
    ftnorm = abs(ft)
    ps =ftnorm**2
    xvals = np.fft.fftfreq(len(ps), d=1.0/SPS)
    f2, ax2 =plt.subplots()
    plt.xlim(0,500)
    ax2.plot(xvals, ps)
    f2.show()

    valuemax=np.amax(ps)
    freqwhere=np.where(ps==valuemax)
    freqmax=xvals[freqwhere[0]]
    if freqmax.shape != (1,1):
        freqmax=freqmax[0]
    print('Dominant Frequency is: ', int(abs(freqmax)), 'Hz')
    
    return valuemax

response = input('Load existing data file? (y/n)')
if response == 'n':
    filter_gain_data = collections.OrderedDict()
elif response == 'y':
    filename = input('File name to load gain data: ')
    file = open(filename, 'rb')
    filter_gain_data = pickle.load(file)
    file.close()
    
end_program = 'n'
while end_program != 'y':
    freq = input('Please enter the frequency you want to test:')
    
    input('Press Enter to test with no filter')
    freq_power_no_filter = get_freq_power()
    print('Maximum frequency power is ', freq_power_no_filter, ' for no filter')
    
    input('Press Enter to test with filter')
    plt.close('all')
    freq_power_with_filter = get_freq_power()
    print('Maximum frequency power is ', freq_power_with_filter, ' with filter')
    
    gain = freq_power_with_filter/freq_power_no_filter
    print('Gain is ', gain)
    filter_gain_data[freq] = gain
    end_program = input('Do you want to end program? (y/n)')
    print('\n \n')
    plt.close('all')

while True:
    filename = input('Enter file name to save gain data (should end with .pickle)')
    try:
        file = open(filename, 'wb')
        pickle.dump(filter_gain_data, file)
        file.close()
    except:
        print('Please enter a valid file name.')
    else:
        break
    
