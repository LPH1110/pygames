import pygame as pg
from constants import SC_WIDTH, SC_HEIGHT

class ScreenFade:
    def __init__(self, color, speed):
        self.fade_counter = 0
        self.fade_speed = speed
        self.color = color
        self.fade_complete = False
        
        # Create a surface to overlay over everything
        self.overlay = pg.Surface((SC_WIDTH, SC_HEIGHT))
        self.overlay.fill(self.color)
        
    def reset(self):
        self.fade_counter = 0
        self.fade_complete = False
        
    def draw_fade_in(self, screen):
        """Fades inward (from a black screen to full visibility)"""
        self.fade_counter += self.fade_speed
        
        # Determine alpha transparency (0 is fully transparent, 255 is fully opaque)
        alpha = 255 - self.fade_counter
        if alpha <= 0:
            alpha = 0
            self.fade_complete = True
            
        self.overlay.set_alpha(alpha)
        screen.blit(self.overlay, (0, 0))
        return self.fade_complete
