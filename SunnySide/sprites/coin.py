import pygame as pg
from sprites.base import BaseSprite, SpriteSheet

class Coin(BaseSprite):
    def __init__(self, x, y, scale=2):
        # Initialize Coin animations
        animations = {
            "idle": SpriteSheet("./assets/Environment/Coin.png", num_frames=4, scale=scale)
        }
        super().__init__(animations, x, y)
        
        # Center the coin inside the 32x32 tile
        width = animations["idle"].frame_width * scale
        height = animations["idle"].frame_height * scale
        
        offset_x = x + (32 - width) // 2
        offset_y = y + (32 - height) // 2
        
        self.hitbox = pg.Rect(offset_x, offset_y, width, height)
        
        # Slower animation for environment items
        self.animation_speed = 0.15

    def update(self, world=None):
        # Coins just animate, they don't move or have gravity
        self.animate()
