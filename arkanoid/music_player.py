import pygame as pg
from constants import (
    BRICK_HIT_SFX,
    LOSE_SFX,
    WIN_SFX,
    WALL_HIT_SFX
)

class MusicPlayer():
    def __init__(self):
        self.is_ready = False 
        
        try:
            pg.mixer.init()
            self.brick_hit_sound = pg.mixer.Sound(BRICK_HIT_SFX)
            self.lose_sound = pg.mixer.Sound(LOSE_SFX)
            self.win_sound = pg.mixer.Sound(WIN_SFX)
            self.wall_hit_sound = pg.mixer.Sound(WALL_HIT_SFX)
            
            self.brick_hit_sound.set_volume(0.5)
            self.wall_hit_sound.set_volume(0.5)
            
            self.is_ready = True
            print("Audio system initialized successfully.")
            
        except Exception as e:
            print(f"Warning: Audio disabled due to error: {e}")
            self.is_ready = False

    def play_brick_hit_sound(self):
        if self.is_ready:
            try:
                self.brick_hit_sound.play()
            except: pass

    def play_lose_sound(self):
        if self.is_ready:
            try:
                self.lose_sound.play()
            except: pass
    
    def play_win_sound(self):
        if self.is_ready:
            try:
                self.win_sound.play()
            except: pass

    def play_wall_hit_sound(self):
        if self.is_ready:
            try:
                self.wall_hit_sound.play()
            except: pass