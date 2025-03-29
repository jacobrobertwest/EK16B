import pygame
from settings import *
from debug import debug
from random import choice
from math import sin
from base_level_class import BaseLevel

class TitlePage(BaseLevel):
    def __init__(self,health,in_dev_mode,metadata):
        super().__init__(health,in_dev_mode)
        self.metadata = metadata
        # self.title_image = pygame.image.load('graphics/title.png') 
        self.bg_img_1 = pygame.image.load('graphics/titlepage/bg1.png')
        self.bg_img_2 = pygame.image.load('graphics/titlepage/bg2.png')
        self.bg_img_3 = pygame.image.load('graphics/titlepage/bg3.png')
        self.bg_img_list = [self.bg_img_1, self.bg_img_2, self.bg_img_3]

        self.button_press_buffer = 200
        self.most_recent_button_press_time = pygame.time.get_ticks()

        # self.logo_img = pygame.image.load('graphics/titlepage/logo_overlay.png')
        self.logo_img_text = pygame.image.load('graphics/titlepage/logo_overlay_text.png')
        self.logo_img_fractal = pygame.image.load('graphics/titlepage/logo_overlay_fractal.png')
        # self.bg_img_list = [1,2,3]
        self.current_bg = choice(self.bg_img_list)
        self.next_bg = self.get_next_bg()
        
        # Alpha values for crossfading
        self.current_alpha = 255
        self.next_alpha = 0
        self.rotation = 0

        # Crossfade duration and timer
        self.static_duration = 1500
        self.static_start_time = pygame.time.get_ticks()
        self.crossfade_duration = 1500  # in milliseconds
        self.crossfade_start_time = None
        self.bg_changing = False

        self.main_sound = pygame.mixer.Sound('audio/title.ogg')
        self.main_sound.set_volume(0.3)
        self.game_over = False
        self.chosen_level = 0
        self.level_complete_status = False
        self.mode_at_start = in_dev_mode
        self.background = 'black'
        self.font = pygame.font.Font(None,23)
        self.notes_font = pygame.font.Font(FUTURA_CONDENSED,16)
        self.instructions_font = pygame.font.Font(FUTURA_FONT,20)
        self.brought_font = pygame.font.Font(FUTURA_FONT,16)
        self.enter_font = pygame.font.Font(FUTURA_CONDENSED_BOLD,22)
        self.hopping_levels = False
        self.rotation_delay = 5000
        self.start_time = pygame.time.get_ticks()


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
 
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.level_complete_status = True
            self.main_sound.stop()
        if pygame.time.get_ticks() - self.most_recent_button_press_time > self.button_press_buffer:
            if self.chosen_level in (0,2,3,4,5,6,7,8,9):
                if keys[pygame.K_1]:
                    self.chosen_level = 1
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_2]:
                    self.chosen_level = 2
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_3]:
                    self.chosen_level = 3
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_4]:
                    self.chosen_level = 4
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_5]:
                    self.chosen_level = 5
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_6]:
                    self.chosen_level = 6
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_7]:
                    self.chosen_level = 7
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_8]:
                    self.chosen_level = 8
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_9]:
                    self.chosen_level = 9
                    self.most_recent_button_press_time = pygame.time.get_ticks()
            elif self.chosen_level == 1:
                if keys[pygame.K_0]:
                    self.chosen_level = 10
                    self.most_recent_button_press_time = pygame.time.get_ticks()
                if keys[pygame.K_1]:
                    self.chosen_level = 11
                    self.most_recent_button_press_time = pygame.time.get_ticks()

        if keys[pygame.K_BACKSPACE]:
            self.chosen_level = 0

        if self.chosen_level > 0:
            self.hopping_levels = True
        else:
            self.hopping_levels = False

    def display(self):
        self.crossfade()
        next_bg_surf = self.next_bg.copy()
        next_bg_surf.set_alpha(255)
        self.display_surface.blit(next_bg_surf, (0, 0))

        current_bg_surf = self.current_bg.copy()
        current_bg_surf.set_alpha(self.current_alpha)
        self.display_surface.blit(current_bg_surf, (0, 0))

        logo_img_fractal_rotated = pygame.transform.rotate(self.logo_img_fractal, self.rotation % 360)
        rotated_rect = logo_img_fractal_rotated.get_rect(center=(159, 142))
        
        self.display_surface.blit(self.logo_img_text, (254, -30))
        self.display_surface.blit(logo_img_fractal_rotated, rotated_rect)
        # self.display_surface.blit(self.logo_img_fractal, (65, 48))
        # print(self.logo_img_fractal.get_rect().center)

        # self.display_surface.blit(self.logo_img, (0, -30))

        updated_surf = self.notes_font.render(f"v{self.metadata['version']} - LAST UPDATED: {self.metadata['updated']}  |  PLAYABLE LEVELS: {self.metadata['lvls']} ", True, "white",True)
        updated_rect = updated_surf.get_rect(midleft=(10,20))
        bg_rect = updated_surf.get_rect(midleft = (10,20))
        pygame.draw.rect(self.display_surface,'Black',bg_rect)
        move_surf = self.instructions_font.render("MOVE - Arrow Keys",True,(243,233,252))
        sprint_surf = self.instructions_font.render("SPRINT - L Shift",True,(243,233,252))
        slash_surf = self.instructions_font.render("SLASH - Space",True,(243,233,252))
        shield_surf = self.instructions_font.render("SHIELD - C",True,(243,233,252))
        interact_surf = self.instructions_font.render("INTERACT - D",True,(243,233,252))
        brought_by_surf = self.brought_font.render("Brought to you by C H POINT",True,(243,233,252))
        move_rect = move_surf.get_rect(midleft=(95,250))
        sprint_rect = sprint_surf.get_rect(midleft=(95,272))
        slash_rect = slash_surf.get_rect(midleft=(95,294))
        shield_rect = shield_surf.get_rect(midleft=(95,316))
        interact_rect = interact_surf.get_rect(midleft=(95,338))
        brought_by_rect = brought_by_surf.get_rect(center=(400,225))

        pygame.draw.rect(self.display_surface,'Black',bg_rect)
        self.display_surface.blit(updated_surf,updated_rect)
        self.display_surface.blit(move_surf,move_rect)
        self.display_surface.blit(sprint_surf,sprint_rect)
        self.display_surface.blit(slash_surf,slash_rect)
        self.display_surface.blit(shield_surf,shield_rect)
        self.display_surface.blit(interact_surf,interact_rect)

        enter_surf = self.enter_font.render("< PRESS ENTER TO BEGIN >",True,(243,233,252))
        enter_rect = enter_surf.get_rect(center=(400,294))
        self.display_surface.blit(brought_by_surf,brought_by_rect)
        if sin(pygame.time.get_ticks()/350) > 0:
            self.display_surface.blit(enter_surf,enter_rect)

        if pygame.time.get_ticks() - self.start_time > self.rotation_delay:
            self.rotation -= 0.25
            if self.rotation <= -36000:
                self.rotation = 0

    def run(self):
        self.input()
        self.display()
        # debug(self.rotation,x=10,y=300)
        if self.hopping_levels:
            debug(f'LVL:{self.chosen_level}',x=410,y=330,font_size=20)

