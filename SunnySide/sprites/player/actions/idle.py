from sprites.player.player_state import PlayerState
import pygame as pg

class IdleState(PlayerState):
    def enter(self):
        self.player.velocity = pg.math.Vector2(0, 0)
        # Set idle animation
        if self.player.facing_right:
            self.player.images = self.player.idle_frames
        else:
            self.player.images = self.player.idle_frames_flipped
            
    def handle_input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a] or \
           keys[pg.K_RIGHT] or keys[pg.K_d] or \
           keys[pg.K_UP] or keys[pg.K_w] or \
           keys[pg.K_DOWN] or keys[pg.K_s]:
            self.player.change_state("WALK")
            
    def update(self):
        self.player.velocity = pg.math.Vector2(0, 0)