import pygame
import csv
import copy

# --- CẤU HÌNH ---
TILE_SIZE = 32
ROWS = 16
COLS = 30
SCREEN_WIDTH = 800
SIDE_MARGIN = 300
LOWER_MARGIN = 100
SCREEN_HEIGHT = ROWS * TILE_SIZE

# Màu sắc
WHITE = (255, 255, 255)
GREEN = (144, 201, 120)
RED = (200, 25, 25)
YELLOW = (255, 255, 0) # Màu cho ô được chọn
GRAY = (70, 70, 70)
DARK_GRAY = (40, 40, 40)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption("Level Editor - Select & Delete Feature")
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 18, bold=True)
background_image = pygame.transform.scale(
    pygame.image.load("Background.png").convert_alpha(),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# --- BIẾN TOÀN CỤC ---
scroll = 0
scroll_left = False
scroll_right = False
current_tile = 0
selected_cell = None # Lưu trữ (grid_x, grid_y) của ô đang được chọn

world_data = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
history_stack = []
redo_stack = []

# --- HÀM BỔ TRỢ ---
def load_tileset(filename):
    try:
        img = pygame.image.load(filename).convert_alpha()
        img_w, img_h = img.get_size()
        tiles = []
        for y in range(0, img_h, TILE_SIZE):
            for x in range(0, img_w, TILE_SIZE):
                tiles.append(img.subsurface((x, y, TILE_SIZE, TILE_SIZE)))
        return tiles
    except:
        return [pygame.Surface((TILE_SIZE, TILE_SIZE)) for _ in range(10)]

tile_list = load_tileset('Tileset.png')

def save_history():
    history_stack.append(copy.deepcopy(world_data))
    if len(history_stack) > 50: history_stack.pop(0)
    redo_stack.clear()

def undo():
    global world_data
    if history_stack:
        redo_stack.append(copy.deepcopy(world_data))
        world_data = history_stack.pop()

def redo():
    global world_data
    if redo_stack:
        history_stack.append(copy.deepcopy(world_data))
        world_data = redo_stack.pop()

# --- LỚP BUTTON ---
class Button:
    def __init__(self, x, y, image, is_text=False, text_str=""):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
        self.is_text = is_text
        self.text_str = text_str

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True
        if not pygame.mouse.get_pressed()[0]: self.clicked = False
        surface.blit(self.image, self.rect)
        if self.is_text:
            text_img = font.render(self.text_str, True, WHITE)
            text_rect = text_img.get_rect(center=self.rect.center)
            surface.blit(text_img, text_rect)
        return action

# --- KHỞI TẠO UI ---
def create_text_btn(x, y, w, h, text, color):
    surf = pygame.Surface((w, h))
    surf.fill(color)
    return Button(x, y, surf, is_text=True, text_str=text)

tile_buttons = []
for i in range(len(tile_list)):
    tile_buttons.append(Button(SCREEN_WIDTH + 20 + ((i % 7) * 36), 20 + ((i // 7) * 36), 
                               pygame.transform.scale(tile_list[i], (30, 30))))

btn_save = create_text_btn(20, SCREEN_HEIGHT + 30, 80, 40, "SAVE", (0, 100, 0))
btn_undo = create_text_btn(110, SCREEN_HEIGHT + 30, 80, 40, "UNDO", (100, 100, 0))
btn_clear = create_text_btn(200, SCREEN_HEIGHT + 30, 80, 40, "CLEAR", RED)
btn_load = create_text_btn(290, SCREEN_HEIGHT + 30, 80, 40, "LOAD", (0, 0, 150))

# --- VÒNG LẶP CHÍNH ---
run = True
while run:
    clock.tick(60)

    # 0. Vẽ Background Lặp Kết Hợp Scroll
    # Tính toán để background cuộn mượt và lặp lại
    bg_width = background_image.get_width()
    for i in range(5): # Số lượng ảnh cần thiết để phủ kín screen khi cuộn (tùy chỉnh nếu map dài)
        screen.blit(background_image, ((i * bg_width) - scroll * 0.5, 0)) # parallax 0.5

    # 1. Vẽ Grid & Map
    for c in range(COLS + 1):
        pygame.draw.line(screen, GRAY, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for r in range(ROWS + 1):
        pygame.draw.line(screen, GRAY, (0, r * TILE_SIZE), (SCREEN_WIDTH, r * TILE_SIZE))

    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tile_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

    # Vẽ khung cho ô đang được chọn (SELECT HIGHLIGHT)
    if selected_cell:
        sel_x, sel_y = selected_cell
        pygame.draw.rect(screen, YELLOW, (sel_x * TILE_SIZE - scroll, sel_y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

    # 2. Sidebar & Bottom Bar
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))
    pygame.draw.rect(screen, BLACK, (0, SCREEN_HEIGHT, SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN))

    for i, btn in enumerate(tile_buttons):
        if btn.draw(screen): current_tile = i
    pygame.draw.rect(screen, RED, tile_buttons[current_tile].rect, 2)

    if btn_save.draw(screen):
        with open('level_data.csv', 'w', newline='') as f:
            csv.writer(f).writerows(world_data)
        print("Saved!")

    if btn_undo.draw(screen): undo()
    if btn_clear.draw(screen):
        save_history()
        world_data = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
        selected_cell = None
        
    if btn_load.draw(screen):
        try:
            with open('level_data.csv', 'r', newline='') as f:
                reader = csv.reader(f)
                new_data = []
                for row in reader:
                    if row:
                        new_data.append([int(tile) for tile in row])
                if len(new_data) >= ROWS and len(new_data[0]) >= COLS:
                    save_history()
                    world_data = [row[:COLS] for row in new_data[:ROWS]]
                    selected_cell = None
                    print("Loaded!")
                else:
                    print("Error: Map size too small in CSV")
        except Exception as e:
            print(f"Error loading: {e}")

    # 3. Logic Chuột & Select
    pos = pygame.mouse.get_pos()
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        mx = (pos[0] + scroll) // TILE_SIZE
        my = pos[1] // TILE_SIZE
        
        # Click chuột trái: Vừa để Vẽ, vừa để Chọn ô
        if pygame.mouse.get_pressed()[0]:
            if world_data[my][mx] != current_tile:
                save_history()
                world_data[my][mx] = current_tile
            selected_cell = (mx, my) # Cập nhật ô được chọn
            
        # Click chuột phải: Xóa nhanh và Chọn ô đó
        if pygame.mouse.get_pressed()[2]:
            if world_data[my][mx] != -1:
                save_history()
                world_data[my][mx] = -1
            selected_cell = (mx, my)

    # 4. Cuộn
    if scroll_left and scroll > 0: scroll -= 5
    if scroll_right and scroll < (COLS * TILE_SIZE) - SCREEN_WIDTH: scroll += 5

    # 5. Sự kiện bàn phím & Chuột
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False
        
        # Cuộn bằng con lăn chuột
        if event.type == pygame.MOUSEWHEEL:
            scroll -= event.y * (TILE_SIZE // 2)
            scroll = max(0, min(scroll, (COLS * TILE_SIZE) - SCREEN_WIDTH))
            
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a): scroll_left = True
            if event.key in (pygame.K_RIGHT, pygame.K_d): scroll_right = True
            
            # CHỨC NĂNG XÓA Ô ĐANG CHỌN (DELETE KEY)
            if event.key in (pygame.K_DELETE, pygame.K_BACKSPACE):
                if selected_cell:
                    sel_x, sel_y = selected_cell
                    if world_data[sel_y][sel_x] != -1:
                        save_history()
                        world_data[sel_y][sel_x] = -1
            
            if event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL: undo()
            if event.key == pygame.K_y and pygame.key.get_mods() & pygame.KMOD_CTRL: redo()

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a): scroll_left = False
            if event.key in (pygame.K_RIGHT, pygame.K_d): scroll_right = False

    pygame.display.update()

pygame.quit()