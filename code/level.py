import pygame
from enemy import Enemy
from settings import TILESIZE
from tile import Tile
from player import Player
from support import import_csv_layout, import_folder
from random import choice

class Level:
    def __init__(self):
        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Import layouts (from CSV files)
        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'floor': import_csv_layout('../map/map_Floor.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_Objects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }

        # Import graphics
        graphics = {
            'wall': pygame.image.load('../graphics/tilemap/mur.png').convert_alpha(),
            'water': pygame.image.load('../graphics/tilemap/eau.png').convert_alpha(),
            'floor': pygame.image.load('../graphics/tilemap/sol.png').convert_alpha(),
            'grass': import_folder('../graphics/Grass'),
            'objects': import_folder('../graphics/objects')
        }

        # Generate tiles based on layout
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':  # If the tile is not empty
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        # Handle boundary (walls and water)
                        if style == 'boundary':
                            if col == '395':  # Water
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'water', graphics['water'])
                            elif col == '1':  # Wall
                                Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', graphics['wall'])

                        # Handle floor
                        elif style == 'floor':
                            Tile((x, y), [self.visible_sprites], 'floor', graphics['floor'])

                        # Handle grass
                        elif style == 'grass':
                            random_grass_image = choice(graphics['grass'])
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)

                        # Handle objects
                        elif style == 'object':
                            surf = graphics['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf)

                        # Handle entities (player and enemies)
                        elif style == 'entities':
                            if col == '394':  # Player
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:
                                # Enemies: based on CSV values
                                if col == '390':
                                    monster_name = 'bamboo'
                                elif col == '391':
                                    monster_name = 'spirit'
                                elif col == '392':
                                    monster_name = 'raccoon'
                                else:
                                    monster_name = 'squid'
                                Enemy(
                                    monster_name,
                                    (x, y),
                                    [self.visible_sprites, self.obstacle_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles,
                                    self.add_exp)

    def create_attack(self):
        """Create an attack for the player."""
        print("Player attack created!")

    def destroy_attack(self):
        """Destroy the current attack."""
        print("Player attack destroyed!")

    def create_magic(self, style, strength, cost):
        """Create a magic attack for the player."""
        print(f"Magic {style} created with strength {strength} and cost {cost}.")

    def damage_player(self, amount, attack_type):
        """Damage the player."""
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            print(f"Player took {amount} damage from {attack_type}!")

    def trigger_death_particles(self, pos, particle_type):
        """Trigger particle effects when an entity dies."""
        print(f"Death particles for {particle_type} at {pos}!")

    def add_exp(self, amount):
        """Add experience points to the player."""
        self.player.exp += amount
        print(f"Player gained {amount} experience points!")

    def run(self):
        """Run the game level (update and draw)."""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Calculate camera offset based on player position
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Draw floor
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
