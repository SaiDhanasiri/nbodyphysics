import math 
import pygame 

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
G = 6.67430e-11 ##gravitational constant 
G = 1000 ## for visual effects as the other one is too small 

class Body: 
    def __init__(self, pos, mass=None, radius = 40, velocity=None, acceleration=None):
        self.pos = pygame.Vector2(pos)
        self.mass = mass if mass is not None else radius
        self.radius = radius 
        self.velocity = velocity if velocity is not None else pygame.Vector2(0,0)
        self.acceleration = pygame.Vector2(0,0)
        self.bounce_damping = 0.8
        self.trail = []  # For drawing motion trails

    def calculate_gravitational_force(self, other_body): 
        ## logic to calculate gravitational force between 2 objects

        directional_vector = other_body.pos - self.pos
        dist = directional_vector.length()

        if dist < self.radius + other_body.radius: ## to avoid collision, could also just make them explode at contact
            dist = self.radius + other_body.radius
        
        ## Newton's Law of Universal Gravitation F_g = (G * m1m2) / distance^2 
        force_magnitude = (G * self.mass * other_body.mass) / (dist ** 2)

        if dist > 0: 
            force_direction = directional_vector / dist
        else: 
            force_direction =  pygame.Vector2(0,0) 
        
        ## force vector 
        force_vector = force_direction * force_magnitude

        ## F = ma, so a = F / m 
        accelGravity = force_vector / self.mass

        self.acceleration += accelGravity
    
    def reset_acceleration(self):  # Fixed typo in method name
        ## acceleration set to 0 before calculating any forces 
        self.acceleration = pygame.Vector2(0,0)

    def updatePos(self, dt, screen_width, screen_height): 
        self.velocity += self.acceleration * dt 
        self.pos += self.velocity * dt

        # Add current position to trail
        self.trail.append(self.pos.copy())
        if len(self.trail) > 100:  # Limit trail length
            self.trail.pop(0)


    def drawCircle(self, screen): 

        # Draw trail
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                alpha = i / len(self.trail)
                trail_radius = max(1, int(self.radius * alpha * 0.3))
                trail_color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
                pygame.draw.circle(screen, trail_color, self.trail[i], trail_radius)
        
        ## body
        pygame.draw.circle(screen, "white", self.pos, self.radius)

        # Draw a smaller circle to show the center
        pygame.draw.circle(screen, "red", self.pos, 3)

## make the object class and draw the same circle on screen but as an object of the class...
bodies = [
        Body((300, 300), mass=5000, radius=30, velocity=pygame.Vector2(0, -50)),
        Body((900, 300), mass=8000, radius=40, velocity=pygame.Vector2(0, 50)),
        Body((600, 150), mass=2000, radius=20, velocity=pygame.Vector2(30, 0))
        ]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Reset simulation
                bodies = [
                    Body((300, 300), mass=5000, radius=30, velocity=pygame.Vector2(0, -50)),
                    Body((900, 300), mass=8000, radius=40, velocity=pygame.Vector2(0, 50)),
                    Body((600, 150), mass=2000, radius=20, velocity=pygame.Vector2(30, 0))
                ]
    
    screen.fill("black")
    
    ## all accelerations set to 0
    for body in bodies:
        body.reset_acceleration() 

    ## Calculate gravitational forces between all pairs
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            b1 = bodies[i]
            b2 = bodies[j]

            # Apply gravitational force from b2 to b1
            b1.calculate_gravitational_force(b2)
            # Apply equal and opposite force from b1 to b2 (Newton's 3rd law)
            b2.calculate_gravitational_force(b1)

    # Update positions and draw bodies
    for body in bodies:
        body.updatePos(dt, screen.get_width(), screen.get_height())
        body.drawCircle(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate
    dt = clock.tick(60) / 1000

pygame.quit()