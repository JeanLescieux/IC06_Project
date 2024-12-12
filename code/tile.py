import pygame
import random
import Sprite_sheet as ss
from settings import TILESIZE, HITBOX_OFFSET

# classifier les sprites
left_side_bricks = [ss.sprite_Brick3, ss.sprite_Brick4]
right_side_bricks = [ss.sprite_Brick3_mirror, ss.sprite_Brick4_mirror]
top_side_bricks = [ss.sprite_Brick1, ss.sprite_Brick2, ss.sprite_Brick1_mirror, ss.sprite_Brick2_mirror,
                   ss.sprite_Brick5]
down_side_bricks = [ss.sprite_Brick1, ss.sprite_Brick2, ss.sprite_Brick1_mirror, ss.sprite_Brick2_mirror,
                    ss.sprite_Brick6]
wall_sprites = [ss.sprite_Wall3,ss.sprite_Wall4]
floors = [ss.sprite_Floor2, ss.sprite_Floor3]
weights_floors = [0.05, 0.95]
corners = [ss.sprite_Brick1, ss.sprite_Brick2, ss.sprite_Brick1_mirror, ss.sprite_Brick2_mirror,ss.sprite_Brick4,ss.sprite_Brick4_mirror]
Decos_2x2 = [ss.sprite_TreasureBox_Empty,ss.sprite_TreasureBox_Full,ss.sprite_TreasureBox_Close,]


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=None, size=None):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.discovered = False
        self.pos = pos
        # Load the image based on sprite type
        if surface:
            self.image = surface
        else:
            if sprite_type == 'water':
                self.image = pygame.image.load('../graphics/tilemap/eau.png').convert_alpha()
            elif sprite_type == 'wall':
                self.image = pygame.image.load('../graphics/tilemap/mur.png').convert_alpha()
            elif sprite_type == 'floor':
                self.image = random.choices(floors, weights=weights_floors, k=1)[0]
            elif sprite_type == 'left_side_bricks':
                self.image = random.choice(left_side_bricks)
            elif sprite_type == 'right_side_bricks':
                self.image = random.choice(right_side_bricks)
            elif sprite_type == 'top_side_bricks':
                self.image = random.choice(top_side_bricks)
            elif sprite_type == 'down_side_bricks':
                self.image = random.choice(down_side_bricks)
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
