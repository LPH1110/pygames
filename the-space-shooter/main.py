import pygame as pg
import sys
import random
from constants import (
    SC_WIDTH, 
    SC_HEIGHT, 
    FPS,
    GAME_TITLE,
    SPACESHIP_IMAGES,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    ENERGY_IMAGES,
    EXPLOSION_IMAGES,
    ENEMY_IMAGE,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    PLAYER_DAMAGE
)
from colors import (
    BLACK,
    WHITE
)
from models.player import Player
from models.particle import Particle
from models.asteroid import Asteroid
from models.bullet import Bullet
from models.sound_manager import SoundManager
from models.explosion import Explosion
from models.enemy import Enemy

class Game():
    # constructor
    def __init__(self):
        # Start Pygame engine
        self.sound_manager = SoundManager()
        pg.init()
        
        self.screen = pg.display.set_mode((SC_WIDTH, SC_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        
        # Font initialization
        self.font = pg.font.SysFont("Consolas", 20)
        
        # Game state
        self.game_state = "SELECTION" 
        
        self.ship_images = []
        self.load_ship_images()
        self.selected_ship_index = 0
        
        self.player = None
        self.all_sprites = pg.sprite.Group() 

        # Create tons of particles
        self.particles = []
        self.create_particles(50)

        # Create tons of asteroids
        self.asteroids = pg.sprite.Group()
        self.create_asteroids(10)

        self.bullets = pg.sprite.Group()

        # --- PLAYER ENERGY ---
        self.energy_images = []
        self.load_energy_images()

        # --- EXPLOSION FRAMES
        self.explosion_frames = [] 
        self.load_explosion_images()

        self.enemies = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()

        # --- START BACKGROUND MUSIC ---
        # self.sound_manager.play_music()

    def load_energy_images(self):
        for img_path in ENERGY_IMAGES:
            try:
                image = pg.image.load(img_path)
                image = pg.transform.scale(image, (80, 20)) 
                self.energy_images.append(image)
            except Exception as e:
                print(f"Unable to load energy images from {img_path}: {e}")

    def load_explosion_images(self):
        """Loads and scales the explosion animation frames."""
        for img_path in EXPLOSION_IMAGES:
            try:
                # Load with alpha for transparency
                image = pg.image.load(img_path).convert_alpha() 
                # Scale the explosion size (e.g., 120x120 is a good size for player)
                image = pg.transform.scale(image, (120, 120)) 
                self.explosion_frames.append(image)
            except Exception as e:
                print(f"Unable to load explosion image from {img_path}: {e}")

    def draw_energy_bar(self):
        """
        Draws the energy bar icon based on the player's current health.
        Uses 4 images for health thresholds: 100%, 75%, 50%, 25%.
        """
        if not self.player:
            return

        energy_percent = (self.player.energy / self.player.max_energy) * 100

        # Determine which image index to use (0 to 3, corresponding to energy1 to energy4)
        if energy_percent > 75:
            # 75% - 100% health: full energy icon
            image_index = 0 
        elif energy_percent > 50:
            # 50% - 75% health: 3/4 energy icon
            image_index = 1
        elif energy_percent > 25:
            # 25% - 50% health: half energy icon
            image_index = 2
        else:
            # 0% - 25% health: low energy icon
            image_index = 3 
            
        # Draw the image in the top left corner (10, 10)
        if image_index < len(self.energy_images):
            energy_img = self.energy_images[image_index]
            self.screen.blit(energy_img, (10, SC_HEIGHT - 40))
            
            # Draw the energy value next to the image for clarity
            energy_text = self.font.render(f"ENERGY: {self.player.energy}", True, WHITE)
            self.screen.blit(
                energy_text, 
                (20 + energy_img.get_width(), SC_HEIGHT - 40)
            )

    def load_ship_images(self):
        for img_path in SPACESHIP_IMAGES:
            try:
                image = pg.image.load(img_path)
                image = pg.transform.scale(image, (100, 80)) # Image size when selecting
                self.ship_images.append(image)
            except Exception as e:
                print(f"Unable to load images from {img_path}: {e}")
                sys.exit()

    def run(self):
        # The main game loop
        running = True
        while running:
            running = self.handle_events()
            
            self.update()
            
            self.draw()
            
            self.clock.tick(FPS)

        sys.exit(pg.quit())

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False # exit the game
                
            # Input handling for Selection mode
            if self.game_state == "SELECTION":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.selected_ship_index = (self.selected_ship_index - 1) % len(self.ship_images)
                        # self.sound_manager.play_sfx("ship_selected")
                    elif event.key == pg.K_RIGHT:
                        self.selected_ship_index = (self.selected_ship_index + 1) % len(self.ship_images)
                        # self.sound_manager.play_sfx("ship_selected")
                    elif event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        self.start_game()
                    
                        
            # Input handling for Gameplay mode
            elif self.game_state == "GAMEPLAY":
                if event.type == pg.KEYDOWN:
                    # When player clicks ESCAPE, then go back to the menu
                    if event.key == pg.K_ESCAPE:
                        self.game_state = "SELECTION" 
                    elif event.key == pg.K_SPACE:
                        self.shoot()  

            # Input handling for Game Over mode
            elif self.game_state == "GAME_OVER":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        # Clear existing asteroids and sprites before returning to menu
                        self.asteroids.empty()
                        self.all_sprites.empty()
                        self.create_asteroids(10) # Re-populate asteroids for next game
                        self.game_state = "SELECTION"
        return True 

    def update(self):
        # Particles will move no matter what the game's state is
        for particle in self.particles:
            particle.update()

        """Update the game logic based on Game's state"""
        if self.game_state == "GAMEPLAY":
            self.all_sprites.update() 

            # Collision checks
            self.check_bullet_collision() 
            self.check_asteroid_collision()
            self.check_enemy_bullet_collision()

        elif self.game_state == "GAME_OVER":
             self.all_sprites.update()

    def draw(self):
        # Draw the background color
        self.screen.fill(BLACK)

        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw state's screen
        if self.game_state == "SELECTION":
            self.draw_selection_screen()
        elif self.game_state == "GAMEPLAY":
            self.draw_gameplay_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_gameplay_screen() 
            self.draw_game_over_screen()
            
        pg.display.update()

    def shoot(self):
        """
            Fire the missile when player hits SPACE
        """
        bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
        self.all_sprites.add(bullet)
        self.bullets.add(bullet)
    
    def check_bullet_collision(self):
        asteroid_hits = pg.sprite.groupcollide(self.asteroids, self.bullets, True, True)
        for _ in asteroid_hits:
            self.create_asteroids(1)

        if hasattr(self, 'enemies'): 
            enemy_hits = pg.sprite.groupcollide(self.enemies, self.bullets, False, True)
            
            for enemy, bullets_hit_list in enemy_hits.items():
                for _ in bullets_hit_list:
                    is_dead = enemy.take_damage(PLAYER_DAMAGE)
                    if is_dead:
                        self.create_explosion(enemy.rect.center)
                        enemy.kill()
                        self.increase_difficulty()
                        self.spawn_new_enemy() 

    def spawn_new_enemy(self):
        enemy = Enemy(
            file_image = ENEMY_IMAGE, 
            x = SC_WIDTH // 2 - ENEMY_WIDTH // 2, 
            y = -100, 
            width = ENEMY_WIDTH, 
            height = ENEMY_HEIGHT,
            player_ref = self.player,          
            all_sprites_ref = self.all_sprites,
            bullet_group_ref = self.enemy_bullets,
            laser_angles = self.current_enemy_angles
        )
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def check_enemy_bullet_collision(self):
        if not self.player:
            return

        hits = pg.sprite.spritecollide(self.player, self.enemy_bullets, True)

        if hits:
           
            if self.player.hit():
                
                if self.player.energy <= 0:
                    explosion_center = self.player.rect.center
                    explosion = Explosion(explosion_center, self.explosion_frames)
                    self.all_sprites.add(explosion)
                    
                    self.player.kill()
                    self.player = None
                    
                    self.game_state = "GAME_OVER"

    def draw_game_over_screen(self):
        """
        Draws the 'YOU LOSE' message and instructions in the center.
        """
        # Create a large font for the main message
        large_font = pg.font.SysFont("Consolas", 60, bold=True)
        
        # --- Draw YOU LOSE message ---
        title_text = large_font.render("YOU LOSE", True, WHITE)
        self.screen.blit(
            title_text, 
            (SC_WIDTH // 2 - title_text.get_width() // 2, SC_HEIGHT // 2 - title_text.get_height())
        )
        
        # --- Draw instruction message ---
        instructions_text = self.font.render("PRESS <SPACE> or <ENTER> TO RETURN TO MENU", True, WHITE)
        self.screen.blit(
            instructions_text, 
            (SC_WIDTH // 2 - instructions_text.get_width() // 2, SC_HEIGHT // 2 + instructions_text.get_height())
        )
        
    def check_asteroid_collision(self):
        if not self.player:
            return

        hits = pg.sprite.spritecollide(self.player, self.asteroids, False)

        if hits:
            # Only process the hit if the player is not currently invincible.
            if self.player.hit():
                
                # The player took damage, so destroy the hitting asteroids and replace them.
                for asteroid in hits:
                    asteroid.kill() # Remove the hitting asteroid from all groups
                    self.create_asteroids(1) # Replace it

                # Check for game over
                if self.player.energy <= 0:
                    
                    # 1. Create Explosion at Player's Position
                    explosion_center = self.player.rect.center
                    explosion = Explosion(explosion_center, self.explosion_frames)
                    self.all_sprites.add(explosion)
                    
                    # 2. Kill the player sprite
                    self.player.kill()
                    self.player = None
                    
                    # 3. End the game 
                    self.game_state = "GAME_OVER"

    def draw_selection_screen(self):
        title_text = self.font.render("SELECT YOUR SPACESHIP", True, WHITE)
        self.screen.blit(title_text, (SC_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        selected_ship_img = self.ship_images[self.selected_ship_index]
        
        self.screen.blit(
            selected_ship_img, 
            (
                SC_WIDTH // 2 - selected_ship_img.get_width() // 2, 
                SC_HEIGHT // 2  - selected_ship_img.get_height() // 2
            )
        )
        
        instructions_text = self.font.render("USE <LEFT | RIGHT> TO SELECT AND HIT <SPACE> TO PLAY", True, WHITE)
        self.screen.blit(instructions_text, (SC_WIDTH // 2 - instructions_text.get_width() // 2, SC_HEIGHT - 100))

    def draw_gameplay_screen(self):
        self.all_sprites.draw(self.screen)

        self.draw_energy_bar()

    def start_game(self):
        # If player already exists (from a previous game), remove it
        if self.player:
            self.player.kill()

        selected_ship_path = SPACESHIP_IMAGES[self.selected_ship_index]
        
        start_x = SC_WIDTH // 2 - PLAYER_WIDTH // 2
        start_y = SC_HEIGHT - PLAYER_HEIGHT - 20 
        
        self.player = Player(selected_ship_path, start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.all_sprites.add(self.player)

        # CREATE ENEMY
        self.enemies.empty()
        self.enemy_bullets.empty()

        self.current_enemy_angles = [0, -15, 15]
        self.spawn_new_enemy()
        # ---------------------------
        
        self.game_state = "GAMEPLAY"

    def increase_difficulty(self):
        current_max_angle = max(self.current_enemy_angles)
        
        new_angle = current_max_angle + 15
        
        if new_angle <= 75:
            self.current_enemy_angles.append(new_angle)
            self.current_enemy_angles.append(-new_angle)
            print(f"DIFFICULTY INCREASED: {self.current_enemy_angles}")

    def create_particles(self, num_particles = 100):
        """ Generate particles based on num_particles and add them to the list"""
        for _ in range(num_particles):
            self.particles.append(Particle())

    def create_asteroids(self, num_asteroids=10): 
        """Create asteroids and add them to the sprite group"""
        for _ in range(num_asteroids):
            asteroid = Asteroid()
            self.asteroids.add(asteroid)
            self.all_sprites.add(asteroid)

    def create_explosion(self, center_position):
        explosion = Explosion(center_position, self.explosion_frames)
        self.all_sprites.add(explosion)
    
if __name__ == "__main__":
    game = Game()
    game.run() 