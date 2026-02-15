import pygame as pg
from sprites.base import BaseSprite
from sprites.utils import load_animation_strip
from constants import PLAYER_IDLE_PATH, PLAYER_WALK_PATH, PLAYER_SCALE

from sprites.player.actions.idle import IdleState
from sprites.player.actions.walk import WalkState

from sprites.state_manager import StateManager

class Player(BaseSprite):
    def __init__(self, x, y):
        # Load Sprite Animations
        self.idle_frames, self.idle_frames_flipped = load_animation_strip(PLAYER_IDLE_PATH, 9, True, False, PLAYER_SCALE)
        self.walk_frames, self.walk_frames_flipped = load_animation_strip(PLAYER_WALK_PATH, 8, True, False, PLAYER_SCALE)
        
        # Initialize BaseSprite with idle frames
        super().__init__(x, y, self.idle_frames, animation_speed=0.2)
        
        self.velocity = pg.math.Vector2(0, 0)
        self.speed = 2
        self.facing_right = True
        
        # State Machine Setup
        self.state_manager = StateManager(self)
        self.state_manager.add_state("IDLE", IdleState(self))
        self.state_manager.add_state("WALK", WalkState(self))
        self.state_manager.set_initial_state("IDLE")
        
    def change_state(self, new_state_name):
        self.state_manager.change_state(new_state_name)
            
    def update(self):
        # Delegate to state manager
        self.state_manager.update()
        
        # Update position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        super().update()