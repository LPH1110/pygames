import pygame as pg
from constants import (
    SC_WIDTH,
    SC_HEIGHT,
    FPS,
    GAME_TITLE,
    BRICK_HEIGHT, 
    BRICK_WIDTH,
    PLATFORM_WIDTH,
    PLATFORM_HEIGHT,
    PLATFORM_SPEED,
    BALL_WIDTH,
    BALL_HEIGHT,
    BALL_SPEED
)
from colors import (
    DARK_GREY,
    BLACK,
    WHITE
)
from models.platform import Platform
from models.ball import Ball
from models.game_sprite import GameSprite
from random import randint
from music_player import MusicPlayer

class Game():
    def __init__(self):
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.finished = False

        # platform
        platform = Platform(
            file_image = "./assets/platform/Player.png",
            x = SC_WIDTH // 2, 
            y = SC_HEIGHT - 150,
            width = PLATFORM_WIDTH,
            height = PLATFORM_HEIGHT,
            speed = PLATFORM_SPEED
        )
        self.platforms = pg.sprite.GroupSingle()
        self.platforms.add(platform)

        # ball
        ball = Ball(
            game = self,
            file_image = "./assets/ball/ball.png",
            x = self.platforms.sprite.rect.x + PLATFORM_WIDTH // 2,
            y = self.platforms.sprite.rect.y - PLATFORM_HEIGHT - 50,
            width = BALL_WIDTH,
            height = BALL_HEIGHT,
            speed = BALL_SPEED
        )
        self.balls = pg.sprite.GroupSingle()
        self.balls.add(ball)
        
        # bricks
        self.bricks = pg.sprite.Group()
        self.generate_bricks()

        # music & sound effects
        self.music = MusicPlayer()
        
        # font
        pg.font.init()
        self.font = pg.font.SysFont("verdana", 32, True)
        
        
        
    def show_win_text(self):
        self.win_text = self.font.render("You Won!", False, WHITE)
        win_text_rect = self.win_text.get_rect(
            center = (SC_WIDTH // 2, SC_HEIGHT // 2)
        )
        self.screen.blit(self.win_text, win_text_rect)
    
    def show_lose_text(self):
        self.lose_text = self.font.render("You Lose!", False, WHITE)
        lose_text_rect = self.lose_text.get_rect(
            center = (SC_WIDTH // 2, SC_HEIGHT // 2)
        )
        self.screen.blit(self.lose_text, lose_text_rect)
    
    def generate_bricks(self):
        x = 0
        y = 0
        num_rows = 4
        num_bricks_per_row = 14

        for i in range(num_rows):
            for j in range(num_bricks_per_row):
                brick = GameSprite(
                    file_image = f"./assets/brick/{randint(1, 9)}.png",
                    x = x, 
                    y = y,
                    width = BRICK_WIDTH,
                    height = BRICK_HEIGHT
                )
                self.bricks.add(brick)
                x += BRICK_WIDTH

            x = 0
            y += BRICK_HEIGHT
    
    def check_winner(self):
        if self.balls.sprite.rect.bottom >= SC_HEIGHT:
            self.finished = True 
            self.music.play_lose_sound()
            return False # lose
        elif len(self.bricks) <= 0:
            self.finished = True
            self.music.play_win_sound()
            return True # win
        return None
        
    def run(self):
        is_running = True
        winner = None

        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
            
            if not self.finished:

                # apply background color
                self.screen.fill(DARK_GREY)
                
                # Platform
                self.platforms.draw(self.screen)
                self.platforms.update()

                # Bricks
                self.bricks.draw(self.screen)
                
                # Ball
                self.balls.draw(self.screen)
                self.balls.update()

                winner = self.check_winner()

            else:
                if winner:
                    self.show_win_text()
                else:
                    self.show_lose_text()


            pg.display.update()
            self.clock.tick(FPS)    
    

if __name__ == "__main__":
    game = Game()
    game.run()