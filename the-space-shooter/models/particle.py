import pygame as pg
import random
from constants import SC_WIDTH, SC_HEIGHT
from colors import WHITE

class Particle():
    def __init__(self):
        # Start at a random pos
        self.x = random.randint(0, SC_WIDTH)
        self.y = random.randint(0, SC_HEIGHT)
        
        self.radius = random.randint(1, 2) # the size
        self.speed = random.randint(1, 3) # the speed
        
        self.color = WHITE # its color

    def update(self):
        # Keep falling down from the top
        self.y += self.speed
        
        # Check if the particle has passed
        if self.y > SC_HEIGHT:
            self.y = random.randint(-10, 0) # Always start at the top
            self.x = random.randint(0, SC_WIDTH) # Random x pos
            self.radius = random.randint(1, 2) # Random size of the particle
            self.speed = random.randint(1, 3) # Random speed

    def draw(self, surface):
        pg.draw.circle(surface, self.color, (self.x, self.y), self.radius)