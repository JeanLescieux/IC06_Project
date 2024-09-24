import pygame
from core.settings import *

class Player:
    def __init__(self, x, y, level):
        # Position en termes de cases sur la grille
        self.grid_x = x
        self.grid_y = y
        self.image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.level = level  # Référence au niveau pour vérifier les murs
        self.update_position()

    def update_position(self):
        # Conversion des coordonnées de la grille en pixels pour l'affichage
        self.rect.topleft = (self.grid_x * TILE_SIZE, self.grid_y * TILE_SIZE)

    def handle_keypress(self, event):
        # Sauvegarder la position actuelle
        new_grid_x = self.grid_x
        new_grid_y = self.grid_y

        # On vérifie les événements de pression des touches
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:  # Haut
                new_grid_y -= 1
            if event.key == pygame.K_s:  # Bas
                new_grid_y += 1
            if event.key == pygame.K_q:  # Gauche
                new_grid_x -= 1
            if event.key == pygame.K_d:  # Droite
                new_grid_x += 1

        # Vérifier si la nouvelle position est un mur
        if not self.level.is_wall(new_grid_x, new_grid_y):
            # Si ce n'est pas un mur, mettre à jour la position
            self.grid_x = new_grid_x
            self.grid_y = new_grid_y

        # Mise à jour de la position en pixels pour l'affichage
        self.update_position()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
