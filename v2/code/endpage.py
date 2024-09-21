import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder
from random import choice
from weapon import Weapon
from math import sin
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from restart import Restart
from base_level_class import BaseLevel

class EndPage(BaseLevel):
    def __init__(self, health, in_dev_mode, num_of_people_who_found_arg):
        super().__init__(health, in_dev_mode)

        self.num_of_people_whove_found_this = num_of_people_who_found_arg

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
        self.end_page_num = 1
        self.start_time = pygame.time.get_ticks()
        
        self.get_dynamic_text()
        
        # Alpha values for crossfading
        self.current_alpha = 255
        self.next_alpha = 0
        # Crossfade duration and timer
        self.static_duration = 1500
        self.static_start_time = pygame.time.get_ticks()
        self.crossfade_duration = 1500  # in milliseconds
        self.crossfade_start_time = None
        self.bg_changing = False

        self.congrats_font = pygame.font.Font(SHERWOOD_FONT, 30)
        self.regular_text_font = pygame.font.Font(FUTURA_CONDENSED_BOLD, 15)
        self.header_text_font = pygame.font.Font(FUTURA_HEAVY_FONT, 22)
        self.notes_font = pygame.font.Font(FUTURA_CONDENSED, 18)
        self.enter_font = pygame.font.Font(FUTURA_CONDENSED_BOLD, 10)

    def get_dynamic_text(self):
        if self.num_of_people_whove_found_this == 0:
            self.number_modifier_text = 'st'
        elif self.num_of_people_whove_found_this == 1:
            self.number_modifier_text = 'nd'
        elif self.num_of_people_whove_found_this == 2:
            self.number_modifier_text = 'rd'
        else:
            self.number_modifier_text = 'th'

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

    def display_line_of_text(self, text, font_type, y):
        if font_type == 'regular':
            font = self.regular_text_font
        elif font_type == 'header':
            font = self.header_text_font
        elif font_type == 'congrats':
            font = self.congrats_font
        elif font_type == 'notes':
            font = self.notes_font
        else:
            font = self.notes_font
        text_surf = font.render(text, True, 'white')
        text_rect = text_surf.get_rect(center=(WIDTH//2, y))
        self.display_surface.blit(text_surf, text_rect)

    def check_for_input(self):
        if self.end_page_num == 1:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                self.end_page_num = 2

    def display_page_1(self):
        self.display_line_of_text('--- CONGRATULATIONS! ---', 'congrats', 20)
        self.display_line_of_text(f'You are the {self.num_of_people_whove_found_this+1}{self.number_modifier_text} person to reach what is', 'header', 50)
        self.display_line_of_text('currently the end of the Ellie Kemper ARG', 'header', 80)
        self.display_line_of_text('Please shoot me an email at ukuleleism7@gmail.com to claim your prize!', 'regular', 110)
        self.display_line_of_text('This game is currently a work-in-progress and has been in development', 'regular', 135)
        self.display_line_of_text('since January 2024, whenever I have free time to work on it', 'regular', 155)

        mission_statement_font = 'notes'
        mission_statement_y = 180
        mission_statement_buffer = 20
        self.display_line_of_text('My MO for art projects has historically consisted of "binging" in short bursts of', mission_statement_font,mission_statement_y)
        self.display_line_of_text("creativity that begin & end quickly. While I've thoroughly enjoyed and become very", mission_statement_font,mission_statement_y+(mission_statement_buffer*1))
        self.display_line_of_text("comfortable in this legacy approach, I've always wanted to learn how to not become", mission_statement_font,mission_statement_y+(mission_statement_buffer*2))
        self.display_line_of_text("so hastily bored of the process. Development of this game thus began as an attempt to", mission_statement_font,mission_statement_y+(mission_statement_buffer*3))
        self.display_line_of_text("create something that I could not realistically complete without continuously revisiting it.", mission_statement_font,mission_statement_y+(mission_statement_buffer*4))
        self.display_line_of_text("Throughout this new process, I have learned much about myself and how to establish", mission_statement_font,mission_statement_y+(mission_statement_buffer*5))
        self.display_line_of_text("short-term goals that bring me towards a longer-term vision, while not burning myself", mission_statement_font,mission_statement_y+(mission_statement_buffer*6))
        self.display_line_of_text("out so quickly in doing so. Thank you for supporting my art and I hope that you come", mission_statement_font,mission_statement_y+(mission_statement_buffer*7))
        self.display_line_of_text("back and replay the game while I continue to flesh it out into the totality of the vision.", mission_statement_font,mission_statement_y+(mission_statement_buffer*8))
        enter_surf = self.enter_font.render("ENTER ->",True,'white')
        enter_rect = enter_surf.get_rect(midleft=(585,343))
        if sin(pygame.time.get_ticks()/350) > 0 and (pygame.time.get_ticks() - self.start_time) > 5000:
            self.display_surface.blit(enter_surf,enter_rect)
    
    def display_page_2(self):
        self.display_line_of_text('Any level in the game can be revisited by simply typing', 'header', 50)
        self.display_line_of_text('in the level number on the start screen before hitting enter', 'header', 80)

        self.display_line_of_text('Furthermore, hitting Q while in the game turns on Dev mode, which enables invincibility and super speed', 'notes', 110)

        self.display_line_of_text('While I aim to keep this game a secret until it is fully complete,', 'regular', 230)
        self.display_line_of_text('please feel free to tell your friends about this game.', 'regular', 245)

        self.display_line_of_text('Thank you again for your support and for the time', 'regular', 280)
        self.display_line_of_text('you have taken to find and complete this game.', 'regular', 295)

        self.display_line_of_text('Peace & love, Jacob R West a.k.a c h point', 'header', 340)

    def display(self):
        self.crossfade()
        next_bg_surf = self.next_bg.copy()
        next_bg_surf.set_alpha(255)
        self.display_surface.blit(next_bg_surf, (0, 0))
        
        current_bg_surf = self.current_bg.copy()
        current_bg_surf.set_alpha(self.current_alpha)
        self.display_surface.blit(current_bg_surf, (0, 0))

        if self.end_page_num == 1:
            self.display_page_1()
        elif self.end_page_num == 2:
            self.display_page_2()

    def run(self):
        self.check_for_input()
        self.display()



