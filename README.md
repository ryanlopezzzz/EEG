# EEG
This project builds an EEG headset which will allow the user to send morse code to a computer through their brain wave activity. It is a basic form of “mind reading” and has applications in helping paralyzed people who can not speak or write. The circuit amplifies electrical signals from the brain and uses various high and low pass analog filters. We then post-process the data using digital filters. We hope to demonstrate the successful communication of words in a timely manner through brainwave data. The biggest challenge is that an EEG which measures voltage differences across your scalp can produce noisy and sometimes unreliable signals, so careful filtering and project design must be done. Our general approach is to distinguish between two mental states with the EEG, whether a person is relaxed (alpha waves, 8-12Hz) or if they are concentrating / alert (beta waves, 12-30Hz). The user can then switch between these two mental states over time signaling a beep or no beep to communicate in morse code. We will use the following link as a starting point (found on instructables.com/DIY-EEG-and-ECG-Circuit/). 

# List of Components
* Raspberry Pi 4
* Bread board and wires
* Instrumental Amplifier AD622ANZ
* Quad Operational Amplifier TL084x
* Capacitors and Resistors
* Potentiometer CT6EW102-ND, 1kOhm
* Open Scope MZ
* TDE-2143-C EEG GOLD CUP ELECTRODES

# Eletrode Placement for Alpha Waves Measurements
There are many possible electrode placements depending on what wave one choose to measure. In our project, we measure alpha waves originating from the occipital lobe, because they are the strongest EEG signals. We need to use three electrode: one at the left mastoid (the bone at the back of the left ear) which is connected to the ground of the circuit; one located one inch above and one inch right of the nasion (the midline bony depression between the eyes where the frontal and two nasal bones meet); the last one located one inch above and one inch right of the inion (the projecting part of the occipital bone at the base of the skull). The 2nd and 3rd electrode placements are approximately in O2 and Fp2 regions in the below diagram:
![](images/head.png)

The voltage difference oscillations between the 2nd and 3rd electrodes are the target alpha waves, which have a signature frequency in the range of 8-12 HZ.

# Circuit Design
![](images/circuit.png)
The above picture is the final schematic. Note that the circuit ground is in fact 3.3V above the ADC ground to make sure the signal is always positive because the ADC chip cannot read negative voltage. The electrode behind the ear is connected to the circuit ground. The other two electrodes are fed into the first instrumental amplifier.

The circuit can be roughly divided into the following sections:
* Instrumental Amplifier (gain ~91)
* Notch Filter (60 HZ, gain = 1)
* High Pass Filter (Fc = 7.2 Hz)
* Low Pass Filter (Fc = 32.9 Hz)
* Instrumental Amplifier with variable gain (gain ~ 90-460)
* Notch Filter (60 HZ, gain = 1)

Individual Sections will be discussed further below.

## Instrumental Amplifier (gain ~91)
![](images/circuit1.png)

## Notch Filter (60 HZ, gain = 1)
![](images/circuit2.png)

## High Pass Filter (Fc = 7.2 Hz)
![](images/circuit3.png)

## Low Pass Filter (Fc = 32.9 Hz)
![](images/circuit4.png)

## Instrumental Amplifier with variable gain (gain ~ 90-460)
![](images/circuit5.png)

## Notch Filter (60 HZ, gain = 1)
![](images/circuit6.png)

# Results
We built our circuit to measure Alpha waves which are from 8-12Hz. When relaxed the power of these waves should increase and when concentrating the power of these waves should decrease. To test relaxed state the user closes their eyes, to test concentrating the user opens their eyes and look at 'crazy' images.

### Lower Amplification Tests:

| Relaxed | Concentrating |
| --- | --- |
| 689 | 85 |
| 958 | 531 |
| 829 | 429 |
| 802 | 50 |
| 421 | 112 |

### Higher Amplification Tests:

| Relaxed | Concentrating |
| --- | --- |
| 5,294 | 23,384 |
| 4,848 | 36,822 |
| 5,077 | 39, 640 |
|11,051 | 55,365 |
| 5,748 | 32,897 |
