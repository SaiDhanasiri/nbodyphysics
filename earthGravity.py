import math 
import pygame 


pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0


## TODO: add functions to add and remove objects

## Class to define the nth body
## no initial velocity, but constant dowward acceleratio going at 500 pixels per second, default mimicks earth's gravity
class Body: 
    def __init__(self, pos, mass=None, radius = 40, velocity=None, acceleration=None):
        self.pos = pygame.Vector2(pos)
        self.mass = mass if mass is not None else radius
        self.radius = radius 
        self.velocity = velocity if velocity is not None else pygame.Vector2(0,0)
        self.acceleration = acceleration if acceleration is not None else pygame.Vector2(0, 500)
        self.bounce_damping = 0.8
    
    def updatePos(self, dt, screen_width, screen_height): 
        self.velocity += self.acceleration * dt 
        self.pos += self.velocity * dt

        # Bounce off bottom
        if self.pos.y + self.radius >= screen_height:
            self.pos.y = screen_height - self.radius
            self.velocity.y = -self.velocity.y * self.bounce_damping

        # Bounce off top
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.velocity.y = -self.velocity.y * self.bounce_damping

        # Bounce off right
        if self.pos.x + self.radius >= screen_width:
            self.pos.x = screen_width - self.radius
            self.velocity.x = -self.velocity.x * self.bounce_damping

        # Bounce off left
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.velocity.x = -self.velocity.x * self.bounce_damping

    def drawCircle(self, screen): 
        pygame.draw.circle(screen, "white", self.pos, self.radius)

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 4)



## make the object class and draw the same circle on screen but as an object of the class...
bodies = [Body((300, 100)),
Body((600, 50)), Body((900, 150), radius=30), Body((600, 80), velocity=(400, 0))]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")

## collision between bodies
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            b1 = bodies[i]
            b2 = bodies[j]

            n = b1.pos - b2.pos ## vector from p2 to p1 to see the vector on which the collision happens 
            dist = n.length()
            min_dist = b1.radius + b2.radius 

            ## if the distance between the 2 objects is less than the sum of the radii then collsion happens
            if dist < min_dist: ## collision happens
                if dist == 0:
                    dist == 0.01 ## avoid division by 0
            
                ## normalize the collision axis 
                normal = n / dist

                ## calcualte the relative velocity
                rel_velocity = b1.velocity - b2.velocity ## how fast b1 is going towards b2 
                vel_along_normal = rel_velocity.dot(normal)
                ## dot product gives you the magnitude of relative velocity along the axis
                ## if negative it means they're going towards each other, positive meaning away, zero being parallel

                ## in case they're moving away from each other
                if vel_along_normal > 0: 
                    continue

                # compute impulse
                m1, m2 = b1.mass, b2.mass
                impulse = (2 * vel_along_normal) / (m1 + m2) 

                ## Apply the impluse to both velocites
                b1.velocity -= (impulse * m2) * normal 
                b2.velocity += (impulse * m1) * normal


                # push bodies apart to avoid voerlap
                overlap = min_dist - dist 
                correction = normal * (overlap / (m1 + m2)) 
                b1.pos += correction * m2 
                b2.pos -= correction * m1


    for body in bodies:
        body.updatePos(dt, screen.get_width(), screen.get_height())
        body.drawCircle(screen)

    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    dt = clock.tick(60) / 1000

pygame.quit()