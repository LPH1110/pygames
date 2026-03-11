import pygame as pg
from constants import SC_WIDTH, SC_HEIGHT, GAME_TITLE

class MainMenu:
    def __init__(self):
        self.title_font = pg.font.SysFont("verdana", 64, bold=True)
        self.menu_font = pg.font.SysFont("verdana", 32, bold=True)
        self.start_rect = pg.Rect(0, 0, 200, 50)
        self.start_rect.center = (SC_WIDTH // 2, SC_HEIGHT // 2)

    def update(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                if self.start_rect.collidepoint(e.pos):
                    return "PLAYING"
        return "MENU"

    def draw(self, screen):
        screen.fill((0, 0, 0))
        # Draw Title
        title_surf = self.title_font.render(GAME_TITLE, True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(SC_WIDTH // 2, SC_HEIGHT // 3))
        screen.blit(title_surf, title_rect)
        
        # Draw Start Button
        pg.draw.rect(screen, (100, 100, 255), self.start_rect, border_radius=10)
        
        start_text = self.menu_font.render("Start Game", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=self.start_rect.center)
        screen.blit(start_text, start_text_rect)
