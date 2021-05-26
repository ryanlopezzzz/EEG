import pickle
import numpy as np
import collections
import matplotlib.pyplot as plt

while True:
    filter_filenames = input('Please enter filter data file names to product gains (separated by spaces): ')
    filter_filenames = filter_filenames.split() #gets list of filenames
    circuit_filename = input('Please enter circuit data file name: ')
    
    try:
        filter_data = []
        for i in range(len(filter_filenames)):
            file = open(filter_filenames[i], 'rb')
            filter_data.append(pickle.load(file))
            file.close()
        
        file = open(circuit_filename, 'rb')
        circuit_data = pickle.load(file)
        file.close()
        break
    except:
        print('Error opening files')

def convert_np_array(filter_data, circuit_data):
    

def sort_data():
    """
    Sorts the filter and circuit data so that the measured frequencies are in increasing order.
    """
    circuit_freq = np.fromiter(circuit_data[0].keys(), dtype=int) #freq measured in circuit
    sorted_index = np.argsort(circuit_freq) #gets index to sort array by increasing frequency
    
    
    

def check_same_frequencies():
    
frequencies = gain_dict.keys()
gains = gain_dict.values()
stderrs = stderr_dict.values()

frequencies = np.fromiter(frequencies, dtype=float)
gains = np.fromiter(gains, dtype=float)
stderrs = np.fromiter(stderrs, dtype=float)