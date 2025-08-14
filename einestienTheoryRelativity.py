import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
G = 6.67430e-11 ##gravitational constant 
G = 1000 ## Scaled for visual effects 

## Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
BLUE = (100, 150, 255)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
GRAY = (150, 150, 150)

## Class to define 3-d objects for calculations 
class vector3d: 
    def __init__(self, x, y, z):
        self.x = x 
        self.y = y 
        self.z = z
    
    def __add__(self, otherBody): 
        return vector3d(self.x + otherBody.x, self.y + otherBody.y, self.z + otherBody.z)
    
    def __sub__(self, otherBody): 
        return vector3d(self.x - otherBody.x, self.y - otherBody.y, self.z - otherBody.z)
    
    def __mul__(self, scalar): 
        return vector3d(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, otherBody):
        return self.x * otherBody.x + self.y + otherBody.y + self.z + otherBody.z

    def cross(self, otherBody): 
        return vector3d(self.y * otherBody.z - self.z * otherBody.y,
                        self.z * otherBody.x - self.x * otherBody.z, 
                        self.x * otherBody.y - otherBody.x * self.y)
    
    def normalize(self): 
        length = math.sqrt(self.x **2 + self.y ** 2, self.z ** 2)

        if length == 0: 
            return vector3d(0,0,0)
        return(vector3d(self.x / length, self.y / length, self.z / length))
    
    def length(self): 
        return math.sqrt(self.x **2 + self.y ** 2, self.z ** 2)

## TODO: Add logic to create a flat flamm paraboloid so that when objects are added it creates a dip and so logic for that as well 



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        
    
    screen.fill("black")
    pygame.display.flip()
