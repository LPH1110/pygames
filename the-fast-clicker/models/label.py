import pygame as pg
from models.area import Area

class Label(Area):
    def set_text(self, text, fsize = 12, text_color = (0, 0, 0)):
        font = pg.font.SysFont('verdana', fsize) # font instance
        self.text_content = text
        self.image = font.render(text, True, text_color)
        self.image_rect = self.image.get_rect(center = self.rect.center)
    
    def draw(self, shift_x = 0, shift_y = 0):
        self.fill() # fill color to Area
        
        if hasattr(self, 'image'):
            text_final_x = self.image_rect.x + shift_x
            text_final_y = self.image_rect.y + shift_y
            self.screen.blit(self.image, (text_final_x, text_final_y)) # draw text
