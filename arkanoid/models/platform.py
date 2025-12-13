import pygame as pg
from models.game_sprite import GameSprite

class Platform(GameSprite):
    def update(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]: # move to the left
            self.rect.x -= self.speed
        elif keys[pg.K_d]: # move to the right
            self.rect.x += self.speed
