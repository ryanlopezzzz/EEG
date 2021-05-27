"""
PROGRAM DESCRIPTION:

We use this program to calculate gain as a function of frequency for various circuit filters. We used an
openscope to generate signals at certain frequencies and used an ADC to measure the gain. This program saves
the data in pickle form at the end.
"""

import time
import numpy as np
from scipy.stats import sem
import matplotlib.pyplot as plt
import pickle
from collections import OrderedDict
from Adafruit import ADS1x15

ACQTIME = 2.0 #Length of time interval to record ADC data
SPS = 920 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 4096 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

print()
print('Initializing ADC...')
print()

adc = ADS1x15()

def get_freq_amp():
    """
    Function which records ADC data, plots the data and fourier transform (mean zero),
    prints the maximum frequency, and returns the fourier transform magnitude.
    """
    indata = np.zeros(nsamples, 'float')
    adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)
    print('Starting %.1f s of data acquisition...' % ACQTIME)

    t0 = time.perf_counter()
    for i in range(nsamples): #Collects data every sinterval
        st = time.perf_counter()
        indata[i] = 0.001*adc.getLastConversionResults() #Times 0.001 since adc measures in mV
        indata[i] -= 3.3 #ADC ground is 3.3 volts below circuit ground
        while (time.perf_counter() - st) <= sinterval:
            pass
    
    t = time.perf_counter() - t0
    adc.stopContinuousConversion()
    print('Time elapsed: %.9f s.' % t) #Can compare time elapsed to acquire time

    xpoints = np.arange(0, ACQTIME, sinterval)
    plt.close('all')
    f1, ax1 = plt.subplots()
    ax1.plot(xpoints, indata)
    ax1.set(xlabel='Time (s)', ylabel='Voltage (V)', title='Input Signal')    

    newdata=indata-np.mean(indata)
    ft = np.fft.fft(newdata)
    ftnorm = abs(ft)
    xvals = np.fft.fftfreq(len(ftnorm), d=1.0/SPS)
    f2, ax2 =plt.subplots()
    plt.xlim(0,150)
    ax2.plot(xvals, ftnorm)
    ax2.set(xlabel='Frequency (Hz)', ylabel='FFT Magnitude', title='Fourier Transform')

    valuemax=np.amax(ftnorm)
    freqwhere=np.where(ftnorm==valuemax)
    freqmax=xvals[freqwhere[0]]
    if freqmax.shape != (1,1):
        freqmax=freqmax[0]
    print('Dominant Frequency is: ', int(abs(freqmax)), 'Hz')
    print('Maximum FFT amplitude is ', valuemax)
    print()
    return valuemax

"""
Asks user if they want to load an existing data file to edit.
"""
while True:
    response = input('Load existing data file? (y/n)')
    if response == 'n':
        filter_data = np.array([OrderedDict(), OrderedDict()])
        break
    elif response == 'y':
        while True:
            filename = input('File name to load gain data: ')
            try:
                file = open(filename, 'rb')
                filter_data = pickle.load(file)
                file.close()
                break
            except:
                print('Please enter a valid file name.')
        break
    else:
        print('Please enter \'y\' or \'n\' ')

"""
Asks user how many times to sample data to get standard error estimate.
"""
while True:
    try:
        num_measurements = int(input('Please enter how many measurements to make for each frequency: '))
        break
    except:
        print('Please enter an integer')

"""
Saves data for plotting by pickling a 2 element array. Each array is an ordered dictionary, both have integer
frequency for keys and the first and second dictionary have values of gain and std error respectively. 
"""
end_program = 'n'
while end_program != 'y': #Loops every time user records data for new frequency
    while True:
        try:
            freq = int(input('Please enter the frequency you want to test:'))
            break
        except:
            print('Please enter an integer frequency')
    
    freq_amp_no_filter = np.zeros((num_measurements)) #saves for num_measurement runs
    freq_amp_with_filter = np.zeros((num_measurements))
    
    input('Press <Enter> to test with no filter')
    print()
    for i in range(num_measurements):
        freq_amp_no_filter[i] = get_freq_amp()
    plt.show()
    print()
    
    input('Press <Enter> to test with filter')
    print()
    for i in range(num_measurements):
        freq_amp_with_filter[i] = get_freq_amp()
    plt.show()
    gain = np.divide(freq_amp_with_filter, freq_amp_no_filter)
    print('Voltage gain is ', np.mean(gain))
    print('Standard error is ', sem(gain))
    filter_data[0][freq] = np.mean(gain)
    filter_data[1][freq] = sem(gain)
    while True:
        end_program = input('Do you want to end program? (y/n)')
        if end_program in ['y', 'n']:
            break
        else:
            print('Please enter \'y\' or \'n\' ')
    print('\n \n \n')

while True:
    filename = input('Enter file name to save gain data (should end with .pickle)')
    try:
        file = open(filename, 'wb')
        pickle.dump(filter_data, file)
        file.close()
        break
    except:
        print('Please enter a valid file name.')
