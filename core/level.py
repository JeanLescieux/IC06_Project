import random
import pygame

class Level:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cell_size = 50
        self.target_pos = [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]

    def draw_grid(self, screen):
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                rect = pygame.Rect(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    def draw_target(self, screen):
        target_rect = pygame.Rect(self.target_pos[1] * self.cell_size, self.target_pos[0] * self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, (0, 0, 0), target_rect)
