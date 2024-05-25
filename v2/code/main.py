import util
try:
    import pygame
except ImportError:
    util.import_or_install('pygame')

import sys
import os
from settings import *
from title import TitleScreen
from level import Level
from level2 import Level2
from level3 import Level3
from level4 import Level4
import asyncio

class Game:
	def __init__(self):
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH),pygame.DOUBLEBUF)
		pygame.display.set_caption('ELLIE KEMPER: 16-Bit Edition (v2)')
		pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))
		
		self.clock = pygame.time.Clock()
		self.level_num = 0
		self.levels = [Level(),Level2(),Level3(),Level4()]
		# self.levels = [Level4()]
		self.level = self.levels[self.level_num]
		self.level.main_sound.play(loops=-1)
	 
	# this is the ultimate run "event loop" that consists of the actual game
	async def main(self):
		title_screen = TitleScreen(self.screen, self.clock)
		title_screen.run()

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
							
			self.screen.fill(self.level.background)
			self.level.run()
			if self.level.level_complete_status:
				self.level_num += 1
				self.level = self.levels[self.level_num]
				self.levels[self.level_num-1] = None
				self.level.main_sound.play(loops=-1)
				if self.level_num == 1:
					self.level.top_sound.play(loops=-1)
			pygame.display.update()
			self.clock.tick(FPS)
			await asyncio.sleep(0)

if __name__ == "__main__":
	asyncio.run(Game().main())