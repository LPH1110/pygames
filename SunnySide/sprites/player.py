import pygame as pg
from sprites.base import BaseSprite
from constants import SC_WIDTH, SC_HEIGHT
import pygame.sprite as sprite

from sound_manager import sound_manager

class Player(BaseSprite):
    def __init__(self, animations, x, y, speed):
        super().__init__(animations, x, y)
        self.start_x = x
        self.start_y = y
        self.speed = speed
        self.is_attacking = False
        self.direction_y = 0
        self.gravity = 0.8
        self.on_ground = False
        self.coins = 0
        from constants import MAX_HEALTH
        self.health = MAX_HEALTH
        self.invincible_timer = 0

    def respawn(self):
        """Resets the player back to the starting point"""
        self.hitbox.x = self.start_x
        self.hitbox.y = self.start_y
        self.direction_y = 0
        self.on_ground = False
        self.is_attacking = False
        self.state = "idle"
        self.invincible_timer = 0

    def take_damage(self, amount=1):
        if self.invincible_timer == 0:
            self.health -= amount
            if self.health > 0:
                from constants import I_FRAMES
                self.invincible_timer = I_FRAMES
        print("Health:", self.health)

    def _handle_input(self):
        """Processes keyboard inputs to calculate movement intentions and attacking."""
        keys = pg.key.get_pressed()
        dx = 0

        if keys[pg.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.state = "attack"
            sound_manager.play('attack')
            self.frame_index = 0

        if not self.is_attacking:
            if keys[pg.K_d]:
                dx = self.speed
                self.state = "walk"
                self.flip = False
            elif keys[pg.K_a]:
                dx = -self.speed
                self.state = "walk"
                self.flip = True
            else:
                self.state = "idle"

            if keys[pg.K_SPACE] and self.on_ground:
                self.direction_y = self.jump_speed
                self.on_ground = False
                
        return dx

    def _apply_gravity(self):
        """Applies gravity to Y-velocity."""
        self.direction_y += self.gravity
        return self.direction_y

    def _handle_x_collisions(self, dx, world):
        """Moves the player on the X axis and resolves tile collisions."""
        self.hitbox.x += dx
        
        if not world:
            return

        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > world.map_width:
            self.hitbox.right = world.map_width
            
        for tile in world.tiles:
            if tile.rect.colliderect(self.hitbox):
                if dx > 0: # moving right
                    self.hitbox.right = tile.rect.left
                elif dx < 0: # moving left
                    self.hitbox.left = tile.rect.right

    def _handle_y_collisions(self, dy, world):
        """Moves the player on the Y axis and resolves tile collisions."""
        self.hitbox.y += dy
        self.on_ground = False
        
        if not world:
            return
            
        for tile in world.tiles:
            if tile.rect.colliderect(self.hitbox):
                if dy > 0: # falling down
                    self.hitbox.bottom = tile.rect.top
                    self.direction_y = 0
                    self.on_ground = True
                elif dy < 0: # jumping up into a ceiling
                    self.hitbox.top = tile.rect.bottom
                    self.direction_y = 0

    def _handle_interactions(self, world):
        """Handles collisions with collectibles and out-of-bounds death zones."""
        if not world:
            return
            
        # Coin Collection
        for coin in list(world.coins):
            if self.hitbox.colliderect(coin.hitbox):
                sound_manager.play('coin')
                coin.kill()
                self.coins += 1

        # Death Pits
        if self.hitbox.top >= SC_HEIGHT + 200:
            self.take_damage(20)
            if self.health > 0:
                self.respawn()

    def _update_state_timers(self):
        """Updates invincibility timers and determines fallback visual states."""
        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        if not self.on_ground and not self.is_attacking:
            self.state = "jump"

        animation_finished = self.animate()
        if animation_finished and self.state == "attack":
            self.is_attacking = False

    def update(self, world=None):
        """Main game loop update for the player character."""
        dx = self._handle_input()
        dy = self._apply_gravity()

        self._handle_x_collisions(dx, world)
        self._handle_y_collisions(dy, world)
        
        self._handle_interactions(world)
        self._update_state_timers()

    def draw(self, surface: pg.Surface, scroll: int = 0):
        # Override draw behavior to implement i-frame blinking
        if self.invincible_timer > 0:
            if self.invincible_timer % 10 < 5:  # Blink effect
                return
        super().draw(surface, scroll)