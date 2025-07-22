import math 
import pygame 


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
velocity = 0 ## init velcoity 0 
acceleration = 500
bRadius = 40
bounce_damping = 0.8


## TODO: add a class object for bodies of mass

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 4)

def drawCircle(): 
    pygame.draw.circle(screen, "white", player_pos, bRadius)

## make the object class and draw the same circle on screen but as an object of the class...


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

    ## updates the position of the circle
    velocity += acceleration * dt
    player_pos.y += velocity * dt


    ## bounce and loss due to heat
    if(player_pos.y + bRadius >= screen.get_height()): 

        player_pos.y = screen.get_height() - bRadius

        velocity = -velocity * bounce_damping ## this makes it so that the bouncing is now as in real life where the ball looses momentum with loss of heat

    drawCircle()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    dt = clock.tick(60) / 1000

pygame.quit()
