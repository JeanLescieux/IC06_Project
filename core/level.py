import pygame
from core.settings import *
from core.player import Player

class Wall:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Goal:
    def __init__(self, x, y):
        self.grid_x = x
        self.grid_y = y
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect)  # L'objectif est un carré vert

class Level:
    def __init__(self):
        self.player = Player(2, 2, self)  # Position initiale du joueur dans la grille et référence au niveau

        # Création des murs
        self.walls = [
            Wall(5, 5),  # Un mur en position (5, 5)
            Wall(5, 6),  # Un mur en position (5, 6)
            Wall(5, 7)   # Un mur en position (5, 7)
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
        # Dessiner les murs
        for wall in self.walls:
            wall.draw(screen)

        # Dessiner l'objectif
        self.goal.draw(screen)

        # Dessiner le joueur
        self.player.draw(screen)
