import pygame as pg

class GameSprite(pg.sprite.Sprite):
    def __init__(self, file_image, x, y, width, height, speed = 0):
        super().__init__()
        self.image = pg.transform.scale(
            pg.image.load(file_image),
            (width, height)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))   