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

class EndPage2(BaseLevel):

    def __init__(self, health, in_dev_mode):
        super().__init__(health, in_dev_mode)
        self.bg_img_1 = pygame.image.load('graphics/titlepage/bg1.png')
        self.bg_img_2 = pygame.image.load('graphics/titlepage/bg2.png')
        self.bg_img_3 = pygame.image.load('graphics/titlepage/bg3.png')
        self.bg_img_list = [self.bg_img_1, self.bg_img_2, self.bg_img_3]
        self.main_sound = pygame.mixer.Sound('audio/4.ogg')
        self.main_sound.set_volume(0.3)
        self.game_over = False
        self.level_complete_status = False
        self.background = 'black'
        self.current_bg = choice(self.bg_img_list)
        self.next_bg = self.get_next_bg()
        
        # Alpha values for crossfading
        self.current_alpha = 255
        self.next_alpha = 0
        # Crossfade duration and timer
        self.static_duration = 1500
        self.static_start_time = pygame.time.get_ticks()
        self.crossfade_duration = 1500  # in milliseconds
        self.crossfade_start_time = None
        self.bg_changing = False

    def get_next_bg(self):
        remaining_bgs = [bg for bg in self.bg_img_list if bg != self.current_bg]
        return choice(remaining_bgs)

    def crossfade(self):
        if self.static_start_time is not None:
            static_elapsed_time = pygame.time.get_ticks() - self.static_start_time
            if static_elapsed_time >= self.static_duration and not self.bg_changing:
                self.static_start_time = None
                self.bg_changing = True
                self.crossfade_start_time = pygame.time.get_ticks()
        elif self.crossfade_start_time is not None:
            crossfade_elapsed_time = pygame.time.get_ticks() - self.crossfade_start_time
            if crossfade_elapsed_time >= self.crossfade_duration and self.bg_changing:
                self.crossfade_start_time = None
                self.bg_changing = False
                self.static_start_time = pygame.time.get_ticks()
                self.current_bg = self.next_bg
                self.next_bg = self.get_next_bg()
                self.current_alpha = 255
                self.next_alpha = 0
            else:
                fade_ratio = crossfade_elapsed_time / self.crossfade_duration
                self.current_alpha = int(255*(1-fade_ratio))
                self.next_alpha = int(255*fade_ratio)

    def display(self):
        self.crossfade()
        next_bg_surf = self.next_bg.copy()
        next_bg_surf.set_alpha(255)
        self.display_surface.blit(next_bg_surf, (0, 0))

        current_bg_surf = self.current_bg.copy()
        current_bg_surf.set_alpha(self.current_alpha)
        self.display_surface.blit(current_bg_surf, (0, 0))

    def run(self):
        self.display()



