import pygame as pg

class BaseSprite(pg.sprite.Sprite):
    def __init__(self, x, y, images, animation_speed=0.2):
        super().__init__()
        # If images is a single image, convert to list
        if not isinstance(images, list):
            self.images = [images]
        else:
            self.images = images
            
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.animation_speed = animation_speed
        self.last_update = pg.time.get_ticks()

    def update(self):
        """
        Handles animation updates.
        """
        if len(self.images) > 1:
            self.image_index += self.animation_speed
            if self.image_index >= len(self.images):
                self.image_index = 0
            self.image = self.images[int(self.image_index)]

    def draw(self, surface: pg.Surface):
        surface.blit(self.image, self.rect)