import pygame
from settings import TILESIZE

class Key(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/donjon/Key.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.copy()  # Ajouter un hitbox (même taille que le rectangle)
