import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH),pygame.DOUBLEBUF)
		pygame.display.set_caption('ELLIE KEMPER: 16-Bit Edition (v1)')
		pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))

		self.clock = pygame.time.Clock()
		self.level = Level()

		# sound
		main_sound = pygame.mixer.Sound('audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops = -1)
	 
	# this is the ultimate run "event loop" that consists of the actual game
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()
					if self.level.game_over:
						if event.key == pygame.K_r:
							self.level.restart_level()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()