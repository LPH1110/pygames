import pygame as pg
import random
from models.base_sprite import BaseSprite
from models.enemy_laser import EnemyLaser
from constants import (
    ENEMY_SPEED,
    SC_WIDTH,
    SC_HEIGHT,
    ENEMY_SHOOT_DELAY,
    ENEMY_MAX_HEALTH
)

class Enemy(BaseSprite):
    def __init__(
            self, 
            file_image, 
            x, y, 
            width, height, 
            player_ref, all_sprites_ref, bullet_group_ref, 
            speed = ENEMY_SPEED,
            laser_angles = [0, -15, 15],
    ):
        super().__init__(file_image, x, y, width, height, speed)
        
        self.position = pg.math.Vector2(x, y)
        self.target_position = pg.math.Vector2(x, y)

        self.current_health = ENEMY_MAX_HEALTH
        self.max_health = ENEMY_MAX_HEALTH

        self.laser_angles = laser_angles
        
        # Tham chiếu đến các đối tượng bên ngoài
        self.player = player_ref
        self.all_sprites = all_sprites_ref
        self.bullet_group = bullet_group_ref
        
        # Quản lý thời gian bắn
        self.last_shot_time = pg.time.get_ticks()
        self.shoot_delay = ENEMY_SHOOT_DELAY

        self.state = "ENTERING"
        self.patrol_area = {
            "min_x": 0,
            "max_x": SC_WIDTH - width,
            "min_y": 50,
            "max_"
            "y": SC_HEIGHT // 2
        }

    def take_damage(self, amount):
        self.current_health -= amount
        if self.current_health <= 0:
            self.current_health = 0
            return True # Die
        return False # Alive

    def select_new_target(self):
        rand_x = random.randint(self.patrol_area["min_x"], self.patrol_area["max_x"])
        rand_y = random.randint(self.patrol_area["min_y"], self.patrol_area["max_y"])
        self.target_position = pg.math.Vector2(rand_x, rand_y)

    def shoot_at_player(self):
        if not self.player or not self.player.alive():
            return 

        now = pg.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            
            start_pos = pg.math.Vector2(self.rect.centerx, self.rect.bottom)
            target_pos = pg.math.Vector2(self.player.rect.centerx, self.player.rect.centery)
            direction = target_pos - start_pos
            
            for angle in self.laser_angles:
                rotated_dir = direction.rotate(angle)
                
                laser = EnemyLaser(start_pos.x, start_pos.y, rotated_dir)
                
                self.all_sprites.add(laser)
                self.bullet_group.add(laser)

    def update(self):
        if self.state == "ENTERING":
            self.position.y += self.speed
            if self.position.y >= 100:
                self.state = "PATROLLING"
                self.select_new_target()
                
        elif self.state == "PATROLLING":
            direction = self.target_position - self.position
            distance = direction.length()
            
            if distance < self.speed:
                self.position = self.target_position
                self.select_new_target()
            else:
                direction = direction.normalize()
                self.position += direction * self.speed

        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)
        
        # Handle shooting lasers
        if self.state == "PATROLLING":
            self.shoot_at_player()