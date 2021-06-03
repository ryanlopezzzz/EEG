"""
Need to test sps or max_frame_rate to make sure fft is accurate

Note
- in the beginning rms are 0 so bird will instantly die and the game will be at the game over page, check if this is ok when running
- when bird dies, we currently do not stop take data
"""

import pygame,sys,random
import time
import numpy as np
from Adafruit import ADS1x15
import pickle
import collections

from analysis_tools import get_power_spectrum, get_rms_voltage
sys.path.insert(1, os.path.dirname(os.getcwd())) #This allows importing files from parent folder

"""
Parameters related to game difficulty
"""
TOP_BOTTOM_SEP = 200 # how much one want the top and bottom pipe to be separated by
FLOOR_RATE = 1 # how fast floor moving left
PIPE_RATE = 1 # how fast pipe moving left
PIPE_HEIGHT = [200,300,400] # all the possible pipe heights
PIPE_INTERVAL = 2000 # time interval between pipes, unit ms
MAX_FRAME_RATE = 128 # Same as SPS, Caps the # frame/sample per second
SCORE_RATE = 0.01
INITIAL_BIRD_Y = 50 # initial y coordinate of the bird
# gravity = 0.5


"""
EEG SECTION
"""

adc = ADS1x15() #Instantiate Analog Digital Converter
VRANGE = 4096
sps = MAX_FRAME_RATE # Samples per second to collect data. Options: 128, 250, 490, 920, 1600, 2400, 3300. Here, this is the same as frame rate
sinterval = 1.0/sps
sampletime = 3 # how long to look back in time for current alpha waves
time_series_len = sampletime * sps
time_series = np.zeros(time_series_len)
freq = np.fft.fftfreq(time_series_len, d=1/sps) #Gets frequencies in Hz/sec
freq_min = 8 #minimum freq in Hz for alpha waves
freq_max = 12 #maximum freq in Hz for alpha waves

"""
Calibration code
"""

def calibration(calibration_time,sps,freq_min=8,freq_max=12,print_time=False):
    """
    code for calibration
    """
    nsamples = calibration_time*sps
    sinterval = 1/sps
    time_series = np.zeros(nsamples)
    adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps)
    t0 = time.perf_counter()
    for i in range(nsamples): #Collects data every sinterval
        st = time.perf_counter()
        time_series[i] = 0.001*adc.getLastConversionResults() #Times 0.001 since adc measures in mV
        time_series[i] -= 3.3 #ADC ground is 3.3 volts above circuit ground
        while (time.perf_counter() - st) <= sinterval:
            pass
    t = time.perf_counter() - t0
    adc.stopContinuousConversion()
    if print_time:
        print('Time elapsed: %.9f s.' % t)
    freq = np.fft.fftfreq(nsamples, d=1.0/sps)
    ps = get_power_spectrum(time_series)
    rms = get_rms_voltage(ps, freq_min, freq_max, freq, nsamples)
    
    return rms
    
calibration_time = 10

input('Press <Enter> to start %.1f s calibration for relaxed data...' % calibration_time)
print()
up_level = calibration(calibration_time,sps)

input('Press <Enter> to start %.1f s calibration for concentrated data... Do not blink please!' % calibration_time)
print()
low_level = calibration(calibration_time,sps)


"""
Game Section
"""

# function to draw 2 floor images next to each other
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos+288,450))
    
# create new pipe with random height in the pipe height list
def create_pipe():
    random_height = random.choice(PIPE_HEIGHT)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_height))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_height - TOP_BOTTOM_SEP))
    return bottom_pipe, top_pipe
    
# take the pipe list as argument, move them to left (the same rate as floor?)
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= PIPE_RATE
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        # draw bottom pipe
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
        # draw top pipe
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True) # false flip in x direction True for flip in y direction
            screen.blit(flip_pipe,pipe)

# check if bird_rect is colliding with any of the pipe_rect, also hit the window frame
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= 450: # 450 is the floor y coordinate
        return False
    return True

def score_display(game_state):
    if game_state == 'main_game':
        score_surface= game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface= game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (144,50))
        screen.blit(score_surface,score_rect)
        
        high_score_surface= game_font.render(f'Best Score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (144,425))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# initializing steps
pygame.init()
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf',20)

# initialize game variables
game_active = True
# bird_movement = 0
score = 0
high_score = 0

# Load surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center = (INITIAL_BIRD_Y,256))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = [] # a list of pipes that pop up every second
SPAWNPIPE = pygame.USEREVENT # an event triggered by timer
pygame.time.set_timer(SPAWNPIPE, PIPE_INTERVAL) # the event is triggered every PIPE_INTERVAL second

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))


"""
Main game loop
"""

### t0 = time.perf_counter()
### times = []
### for i in range(40):

adc.startContinuousDifferentialConversion(2, 3, pga=VRANGE, sps=sps) #Returns the voltage difference in millivolts between port 2 and 3 on the ADC.
while True:

    # data taking part
    time_series = np.roll(time_series, -1) #rolls all voltage values back 1.
    time_series[-1] = 0.001*adc.getLastConversionResults()-3.3 #0.001 to convert mV -> V, adc ground is 3.3 volts above circuit ground, puts into most current time_series point
    ps = get_power_spectrum(time_series)
    rms_value = get_rms_voltage(ps, freq_min, freq_max, freq, time_series_len)
    
    # game part
    
    for event in pygame.event.get(): # all events that pygame can detect
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            """
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 1
            """
            # press space key to restart the game
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (INITIAL_BIRD_Y,256)
                #bird_movement = 0
                score = 0
        
        
        #every PIPE_INTERVAL second, the event is triggered to create a new pipe
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # extend allows list to include whatever that is in the tuple
    
    # display background
    screen.blit(bg_surface,(0,0))
    
    # display and create continuously moving floor effect
    floor_x_pos -= FLOOR_RATE
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
        
    if game_active:
        # bird_movement += gravity
        # bird_rect.centery += bird_movement
        
        # more concentrate = higher
        bird_rect.centery = 512*(rms_value-low_level)/(up_level-low_level)
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)
    
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        score += SCORE_RATE
        
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    
    pygame.display.update()
    
    clock.tick(MAX_FRAME_RATE)
    ### times.append(time.perf_counter()-t0)

### print(times)
### header code for testing how much time elapse during one loop, important for fft
