import pygame
from settings import *

class Restart:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

    def display(self):
        self.display_surface.fill('black')
        game_over_surf = self.font.render('GAME OVER',False,'red')
        game_over_rect = game_over_surf.get_rect(center = (WIDTH/2,HEIGTH/2))
        press_r_surf = self.font.render('Press R to Restart',False,'red')
        press_r_rect = press_r_surf.get_rect(midtop = game_over_rect.midbottom)
        self.display_surface.blit(game_over_surf,game_over_rect)
        self.display_surface.blit(press_r_surf,press_r_rect)