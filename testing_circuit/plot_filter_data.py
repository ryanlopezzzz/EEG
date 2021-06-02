"""
PROGRAM DESCRIPTION:

We use this program to graph pickled filter gain data in voltage gain and decibel units.
"""
import os
import pickle
import numpy as np
import collections
import matplotlib
import matplotlib.pyplot as plt

filename = input('Please enter filename path to read: ')
filename = os.path.join('pickle_data', filename)+'.pickle'
file = open(filename, 'rb')
data = pickle.load(file)
file.close()

title = input('Please enter plot title (or <Enter for none): ')
caption = input('Please enter caption (or <Enter> for none):')

gain_dict = data[0]
stderr_dict = data[1]

frequencies = gain_dict.keys()
gains = gain_dict.values()
stderrs = stderr_dict.values()

frequencies = np.fromiter(frequencies, dtype=float)
gains = np.fromiter(gains, dtype=float)
stderrs = np.fromiter(stderrs, dtype=float)

if caption is None:
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
else:
    fig1 = plt.figure()
    ax1 = fig1.add_axes((0.1,0.2,0.8,0.7))
    fig1.text(.5, 0.02, caption, ha='center', fontsize=12, wrap=True)
    
    fig2 = plt.figure()
    ax2 = fig2.add_axes((0.1,0.2,0.8,0.7))
    fig2.text(.5, 0.02, caption, ha='center', fontsize=12, wrap=True)
    
ax1.errorbar(frequencies, gains, yerr = stderrs, fmt='bo', capsize=5, ms=5)
ax1.axvspan(8, 12, alpha=0.25, label='Alpha Wave Range', linestyle='--', color='purple')
ax1.set(xlabel='Frequency (Hz)', ylabel='Voltage Gain', title=title)
ax1.set_xscale('log')
ax1.set_xticks([2,4,6,8,12,20,40,60,100])
ax1.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.legend()

gains_db = 20*np.log10(gains) #gains in decibel units
stderrs_db = (20/np.log(10)) * np.divide(stderrs, gains) #get differential error
ax2.errorbar(frequencies, gains_db, yerr = stderrs_db, fmt='bo', capsize=5, ms=5)
ax2.axvspan(8, 12, alpha=0.25, label='Alpha Wave Range', linestyle='--', color='purple')
ax2.set(xlabel='Frequency (Hz)', ylabel='Gain (dB)', title=title)
ax2.set_xscale('log')
ax2.set_xticks([2,4,6,8,12,20,40,60,100])
ax2.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax2.legend()

plt.show()

input('Press <Enter> to end')