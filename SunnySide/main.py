from constants import SC_WIDTH
import pygame as pg
from constants import *
from sprites.player import Player
from sprites.base import SpriteSheet
from map_generator import World 

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()

        self.world = World(TILE_SIZE, TILE_PATH)
        self.world.process_data('./level_data.csv') 
        self.background_image = pg.transform.scale(
            pg.image.load("Background.png").convert_alpha(),
            (SC_WIDTH, SC_HEIGHT)
        )

        # Camera scroll variable
        self.scroll = 0

        player_animations = {
            "idle": SpriteSheet(PLAYER_IDLE_PATH, num_frames=9, scale=PLAYER_SCALE),
            "walk": SpriteSheet(PLAYER_WALK_PATH, num_frames=8, scale=PLAYER_SCALE),
            "jump": SpriteSheet(PLAYER_JUMP_PATH, num_frames=9, scale=PLAYER_SCALE),
            "attack": SpriteSheet(PLAYER_ATTACK_PATH, num_frames=10, scale=PLAYER_SCALE),
        }
        
        self.player = Player(player_animations, 100, 100, speed=2)
    
    def run(self):
        running = True

        while running:
            # Vẽ Background Lặp Kết Hợp Scroll (parallax 0.5)
            bg_width = self.background_image.get_width()
            for i in range(5): # Số lượng ảnh cần thiết để phủ kín screen khi cuộn (tùy chỉnh nếu map dài)
                self.screen.blit(self.background_image, ((i * bg_width) - self.scroll * 0.5, 0))

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False

            self.scroll = self.player.hitbox.centerx - SC_WIDTH // 2
            
            if self.scroll < 0:
                self.scroll = 0
            if self.scroll > self.world.map_width - SC_WIDTH:
                self.scroll = self.world.map_width - SC_WIDTH

            self.world.draw(self.screen, self.scroll)

            self.player.update(self.world)
            self.player.draw(self.screen, self.scroll)
            
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()