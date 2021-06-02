"""
PROGRAM DESCRIPTION:

Loads saved brain data into two lists (relaxed and concentrated) which contain time series data in numpy array format.
"""

import os
import sys
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder
import numpy as np
import matplotlib.pyplot as plt
import pickle
from analysis_tools import get_power_spectrum, get_rms_voltage

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
        
relaxed_file = os.path.join(save_path,'relaxed.pickle')
concentrated_file = os.path.join(save_path,'concentrated.pickle')

file = open(relaxed_file, 'rb')
relaxed_data = pickle.load(file)
file.close()
file = open(concentrated_file, 'rb')
concentrated_data = pickle.load(file)
file.close()
print("There are ", len(relaxed_data), " relaxed data samples")
print("There are ", len(concentrated_data), "concentrated data samples")

relaxed_data = np.array(relaxed_data)
concentrated_data = np.array(concentrated_data)
print(relaxed_data.shape)
print(concentrated_data.shape)

