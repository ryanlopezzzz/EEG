"""
Program Description:

We use this data to collect brain wave data for the concentrating and relaxed state and save it with
pickle. Each person gets their own folder, inside this there are separate session folders, inside each of these there is a relaxed.pickle
and concentrated.pickle file which contain a list of the different numpy array time series.
"""
import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import time
import numpy as np
import matplotlib.pyplot as plt
import pickle
from analysis_tools import get_power_spectrum, get_rms_voltage
from Adafruit import ADS1x15

ACQTIME = 5
SPS = 920 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS
freq_min = 8 #min freq of alpha waves
freq_max = 12 #max freq of alpha waves

print()
print('Initializing ADC...')
print()

adc = ADS1x15()

"""
Ask user to specify what folder to save in
"""
while True:
    person_name = input('Please enter your name (hak/ryan/ruining):')
    if person_name in ['hak', 'ryan', 'ruining']:
        break
    else:
        print('Please enter a correct formatted name')
        
save_folder = input('Please input folder name to make or save to:')
save_path = os.path.join(person_name, save_folder)
if not os.path.isdir(save_path): #Check if already a directory
    try:
        os.mkdir(save_path)
        print("Successfully created folders")
    except OSError:
        print("Creation of the folder %s failed" % save_path)
else:
    print("Successfully connected to the folder %s " % save_path)
    
while True:
    wavetype = input('Record relaxed or concentrated waves? Type (r/c)')
    if wavetype in ['r','c']:
        break   
    else:
        print('Please type r or c')                   
if wavetype == 'r':
    exp_file = os.path.join(save_path,'relaxed.pickle')
elif wavetype == 'c':
    exp_file = os.path.join(save_path,'concentrated.pickle')

"""
Continue to collect brain wave data until user specifies stop
"""
end_program = 'n'
while end_program != 'y': #Loops every time user records data

    input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
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
    t = time.perf_counter() - t0    
    adc.stopContinuousConversion()
    print('Time elapsed: %.9f s.' % t)
    freq = np.fft.fftfreq(nsamples, d=1.0/SPS)
    ps = get_power_spectrum(time_series)
    rms = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)
    print('RMS of Alpha Wave Voltage: ', rms)
    
    f1, ax1 = plt.subplots()
    times = np.arange(0, ACQTIME, sinterval)
    ax1.plot(times, time_series)
    ax1.set(xlabel='Time (s)', ylabel='Voltage', title='Raw Signal')    
    f1.show()
    
    f2, ax2 =plt.subplots()
    plt.xlim(0,200)
    ax2.plot(freq, ps)
    ax2.set(xlabel='Frequency (Hz)', ylabel='Power Spectrum', title='Power Spectrum of FFT')    
    f2.show()
    
    while True:
        save = input('Save this last run? (y/n)')
        if save == 'y':
            if os.path.exists(exp_file): #adds to existing file
                file = open(exp_file, 'rb')
                brain_data = pickle.load(file)
                file.close()
                brain_data.append(time_series)
                file = open(exp_file, 'wb')
                pickle.dump(brain_data, file)
                file.close()
            else: #creates new file to save
                brain_data = [time_series]
                file = open(exp_file, 'wb')
                pickle.dump(brain_data, file)
                file.close()
            break            
        elif save == 'n':
            break
        else:
            print('Please type y or n.')
    plt.close('all')
    while True:
        end_program = input('Do you want to end program? (y/n)')
        if end_program in ['y', 'n']:
            break
        else:
            print('Please enter \'y\' or \'n\' ')
    print('\n')
                     
                     
                     
                     

