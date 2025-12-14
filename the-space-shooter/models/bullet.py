import pygame as pg
from models.base_sprite import BaseSprite
from constants import BULLET_IMG, BULLET_SPEED

class Bullet(BaseSprite):
    def __init__(self, center_x, top_y):
        self.width = 10
        self.height = 20
        self.speed = BULLET_SPEED # Negative speed moves up
        
        # Call the parent constructor
        super().__init__(BULLET_IMG, center_x, top_y, self.width, self.height, self.speed)
        
        # Adjust the rect to spawn from the correct position
        self.rect.centerx = center_x
        self.rect.bottom = top_y

    def update(self):
        """
        Move the bullet up the screen.
        """
        self.rect.y += self.speed
        
        # Kill the sprite if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill() # kill() removes the sprite from all groups