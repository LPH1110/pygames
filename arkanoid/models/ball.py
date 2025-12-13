import pygame as pg
from models.game_sprite import GameSprite
from random import choice
from constants import SC_WIDTH, SC_HEIGHT

class Ball(GameSprite):
    def __init__(self, game, file_image, x, y, width, height, speed = 0):
        super().__init__(file_image, x, y, width, height, speed)
        self.dx = choice([-speed, speed])
        self.dy = choice([-speed, speed])
        self.game = game
        
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
    
        # checking borders
        if self.rect.top <= 0:
            self.game.music.play_wall_hit_sound()
            self.dy *= -1
            
        
        if self.rect.left <= 0 or self.rect.right >= SC_WIDTH:
            self.game.music.play_wall_hit_sound()
            self.dx *= -1

        # checking platform
        if pg.sprite.spritecollide(self, self.game.platforms, False):
            self.game.music.play_wall_hit_sound()
            self.dy *= -1

        # check bricks
        if pg.sprite.spritecollide(self, self.game.bricks, True):
            self.game.music.play_brick_hit_sound()
            self.dy *= -1
        
    