"""
PROGRAM DESCRIPTION:

Loads saved brain data into two lists (relaxed and concentrated) which contain time series data in numpy array format.
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
import pickle
from analysis_tools import get_power_spectrum, get_rms_voltage, gaussian_eval

#These should match data being taken
ACQTIME = 5
SPS = 920 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS
freq_min = 8 #min freq of alpha waves
freq_max = 12 #max freq of alpha waves

"""
Asks user where to locate data
"""
while True:
    person_name = input('Please enter name to load data (hak/ryan/ruining):')
    if person_name in ['hak', 'ryan', 'ruining']:
        break
    else:
        print('Please enter a correct formatted name')
while True:        
    save_folder = input('Please input folder name to load:')
    save_path = os.path.join(person_name, save_folder)
    if os.path.isdir(save_path): #Check if already a directory
        break
    else:
        print("Please enter an existing folder name")

"""
Loads data files
"""
relaxed_file = os.path.join(save_path,'relaxed.pickle')
concentrated_file = os.path.join(save_path,'concentrated.pickle')

file = open(relaxed_file, 'rb')
relaxed_data = pickle.load(file)
file.close()
file = open(concentrated_file, 'rb')
concentrated_data = pickle.load(file)
file.close()
print("There are", len(relaxed_data), "relaxed data samples")
print("There are", len(concentrated_data), "concentrated data samples")
relaxed_data = np.array(relaxed_data)
concentrated_data = np.array(concentrated_data)

"""
Calculates statistics on data
"""
freq = np.fft.fftfreq(nsamples, d=1.0/SPS) #frequencies for FFT of data
relaxed_rms = np.zeros(len(relaxed_data))
concentrated_rms = np.zeros(len(concentrated_data))

for index, time_series in enumerate(relaxed_data):
    ps = get_power_spectrum(time_series)
    relaxed_rms[index] = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)
for index, time_series in enumerate(concentrated_data):
    ps = get_power_spectrum(time_series)
    concentrated_rms[index] = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)

V0, wrong_relax, wrong_concentrate = gaussian_eval(relaxed_rms, concentrated_rms)
r_mean = np.mean(relaxed_rms)
r_std = np.std(relaxed_rms)
c_mean = np.mean(concentrated_rms)
c_std = np.std(concentrated_rms)
xpoints = np.linspace(c_mean-4*c_std, r_mean+4*r_std, 1000)

fig, ax = plt.subplots()
ax.hist(relaxed_rms, bins=6, density=True, label='Relaxed')
ax.hist(concentrated_rms, bins=6, density=True, label='Concentrated')
ax.plot(xpoints, norm.pdf(xpoints, r_mean, r_std), linestyle='--', color='red') #Relaxed gaussian dist
ax.plot(xpoints, norm.pdf(xpoints, c_mean, c_std), linestyle='--', color='green') #Concentrated gaussian dist
plt.axvline(V0, color='purple', linestyle='--', label='Cutoff Voltage')
ax.set(xlabel='RMS Alpha Wave Voltage (V)', ylabel='Frequency', title='Concentrated / Relaxed EEG Data')
ax.legend()
plt.show()
print('Chance of getting incorrect classification is', 50*(wrong_relax+wrong_concentrate))
input('Press <Enter> to end program')
plt.close('all')

