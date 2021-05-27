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
        
def check_same_frequencies():
    """
    Makes sure all data files have the same frequency
    """
    freq = circuit_data[0].keys()
    for i in range(len(filter_data)):
        if filter_data[i][0].keys() != freq:
            print('Error: not all frequencies match for data files')
            quit()

check_same_frequencies()

filter_gains_data = [] #Size: [num of filters, num of frequencies]
filter_stderr_data = [] #Size: [num of filters, num of frequencies]
circuit_gains_data = [] #Size: [num of frequencies]
circuit_stderr_data = [] #Size: [num of frequencies]


circuit_freq = np.fromiter(circuit_data[0].keys(), dtype=int) #freq measured in circuit
sorted_index = np.argsort(circuit_freq) #gets index to sort array by increasing frequency
freq = circuit_freq[sorted_index] #Array of measured frequencies in ascending order
circuit_gains_data = np.fromiter(circuit_data[0].values(),dtype=float)[sorted_index] #first element of circuit_data is gains data dict
circuit_stderr_data = np.fromiter(circuit_data[1].values(),dtype=float)[sorted_index] #second element of circuit_data is stderr data dict

for i in range(len(filter_filenames)):
    filter_freq = np.fromiter(filter_data[i][0].keys(), dtype=int)
    sorted_index = np.argsort(filter_freq)
    
    filter_gains_data_i = np.fromiter(filter_data[i][0].values(),dtype=float)[sorted_index] #Same for filters as circuit above
    filter_gains_data.append(filter_gains_data_i)
    filter_stderr_data_i = np.fromiter(filter_data[i][1].values(),dtype=float)[sorted_index]
    filter_stderr_data.append(filter_stderr_data_i)

pred_circuit_gain = np.full((len(freq)), 1)
for i in range(len(filter_filenames)):
    pred_circuit_gain = pred_circuit_gain * filter_gains_data[i]
    
plt.plot(freq, pred_circuit_gain)
plt.plot(freq, circuit_gains_data)
plt.show()
input('Press <Enter> to exit')
