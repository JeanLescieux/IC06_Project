import pygame, sys
from settings import *
from level import Level
from generation_csv import generate_and_save_csv


def load_animation_frames(path, size):
    frames = []
    for i in range(0, 6):
        image = pygame.image.load(f'../graphics/player/down/down_{i}.png').convert_alpha()
        scaled_image = pygame.transform.scale(image, size=(220,220))  # 调整大小
        frames.append(scaled_image)
    return frames


class Game:
	def __init__(self):
		pygame.mixer.init()
		pygame.mixer.music.load("../audio/8bit Dungeon Level.mp3")
		pygame.mixer.music.play(-1)
		
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
		pygame.display.set_caption('Prison maze')
		self.clock = pygame.time.Clock()

		self.nLevel = 1
		self.alert = 0
		self.state = 'menu'
		self.tutorial_start_time = None

		# download
		self.light_image = pygame.image.load('../graphics/light.png').convert_alpha()
		self.light_image = pygame.transform.scale(self.light_image, (400, 400))

		# Running animation
		self.animation_frames = load_animation_frames('../graphics/animation', (200, 200))
		self.current_frame_index = 0
		self.last_animation_time = pygame.time.get_ticks()
		self.animation_interval = 100


	def create_light_surface(self, radius, color, alpha):
		"""Create a circular light surface with gradient transparency."""
		light_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
		for i in range(radius, 0, -1):
			intensity = int(alpha * (i / radius))
			pygame.draw.circle(light_surface, (*color, intensity), (radius, radius), i)
		return light_surface

	def display_menu(self):
		"""Display the main menu with light following the mouse."""
		background_image = pygame.image.load('../graphics/Menu.png')
		background_image = pygame.transform.scale(background_image, (WIDTH, HEIGTH))
		self.screen.blit(background_image, (0, 0))

		# self.screen.fill('black')
		font_title = pygame.font.Font(None, 50)

		# Running Animation
		current_time = pygame.time.get_ticks()
		if current_time - self.last_animation_time >= self.animation_interval:
			self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames)
			self.last_animation_time = current_time

		animation_frame = self.animation_frames[self.current_frame_index]
		animation_rect = animation_frame.get_rect(center=(WIDTH // 2, HEIGTH // 1.8))
		self.screen.blit(animation_frame, animation_rect)

		# light following the mouse
		mouse_x, mouse_y = pygame.mouse.get_pos()
		light_rect = self.light_image.get_rect(center=(mouse_x, mouse_y))
		self.screen.blit(self.light_image, light_rect)

		current_time = pygame.time.get_ticks()
		blink_interval = 500
		if (current_time // blink_interval) % 2 == 0:
			play_text = font_title.render('Press SPACE to Continue', True, 'gray')
			play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGTH // 1.1))
			self.screen.blit(play_text, play_rect)

	def display_tutorial(self):
		"""Display tutorial page"""
		background_image = pygame.image.load('../graphics/tutorial.png')
		background_image = pygame.transform.scale(background_image, (WIDTH, HEIGTH))
		self.screen.blit(background_image, (0, 0))

		font_text = pygame.font.Font(None, 36)
		current_time = pygame.time.get_ticks()
		blink_interval = 500
		if (current_time // blink_interval) % 2 == 0:
			play_text = font_text.render('Press SPACE to Skip', True, 'gray')
			play_rect = play_text.get_rect(center=(WIDTH // 1.15, HEIGTH // 1.05))
			self.screen.blit(play_text, play_rect)

	def display_game_over(self):
		"""Display Game Over Page"""
		background_image = pygame.image.load('../graphics/Game_over.png')
		background_image = pygame.transform.scale(background_image, (WIDTH, HEIGTH))
		self.screen.blit(background_image, (0, 0))

		font_title = pygame.font.Font(None, 50)
		current_time = pygame.time.get_ticks()
		blink_interval = 500
		if (current_time // blink_interval) % 2 == 0:
			play_text = font_title.render('Press SPACE to Restart or Press Down to Quit', True, 'gray')
			play_rect = play_text.get_rect(center=(WIDTH // 2, HEIGTH // 1.1))
			self.screen.blit(play_text, play_rect)



	def next_level(self):
		self.nLevel += 1
		self.alert = self.level.player.alert
		generate_and_save_csv()
		self.level = Level(self.alert)  # Generate a new level

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if self.state == 'menu' and event.key == pygame.K_SPACE:
						self.state = 'tutorial'
						self.tutorial_start_time = pygame.time.get_ticks()

					elif self.state == 'tutorial' and event.key == pygame.K_SPACE:
						self.state = 'game'
						generate_and_save_csv()
						self.level = Level(0)

					elif self.state == 'game_over' and event.key == pygame.K_SPACE:
						self.state = 'game'
						generate_and_save_csv()
						self.level = Level(0)

					elif self.state == 'game_over' and event.key == pygame.K_DOWN:
						pygame.quit()
						sys.exit()


			if self.state == 'menu':
				self.display_menu()

			elif self.state == 'tutorial':
				self.display_tutorial()
				if pygame.time.get_ticks() - self.tutorial_start_time > 20000: # Display 20s
					self.state = 'game'
					generate_and_save_csv()
					self.level = Level(0)

			elif self.state == 'game':
				self.screen.fill('black')
				self.level.run()
				draw_text(self.screen, f'Levels Completed  {self.nLevel - 1}', font_size=30, color=(131, 67, 51))
				if self.level.check_victory():
					self.next_level()
				if self.level.checkDeath():
					self.state = 'game_over'

			elif self.state == 'game_over':
				self.display_game_over()

			pygame.display.update()
			self.clock.tick(FPS)

def draw_text(screen, text, font_size=24, color=(255, 255, 255)):
    """Affiche un texte centré en haut de l'écran."""
    font = pygame.font.Font(FONT_PATH, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGTH // 20))  # Position centré en haut
    screen.blit(text_surface, text_rect)


if __name__ == '__main__':
	GAME = Game()
	GAME.run()


