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

class TitlePage:
    def __init__(self,health):
        self.display_surface = pygame.display.get_surface()
        self.title_image = pygame.image.load('graphics/title.png')  # Path to your title screen image
        self.main_sound = pygame.mixer.Sound('audio/4.ogg')
        self.main_sound.set_volume(0.3)
        self.game_over = False
        self.chosen_level = 0
        self.level_complete_status = False
        self.background = 'black'
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.level_complete_status = True
            self.main_sound.stop()
        if keys[pygame.K_1]:
            self.chosen_level = 0
        if keys[pygame.K_2]:
            self.chosen_level = 1
        if keys[pygame.K_3]:
            self.chosen_level = 2
        if keys[pygame.K_4]:
            self.chosen_level = 3
        if keys[pygame.K_5]:
            self.chosen_level = 4

    def display(self):
        self.display_surface.blit(self.title_image, (0, 0))
        updated_surf = self.font.render(" v2.1.1 - Last Updated: 7/21/24", False, "white")
        updated_rect = updated_surf.get_rect(center=(100,20))
        self.display_surface.blit(updated_surf,updated_rect)

    def run(self):
        self.input()
        self.display()

