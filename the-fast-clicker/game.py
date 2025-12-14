import pygame as pg
import sys
from constants import (
    SC_WIDTH, 
    SC_HEIGHT, 
    GAME_TITLE, 
    FPS
)
from colors import (
    BG_COLOR,
    YELLOW,
    BLUE,
    WHITE,
    BLACK,
    GREEN, 
    RED
)
from models.label import Label
from random import randint
from time import time

class TheFastClicker():
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.screen.fill(BG_COLOR)
        self.num_cards = 4
        self.cards = self.create_cards()
        self.total_game_time = 10
        self.current_score = 0
        self.init_gui()
    
    def create_cards(self) -> list[Label]:
        cards = list()
        x = 70
        for i in range(self.num_cards):
            new_card = Label(
                screen = self.screen,
                x = x,
                y = 170,
                width = 70,
                height = 100,
                color = YELLOW
            )
            new_card.outline(BLUE, 4)
            cards.append(new_card)
            x += 100
        return cards

    def init_gui(self):
        self.timer_lb = Label(
            screen = self.screen,
            x = 10,
            y = 10,
            width = 100,
            height = 30,
            color = BG_COLOR
        )

        self.score_lb = Label(
            screen = self.screen,
            x = SC_WIDTH - 100,
            y = 10,
            width = 100,
            height = 30,
            color = BG_COLOR
        )

        self.win_lb = Label(
            screen = self.screen,
            x = SC_WIDTH // 2 - 30,
            y = 50,
            width = 30,
            height = 30,
            color = BG_COLOR
        )

        self.lose_lb = Label(
            screen = self.screen,
            x = SC_WIDTH // 2 - 30,
            y = 50,
            width = 30,
            height = 30,
            color = BG_COLOR
        )
    
    def show_win_screen(self):
        self.win_lb.set_text(
            text = "You Won!",
            fsize = 20,
            text_color = BLACK
        )
        self.win_lb.draw()

    def show_lose_screen(self):
        self.lose_lb.set_text(
            text = "You Lose!",
            fsize = 20,
            text_color = BLACK
        )
        self.lose_lb.draw()

    def update_timer(self, new_time):
        formatted_time = f"{new_time:02d}"
        self.timer_lb.set_text(
            text = f'Time: {formatted_time}',
            fsize = 14,
            text_color = BLACK
        )
        self.timer_lb.draw()
    
    def update_score(self, new_score):
        self.score_lb.set_text(
            text = f'Score: {new_score}',
            fsize = 14,
            text_color = BLACK
        )
        self.score_lb.draw()
    
    def run(self):
        self.is_running = True
        click_duration = 0
        self.right_card_index = randint(0, self.num_cards - 1)
        start_time = int(time()) # fix this one
        elapsed_time = 0
        is_finished = False
        
        # game loop
        while self.is_running:
            # events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                if event.type == pg.MOUSEBUTTONDOWN and not is_finished:
                    (x, y) = event.pos
                    for i in range(self.num_cards):
                        card = self.cards[i]
                        if card.collidepoint(x, y):
                            if i == self.right_card_index:
                                self.current_score += 10
                                self.update_score(self.current_score)
                                card.color(GREEN)
                            else:
                                self.current_score -= 10
                                self.update_score(self.current_score)
                                card.color(RED)
                            
                            card.set_text('', 16)
                            card.fill()
                            break
            
            # drawings
            for card in self.cards:
                card.draw()
            
            # GUI
            if not is_finished:
                # Handle click jumping
                if click_duration == 0:
                    click_duration = 20
                    for i in range(self.num_cards):
                        self.cards[i].color(YELLOW)
                        self.cards[i].set_text('', 16)
                        self.cards[i].outline(BLUE, 4)

                    self.right_card_index = randint(0, self.num_cards - 1)
                    
                    self.cards[self.right_card_index].set_text("CLICK", 16)
                else:
                    click_duration -= 1

                # Timer
                self.update_timer(self.total_game_time - elapsed_time)
                self.update_score(self.current_score)
                current_time = int(time())
                new_elapsed_time = current_time - start_time
                
                if new_elapsed_time != elapsed_time:
                    elapsed_time = new_elapsed_time
                    remaining_time = self.total_game_time - elapsed_time
                    if remaining_time >= 0:
                        self.update_timer(remaining_time)
                    else:
                        is_finished = True
                        if self.current_score >= 20:
                            self.show_win_screen()
                        else:
                            self.show_lose_screen()

            
            pg.display.update()
            self.clock.tick(FPS)
    


if __name__ == "__main__":
    game = TheFastClicker()
    game.run()

    