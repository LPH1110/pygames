import os

# GAME CONFIG
SC_WIDTH = 900
SC_HEIGHT = 700
FPS = 60
GAME_TITLE = "The Space Shooter"

# FOLDER PATHS
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites")
SPACESHIP_DIR = os.path.join(SPRITES_DIR, "Spaceship")


SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
OTHERS_DIR = os.path.join(SPRITES_DIR, "Others")
ENERGY_DIR = os.path.join(SPRITES_DIR, "Energy")
MISSILES_DIR = os.path.join(SPRITES_DIR, "Missiles")
ENEMIES_DIR = os.path.join(SPRITES_DIR, "Enemy")

# ENERGY CONFIG
ENERGY_ICON = os.path.join(ENERGY_DIR, "energy1.png")
ENERGY_IMAGES = [
    os.path.join(ENERGY_DIR, f"energy{i}.png") for i in range(1, 5)
]

# SOUND SFX
FIRE_SOUND = os.path.join(SOUNDS_DIR, "fire.ogg")
BGM_SOUND = os.path.join(SOUNDS_DIR, "space.ogg")

# BULLET CONFIG
BULLET_IMG = os.path.join(MISSILES_DIR, "missile2.png")
BULLET_SPEED = -10

# PLAYER CONFIG
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_SPEED = 3
PLAYER_DAMAGE = 10
PLAYER_START_ENERGY = 100 # Player's starting health
PLAYER_INVINCIBILITY_MS = 1000 # 1 second of invincibility after being hit
SPACESHIP_IMAGES = [
    os.path.join(SPACESHIP_DIR, f"ship_{i}.png") for i in range(1, 6)
]

# ASTEROID CONFIG
ASTEROID_DAMAGE = 25 # How much damage one asteroid hit does
ASTEROID_IMG = os.path.join(OTHERS_DIR, "asteroid.png")


# EXPLOSION CONFIG
EXPLOSION_DIR = os.path.join(SPRITES_DIR, "Explosions")
EXPLOSION_IMAGES = [
    os.path.join(EXPLOSION_DIR, f"{i}.png") for i in range(1, 8) # Assuming 7 frames: 1.png to 7.png
]
EXPLOSION_SPEED = 50 # Time in milliseconds to show each frame

# ENEMY CONFIG
ENEMY_IMAGE = os.path.join(ENEMIES_DIR, "ship_1.png")
ENEMY_SPEED = 2
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 40
ENEMY_MAX_HEALTH = 30

# ENEMY WEAPON CONFIG
ENEMY_LASER_IMG = os.path.join(SPRITES_DIR, "Lasers", "Red", "laserRed08.png")
ENEMY_LASER_SPEED = 3   # Tốc độ bay của đạn địch
ENEMY_SHOOT_DELAY = 2000 # Thời gian chờ giữa các lần bắn (2000ms = 2 giây)