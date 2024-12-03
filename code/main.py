import pygame, sys
from settings import *
from level import Level
from generation_csv import generate_and_save_csv  

class Game:
	def __init__(self):
		pygame.mixer.init()
		pygame.mixer.music.load("../audio/8bit Dungeon Level.mp3")
		pygame.mixer.music.play(-1)

		generate_and_save_csv()
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Prison maze')
		self.clock = pygame.time.Clock()

		self.nLevel = 1
		self.alert = 0
		self.level = Level(self.alert)
		self.state = 'menu'

	def display_menu(self):
		"""Affiche le menu principal avec une phrase sur plusieurs lignes"""
		self.screen.fill('black')
		font_title = pygame.font.Font(None, 74)  # Police pour le titre
		font_text = pygame.font.Font(None, 36)  # Police pour le texte secondaire
		
		# Texte principal
		title_text = font_title.render('Prison Maze', True, 'white')
		
		# Texte secondaire découpé en plusieurs lignes
		instructions = [
			"Explore the labyrinth to retrieve the key",
			"and free the witch. Watch out for the guards,",
			"who may sound the alarm."
		]
		
		# Texte pour jouer
		play_text = font_title.render('Press SPACE to Play', True, 'gray')

		# Position du texte principal
		title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGTH // 6))

		# Position des instructions
		instruction_start_y = HEIGTH // 3
		instruction_lines = []
		for i, line in enumerate(instructions):
			rendered_line = font_text.render(line, True, 'white')
			line_rect = rendered_line.get_rect(center=(WIDTH // 2, instruction_start_y + i * 40))  # 40 pixels d'espacement
			instruction_lines.append((rendered_line, line_rect))
		
		# Position du texte pour jouer
		play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGTH // 1.5))

		# Dessiner tout le texte sur l'écran
		self.screen.blit(title_text, title_rect)
		for line_surface, line_rect in instruction_lines:
			self.screen.blit(line_surface, line_rect)
		self.screen.blit(play_text, play_rect)

	def next_level(self):
		self.nLevel += 1
		self.alert = self.level.player.alert
		self.level = Level(self.alert)  # Génère un nouveau niveau
		generate_and_save_csv()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				
				if self.state == 'menu' and event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:  # Lancer le jeu
						self.state = 'game'
			if self.state == 'menu':
				self.display_menu()
			elif self.state == 'game':
				self.screen.fill('black')
				self.level.run()
				if self.level.check_victory():
					self.next_level()
			pygame.display.update()
			self.clock.tick(FPS)




if __name__ == '__main__':
    GAME = Game()
    GAME.run()
