import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from restart import Restart
from base_level_class import BaseLevel
from debug import debug

class EndPage(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)
        self.title_image = pygame.image.load('graphics/end.png')  # Path to your title screen image
        self.main_sound = pygame.mixer.Sound('audio/4.ogg')
        self.main_sound.set_volume(0.3)
        self.game_over = False
        self.level_complete_status = False
        self.background = 'black'

    def display(self):
        self.display_surface.blit(self.title_image, (0, 0))
        debug("Any specific level can be revisited by typing the level number on the game start screen before pressing enter.",x=25,y=102,font_size=17,bg=None)
        pygame.display.update()

    def run(self):
        self.display()

