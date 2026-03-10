import pygame as pg
from sprites.base import BaseSprite, SpriteSheet

class Flag(BaseSprite):
    def __init__(self, x, y, scale=1):
        # Initialize Flag animations
        animations = {
            "idle": SpriteSheet("./assets/Environment/Flag.png", num_frames=4, scale=scale)
        }
        super().__init__(animations, x, y)
        
        # Bottom-align the flag with the 32x32 tile
        width = animations["idle"].frame_width * scale
        height = animations["idle"].frame_height * scale
        
        # Place the bottom of the flag at the bottom of the tile
        offset_y = y + (32 - height)
        
        self.hitbox = pg.Rect(x, offset_y, width, height)
        
        # Slower animation
        self.animation_speed = 0.15

    def update(self, world=None):
        # Flags just animate, no gravity or movement
        self.animate()
