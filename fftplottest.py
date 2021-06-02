ACQTIME = 5
SPS = 920 #Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300.
VRANGE = 6144 #Full range scale in mV. Options: 256, 512, 1024, 2048, 4096, 6144.
nsamples = int(ACQTIME*SPS)
sinterval = 1.0/SPS

import sys
import time
import numpy as np
import matplotlib.pyplot as plt
from Adafruit import ADS1x15


indata = np.zeros(nsamples, 'float')

print()
print('Initializing ADC...')
print()

adc = ADS1x15()

adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=SPS)

input('Press <Enter> to start %.1f s data acquisition...' % ACQTIME)
print()

t0 = time.perf_counter()

for i in range(nsamples):
        st = time.perf_counter()
        indata[i] = 0.001*adc.getLastConversionResults() #Gets voltage in volts
        #if indata[i] > 0.001*VRANGE:
        #        indata[i] = indata[i]-2*0.001*VRANGE #If in upper half of vrange, should be negative
        indata[i] -= 3.3 #adc ground is 3.3 volts below circuit ground 
        while (time.perf_counter() - st) <= sinterval:
                pass

t = time.perf_counter() - t0

adc.stopContinuousConversion()

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t)
print()

f1, ax1 = plt.subplots()
ax1.plot(xpoints, indata)
ax1.set(xlabel='Time (s)', ylabel='Voltage', title='Raw Signal')    
f1.show()

ave=np.mean(indata)
newdata=indata-ave
ft = np.fft.fft(newdata)
ftnorm = abs(ft)
ps =ftnorm**2
xvals = np.fft.fftfreq(len(ps), d=1.0/SPS)
f2, ax2 =plt.subplots()
plt.xlim(0,500)
ax2.plot(xvals, ps)
ax2.set(xlabel='Frequency (Hz)', ylabel='FFT Power Spectrum', title='Power Spectrum')    
f2.show()

valuemax=np.amax(ps)
freqwhere=np.where(ps==valuemax)
freqmax=xvals[freqwhere[0]]
if freqmax.shape != (1,1):
        freqmax=freqmax[0]
print('Dominant Frequency is: ', int(abs(freqmax)), 'Hz')
alphamin=8
alphamax=12
alphamag=np.mean(ps[(xvals <= alphamax) & (xvals >= alphamin)])
print('Alpha wave magnitude is: ' + str(alphamag))
input('\nPress <Enter> to exit...\n')

