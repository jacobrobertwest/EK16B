import util
try:
    import pygame
except ImportError:
    util.import_or_install('pygame')

import sys
import os
from settings import *
from titlepage import TitlePage
from level import Level
from level2 import Level2
from level3 import Level3
from level4 import Level4
from endpage import EndPage
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
		self.health = 100

		self.music_start_time = None
		self.music_delay = 1000

	def create_level(self, level_num):
        # Dynamically create level based on level number
		levels = [TitlePage, Level, Level2, Level3, Level4, EndPage]
		if level_num < len(levels):
			return levels[level_num](self.health)
		return None
	 
	# this is the ultimate run "event loop" that consists of the actual game
	async def main(self):
		self.level = self.create_level(self.level_num)
		self.level.main_sound.play(loops=-1)
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
				if self.level_num > 0:
					self.health = self.level.player.health
				self.level_num += 1
				self.level = self.create_level(self.level_num)
				self.music_start_time = pygame.time.get_ticks()
				self.waiting_to_start = True
			if self.level_num > 0 and pygame.time.get_ticks() - self.music_start_time > self.music_delay and self.waiting_to_start:
				self.level.main_sound.play(loops=-1)
				if self.level_num == 2:
					self.level.top_sound.play(loops=-1)
				self.waiting_to_start = False
			pygame.display.update()
			self.clock.tick(FPS)
			await asyncio.sleep(0)

if __name__ == "__main__":
	asyncio.run(Game().main())


# TODO
# - Add "arsenic clouds" into level 4 that float by randomly from left to right of screen
# - add in 2 kinds of enemies to level 4