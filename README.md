# Project Description (CHANGE) 
This project builds an EEG circuit which will allow the user to send morse code to a computer through their brain wave activity. It is a basic form of “mind reading” and has applications in helping paralyzed people who can not speak or write. The circuit amplifies electrical signals from the brain and uses various high and low pass analog filters. We then post-process the data using digital filters, statistical methods, and Single Component analysis. We hope to demonstrate the successful communication of words in a timely manner through brainwave data. The biggest challenge is that an EEG which measures voltage differences across your scalp can produce noisy and sometimes unreliable signals, so careful filtering and project design must be done. Our general approach is to distinguish between two mental states with the EEG, whether a person is relaxed (alpha waves, 8-12Hz) or if they are concentrating / alert (beta waves, 12-30Hz). The user can then switch between these two mental states over time signaling a beep or no beep to communicate in morse code. We will use the following link as a starting point (found on instructables.com/DIY-EEG-and-ECG-Circuit/). 

## EEG Crash Course
EEG stands for electroencephalogram. It measures voltage fluctuations resulting from ionic current within the neurons of the brain. 
Neurons exchange ions with environment and when many ions are pushed out of many neurons at the same time, they repel and push each other forming a wave. The waves reachs scalp and can be captured by the electrodes. Note that EEG does not capture the activities of single neurons-the electric potential is way to small to be captured. Instead, EEG measures the voltage difference in 2 electrodes over time, which reflect synchronized activity over a network of neurons. Spatially well-aligned neurons fire together, so the electrode placements need to be in specific regions to observe oscillations/waves of interest. These waves have different characteristic frequency, magnitude, and are related to different brain activties. 

In our project, we measure alpha waves originating from the occipital lobe because they are one of the strongest EEG signals. Alpha waves have a signature frequency in the range of 8-12 HZ. Alpha waves are reduced with open eyes, drowsiness, and sleep. It is still under study but main stream research shows it represent the activity of the visual cortex in an idle state. Our circuit also has the capacity to measure beta waves (12-30 HZ).

# Methods

## Eletrode Placement for Alpha Waves Measurements
There are many possible electrode placements depending on what wave one choose to measure. In our project, we measure alpha waves  We need to use three electrode: one at the left mastoid (the bone at the back of the left ear) which is connected to the ground of the circuit; one located one inch above and one inch right of the nasion (the midline bony depression between the eyes where the frontal and two nasal bones meet); the last one located one inch above and one inch right of the inion (the projecting part of the occipital bone at the base of the skull). The 2nd and 3rd electrode placements are approximately in O2 and Fp2 regions in the below diagram:

<img src="images/head.png" width=300>

The voltage difference oscillations between the 2nd and 3rd electrodes are the target alpha waves, which is then fed to the circuit to be amplified, filtered, and analyzed.

## List of Components
* Raspberry Pi 4
* [TDE-2143-C EEG Gold Cup Electrodes](http://www.discountdisposables.com/index.php?act=viewProd&productId=16)
* Electrode gel, tape, bandana
* [Instrumental Amplifier AD622ANZ](https://www.analog.com/media/en/technical-documentation/data-sheets/AD622.pdf)
* [Quad Operational Amplifier TL084x](https://www.ti.com/lit/ds/symlink/tl081a.pdf?HQS=dis-dk-null-digikeymode-dsf-pf-null-wwe&ts=1619312373475&ref_url=https%253A%252F%252Fwww.digikey.ca%252F)
* Potentiometer CT6EW102-ND, 1kOhm
* Capacitors and Resistors
* two 9V batteries
* Bread board and wires
* Open Scope MZ (Used as oscilloscope and wave generator for testing circuit only)

## Wiring
![](images/Wiring.png)

Note that the circuit ground is 3.3V above the ADC/Rpi ground to make sure the signal is always positive because the ADC chip cannot read negative signals. The electrode behind the ear is connected to the 3.3V circuit ground. The other two electrodes are fed into the first instrumental amplifier. The instrumental amplifiers are fed with -9V to 9V of power with respect to the 3.3V ground, by connecting one 9V battery the correct way, and one backwards. The ADC and RPI are connected to the true ground.

## Circuit Schematic
![](images/circuit.png)

The circuit consist of the following sections:
* Instrumental Amplifier (gain ~91)
* Notch Filter (60 HZ, gain = 1)
* High Pass Filter (Fc = 7.2 Hz)
* Low Pass Filter (Fc = 32.9 Hz)
* Instrumental Amplifier with variable gain (gain ~ 90-460)
* Notch Filter (60 HZ, gain = 1)

Individual Section are discussed further below.

### Instrumental Amplifier (gain ~91)
<img src="images/circuit1.png" width=400>
Alpha wave signals is 15-50 uV so we need a lot of amplification in the circuit. 
An instrumentation amplifier takes as its inputs 2 voltages, and outputs the difference between the two multiplied by some gain given by: G = 1 + (50.5 kOhm)/R, where R is the total resistance between pin 1 and 8. Note it is possible to make home-made instrumentation amplifier usually with 3 op-amps. However, it suffers from a low CMRR unless precision resitors are used.

### 1st Notch Filter (60 HZ, gain = 1)
<img src="images/circuit2.png" width=600>
The biggest source of noise in our system is centered at 60 Hz due to power line interference. This noise is present even though we use batteries to power the circuit. Thus we have 2 notch filters in the circuit (filters that have a severe reduction of gain around 1 particular frequency). The first notch filter intends to filter out interference before more gains are applied. 

* [More readings on PLI in biopotentials applications](https://www.intechopen.com/books/compendium-of-new-techniques-in-harmonic-analysis/cancelling-harmonic-power-line-interference-in-biopotentials)

The notch frequency is given by f = 1/(2 PI R C) where R = R3 = R5. The other two resistor values are related to the quality factor of the filter, which determines how sharp the attenuation is.

### High Pass Filter (Fc = 7.2 Hz)
<img src="images/circuit3.png" width=600>
The high pass filter intends to filter out frequencies corresponding to galvanic skin response across our head. This interference is primarily low frequency. A second order filter design is used here and is shown to be necessary for noise reduction. 

### Low Pass Filter (Fc = 32.9 Hz)
<img src="images/circuit4.png" width=600>
The EEG waves of interest to our project are alpha (8-12 HZ) and beta waves (12-30 HZ). Thus, we are not interested in frequency > 30HZ and filter them out. A second order filter design is used.

### Instrumental Amplifier with variable gain (gain ~ 90-460)
<img src="images/circuit5.png" width=400>

This 90-460 gain is on top of the 90x gain from the first instrumentation amplifier. Alpha wave amplitude varies from person to person, from about 10 to 30 uV. Using a middle value of 20 uV, this means the ending voltage reading could range from 90*90*20e-6 = 0.162V to 460*90*20e-6 = 0.828V. The variable gain is achieved by putting resitors in series and in parallel. The gain is roughly in the range of 90-460, which corresponds to potentiometer value 1k (maximum) to 0 (minimum).

To adjust the potentiometer, start taking readings and make sure one is not moving at all. Make sure voltages don't fluctuate offscreen, but avoid making it too small because then the errors incurred from digitally reading the data into rpi would be relatively increased. 

### 2nd Notch Filter (60 HZ, gain = 1)
<img src="images/circuit6.png" width=600>
Another 60 HZ is necessary at the end of the circuit since the power line interferences seep into the circuit through prior steps. 

## Debugging Tips (RYAN)
Debugging has been a pain in this project, but we got down a few tips~


## Post-processing (LINK THE CODE IN GITHUB TO EACH RELEVANT SECTION)
### Data Taking Methods (RYAN)

### Digital Filtering (RYAN)
Inverse forier and power calculation within frequency range 8-12 HZ


### Gaussian Analysis and Voltage Threshold Determination
[Gaussian_eval.py](link later)

This code is created to 1) find the optimal voltage threshold which separates relaxed and concentrated data and 2) Evaluate how distinct the relaxed and concentrated datasets using statistical analysis.

We approximate concentrated and relaxed brain wave data sets each as normal Gaussian distributions. The cross point of the two gaussians give the best threshold voltage V0 which separates relaxed and concentrated data. This voltage threhold would minimizes overall wrong classifications. The overlap area divided by 2 give the probability of wrong classification since we have two normal distributions. More specifically, the ratio of overlap area left of V0 to right of V0 gives the percentage of wrong estimation being we guessed concentrated but is actually relaxed.


# Results

## Filter Performance
<img src="testing_circuit/figures/circuit_VG.png" width=600>
<img src="testing_circuit/figures/circuit_dB.png" width=600>
(RYAN)
(EXPLAIN DB AND TALK ABOUT THE NECESSARY LEVEL OF NOISE ATTENUATION TO SEE BRAIN WAVE DATA)

## Alpha Wave Data
(RYAN PLOT THE IMAGES)


# Applications

## EEG Bird (inspired by Flappy Bird) - Ruining
This program is inspired by the game Flappy Bird, but with several rule changes so that it can be adapted to EEG. Firstly, there is no "gravity" that makes the bird fall. Secondly, instead of clicking at the screen to give bird a boost up, the bird's y coordinate has a direct relation with the EEG signal. To achieve this, we ask the user to record 10 seconds each of pure concentrated and relaxed data, so that we can calibrate the top screen of the game to concentrated voltage level, and bottom screen of the game to relaxed voltage level. This calibration is very necessary since EEG signal vary from person to person, and we also have an adjustable gain section in the circuit. To stablize the height of the bird, we also does a rms calculation over the last 3 seconds of data and use the rms as the height of the bird. There are a number parameters one can adjust in the beginning of the program to adjust the difficulty of the game play, such as the separation of the top pipe and bottom pipe, the rate ground moves to the left, etc. The program is plotted in pygame and is modified from https://github.com/clear-code-projects/FlappyBird_Python.

## Morse Code - Ryan

## Child Concentration Monitor - Hak




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

# Next Step

## Future improvement

### Artifact Removal Using Independent Component Analysis
The circuit has already shown success in filtering out noise in a wide frequency range (caused by skin, power line, etc). However, it is still subject to artifact signals unrelated to the brain waves of interest. The method we would like to experiment in the future is independent component analysis (ICA). It has shown to be a robust method used for EEG in field as well as in research to separate mixture of brain activities, as well as to eliminate contamination of signals by eye movements, blinks, muscle, heart and line noise.

ICA is a signal processing method to separate independent sources linearly mixed in several sensors. ICA recovers a version of the original sources, by multiplying the data with an unmixing matrix: U = WX, where X is the data with dimension (channel * time), U is the ICA source activties (components * time), and W is the ICA unmixing matrix.
ICA separates out the independent components by finding W such to minimize the gaussianicity of each data set.

To apply ICA to EEG data, we assume the following
* Mixing is linear at electrodes
* Propagation Delays are negligible
* Component time courses are independent
* Number of components are equal or less than the number of channels

The last condition poses a limitation to using ICA in our current project since the current circuit only takes in 3 electrode channel, one of which is ground. In order to implement ICA, we need to accomodate for more electrode data.

### Beta Wave
Our current circuit design has the capacity to measure beta wave (12-30 HZ). 

Description of beta wave from http://www.csun.edu/~vcpsy00i/dissfa01/xEEG_lesson.html:
"Beta rhythms occur in individuals who are alert and attentive to external stimuli or exert specific mental effort, or paradoxically, beta rhythms also occur during deep sleep, REM (Rapid Eye Movement) sleep when the eyes switch back and forth. Notice that the amplitude of beta rhythms tends to be lower than for alpha rhythms. This does not mean that there is less electrical activity, rather that the "positive" and "negative" activities are starting to counterbalance so that the sum of the electrical activity is less. Thus, instead of getting the wave-like synchronized pattern of alpha waves, desynchronization or alpha block occurs. So, the beta wave represents arousal of the cortex to a higher state of alertness or tension. It may also be associated with "remembering" or retrieving memories." (There are interesting facts about other brain waves on this website as well.)

### Robust Electrode Headset
Accurate positioning of electrodes plays an important role in good EEG data acquisition. There are several things we can improve:
* We need to find a more systematic method to pin point the electrode placement locations
* We need to use things more robust than just tape

## Potential Application
* Meditation Score App based on Alpha Wave
* Child Concentration Monitor for strict parents ;)
* Prosthetic limbs
* Communication device

# Reference and Acknolwedgement
* The project owes much thanks to instructables.com/DIY-EEG-and-ECG-Circuit/. We have based our procedures and methods on the instructions in this article, but we created our own circuit design and wrote our own code for data-taking and analysis. 
* Independent Component Analysis: http://arnauddelorme.com/ica_for_dummies/; youtube series https://www.youtube.com/watch?v=kWAjhXr7pT4&list=PLXc9qfVbMMN2uDadxZ_OEsHjzcRtlLNxc&index=2; https://sccn.ucsd.edu/~jung/Site/EEG_artifact_removal.html
* Flappy bird code reference: https://github.com/clear-code-projects/FlappyBird_Python
* EEG and Alpha Wave informtions are mainly from Wikipedia, and http://www.csun.edu/~vcpsy00i/dissfa01/xEEG_lesson.html.
