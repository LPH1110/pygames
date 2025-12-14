# File: the-space-shooter - test/models/explosion.py

import pygame as pg
from constants import EXPLOSION_SPEED

class Explosion(pg.sprite.Sprite):
    def __init__(self, center, frames):
        """
        Initializes an explosion animation sprite.
        :param center: The (x, y) coordinates where the explosion should be centered.
        :param frames: A list of pre-loaded and scaled image frames for the animation.
        """
        super().__init__()
        
        self.frames = frames 
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = center
        
        # Timing for animation
        self.last_update = pg.time.get_ticks()
        self.frame_rate = EXPLOSION_SPEED # Time in milliseconds to show each frame

    def update(self):
        """
        Updates the explosion animation.
        """
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            
            # Move to the next frame
            self.frame_index += 1
            
            # Check if animation is finished
            if self.frame_index == len(self.frames):
                self.kill() # Animation finished, remove sprite
            else:
                # Update image and preserve center position
                center = self.rect.center
                self.image = self.frames[self.frame_index]
                self.rect = self.image.get_rect()
                self.rect.center = center