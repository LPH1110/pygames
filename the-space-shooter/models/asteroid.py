import pygame as pg
import random
from models.base_sprite import BaseSprite
from constants import SC_WIDTH, SC_HEIGHT, ASTEROID_IMG

class Asteroid(BaseSprite):
    def __init__(self):
        # Generate random properties before calling super()
        self.size = random.randint(20, 50)
        start_x = random.randint(0, SC_WIDTH - self.size)
        start_y = random.randint(-SC_HEIGHT, -self.size) # Start above the screen
        speed_y = random.randint(1, 4) # Vertical speed
        speed_x = random.randint(-2, 2) # Horizontal drift
        
        # Call the parent class (BaseSprite) constructor
        super().__init__(ASTEROID_IMG, start_x, start_y, self.size, self.size, speed_y)
        
        # Store horizontal speed separately
        self.speed_x = speed_x

    def update(self):
        """ Update the asteroid's position (drift down and sideways) """
        self.rect.y += self.speed # self.speed is the vertical speed from BaseSprite
        self.rect.x += self.speed_x
        
        # Check if the asteroid has gone off-screen (bottom, left, or right)
        if self.rect.top > SC_HEIGHT or self.rect.left > SC_WIDTH or self.rect.right < 0:
            self.reset() # Reset its position

    def reset(self):
        """ Reset the asteroid to a new random position above the screen """
        self.size = random.randint(20, 50)
        self.rect.width = self.size
        self.rect.height = self.size
        
        # Reset position and speed
        self.rect.x = random.randint(0, SC_WIDTH - self.size)
        self.rect.y = random.randint(-SC_HEIGHT, -self.size) # Start above screen
        self.speed = random.randint(1, 4) # Vertical speed
        self.speed_x = random.randint(-2, 2) # Horizontal drift
        
        # We must also update the scaled image to match the new size
        # self.original_image is stored in BaseSprite
        self.image = pg.transform.scale(self.original_image, (self.size, self.size))