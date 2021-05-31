"""
Program Description:

We use this data to collect brain wave data for the concentrating and relaxed state and save it with
pickle.
"""
import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
from in_progress import cont_fourier_trans as analysis
from Adafruit import ADS1x15

ACQTIME = 5
SPS = 920 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

print()
print('Initializing ADC...')
print()

adc = ADS1x15()

save_path = input('Please input folder name to make or save to:')
if not os.path.isdir(save_path): #Check if exp_dir is already a directory
    try:
        os.mkdir(save_path)
        os.mkdir(os.path.join(save_path,'/relaxed'))
        os.mkdir(os.path.join(save_path,'/concentrated'))
        print("Successfully created folders")
    except OSError:
        print("Creation of the folder %s failed" % save_path)
else:
    print("Successfully connected to the folder %s " % save_path)

while True:
    wavetype = input('Record relaxed or concentrated waves? Type r or c.)')
    if wavetype in ['r','c']:
        break   
    else:
        print('Please type r or c')                   
if wavetype == 'r':
    exp_file = os.path.join(save_path,'/relaxed.py')
elif wavetype == 'c':
    exp_file = os.mkdir(os.path.join(save_path,'/concentrated.py'))
                   
end_program = 'n'
while end_program != 'y': #Loops every time user records data

    input('Press <Enter> to start %.1f s data acquisition...' % recordtime)
    print()
    adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)
    time_series = np.zeros(nsamples, 'float')

    t0 = time.perf_counter()
    for i in range(nsamples): #Collects data every sinterval
        st = time.perf_counter()
        time_series[i] = 0.001*adc.getLastConversionResults() #Times 0.001 since adc measures in mV
        time_series[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
        while (time.perf_counter() - st) <= sinterval:
            pass
    ps = analysis.get_power_spectrum(time_series)
    rms = analysis.get_rms_voltage(ps, freq_min, freq_max)
    print('RMS of Alpha Wave Voltage: ', rms)
    
    f1, ax1 = plt.subplots()
    times = np.arange(0, ACQTIME, sinterval)
    ax1.plot(times, time_series)
    ax1.set(xlabel='Time (s)', ylabel='Voltage', title='Raw Signal')    
    f1.show()
    
    freqs = np.fft.fftfreq(len(ps), d=1.0/SPS)
    f2, ax2 =plt.subplots()
    plt.xlim(0,200)
    ax2.plot(freqs, ps)
    ax2.set(xlabel='Frequency (Hz)', ylabel='Power Spectrum', title='Power Spectrum of FFT')    
    f2.show()
    
    while True:
        save = input('Save this last run? (y/n)')
        if save == 'y':
            file = open(exp_file, 'wb')
            pickle.dump(time_series, file)
            file.close()
            break            
        elif save == 'n':
            break
        else:
            print('Please type y or n.')
    while True:
        end_program = input('Do you want to end program? (y/n)')
        if end_program in ['y', 'n']:
            break
        else:
            print('Please enter \'y\' or \'n\' ')
    print('\n \n \n')
                     
                     
                     
                     

