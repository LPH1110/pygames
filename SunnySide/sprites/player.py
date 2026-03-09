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

    def update(self):
        keys = pg.key.get_pressed()

        # 1. Kích hoạt Attack
        if keys[pg.K_j] and not self.is_attacking:
            self.is_attacking = True
            self.state = "attack"
            self.frame_index = 0 # Reset về frame đầu tiên ngay lập tức

        # 2. Logic di chuyển & Jump (CHỈ chạy khi không tấn công)
        if not self.is_attacking:
            if keys[pg.K_RIGHT] and self.hitbox.right <= SC_WIDTH:
                self.hitbox.x += self.speed
                self.state = "walk"
                self.flip = False
            elif keys[pg.K_LEFT] and self.hitbox.left >= 0:
                self.hitbox.x -= self.speed
                self.state = "walk"
                self.flip = True
            else:
                self.state = "idle"

            if keys[pg.K_SPACE] and self.on_ground:
                self.direction_y = -15
                self.on_ground = False
        
        # 3. Trọng lực (Vẫn chạy để nhân vật rơi xuống khi đang đánh)
        self.direction_y += self.gravity
        self.hitbox.y += self.direction_y

        # Kiểm tra va chạm sàn
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