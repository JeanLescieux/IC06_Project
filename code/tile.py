import pygame
from settings import TILESIZE, HITBOX_OFFSET

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None, size=None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.discovered = False
        # Load the image based on sprite type
        if surface:
            self.image = surface
        else:
            if sprite_type == 'water':
                self.image = pygame.image.load('../graphics/tilemap/eau.png').convert_alpha()
            elif sprite_type == 'wall':
                self.image = pygame.image.load('../graphics/tilemap/mur.png').convert_alpha()
            elif sprite_type == 'floor':
                self.image = pygame.image.load('../graphics/tilemap/sol.png').convert_alpha()
            else:
                raise ValueError(f"Unknown sprite_type '{sprite_type}' provided for tile.")

        # Resize the image if a custom size is provided
        if size:
            self.image = pygame.transform.scale(self.image, size)
        else:
            self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE))
        
        self.rect = self.image.get_rect(topleft=pos)
        y_offset = HITBOX_OFFSET.get(sprite_type, 0)
        self.hitbox = self.rect.inflate(0, y_offset)
