import pygame
import os

class Player:
    def __init__(self, start_pos):
        # Charger l'image du joueur
        self.image = pygame.image.load(os.path.join("assets", "sprites", "test.png")).convert_alpha()

        # Redimensionner l'image pour qu'elle ne dépasse pas la taille de la case
        self.image = pygame.transform.scale(self.image, (40, 40))  # Taille légèrement inférieure à 50x50

        # Ajuster le rect pour suivre les mouvements du joueur
        self.rect = self.image.get_rect()
        self.rect.topleft = (start_pos[0] * 50 + 5, start_pos[1] * 50 + 5)  # Centré dans une case de 50x50

    def move(self, direction):
        if direction == "up":
            self.rect.y -= 50
        elif direction == "down":
            self.rect.y += 50
        elif direction == "left":
            self.rect.x -= 50
        elif direction == "right":
            self.rect.x += 50

    def draw(self, screen):
        # Afficher l'image du joueur sur l'écran
        screen.blit(self.image, self.rect)
