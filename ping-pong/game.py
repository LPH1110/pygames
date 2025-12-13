import pygame as pg 
from constants import (
    FPS,
    SC_WIDTH,
    SC_HEIGHT,
    GAME_TITLE
)
import sys
from models.racket import Racket
from models.ball import Ball
from colors import BLUE, RED, WHITE
from time import time

class Game():
    # constructor 
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.screen.fill((0, 255, 0))
        self.clock = pg.time.Clock()
        self.background = pg.transform.scale(
            pg.image.load("background.png"), (SC_WIDTH, SC_HEIGHT)
        )
        self.game_duration = 30

        # Font
        self.score_font = pg.font.Font("fonts/Intel_One_Mono/static/IntelOneMono-SemiBold.ttf", 16)
        self.timer_font = pg.font.Font("fonts/Intel_One_Mono/static/IntelOneMono-Bold.ttf", 16)
        self.result_font = pg.font.Font("fonts/Poppins/Poppins-BoldItalic.ttf", 24)
        self.player1_score = 0
        self.player2_score = 0

        # Music
        pg.mixer.init()
        self.ball_hit_sound = pg.mixer.Sound('sounds/ball-bouncing-1.wav')
        self.init_game_objects()

    def show_result_gui(self, winner):
        message = ""
        if winner:
            message = f"The winner is {winner}!"
        else:
            message = f"Its a draw!"

        self.result_text = self.result_font.render(
            message, True, WHITE
        )
        self.screen.blit(self.result_text, (SC_WIDTH // 3, SC_HEIGHT // 3))

    def update_gui(self, player1_score, player2_score, current_time):
        # score
        self.player1_score_text = self.score_font.render(
            f"Player 1: {player1_score}", True, WHITE
        )
        self.player2_score_text = self.score_font.render(
            f"Player 2: {player2_score}", True, WHITE
        )

        self.screen.blit(self.player1_score_text, (10, 10))
        self.screen.blit(
            self.player2_score_text, 
            (SC_WIDTH - self.player2_score_text.get_rect().right - 10, 10)
        )
        
        # timer
        self.timer_text = self.timer_font.render(
            f"00:{current_time}", True, WHITE
        )
        self.total_time = 30 # seconds

        
        self.screen.blit(self.timer_text, (SC_WIDTH//2, 10))
    
    def init_game_objects(self):
        self.ball = Ball(
            x = SC_WIDTH // 2,
            y = SC_HEIGHT // 2,
            image_file_name = "ball.png",
            width = 50,
            height = 50,
            speed = 5
        )
        self.racket1 = Racket(
            x = 100,
            y = SC_HEIGHT // 2,
            width = 30, 
            height = 100,
            speed = 5,
            color = BLUE
        )
        self.racket2 = Racket(
            x = SC_WIDTH - 100,
            y = SC_HEIGHT // 2,
            width = 30, 
            height = 100,
            speed = 5,
            color = RED
        )
    
    def check_winner(self):
        if self.player1_score > self.player2_score:
            return "Player 1"
        elif self.player1_score < self.player2_score:
            return "Player 2"
        else:
            return None

    def run(self):
        is_running = True 
        is_finished = False
        start_time = time()
        # game loop
        while is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False
                    
            self.screen.blit(self.background, (0,0))
            
            # Drawings
            self.ball.draw(self.screen)
            self.racket1.draw(self.screen)
            self.racket2.draw(self.screen)

            if not is_finished:
                # Movements
                self.ball.update_move()
                self.racket1.update_move1()
                self.racket2.update_move2()
                
                # Handle timer
                elapsed_time = time() - start_time 
                time_remaining = self.game_duration - elapsed_time 
                if time_remaining <= 0:
                    is_finished = True
                    winner = self.check_winner()
                    self.show_result_gui(winner)

                # Handle update guis
                self.update_gui(self.player1_score, self.player2_score, int(time_remaining))
                
                # Handle collisions
                if pg.sprite.collide_rect(self.ball, self.racket1):
                    self.ball.dx *= -1
                    if self.ball.dx > 0: 
                        self.ball.rect.left = self.racket1.rect.right
                    else:
                        self.ball.rect.right = self.racket1.rect.left
                    self.ball_hit_sound.play()

                elif pg.sprite.collide_rect(self.ball, self.racket2):
                    self.ball.dx *= -1
                    if self.ball.dx > 0: 
                        self.ball.rect.left = self.racket2.rect.right
                    else:
                        self.ball.rect.right = self.racket2.rect.left
                    self.ball_hit_sound.play()
                elif self.ball.rect.left <= 0:
                    # when the ball touches the left border
                    self.player2_score += 1
                elif self.ball.rect.right >= SC_WIDTH:
                    # when the ball touches the rigth border
                    self.player1_score += 1
                

                pg.display.update()
                self.clock.tick(FPS)

        sys.exit(pg.quit()) 

if __name__ == "__main__":
    game = Game()
    game.run()