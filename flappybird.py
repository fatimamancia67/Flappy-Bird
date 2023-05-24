import random  
import sys 
import pygame
from pygame.locals import * 
  
# Global Variables for the game
window_width = 600
window_height = 499
  
# set height and width of window
window = pygame.display.set_mode((window_width, window_height))   
elevation = window_height * 0.8
game_images = {}      
framepersecond = 32
pipeimage = '/Users/fatimamancia/Desktop/flappybird/pipe.png'
background_image = '/Users/fatimamancia/Desktop/flappybird/background.jpg'

# program where the game starts
if __name__ == "__main__":          
      
    # For initializing modules of pygame library
    pygame.init()  
    framepersecond_clock = pygame.time.Clock()
      
    # This sets the title on top of game window
    pygame.display.set_caption('Flappy Bird Game')      
  
    # These lines are inputing the images from my desktop on my computer
    game_images['scoreimages'] = (
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/0.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/1.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/2.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/3.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/4.png').convert_alpha(),        
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/5.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/6.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/7.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/8.png').convert_alpha(),
        pygame.image.load('/Users/fatimamancia/Desktop/flappybird/9.png').convert_alpha()
    )
    game_images['flappybird'] = pygame.image.load("/Users/fatimamancia/Desktop/flappybird/bird.png").convert_alpha()   
    game_images['background'] = pygame.image.load("/Users/fatimamancia/Desktop/flappybird/background.jpg").convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load("/Users/fatimamancia/Desktop/flappybird/pipe.png").convert_alpha(),180), pygame.image.load("/Users/fatimamancia/Desktop/flappybird/pipe.png").convert_alpha())
  
    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()
      
    # This generates the random heights of the pipes 
    y2 = offset + random.randrange(0, int(window_height - 1.2 * offset))  
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        # upper Pipe
        {'x': pipeX, 'y': -y1},
          #lower Pipe
        {'x': pipeX, 'y': y2}  
    ]
    return pipe

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical < 0: 
        return True
  
    # This checks if the bird hits the upper pipe and tells it what to do
    for pipe in up_pipes:    
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] 
           and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
            
    # This checks if the bird hits the bottom pipe and tells it what to do
    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            return True
    return False


def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100
  
    # generating the two pipes to show up on the window screen as the bird goes on
    first_pipe = createPipe()
    second_pipe = createPipe()
  
    # these are lists for the pipes that are in the lower part of the screen
    down_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
         'y': second_pipe[1]['y']},
    ]
  
    # these are lists for the pipes that are in the upper part of the screen
    up_pipes = [
        {'x': window_width+300-mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
         'y': second_pipe[0]['y']},
    ]
  
    pipeVelX = -4 #the velocty of the pipes as the game goes on
  
    bird_velocity_y = -9  # how much the bird is moving as soon as the game starts
    bird_Max_Vel_Y = 10   
    bird_Min_Vel_Y = -8
    birdAccY = 1
      
     # the velocity of the bird when flapping
    bird_flap_velocity = -8
      
    # these things are true while the bird is flapping
    bird_flapped = False  
    while True:
         
        # This makes the keys to make the flapping work
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
  
        # if the flappybird crashes this function witll be true
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            return
  
        # this helps keep track of score
        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                  # prints the score
                your_score += 1
                print(f"Your your_score is {your_score}")
  
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY
  
        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation - vertical - playerHeight)
  
        # moves the pipe to the left and outside of screen as the bird moves
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX
  
        # Add a new pipe when the first is about
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])
  
        # if the pipe is out of the screen, it's remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)
  
        # This blits the game images
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
        window.blit(game_images['flappybird'], (horizontal, vertical))
          
        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0
          
        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1
          
        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
              
        # Refreshing the game window and displaying the score.
        pygame.display.update()
          
        # Set the framepersecond
        framepersecond_clock.tick(framepersecond)

    return

while True:

        # sets the coordinates of flappy bird
    horizontal = int(window_width/5)
    vertical = int((window_height - game_images['flappybird'].get_height())/2)
          
        # for selevel
    ground = 0  
    while True:
        for event in pygame.event.get():
  
        # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                      
                    # Exit the program
                sys.exit()   
  
                # If the user presses space or up key,
                # start the game for them
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappygame()
                  
                # if user doesn't press anykey Nothing happen
            else:
                window.blit(game_images['background'], (0, 0))
                window.blit(game_images['flappybird'], (horizontal, vertical))
                      
                # Just Refresh the screen
                pygame.display.update()        
                      
                # set the rate of frame per second
                framepersecond_clock.tick(framepersecond)