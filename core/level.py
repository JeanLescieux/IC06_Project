import pygame
from core.player import Player
from core.settings import *

class Wall:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        # Charger l'image du mur
        self.image = pygame.image.load(WALL_SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        # Afficher le sprite du mur
        screen.blit(self.image, self.rect)

class Goal:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        # Charger l'image de l'objectif
        self.image = pygame.image.load(GOAL_SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        # Afficher le sprite de l'objectif
        screen.blit(self.image, self.rect)

class Level:
    def __init__(self):
        # Charger l'image de fond
        self.background_image = pygame.image.load(BACKGROUND_SPRITE).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (TILE_SIZE, TILE_SIZE))

        self.player = Player(2, 2, self)  # Position initiale du joueur dans la grille et référence au niveau

        # Création des murs
        self.walls = [
            Wall(5, 5),
            Wall(5, 6),
            Wall(5, 7)
        ]

        self.goal = Goal(10, 10)  # Position de l'objectif
        self.goal_reached = False

    def is_wall(self, x, y):
        # Vérifier si une case (x, y) est occupée par un mur
        for wall in self.walls:
            if wall.grid_x == x and wall.grid_y == y:
                return True
        return False

    def update(self):
        self.check_collisions()

    def check_collisions(self):
        # Vérification si le joueur atteint l'objectif
        if self.player.grid_x == self.goal.grid_x and self.player.grid_y == self.goal.grid_y:
            self.goal_reached = True

    def draw(self, screen):
        # Afficher le fond pour chaque case de la grille
        for y in range(SCREEN_HEIGHT // TILE_SIZE):
            for x in range(SCREEN_WIDTH // TILE_SIZE):
                screen.blit(self.background_image, (x * TILE_SIZE, y * TILE_SIZE))

        # Dessiner les murs
        for wall in self.walls:
            wall.draw(screen)

        # Dessiner l'objectif
        self.goal.draw(screen)

        # Dessiner le joueur
        self.player.draw(screen)
