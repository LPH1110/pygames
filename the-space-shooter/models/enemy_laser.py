import pygame as pg
from models.base_sprite import BaseSprite
from constants import ENEMY_LASER_SPEED, ENEMY_LASER_IMG, SC_HEIGHT, SC_WIDTH

class EnemyLaser(BaseSprite):
    def __init__(self, center_x, center_y, direction_vector):
        width = 20   # The laser's width
        height = 20
        speed = ENEMY_LASER_SPEED
        
        super().__init__(ENEMY_LASER_IMG, center_x, center_y, width, height, speed)
        
        self.rect.centerx = center_x
        self.rect.centery = center_y
        
        # Save the exact position as a 2d vector
        self.pos = pg.math.Vector2(center_x, center_y)
        
        # Standardize the vector (len = 1) and times by the speed
        # If the given vector is (0,0), then shoots downward by default
        if direction_vector.length() == 0:
            self.velocity = pg.math.Vector2(0, 1) * speed
        else:
            self.velocity = direction_vector.normalize() * speed

    def update(self):
        # Add the velocity to the position
        self.pos += self.velocity
        
        # Update rect
        self.rect.centerx = int(self.pos.x)
        self.rect.centery = int(self.pos.y)
        
        # Kill itself when going outside of the game scene
        if (self.rect.top < -50 or self.rect.bottom > SC_HEIGHT + 100 or 
            self.rect.left < - 100 or self.rect.right > SC_WIDTH + 100):
            self.kill()