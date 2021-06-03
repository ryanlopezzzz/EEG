import pygame,sys,random

# function to draw 2 floor images next to each other
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos+288,450))
    
# create new pipe with random height in the pipe height list
def create_pipe():
    random_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (350,random_height))
    top_pipe = pipe_surface.get_rect(midbottom = (350,random_height-200))
    return bottom_pipe, top_pipe
    
# take the pipe list as argument, move them to left (the same rate as floor?)
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 1
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface,pipe)
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

# game variables
gravity = 0.05 # bird tends to fall down, we can change this too
bird_movement = 0
game_active = True
score = 0
high_score = 0

# Load surfaces
bg_surface = pygame.image.load('assets/background-day.png').convert()

floor_surface = pygame.image.load('assets/base.png').convert()
floor_x_pos = 0

bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect = bird_surface.get_rect(center = (50,256))

pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_list = [] # a list of pipes that pop up every second
SPAWNPIPE = pygame.USEREVENT # an event triggered by timer
pygame.time.set_timer(SPAWNPIPE, 2000) # the event is triggered every 1.2 second
pipe_height = [200,300,400] # all the possible pipe heights

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144, 256))

# Main game loop
while True:
    
    for event in pygame.event.get(): # all events that pygame can detect
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 1
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50,256)
                bird_movement = 0
                score = 0
        
        #every 1.2 second, the event is triggered which creates a green pipe on screen
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe()) # extend include whatever that is in the tuple
    
    # display background
    screen.blit(bg_surface,(0,0))
    
    # display and create continuously moving floor effect
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0
        
    if game_active:
        # bird movement (weighed down by gravity, and goes up every time click space bar)
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird_surface,bird_rect)
        game_active = check_collision(pipe_list)
    
        # pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        score += 0.01
        
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    
    pygame.display.update()
    clock.tick(120) # change frame rate based on how the speed of the game feels
