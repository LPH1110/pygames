import pygame as pg
from sprites.base import BaseSprite
from sprites.spritesheet import SpriteSheet

player_img_path = "./World_Assets/Characters/Human/IDLE/base_idle_strip9.png"

class Player(BaseSprite):
    def __init__(self, x, y):
        # Load the sprite sheet
        self.sheet = SpriteSheet(player_img_path)
        
        # Calculate frame width dynamically (assuming single row, 9 frames)
        sheet_width = self.sheet.sheet.get_width()
        sheet_height = self.sheet.sheet.get_height()
        frame_width = sheet_width // 9
        frame_height = sheet_height
        
        # Load the strip of 9 frames
        frames = self.sheet.load_strip((0, 0, frame_width, frame_height), 9)
        
        # Initialize BaseSprite with the list of frames
        super().__init__(x, y, frames, animation_speed=0.2)