import util
try:
    import pygame
except ImportError:
    util.import_or_install('pygame')
import sys
import os
from settings import *
from titlepage import TitlePage
from level import Level1
from level2 import Level2
from level3 import Level3
from level4 import Level4
from level5 import Level5
from level6 import Level6
from level7 import Level7
from level8 import Level8
from level9 import Level9
from level10 import Level10
from endpage import EndPage
from level_fairyfountain import FairyFountain
import asyncio

VERSION = "2.4.2"
LAST_UPDATED_DATE = "3/29/25"
MASTER_LEVEL_LIST = [TitlePage, Level1, Level2, Level3, Level4, Level5, Level6, Level7, Level8, Level9, Level10, EndPage]
# MASTER_LEVEL_LIST = [Level10]
PLAYABLE_LEVELS = len(MASTER_LEVEL_LIST) - 2
METADATA = {
	"version":VERSION,
	"updated":LAST_UPDATED_DATE,
	"lvls":PLAYABLE_LEVELS,
	"finderCount":0
}

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH),pygame.DOUBLEBUF)
		pygame.display.set_caption('The Legend of Ellie Kemper - v' + VERSION)
		pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))
		
		self.clock = pygame.time.Clock()
		self.level_num = 0
		self.health = 100
		self.in_dev_mode = False
		self.music_start_time = None
		self.music_delay = 750

	def create_level(self, level_num):
		levels = MASTER_LEVEL_LIST
		if level_num < len(levels):
			level_class = levels[level_num]
			if level_class == TitlePage:
				return level_class(self.health, self.in_dev_mode, METADATA)
			elif level_class == EndPage:
				return level_class(self.health, self.in_dev_mode, METADATA["finderCount"])
			else:
				return level_class(self.health, self.in_dev_mode)
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
						Game().main()
						self.level.main_sound.play(loops=-1)
					if self.level.game_over:
						if event.key == pygame.K_r:
							self.level.restart_level()

			self.screen.fill(self.level.background)
			self.level.run()
			if self.level.level_complete_status:
				if self.level_num > 0:
					self.health = self.level.player.health
					self.in_dev_mode = self.level.player.in_dev_mode
				else:
					if self.level.chosen_level == 0:
						self.level_num = 0
					else:
						self.level_num = self.level.chosen_level - 1
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
# technical debt / glitches - shot aiming for shooting enemy is off
# Overall - add scoring system, add pausing system, breakable grass & boxes, better collision boundaries, figure out angled boundaries
#           make it so that if player goes too far away from starting point, it moves them back to starting point
# Level 1 - move boulders more overlapping the edge of the boundary & path
# Level 2 - make forest exterior overlaying everything
# Level 3 - 
# Level 4 - finish water particle effects, make enemies shake when they collide with something
# Level 5 - make it difficult to run against the wind, easier to run with, add water particle effects
# Level 6 - make moon actually waning
# Level 7 - dialogue box artwork, add more dialogue, ruins artwork, another room?, torch mechanics
# Level 8 - add in deku babas, add artwork
# Level 9 - 
# End Page - 