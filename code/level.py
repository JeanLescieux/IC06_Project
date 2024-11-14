import pygame
from settings import TILESIZE, ZOOM_FACTOR, WATER_COLOR
from tile import Tile
from player import Player
from support import import_csv_layout

class Level:
    def __init__(self):
        # Sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # Import layout from the CSV file
        layout = import_csv_layout('../map/map_FloorBlocks.csv')

        # Import graphics for different wall and floor types
        self.graphics = {
            'top_wall': pygame.image.load('../graphics/donjon/TopTop.png').convert_alpha(),
            'middle_wall': pygame.image.load('../graphics/donjon/TopBottom.png').convert_alpha(),
            'side_wall': pygame.image.load('../graphics/donjon/LeftRight.png').convert_alpha(),
            'corner_wall': pygame.image.load('../graphics/donjon/corner.png').convert_alpha(),
            'bottom_wall': pygame.image.load('../graphics/donjon/downTile.png').convert_alpha(),
            'floor': pygame.image.load('../graphics/donjon/floor.png').convert_alpha(),
            'barrel': pygame.image.load('../graphics/donjon/Barrel.png').convert_alpha(),
        }

       # List to keep track of middle wall positions for placing top walls later
        self.middle_wall_positions = []

        # First pass: Place middle walls, side walls, bottom walls, and corner walls
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == '395':  # Wall tile
                    # Middle Wall - has a walkable tile below
                    if row_index < len(layout) - 1 and layout[row_index + 1][col_index] == '0':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['middle_wall'])
                        self.middle_wall_positions.append((x, y))  # Store position for top wall placement

                    # Side Wall - adjacent to a walkable tile on either side
                    elif (col_index > 0 and layout[row_index][col_index - 1] == '0') or \
                         (col_index < len(row) - 1 and layout[row_index][col_index + 1] == '0'):
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['side_wall'])

                    # Bottom Wall - has a walkable tile above
                    elif row_index > 0 and layout[row_index - 1][col_index] == '0':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['bottom_wall'])

                    # Corner Wall - in a corner configuration with walkable tile in diagonal
                    elif self.is_corner_wall(layout, row_index, col_index):
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['corner_wall'])

                elif col == '0':  # Floor tile
                    Tile((x, y), [self.visible_sprites], 'floor', self.graphics['floor'])

        # Second pass: Place top walls above each recorded middle wall position
        for middle_x, middle_y in self.middle_wall_positions:
            Tile((middle_x, middle_y - TILESIZE), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['top_wall'])

        # Third pass: Ensure all walkable areas have a floor tile
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Check if the tile is walkable ('0') and does not already have a floor sprite
                if col == '0':
                    # Check if there's already a floor tile at this position
                    if not any(sprite.rect.topleft == (x, y) and sprite.image == self.graphics['floor'] for sprite in self.visible_sprites):
                        Tile((x, y), [self.visible_sprites], 'floor', self.graphics['floor'])

        # Fourth pass: Place barrels based on the specified conditions
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Barrel conditions
                if col == '395':  # Wall tile
                    above = row_index > 0 and layout[row_index - 1][col_index] == '0'
                    below = row_index < len(layout) - 1 and layout[row_index + 1][col_index] == '0'
                    left = col_index > 0 and layout[row_index][col_index - 1] == '0'
                    right = col_index < len(row) - 1 and layout[row_index][col_index + 1] == '0'

                    # Place barrel if it has walkable tiles above and below or on both sides
                    if (above and below) or (left and right):
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'barrel', self.graphics['barrel'])

        # Set player spawn position
        player_spawn = self.find_player_spawn(layout)
        if player_spawn:
            self.player = Player(player_spawn, [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)
        else:
            # Default spawn position if none is found
            self.player = Player((100, 100), [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack, self.create_magic)

    def is_corner_wall(self, layout, row, col):
        """ Determines if a wall is in a corner configuration. """
        if row > 0 and col > 0 and layout[row - 1][col] == '395' and layout[row][col - 1] == '395' and layout[row - 1][col - 1] == '0':
            return True
        elif row > 0 and col < len(layout[0]) - 1 and layout[row - 1][col] == '395' and layout[row][col + 1] == '395' and layout[row - 1][col + 1] == '0':
            return True
        elif row < len(layout) - 1 and col > 0 and layout[row + 1][col] == '395' and layout[row][col - 1] == '395' and layout[row + 1][col - 1] == '0':
            return True
        elif row < len(layout) - 1 and col < len(layout[0]) - 1 and layout[row + 1][col] == '395' and layout[row][col + 1] == '395' and layout[row + 1][col + 1] == '0':
            return True
        return False

    def find_player_spawn(self, layout):
        """Find a position in the layout surrounded by floor tiles."""
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == '0' and self.is_surrounded_by_floor(layout, row_index, col_index):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    return (x, y)
        return None

    def is_surrounded_by_floor(self, layout, row, col):
        """Check if a tile is surrounded by floor tiles (0) on all sides."""
        if (
            row > 0 and row < len(layout) - 1 and
            col > 0 and col < len(layout[0]) - 1 and
            layout[row - 1][col] == '0' and  # above
            layout[row + 1][col] == '0' and  # below
            layout[row][col - 1] == '0' and  # left
            layout[row][col + 1] == '0'      # right
        ):
            return True
        return False

    # Additional functions related to player actions
    def create_attack(self):
        print("Player attack created!")

    def destroy_attack(self):
        print("Player attack destroyed!")

    def create_magic(self, style, strength, cost):
        print(f"Magic {style} created with strength {strength} and cost {cost}.")

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

        # Surface temporaire pour le zoom
        self.temp_surface = pygame.Surface(
            (self.display_surface.get_width() // ZOOM_FACTOR, self.display_surface.get_height() // ZOOM_FACTOR)
        )

    def custom_draw(self, player):
        # Calcul de l'offset de la caméra
        self.offset.x = player.rect.centerx - self.half_width / ZOOM_FACTOR
        self.offset.y = player.rect.centery - self.half_height / ZOOM_FACTOR

        # Remplissage du fond
        self.temp_surface.fill(WATER_COLOR)

        # Première passe : Dessiner toutes les tuiles de sol en premier
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'sprite_type', None) == 'floor':
                offset_pos = sprite.rect.topleft - self.offset
                self.temp_surface.blit(sprite.image, offset_pos)

        # Deuxième passe : Dessiner les autres éléments (joueur, murs, etc.)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'sprite_type', None) != 'floor':
                offset_pos = sprite.rect.topleft - self.offset
                self.temp_surface.blit(sprite.image, offset_pos)

        # Mise à l'échelle pour l'affichage
        zoomed_surface = pygame.transform.scale(self.temp_surface, self.display_surface.get_size())
        self.display_surface.blit(zoomed_surface, (0, 0))
