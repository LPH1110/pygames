import pygame as pg

class BaseSprite(pg.sprite.Sprite):
    def __init__(self, file_image, x, y, width, height, speed):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(file_image), (width, height))
        self.original_image = self.image
        self.speed = speed
        # rect stands for the sprite's position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x ,self.rect.y))