import pygame
from settings import *

class UI:
    def __init__(self):

        # general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)
        
        # bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.stamina_bar_rect = pygame.Rect(10,34,STAMINA_BAR_WIDTH,STAMINA_BAR_HEIGHT)

        # convert weapon dictionary into list of images
        self.weapon_graphics = []
        for weapon in weapon_data.values():
            path = weapon['graphic']
            weapon = pygame.image.load(path).convert_alpha()
            self.weapon_graphics.append(weapon)

    def show_bar(self,current,max_amount,bg_rect,color):
        # draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

        # drawing the bar
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,current_rect,3)    

    def selection_box(self,left,top,has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect = self.selection_box(10,630,has_switched)
        weapon_surface = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surface.get_rect(center = bg_rect.center)
        self.display_surface.blit(weapon_surface,weapon_rect)

    def display(self,player):
        if player.oversprinting_status:
            stamina_col = STAMINA_COLOR_OVERSPRINT
        else:
            stamina_col = STAMINA_COLOR
        self.show_bar(player.health,player.stats['health'],self.health_bar_rect,HEALTH_COLOR)
        self.show_bar(player.stamina,player.stats['stamina'],self.stamina_bar_rect,stamina_col) 
        self.weapon_overlay(player.weapon_index,not player.can_switch_weapon)
