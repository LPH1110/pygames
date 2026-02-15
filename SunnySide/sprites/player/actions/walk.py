from sprites.player.player_state import PlayerState
import pygame as pg

class WalkState(PlayerState):
    def enter(self):
        # Set walk animation
        if self.player.facing_right:
            self.player.images = self.player.walk_frames
        else:
            self.player.images = self.player.walk_frames_flipped
            
    def handle_input(self):
        keys = pg.key.get_pressed()
        self.player.velocity = pg.math.Vector2(0, 0)
        
        moving = False
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.player.velocity.x = -1
            self.player.facing_right = False
            moving = True
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.player.velocity.x = 1
            self.player.facing_right = True
            moving = True
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.player.velocity.y = -1
            moving = True
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.player.velocity.y = 1
            moving = True
            
        if not moving:
            self.player.change_state("IDLE")
        else:
            # Normalize velocity
            if self.player.velocity.length() > 0:
                self.player.velocity = self.player.velocity.normalize() * self.player.speed
                
    def update(self):
        # Update animation based on facing direction
        if self.player.facing_right:
            self.player.images = self.player.walk_frames
        else:
            self.player.images = self.player.walk_frames_flipped