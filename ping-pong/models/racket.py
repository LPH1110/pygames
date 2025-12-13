import pygame as pg
from constants import SC_HEIGHT, SC_WIDTH
from models.game_sprite import GameSprite
from colors import BLACK

class Racket(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, color = BLACK):
        super().__init__()
        self.rect = pg.rect.Rect(x, y, width, height)
        self.speed = speed
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect)
    
    def update_move1(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys[pg.K_s] and self.rect.y < SC_HEIGHT:
            self.rect.y += self.speed

    def update_move2(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys[pg.K_DOWN] and self.rect.y < SC_HEIGHT:
            self.rect.y += self.speed