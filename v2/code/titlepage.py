import pygame
from settings import *
from debug import debug
from base_level_class import BaseLevel

class TitlePage(BaseLevel):
    def __init__(self,health,in_dev_mode,metadata):
        super().__init__(health,in_dev_mode)
        self.metadata = metadata
        self.title_image = pygame.image.load('graphics/title.png') 
        self.main_sound = pygame.mixer.Sound('audio/4.ogg')
        self.main_sound.set_volume(0.3)
        self.game_over = False
        self.chosen_level = 0
        self.level_complete_status = False
        self.mode_at_start = in_dev_mode
        self.background = 'black'
        self.font = pygame.font.Font(None,23)
        self.notes_font = pygame.font.Font(None,16)
        self.hopping_levels = False

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.level_complete_status = True
            self.main_sound.stop()
        if keys[pygame.K_1]:
            self.chosen_level = 1
        if keys[pygame.K_2]:
            self.chosen_level = 2
        if keys[pygame.K_3]:
            self.chosen_level = 3
        if keys[pygame.K_4]:
            self.chosen_level = 4
        if keys[pygame.K_5]:
            self.chosen_level = 5
        if keys[pygame.K_6]:
            self.chosen_level = 6
        if keys[pygame.K_7]:
            self.chosen_level = 7
        if keys[pygame.K_8]:
            self.chosen_level = 8

        if self.chosen_level > 0:
            self.hopping_levels = True

    def display(self):
        self.display_surface.blit(self.title_image, (0, 0))
        updated_surf = self.notes_font.render(f"v{self.metadata['version']} - Last Updated: {self.metadata['updated']}  |  Playable Levels: {self.metadata['lvls']}", False, "white",True)
        updated_rect = updated_surf.get_rect(midleft=(10,20))
        bg_rect = updated_surf.get_rect(midleft = (10,20))
        pygame.draw.rect(self.display_surface,'Black',bg_rect)
        d = self.notes_font.render(" / Interact", False, "white",True)
        # updated_rect = updated_surf.get_rect(midleft=(10,20))
        # bg_rect = updated_surf.get_rect(midleft = (10,20))
        pygame.draw.rect(self.display_surface,'Black',bg_rect)
        self.display_surface.blit(updated_surf,updated_rect)

    def run(self):
        self.input()
        self.display()
        if self.hopping_levels:
            debug(f'LVL:{self.chosen_level}',x=410,y=330,font_size=20)

