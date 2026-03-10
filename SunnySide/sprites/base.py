import pygame as pg

class SpriteSheet:
    def __init__(self, file_path, num_frames, scale=1):
        self.full_sheet = pg.image.load(file_path).convert_alpha()
        self.num_frames = num_frames
        self.frame_width = self.full_sheet.get_width() // num_frames
        self.frame_height = self.full_sheet.get_height()
        self.scale = scale
        self.frames = self._load_frames()

    def _load_frames(self):
        frames = []
        for i in range(self.num_frames):
            raw_rect = pg.Rect(i * self.frame_width, 0, self.frame_width, self.frame_height)
            raw_frame = self.full_sheet.subsurface(raw_rect)
            
            # Remove white spaces
            trimmed_rect = raw_frame.get_bounding_rect()
            trimmed_frame = pg.Surface(trimmed_rect.size, pg.SRCALPHA)
            trimmed_frame.blit(raw_frame, (0, 0), trimmed_rect)
            
            if self.scale != 1:
                trimmed_frame = pg.transform.scale(
                    trimmed_frame, 
                    (int(trimmed_rect.width * self.scale), int(trimmed_rect.height * self.scale))
                )
            frames.append(trimmed_frame)
        return frames

class BaseSprite(pg.sprite.Sprite):
    def __init__(self, animations_dict, x, y, speed=0):
        super().__init__()
        self.animations = animations_dict
        self.state = "idle"
        self.frame_index = 0
        self.flip = False
        
        first_frame = self.animations[self.state].frames[0]
        
        self.hitbox = pg.Rect(x, y, 30, 40)
        
        self.image = first_frame
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.speed = speed
        self.animation_speed = 0.3

        self.direction_y = 0  # Vận tốc theo trục Y
        self.gravity = 0.8    # Độ mạnh của trọng lực
        self.jump_speed = -14 # Lực nhảy (giá trị âm để đi lên)
        self.on_ground = False

    def animate(self):
        frames = self.animations[self.state].frames
        self.frame_index += self.animation_speed 
        
        # Reset frame index khi hết ảnh
        if self.frame_index >= len(frames):
            self.frame_index = 0
            # Nếu đang tấn công và đã hết frame, giải phóng trạng thái
            if self.state == "attack":
                return True 
        
        temp_img = frames[int(self.frame_index)]
        self.image = pg.transform.flip(temp_img, self.flip, False)

        # Cập nhật mask sau khi lật/đổi frame
        self.mask = pg.mask.from_surface(self.image)

        # Luôn giữ ảnh bám theo chân (midbottom) của hitbox
        self.rect = self.image.get_rect(midbottom=self.hitbox.midbottom)
        return False

    def draw(self, surface: pg.Surface, scroll: int = 0):
        # pg.draw.rect(surface, (255,0,0), self.hitbox, 1) # Vẽ hitbox đỏ
        surface.blit(self.image, (self.rect.x - scroll, self.rect.y))