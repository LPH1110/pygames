import pygame as pg
from sprites.base import BaseSprite
from constants import SC_WIDTH, SC_HEIGHT

class Player(BaseSprite):
    def __init__(self, animations, x, y, speed):
        super().__init__(animations, x, y)
        self.speed = speed
        self.is_attacking = False
        self.direction_y = 0
        self.gravity = 0.8
        self.on_ground = False

    def update(self, world=None):
        keys = pg.key.get_pressed()

        # 1. Kích hoạt Attack
        if keys[pg.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.state = "attack"
            self.frame_index = 0 # Reset về frame đầu tiên ngay lập tức

        dx = 0
        dy = 0

        # 2. Logic di chuyển & Jump (CHỈ chạy khi không tấn công)
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
        
        # 3. Trọng lực (Vẫn chạy để nhân vật rơi xuống khi đang đánh)
        self.direction_y += self.gravity
        dy = self.direction_y

        # Kiểm tra va chạm
        if world:
            # X axis
            self.hitbox.x += dx
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
                        
            # Y axis
            self.hitbox.y += dy
            self.on_ground = False
            for tile in world.tiles:
                if tile.rect.colliderect(self.hitbox):
                    if dy > 0: # falling
                        self.hitbox.bottom = tile.rect.top
                        self.direction_y = 0
                        self.on_ground = True
                    elif dy < 0: # jumping
                        self.hitbox.top = tile.rect.bottom
                        self.direction_y = 0
        else:
            self.hitbox.x += dx
            self.hitbox.y += dy

        # Kiểm tra va chạm sàn màn hình dự phòng
        if self.hitbox.bottom >= SC_HEIGHT:
            self.hitbox.bottom = SC_HEIGHT
            self.direction_y = 0
            self.on_ground = True

        # Đổi state sang Jump nếu đang ở trên không và không tấn công
        if not self.on_ground and not self.is_attacking:
            self.state = "jump"

        # 4. Cập nhật Animation và xử lý kết thúc Attack
        animation_finished = self.animate()
        if animation_finished and self.state == "attack":
            self.is_attacking = False # Mở khóa trạng thái