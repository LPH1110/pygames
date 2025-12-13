import pygame as pg
from models.game_sprite import GameSprite
from random import choice
from constants import SC_HEIGHT, SC_WIDTH

class Ball(GameSprite):
    def __init__(self, x, y, image_file_name, width, height, speed):
        super().__init__(x, y, image_file_name, width, height, speed)
        self.dx = speed * choice([-1, 1])
        self.dy = speed * choice([-1, 1])

    def update_move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.top <= 0 or self.rect.bottom >= SC_HEIGHT:
            self.dy *= -1
        
        if self.rect.left <= 0 or self.rect.right >= SC_WIDTH:
            self.dx *= -1



    