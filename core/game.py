import pygame
from core.player import Player
from core.level import Level

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((250, 250))
        pygame.display.set_caption("Jeu d'infiltration")
        self.clock = pygame.time.Clock()
        self.player = Player([0, 0])
        self.level = Level(5)
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move("up")
                elif event.key == pygame.K_DOWN:
                    self.player.move("down")
                elif event.key == pygame.K_LEFT:
                    self.player.move("left")
                elif event.key == pygame.K_RIGHT:
                    self.player.move("right")

    def update(self):
        pass  # Ici tu peux ajouter de la logique comme les collisions

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.level.draw_grid(self.screen)
        self.player.draw(self.screen)
        self.level.draw_target(self.screen)
        pygame.display.flip()
