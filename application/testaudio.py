import pygame
from pygame import mixer #modulo for playing audio
mixer.init() 
alert=mixer.Sound('richard.wav') #sets alert sound

input('press <Enter> to start')
for i in range(2):
    alert.play()


input('press <Enter> to stop')

mixer.stop()