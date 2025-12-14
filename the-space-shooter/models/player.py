import pygame as pg
from models.base_sprite import BaseSprite
from constants import (
    SC_WIDTH, 
    SC_HEIGHT, 
    PLAYER_SPEED, 
    PLAYER_START_ENERGY, 
    PLAYER_INVINCIBILITY_MS,
    ASTEROID_DAMAGE
)

class Player(BaseSprite):
    def __init__(self, file_image, x, y, width, height, speed=PLAYER_SPEED):
        super().__init__(file_image, x, y, width, height, speed)
        self.energy = PLAYER_START_ENERGY
        self.max_energy = PLAYER_START_ENERGY
        
        # Invincibility timer
        # This prevents the player from losing all health in one frame
        self.last_hit_time = pg.time.get_ticks()
        self.invincibility_duration = PLAYER_INVINCIBILITY_MS
        
    def update(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP] and self.rect.top >= 0:
            self.rect.y -= self.speed
        elif keys[pg.K_DOWN] and self.rect.bottom < SC_HEIGHT:
            self.rect.y += self.speed
        elif keys[pg.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        elif keys[pg.K_RIGHT] and self.rect.right < SC_WIDTH:
            self.rect.x += self.speed

    def hit(self):
        """
        Handles taking damage if the player is not currently invincible.
        Reduces energy by ASTEROID_DAMAGE.
        Returns True if the player was damaged, False otherwise.
        """
        now = pg.time.get_ticks()
        if now - self.last_hit_time > self.invincibility_duration:
            # Player is not invincible, so take damage
            self.energy -= ASTEROID_DAMAGE
            self.last_hit_time = now # Reset the invincibility timer
            return True
        return False