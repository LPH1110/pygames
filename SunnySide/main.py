import pygame as pg
from constants import *
from sprites.player import Player
from sprites.base import SpriteSheet

class Game():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()

        player_animations = {
            "idle": SpriteSheet(PLAYER_IDLE_PATH, num_frames=9, scale=PLAYER_SCALE),
            "walk": SpriteSheet(PLAYER_WALK_PATH, num_frames=8, scale=PLAYER_SCALE),
            "jump": SpriteSheet(PLAYER_JUMP_PATH, num_frames=9, scale=PLAYER_SCALE),
            "attack": SpriteSheet(PLAYER_ATTACK_PATH, num_frames=10, scale=PLAYER_SCALE),
        }
        
        self.player = Player(player_animations, 100, 100, speed=3)

    def run(self):
        running = True
        while running:
            self.screen.fill((100, 100, 100))
            
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    running = False

            self.player.update()
            self.player.draw(self.screen)
            
            pg.display.update()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()