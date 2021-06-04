"""
Program Description:

This program allows the user to communicate text by using concentration levels to signal binary data which is converted to letters
and spaces.
"""
import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pickle
from analysis_tools import get_power_spectrum, get_rms_voltage, gaussian_eval

"""
Prompt user for info about program.
"""
while True:
    try:
        sentencelength = int(input('Please enter number of characters to communicate'))
        break
    except:
        print('Please enter a valid input. The input should be an integer.')
while True:
    try:
        binarytime = float(input('Please enter number of seconds per single binary data'))
        break
    except:
        print('Please enter a valid input. The input should be a number.')        
while True:
    try:
        switchtime = float(input('Please enter number of seconds to ignore data inbetween transitions.'))
        break
    except:
        print('Please enter a valid input. The input should be a number.')
while True:
    response = input('Enter good cutoff voltage (number) or type c to calibrate (c).')
    if response == 'c':
        cutoff = get_cutoff(3,5,490,adc)
        print('You have cutoff voltage',cutoff)
        break
    try:
        cutoff = float(response)
        break
    except:
        print('Please enter correct format input')

VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sps = 250 # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
sinterval = 1.0/sps
sampletime = 1 # how long to look back in time for current alpha waves
time_series_len = int(sampletime*sps)
time_series = np.zeros(time_series_len)
raw_data_len = int(exptime*sps)
freq = np.fft.fftfreq(time_series.size, d=1/sps) #Gets frequencies in Hz/sec
freq_min = 8 #minimum freq in Hz for alpha waves
freq_max = 12 #maximum freq in Hz for alpha waves
times = np.linspace(0, exptime, num=exptime*sps)
rms_times = np.linspace(0,exptime-sampletime, num=(exptime-sampletime)*sps)
        
     
        

        
        
        
        
        
        
        
        
        
        
        
        
