import pygame
from settings import TILESIZE
from tile import Tile
from player import Player
from support import import_csv_layout

class Level:
    def __init__(self):
        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Import layout from the CSV file (only FloorBlocks)
        layout = import_csv_layout('../map/map_FloorBlocks.csv')

        # Import graphics for wall and floor
        graphics = {
            'wall': pygame.image.load('../graphics/tilemap/mur.png').convert_alpha(),
            'floor': pygame.image.load('../graphics/tilemap/sol.png').convert_alpha(),
        }

        # Generate tiles based on layout and find player spawn location
        player_spawn = None
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Handle wall (395) and floor (0)
                if col == '395':  # Wall
                    Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', graphics['wall'])
                elif col == '0':  # Floor
                    Tile((x, y), [self.visible_sprites], 'floor', graphics['floor'])
                    if not player_spawn:
                        player_spawn = (x, y)  # Set player spawn at first available floor

        # If a floor tile is found, place the player there
        if player_spawn:
            self.player = Player(player_spawn, [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
        else:
            # Fallback if no floor tile was found (default to (100, 100))
            self.player = Player((100, 100), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)

    # Attack, Magic, Damage, and Experience Logic (unchanged)
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

        # Draw floor and walls
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
