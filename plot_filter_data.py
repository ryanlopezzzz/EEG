import pickle
import numpy as np
import collections
import matplotlib.pyplot as plt

filename = input('Please enter filename to read: ')
file = open(filename, 'rb')
data_dict = pickle.load(file)
file.close()

frequencies = []
for key in data_dict.keys():
    frequencies.append(float(key))
gains = data_dict.values()

plt.scatter(frequencies, gains)
plt.show()
input('Press <Enter> to end')