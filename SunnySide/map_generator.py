import pygame
import csv

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, tile_size):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.tile_size = tile_size
        self.mask = pygame.mask.from_surface(self.image)

class World:
    def __init__(self, tile_size, tileset_path):
        self.tile_size = tile_size
        self.tile_list = self.load_tileset(tileset_path)
        self.map_data = []
        self.map_width = 0
        self.tiles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()

    def load_tileset(self, filename):
        try:
            img = pygame.image.load(filename).convert_alpha()
            img_w, img_h = img.get_size()
            tiles = []
            for y in range(0, img_h, self.tile_size):
                for x in range(0, img_w, self.tile_size):
                    tiles.append(img.subsurface((x, y, self.tile_size, self.tile_size)))
            return tiles
        except:
            return [pygame.Surface((self.tile_size, self.tile_size)) for _ in range(10)]
    def update(self):
        self.coins.update(self)
        self.flags.update(self)

    def draw(self, surface: pygame.Surface, scroll: int = 0):
        for tile in self.tiles:
            surface.blit(tile.image, (tile.rect.x - scroll, tile.rect.y))
        for coin in self.coins:
            coin.draw(surface, scroll)
        for flag in self.flags:
            flag.draw(surface, scroll)
    
    def process_data(self, csv_filename):
        try:
            with open(csv_filename, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.map_data.append([int(tile) for tile in row])
            self.map_width = len(self.map_data[0]) * self.tile_size
            
            base_tile_count = len(self.tile_list)
            from sprites.coin import Coin
            from sprites.flag import Flag

            for y, row in enumerate(self.map_data):
                for x, tile_idx in enumerate(row):
                    if tile_idx >= 0:
                        if tile_idx < base_tile_count:
                            tile = Tile(self.tile_list[tile_idx], x * self.tile_size, y * self.tile_size, self.tile_size)
                            self.tiles.add(tile)
                        elif tile_idx == base_tile_count:
                            c = Coin(x * self.tile_size, y * self.tile_size, scale=2)
                            self.coins.add(c)
                        elif tile_idx == base_tile_count + 1:
                            f = Flag(x * self.tile_size, y * self.tile_size, scale=1)
                            self.flags.add(f)
                        
                        
        except Exception as e:
            print(f"Error loading map data: {e}")