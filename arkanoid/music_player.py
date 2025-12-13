import pygame as pg
from constants import (
    BRICK_HIT_SFX,
    LOSE_SFX,
    WIN_SFX,
    WALL_HIT_SFX
)

class MusicPlayer():
    def __init__(self):
        pg.mixer.init()
    
    def play_brick_hit_sound(self):
        pg.mixer_music.load(BRICK_HIT_SFX)
        pg.mixer_music.play()

    def play_lose_sound(self):
        pg.mixer_music.load(LOSE_SFX)
        pg.mixer_music.play()
    
    def play_win_sound(self):
        pg.mixer_music.load(WIN_SFX)
        pg.mixer_music.play()

    def play_wall_hit_sound(self):
        pg.mixer_music.load(WALL_HIT_SFX)
        pg.mixer_music.play()
        