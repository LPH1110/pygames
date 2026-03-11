import pygame as pg
from constants import HEALTH_BAR_WIDTH_MAX, HEALTH_BAR_HEIGHT, MAX_HEALTH

class HUDManager:
    def __init__(self):
        self.coin_font = pg.font.SysFont("verdana", 24, bold=True)
        self.coin_img = pg.image.load("assets/HUD/coins_hud.png").convert_alpha()
        self.coin_img = pg.transform.scale(self.coin_img, (32, 32))

    def draw(self, screen, player):
        # Draw Coins
        screen.blit(self.coin_img, (20, 60))
        coin_text = self.coin_font.render(f"x {player.coins}", True, (255, 255, 255))
        coin_text_outline = self.coin_font.render(f"x {player.coins}", True, (0, 0, 0))
        screen.blit(coin_text_outline, (62, 62))
        screen.blit(coin_text, (60, 60))
        
        # Draw Health Bar UI
        bg_rect = pg.Rect(20, 20, HEALTH_BAR_WIDTH_MAX, HEALTH_BAR_HEIGHT)
        ratio = max(0, player.health / MAX_HEALTH)  # Prevent negative health drawing backwards
        current_width = int(HEALTH_BAR_WIDTH_MAX * ratio)
        fg_rect = pg.Rect(20, 20, current_width, HEALTH_BAR_HEIGHT)
        
        # Draw the background structure and health fill
        pg.draw.rect(screen, (100, 100, 100), bg_rect)             # Dark gray background
        pg.draw.rect(screen, (220, 20, 60), fg_rect)               # Crimson red fill
        pg.draw.rect(screen, (255, 255, 255), bg_rect, width=2)    # White border
