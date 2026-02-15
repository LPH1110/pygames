import pygame as pg
from constants import *
from sprites.player import Player

class SunnySide():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()

        self.player = Player(100, 100)

    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.player.update()
            self.player.draw(self.screen)
            pg.display.flip()
            self.clock.tick(FPS)
        pg.quit()

if __name__ == "__main__":
    game = SunnySide()
    game.run()
