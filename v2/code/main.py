import pygame, sys
from settings import *
from level import Level
from level2 import Level2
from level3 import Level3

class Game:
	def __init__(self):
		  
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH),pygame.DOUBLEBUF)
		pygame.display.set_caption('ELLIE KEMPER: 16-Bit Edition (v2)')
		pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))
		
		self.clock = pygame.time.Clock()
		self.level_num = 0
		self.levels = [Level(),Level2(),Level3()]
		# self.levels = [Level3()]
		self.level = self.levels[self.level_num]
		self.level.main_sound.play(loops=-1)
	 
	# this is the ultimate run "event loop" that consists of the actual game
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE: # restarting 
						self.level.main_sound.stop()
						if hasattr(self.level,'top_sound'):
							self.level.top_sound.stop()
						Game().run()
					if self.level.game_over:
						if event.key == pygame.K_r:
							self.level.restart_level()

			self.screen.fill('black')
			self.level.run()
			if self.level.level_complete_status:
				self.level_num += 1
				self.level = self.levels[self.level_num]
				self.level.main_sound.play(loops=-1)
				if self.level_num == 1:
					self.level.top_sound.play(loops=-1)
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()