import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('ELLIE KEMPER: 16-Bit Edition (v1)')
		pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))
		self.clock = pygame.time.Clock()
		
		self.level = Level()
	
	# this is the ultimate run "event loop" that consists of the actual game
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()