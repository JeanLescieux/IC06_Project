import pygame
from core.settings import *
from core.player import Player
from core.level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jeu de Déplacement par Case")
        self.clock = pygame.time.Clock()
        self.running = True
        self.level = Level()
        self.game_over = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()  # Gestion des événements
            if not self.game_over:
                self.update()
            self.draw()

    def handle_events(self):
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Déléguer la gestion des touches au joueur
            self.level.player.handle_keypress(event)

    def update(self):
        self.level.update()
        if self.level.goal_reached:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)
        self.level.draw(self.screen)

        if self.game_over:
            self.show_victory_message()

        pygame.display.flip()

    def show_victory_message(self):
        font = pygame.font.SysFont(None, 55)
        text = font.render('Bravo !', True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))

    def quit(self):
        pygame.quit()
