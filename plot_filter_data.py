import pickle
import numpy as np
import collections
import matplotlib.pyplot as plt

filename = input('Please enter filename to read: ')
file = open(filename, 'rb')
data = pickle.load(file)
file.close()

title = input('Please enter plot title (or <Enter for none): ')
caption = input('Please enter caption (or <Enter> for none):')

gain_dict = data[0]
stddev_dict = data[1]

frequencies = gain_dict.keys()
gains = gain_dict.values()
stddevs = stddev_dict.values()

if caption is None:
    fig, ax = plt.subplots()
else:
    fig = plt.figure()
    ax = fig.add_axes((0.1,0.2,0.8,0.7))
    fig.text(.5, 0.02, caption, ha='center', fontsize=12, wrap=True)
    
ax.errorbar(frequencies, gains, yerr = stddevs, fmt='bo')
ax.set(xlabel='Frequency (Hz)', ylabel='Voltage Gain', title=title)    
plt.show()
input('Press <Enter> to end')