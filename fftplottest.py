ACQTIME = 5
SPS = 920
VRANGE = 4096
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
        indata[i] = 0.001*adc.getLastConversionResults()
        #if indata[i] > 4:
        #        indata[i] = indata[i]-2*0.001*VRANGE
        #print(indata[i])
        while (time.perf_counter() - st) <= sinterval:
                pass

t = time.perf_counter() - t0

adc.stopContinuousConversion()

xpoints = np.arange(0, ACQTIME, sinterval)

print('Time elapsed: %.9f s.' % t)
print()

f1, ax1 = plt.subplots()
ax1.plot(xpoints, indata)
f1.show()

ave=np.mean(indata)
newdata=indata-ave
ft = np.fft.fft(newdata)
ftnorm = abs(ft)
ps =ftnorm**2
xvals = np.fft.fftfreq(len(ps), d=1.0/SPS)
f2, ax2 =plt.subplots()
plt.xlim(0,100)
ax2.plot(xvals, ps)
f2.show()

valuemax=np.amax(ps)
freqwhere=np.where(ps==valuemax)
freqmax=xvals[freqwhere[0]]
if freqmax.shape != (1,1):
        freqmax=freqmax[0]
print('Dominant Frequency is: ', int(abs(freqmax)), 'Hz')
input('\nPress <Enter> to exit...\n')

