"""
Program Description:

This program allows the user to communicate text by using concentration levels to signal binary data which is converted to letters
and spaces.
"""
from Adafruit import ADS1x15
import time
import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pickle
from analysis_tools import get_power_spectrum, get_rms_voltage, gaussian_eval, get_cutoff
import pygame
from pygame import mixer #modulo for playing audio
mixer.init() 
alert=mixer.Sound('beep.wav') #sets alert sound

alphabet = {   #This alphabet dictionary is the defined mapping from a-z + ' ' to 5 binary digits.
    'a': [1,1,0,0,0],
    'b': [1,0,0,0,0],
    'c': [1,1,1,1,1],
    'd': [0,0,1,0,0],
    'e': [0,0,0,1,0],
    'f': [0,1,1,1,1],
    'g': [1,1,1,1,0],
    'h': [1,0,0,0,1],
    'i': [1,1,1,0,0],
    'j': [0,0,1,0,1],
    'k': [0,0,1,1,0],
    'l': [0,1,0,0,0],
    'm': [0,1,0,0,1],
    'n': [0,1,1,1,0],
    'o': [0,0,1,1,1],
    'p': [0,1,0,1,1],
    'q': [0,1,0,1,0],
    'r': [0,1,1,0,0],
    's': [0,1,1,0,1],
    't': [1,0,0,1,0],
    'u': [0,0,0,1,1],
    'v': [1,0,0,1,1],
    'w': [1,0,1,1,1],
    'x': [1,0,1,0,1],
    'y': [0,0,0,0,1],
    'z': [1,0,1,0,0],
    ' ': [0,0,0,0,0]
}

def get_binary_from_sentence(string):
    """
    Takes as argument a string and converts the string to binary as defined by alphabet dictionary
    """
    character_list = list(string) #breaks string into list of every character
    binary_list = []
    for char in character_list:
        binary_list.append(alphabet[char]) #adds binary conversion of each letter to binary list
    return binary_list

def get_sentence_from_binary(binary):
    """
    Takes as argument binary list of 0 and 1 and converts to string as defined by alphabet dictionary
    """
    string = ''
    for i in range(int(len(binary)/5)): #goes through all characters
        binary_char = binary[5*i:5*(i+1)] #continues to get 5 binary characters corresponding to each letter
        character = list(alphabet.keys())[list(alphabet.values()).index(binary_char)] #finds letter corresponding to binary
        string += character
    return string
        
def update_timeseries(time_series, volt_diff):
    """
    Adds a new voltage difference measurement to the end of timeseries while deleting the first element to keep the same size.

    :param timeseries: Numpy array containing the most recent ADC voltage difference measurements
    """
    time_series = np.roll(time_series, -1)
    time_series[-1] = volt_diff
    return time_series

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
sentence_target = input('Input sentence you want to communicate:')
print('Must communicate binary data (concentrate for 0, relax for 1): \n')
print(get_binary_from_sentence(sentence_target)) #to make easier, gives user the binary data they must communicate
print()

"""
Parameters to set for how to collect data
"""
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
sps = 250 # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
sinterval = 1.0/sps
sampletime = 1 # how long to look back in time for current alpha waves
exptime = int(5*sentencelength*binarytime+sampletime) #wait for sample time in beginning
time_series_len = int(sampletime*sps)
time_series = np.zeros(time_series_len)
raw_data_len = int(exptime*sps)
freq = np.fft.fftfreq(time_series.size, d=1/sps) #Gets frequencies in Hz/sec
freq_min = 8 #minimum freq in Hz for alpha waves
freq_max = 12 #maximum freq in Hz for alpha waves
times = np.linspace(0, exptime, num=exptime*sps)
rms_times = np.linspace(0,exptime, num=exptime*sps)    
rms_values = []
adc = ADS1x15() #Instantiate Analog Digital Converter


"""
Set up times for comuting RMS average and doing beeps.
"""
switch_points = np.arange(sampletime,exptime,binarytime) #when beeping should occur to denote a switch, doesn't include exptime
switch_indices = (switch_points*sps).astype(np.int32) #on what index to beep.
start_record = switch_points + switchtime/2 #start of each recording interval (ignores very beginning while switching)
end_record = switch_points + binarytime - switchtime/2 #end of each recording interval (ignores very end while switching)
interval_times = np.array([start_record, end_record]).T
interval_indices = (interval_times*sps).astype(np.int32) #shape: [num of binary data points, 2 (start and stop of recording interval)]
print('You will have %.1f seconds before recording starts, you should move onto the next character every %.2f seconds and will be notified of this with a beep.'%(sampletime,binarytime))
input('Press <Enter> to start %.1f s data acquisition...' % exptime)
print()
adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps)

t0 = time.perf_counter()
for i in range(raw_data_len): #Collects data every sinterval
    st = time.perf_counter()
    if i in switch_indices:
        alert.play()
    volt_diff = 0.001*adc.getLastConversionResults()-3.3 #0.001 to convert mV -> V, adc ground is 3.3 volts above circuit ground 
    time_series = update_timeseries(time_series, volt_diff)
    ps = get_power_spectrum(time_series)
    rms = get_rms_voltage(ps, freq_min, freq_max, freq, time_series_len)
    rms_values.append(rms)
    while (time.perf_counter() - st) <= sinterval:
        pass
t = time.perf_counter() - t0    
adc.stopContinuousConversion()
print('Time elapsed: %.9f s.' % t)

binary_data = []
for interval in interval_indices: #goes through each interval -- one for each binary character
    if np.mean(rms_values[interval[0]:interval[1]]) < cutoff:
        binary_data.append(0) #if in concentrated state, give 0
    else:
        binary_data.append(1) #if in relaxed state, give 1
predicted_sentence = get_sentence_from_binary(binary_data)
print('Read binary: ', binary_data)
print('\n \n')
print('Alpha Waves read that you want to say: \n')
print(predicted_sentence)
print()
plt.plot(rms_times,rms_values)
plt.show()
input('Press <Enter> to end program')



        
        
        
        
        
        
        
        
        
        
        
