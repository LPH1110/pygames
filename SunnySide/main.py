from constants import SC_WIDTH
import pygame as pg
from constants import *
from sprites.player import Player
from sprites.base import SpriteSheet
from map_generator import World 
from sound_manager import sound_manager
from ui import MainMenu, HUDManager, ScreenFade

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        
        self.game_state = "MENU" # Initialize game in MENU state

        self.world = World(TILE_SIZE, TILE_PATH)
        self.world.process_data('./level_data.csv') 
        self.background_image = pg.transform.scale(
            pg.image.load("Background.png").convert_alpha(),
            (SC_WIDTH, SC_HEIGHT)
        )

        # Camera scroll variable
        self.scroll = 0

        self.main_menu = MainMenu()
        self.hud_manager = HUDManager()
        self.screen_fade = ScreenFade((0, 0, 0), speed=5) # Black mask fading at a speed of 5 out of 255/frame

        player_animations = {
            "idle": SpriteSheet(PLAYER_IDLE_PATH, num_frames=9, scale=PLAYER_SCALE),
            "walk": SpriteSheet(PLAYER_WALK_PATH, num_frames=8, scale=PLAYER_SCALE),
            "jump": SpriteSheet(PLAYER_JUMP_PATH, num_frames=9, scale=PLAYER_SCALE),
            "attack": SpriteSheet(PLAYER_ATTACK_PATH, num_frames=10, scale=PLAYER_SCALE),
        }
        
        self.player = Player(player_animations, 100, 100, speed=2)
        
    def reset_game(self):
        self.world = World(TILE_SIZE, TILE_PATH)
        self.world.process_data('./level_data.csv')
        self.player.respawn()
        self.player.health = MAX_HEALTH
        self.scroll = 0
    
    def draw_menu_screen(self, events):
        new_state = self.main_menu.update(events)
        if new_state == "PLAYING":
            self.game_state = "FADING" 
            self.screen_fade.reset()
        else:
            self.main_menu.draw(self.screen)
    
    def draw_fading_effect(self):
        # Draw the static first frame of the game so the fade has something to reveal
        bg_width = self.background_image.get_width()
        for i in range(5):
            self.screen.blit(self.background_image, ((i * bg_width) - self.scroll * 0.5, 0))
        self.world.draw(self.screen, self.scroll)
        self.player.draw(self.screen, self.scroll)
        self.hud_manager.draw(self.screen, self.player)

        # Overlay the fade
        if self.screen_fade.draw_fade_in(self.screen):
            # Transition complete -> Move to actual playing state
            self.reset_game()
            self.game_state = "PLAYING"

    def draw_playing_screen(self):
        # Vẽ Background Lặp Kết Hợp Scroll (parallax 0.5)
        bg_width = self.background_image.get_width()
        for i in range(5): # Số lượng ảnh cần thiết để phủ kín screen khi cuộn (tùy chỉnh nếu map dài)
            self.screen.blit(self.background_image, ((i * bg_width) - self.scroll * 0.5, 0))

        self.scroll = self.player.hitbox.centerx - SC_WIDTH // 2
        
        if self.scroll < 0:
            self.scroll = 0
        if self.scroll > self.world.map_width - SC_WIDTH:
            self.scroll = self.world.map_width - SC_WIDTH

        self.world.update()
        self.world.draw(self.screen, self.scroll)

        self.player.update(self.world)
        self.player.draw(self.screen, self.scroll)
        
        # Check for death condition
        if self.player.health <= 0:
            self.game_state = "MENU"
    
    def run(self):
        running = True

        while running:
            # Handle Events First
            events = pg.event.get()
            for e in events:
                if e.type == pg.QUIT:
                    running = False

            if self.game_state == "MENU":
                self.draw_menu_screen(events)
            
            elif self.game_state == "FADING":
                self.draw_fading_effect()
            
            elif self.game_state == "PLAYING":
                self.draw_playing_screen()
                # --- Draw UI ---
                self.hud_manager.draw(self.screen, self.player)

            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()