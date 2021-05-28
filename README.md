# EEG
This project builds an EEG headset which will allow the user to send morse code to a computer through their brain wave activity. It is a basic form of “mind reading” and has applications in helping paralyzed people who can not speak or write. The circuit amplifies electrical signals from the brain and uses various high and low pass analog filters. We then post-process the data using digital filters. We hope to demonstrate the successful communication of words in a timely manner through brainwave data. The biggest challenge is that an EEG which measures voltage differences across your scalp can produce noisy and sometimes unreliable signals, so careful filtering and project design must be done. Our general approach is to distinguish between two mental states with the EEG, whether a person is relaxed (alpha waves, 8-12Hz) or if they are concentrating / alert (beta waves, 12-30Hz). The user can then switch between these two mental states over time signaling a beep or no beep to communicate in morse code. We will use the following link as a starting point (found on instructables.com/DIY-EEG-and-ECG-Circuit/). 

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
