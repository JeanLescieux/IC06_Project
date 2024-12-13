import math
import random
import pygame
from settings import TILESIZE, ZOOM_FACTOR, WIDTH, HEIGTH, FONT_PATH
from tile import Tile
from player import Player
from enemy import Enemy
from support import import_csv_layout
from debug import debug
from Sprite_sheet import sprite_Door_Close

def draw_message(screen, message, font_size, color, pos):
        """Affiche un message sur l'écran."""
        font = pygame.font.Font(FONT_PATH, font_size)
        text_surface = font.render(message, True, color)
        text_rect = text_surface.get_rect(center=pos)
        screen.blit(text_surface, text_rect)

class Level:
    def __init__(self, alert):
        # Sprite groups
        self.alert = alert
        pygame.mixer.music.load("../audio/8bit Dungeon Level.mp3")
        pygame.mixer.music.play(-1)
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        player_spawn = None  # Initialisation par défaut

        self.message = ""  # Message à afficher
        self.message_timer = 0  # Durée d'affichage du message
        self.message_duration = 3000  # Durée (en ms) avant disparition du message
        self.newEnnemy = 5000
        self.newEnnemyTimer = 0

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
            'door': pygame.image.load('../graphics/donjon/door.png').convert_alpha(),
            'witch': pygame.image.load('../graphics/donjon/witch.png').convert_alpha(),
        }

        #Liste pour stocker les positions des murs du milieu pour placer les murs du haut plus tard
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
                
                if col == '99':  # Porte
                    # Vérifiez si c'est une porte de 3x3
                    if (
                        row_index < len(layout) - 2 and col_index < len(row) - 2 and
                        layout[row_index][col_index + 1] == '99' and layout[row_index][col_index + 2] == '99' and
                        layout[row_index + 1][col_index] == '99' and layout[row_index + 1][col_index + 1] == '99' and layout[row_index + 1][col_index + 2] == '99' and
                        layout[row_index + 2][col_index] == '99' and layout[row_index + 2][col_index + 1] == '99' and layout[row_index + 2][col_index + 2] == '99'
                    ):
                        # Placer un unique sprite de porte de 48x48 centré sur les 9 cases
                        Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'door', self.graphics['door'], size=(48, 48))
                        player_spawn = (x + TILESIZE, y + 3 * TILESIZE)  # Spawner le joueur en dessous de la porte

        # Troisième passe : Assurer que toutes les zones walkable ont un sprite de sol
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE

                # Placer un sprite de sol sur toutes les cases walkables
                if col == '0' or col == '2':  # Inclure '2' pour placer un sol sous la witch
                    for sprite in self.visible_sprites:
                        if sprite.rect.topleft == (x, y):
                            sprite.kill()  # Supprimer tout sprite existant à cette position
                    Tile((x, y), [self.visible_sprites], 'floor')  # Placer le sol

                # Si la case est une witch, placer le sprite witch au-dessus
                if col == '2':  # Case pour l'objectif
                    witch_tile = Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'witch', self.graphics['witch'])
                    witch_tile.discovered = False  # Rendre la witch invisible jusqu'à découverte

        # Position de spawn du joueur
        if player_spawn:
            self.player_spawn = player_spawn
            self.player = Player(player_spawn, [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites, self.visible_sprites, self.show_message, self.alert)
            self.spawn_enemies(layout, num_enemies=5)
        else:
            self.player_spawn = (100, 100)
            # Position par défaut si aucune position de spawn trouvée
            self.player = Player((100, 100), [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites, self.visible_sprites, self.alert)
            self.spawn_enemies(layout, num_enemies=5)

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
    
    # Dans la classe Level, ajoutez cette méthode
    # def spawn_enemies(self, layout, num_enemies=5):
    #     """Fait apparaître un certain nombre d'ennemis sur des cases marchables."""
    #     walkable_positions = []

    #     # Parcourir le layout pour trouver toutes les cases marchables
    #     for row_index, row in enumerate(layout):
    #         for col_index, col in enumerate(row):
    #             if col == '0' and self.is_surrounded_by_floor(layout, row_index, col_index):
    #                 x = col_index * TILESIZE
    #                 y = row_index * TILESIZE
    #                 walkable_positions.append((x, y))

    #     # Mélanger les positions pour garantir une répartition aléatoire
    #     random.shuffle(walkable_positions)

    #     # Faire apparaître les ennemis à partir des positions disponibles
    #     for _ in range(min(num_enemies, len(walkable_positions))):
    #         pos = walkable_positions.pop()  # Retirer une position pour éviter les doublons
    #         Enemy(pos, [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites, self.player)


    def spawn_enemies(self, layout, num_enemies=5):
        walkable_positions = []

        # Trouver les positions marchables
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == '0' and self.is_surrounded_by_floor(layout, row_index, col_index) and math.dist(self.player_spawn, (col_index * TILESIZE, row_index * TILESIZE)) > 200:
                    x = col_index * TILESIZE
                    y = row_index * TILESIZE
                    walkable_positions.append((x, y))

        random.shuffle(walkable_positions)

        # Sélectionner un ennemi aléatoire pour avoir la clé
        key_enemy_index = random.randint(0, min(num_enemies, len(walkable_positions)) - 1)

        for i in range(min(num_enemies, len(walkable_positions))):
            pos = walkable_positions.pop()
            has_key = (i == key_enemy_index)  # L'ennemi sélectionné a la clé
            Enemy(pos, [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites, self.player, has_key)

    def spawn_new_enemies(self):
        possible_spawns = []
        for sprite in self.visible_sprites:
                player_center = pygame.math.Vector2(self.player.rect.center)
                sprite_center = pygame.math.Vector2(sprite.rect.center)
                distance = player_center.distance_to(sprite_center)
                if getattr(sprite, 'sprite_type', None) == 'floor' and distance > 200:
                    possible_spawns.append(getattr(sprite, 'pos', None))
        if len(possible_spawns) > 0:
            pos = random.randint(0, len(possible_spawns))
            Enemy(possible_spawns[pos], [self.visible_sprites, self.obstacle_sprites], self.obstacle_sprites, self.player)

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
        pass
    
    def checkDeath(self):
        if self.player.health <= 0:
            return True
        else:
            return False

    def check_witch_interaction(self):
        """Vérifie si le joueur interagit avec la sorcière."""
        for sprite in self.obstacle_sprites:
            if getattr(sprite, 'sprite_type', None) == 'witch' and sprite.rect.colliderect(self.player.rect):
                if self.player.has_key:  # Vérifie si le joueur a une clé
                    self.player.has_witch = True
                    sprite.kill()  # Supprime le sprite witch après interaction
                    self.show_message("You saved the witch, time to get out fast !")
                    pygame.mixer.music.load("../audio/8bit Dungeon Boss.mp3")
                    pygame.mixer.music.play(-1)
                else:
                    self.show_message("You need a key kept by a guard to save the witch !")


    def check_victory(self):
        """Vérifie si le joueur peut terminer le niveau."""
        for sprite in self.obstacle_sprites:
            if getattr(sprite, 'sprite_type', None) == 'door' and sprite.rect.colliderect(self.player.rect):
                if self.player.has_witch:
                    self.show_message("You escaped like a pro !")
                    return True
                else:
                    self.show_message("Rather die than leave the prison without your loved one!")
                    return False
        return False


    def destroy_attack(self):
        print("Attaque du joueur détruite !")

    def create_magic(self, style, strength, cost):
        print(f"Magie {style} créée avec force {strength} et coût {cost}.")
    
    def run(self):
        """Exécute le niveau (mise à jour et dessin)."""
        
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        self.check_witch_interaction()
        self.check_victory()
        self.draw_message(self.visible_sprites.display_surface)
        current_time = pygame.time.get_ticks()
        if (current_time - self.newEnnemyTimer >= self.newEnnemy) & (self.player.has_witch == True):
            self.newEnnemyTimer = current_time
            self.spawn_new_enemies()


    def show_message(self, message):
        """Définit un message à afficher temporairement."""
        self.message = message
        self.message_timer = pygame.time.get_ticks()

    def draw_message(self, screen):
        """Affiche le message si le délai n'est pas expiré."""
        if self.message and pygame.time.get_ticks() - self.message_timer < self.message_duration:
            draw_message(screen, self.message, 30, (255, 255, 255), (WIDTH // 2, HEIGTH // 4))
        else:
            self.message = ""  # Efface le message après expiration

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
        # Calcul du décalage pour centrer la caméra sur le joueur
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # Premier passage : Dessiner les sols, murs, et tonneaux découverts
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'sprite_type', None) in ['floor', 'wall', 'barrel', 'witch'] and getattr(sprite, 'discovered', False):
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # Deuxième passage : Dessiner les ennemis uniquement s'ils sont sur une case découverte
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if isinstance(sprite, Enemy):
                # Vérifier si l'ennemi est sur une case découverte
                enemy_on_discovered_tile = any(
                    other.rect.colliderect(sprite.rect) and getattr(other, 'sprite_type', None) in ['floor', 'wall', 'barrel'] and getattr(other, 'discovered', None)
                    for other in self.sprites()
                )
                if enemy_on_discovered_tile:
                    offset_pos = sprite.rect.topleft - self.offset
                    offset_pos.y -= 6
                    self.display_surface.blit(sprite.image, offset_pos)
                    #sprite.display_weapon(self.display_surface, self.offset)

        # Troisième passage : Dessiner les autres éléments (joueur, bouclier, etc.)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if getattr(sprite, 'sprite_type', None) not in ['floor', 'wall', 'barrel', 'witch'] and not isinstance(sprite, Enemy):
                offset_pos = sprite.rect.topleft - self.offset
                if isinstance(sprite, Player):
                    offset_pos.y -= 6
                self.display_surface.blit(sprite.image, offset_pos)

        # Dessiner les armes et le bouclier du joueur
        # player.draw_weapon(self.display_surface, self.offset)
        player.draw_shield(self.display_surface, self.offset)
        

            

