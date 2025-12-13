import pygame as pg

class GameSprite(pg.sprite.Sprite):
    def __init__(self, x, y, image_file_name, width, height, speed):
        super().__init__()
        self.image = pg.transform.scale(
            pg.image.load(image_file_name),
            (width, height)
        )
        self.width = width
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))