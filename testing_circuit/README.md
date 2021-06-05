# Testing Circuit

To test each component of our circuit, we used a Digilent OpenScope MZ to generate voltage signals and the ADC to read voltage signals. We can not recommend
this since the sale of OpenScope MZ has been discontinued by Digikey. Typically one can calculate the gain of each component solely with an oscilloscope, but if
you happen to want to read your data with an ADC these codes can help.

## figures/ 
The **figures/** folder contains graphs of the gain values for each element of the circuit (in absolute voltage gain units and decibel units) except 
for the amplifiers. It also has a graph of gains for the whole circuit (except amplifiers). All circuit elements were tested with sinusoidal waves of 1 Volt,
and standard error was calculated by taking 5 samples each.

## pickle_data/
The **pickle_data/** folder contains the voltage gain and standard error data for each filter in pickle file. The format is somewhat strange because each pickle file is 
a 2 element numpy array, where each element is an OrderedDict() with frequency as keys and gains / standard error as values respectively. Despite being an OrderedDict(),
the frequencies are not necessarily in order.

## testfiltergains.py
Python program to calculate filter gains. User must switch going through the filter or not before going into the ADC manually.
