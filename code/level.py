import pygame
from settings import TILESIZE, ZOOM_FACTOR, WATER_COLOR
from tile import Tile
from player import Player
from enemy import Enemy
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

       # Liste pour stocker les positions des murs du milieu pour placer les murs du haut plus tard
        self.middle_wall_positions = []

        # Première passe : Placement des murs (middle, side, bottom, corner)
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                if col == '395':  # Case murale
                    # Mur du milieu - a une case walkable en dessous
                    if row_index < len(layout) - 1 and layout[row_index + 1][col_index] == '0':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['middle_wall'])
                        self.middle_wall_positions.append((x, y))  # Stocker la position pour le placement des murs du haut

                    # Mur latéral - adjacent à une case walkable de chaque côté
                    elif (col_index > 0 and layout[row_index][col_index - 1] == '0') or \
                         (col_index < len(row) - 1 and layout[row_index][col_index + 1] == '0'):
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['side_wall'])

                    # Mur du bas - a une case walkable au-dessus
                    elif row_index > 0 and layout[row_index - 1][col_index] == '0':
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['bottom_wall'])

                    # Coin - configuration en coin avec une case walkable en diagonale
                    elif self.is_corner_wall(layout, row_index, col_index):
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['corner_wall'])

        # Deuxième passe : Placement des top walls et des tonneaux
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Placement des murs du haut au-dessus de chaque mur du milieu enregistré
                if (x, y) in self.middle_wall_positions:
                    Tile((x, y - TILESIZE), [self.visible_sprites, self.obstacle_sprites], 'wall', self.graphics['top_wall'])

                # Conditions pour placer un tonneau
                if col == '395':  # Case murale
                    walkable_neighbors = self.count_walkable_neighbors(layout, row_index, col_index)
                    # Placer un tonneau si la case murale a 3 voisins ou plus walkable
                    if walkable_neighbors >= 3:
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'barrel', self.graphics['barrel'])

        # Troisième passe : Assurer que toutes les zones walkable ont un sprite de sol
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Remplace tout sur les cases `0` par un sol (floor)
                if col == '0':
                    # Supprime les sprites existants à cette position
                    for sprite in self.visible_sprites:
                        if sprite.rect.topleft == (x, y):
                            sprite.kill()
                    # Ajoute le sol
                    Tile((x, y), [self.visible_sprites], 'floor', self.graphics['floor'])

        # Position de spawn du joueur
        player_spawn = self.find_player_spawn(layout)
        if player_spawn:
            self.player = Player(player_spawn, [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites)
        else:
            # Position par défaut si aucune position de spawn trouvée
            self.player = Player((100, 100), [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites)

    def is_corner_wall(self, layout, row, col):
        """ Détermine si une case murale est dans une configuration en coin. """
        if row > 0 and col > 0 and layout[row - 1][col] == '395' and layout[row][col - 1] == '395' and layout[row - 1][col - 1] == '0':
            return True
        elif row > 0 and col < len(layout[0]) - 1 and layout[row - 1][col] == '395' and layout[row][col + 1] == '395' and layout[row - 1][col + 1] == '0':
            return True
        elif row < len(layout) - 1 and col > 0 and layout[row + 1][col] == '395' and layout[row][col - 1] == '395' and layout[row + 1][col - 1] == '0':
            return True
        elif row < len(layout) - 1 and col < len(layout[0]) - 1 and layout[row + 1][col] == '395' and layout[row][col + 1] == '395' and layout[row + 1][col + 1] == '0':
            return True
        return False

    def count_walkable_neighbors(self, layout, row, col):
        """Compte le nombre de voisins walkable autour d'une case murale."""
        neighbors = 0
        # Haut
        if row > 0 and layout[row - 1][col] == '0':
            neighbors += 1
        # Bas
        if row < len(layout) - 1 and layout[row + 1][col] == '0':
            neighbors += 1
        # Gauche
        if col > 0 and layout[row][col - 1] == '0':
            neighbors += 1
        # Droite
        if col < len(layout[0]) - 1 and layout[row][col + 1] == '0':
            neighbors += 1
        return neighbors

    def find_player_spawn(self, layout):
        """Trouve une position de spawn entourée de cases de sol."""
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == '0' and self.is_surrounded_by_floor(layout, row_index, col_index):
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    return (x, y)
        return None

    def is_surrounded_by_floor(self, layout, row, col):
        """Vérifie si une case est entourée de cases de sol (0) de tous les côtés."""
        if (
            row > 0 and row < len(layout) - 1 and
            col > 0 and col < len(layout[0]) - 1 and
            layout[row - 1][col] == '0' and  # au-dessus
            layout[row + 1][col] == '0' and  # en-dessous
            layout[row][col - 1] == '0' and  # à gauche
            layout[row][col + 1] == '0'      # à droite
        ):
            return True
        return False

    # Fonctions supplémentaires liées aux actions du joueur
    def create_attack(self):
        print("Attaque du joueur créée !")

    def destroy_attack(self):
        print("Attaque du joueur détruite !")

    def create_magic(self, style, strength, cost):
        print(f"Magie {style} créée avec force {strength} et coût {cost}.")

    def run(self):
        """Exécute le niveau (mise à jour et dessin)."""
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()



class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.temp_surface = pygame.Surface(
            (self.display_surface.get_width() // ZOOM_FACTOR, self.display_surface.get_height() // ZOOM_FACTOR)
        )

    def custom_draw(self, player):
        # Getting the offset 
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'sprite_type', None) == 'floor':
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
        
		
		# Deuxième passe : Dessiner les autres éléments (joueur, murs, etc.)
        
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'sprite_type', None) != 'floor':
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
		
        # Dessiner les sprites avec le décalage
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if isinstance(sprite, Enemy):
                sprite.display_weapon(self.display_surface, self.offset)
        
        # Afficher l'arme du joueur en appliquant le même décalage
        player.draw_weapon(self.display_surface, self.offset)
        
        # Dessiner le bouclier du joueur avec le décalage
        player.draw_shield(self.display_surface, self.offset)
        

