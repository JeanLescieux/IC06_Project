import pygame, sys
from settings import *
from level import Level
from generation_csv import generate_and_save_csv  

class Game:
    def __init__(self):

        # Générer les fichiers CSV avant de commencer le jeu
        generate_and_save_csv()  # Appel à la fonction de génération

        # Setup général
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        pygame.display.set_caption('Zelda')
        self.clock = pygame.time.Clock()

        # Initialiser le niveau
        self.level = Level()

        # Son
        main_sound = pygame.mixer.Sound('../audio/main.ogg')
        main_sound.set_volume(0.5)
        main_sound.play(loops = -1)
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            # Couleur de fond (eau, par exemple)
            self.screen.fill(WATER_COLOR)

            # Logique et affichage du niveau
            self.level.run()

            # Mise à jour de l'affichage
            pygame.display.update()
            
            # Contrôle des FPS
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
