import pygame as pg

class Area():
    def __init__(self, screen: pg.Surface, x = 0, y = 0, width = 10, height = 10, color = None):
        self.rect = pg.Rect(x, y, width, height)
        self.fill_color = color
        self.screen = screen
        self.outline_color = None
        self.outline_thickness = 0
    
    def color(self, new_color):
        self.fill_color = new_color
    
    def fill(self):
        pg.draw.rect(self.screen, self.fill_color, self.rect)
        if self.outline_color and self.outline_thickness > 0:
            pg.draw.rect(self.screen, self.outline_color, self.rect, self.outline_thickness)
    
    def outline(self, frame_color, thickness):
        self.outline_color = frame_color
        self.outline_thickness = thickness

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)