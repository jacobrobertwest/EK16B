import pygame
from settings import *
from math import sin
from debug import debug

class DialogBox:
    def __init__(self, message,font=None,time_before_prompt=1000):
        self.message = message
        self.font = pygame.font.Font(font, 36)  
        self.text_surface = self.font.render(self.message, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(WIDTH / 2, HEIGTH / 2))

        self.created_time = pygame.time.get_ticks()
        self.time_before_prompt = time_before_prompt
        self.prompting = False
        self.prompt_font = pygame.font.Font(None,18)
        self.prompt_surface = self.prompt_font.render('> ENTER <',True,(255,255,255))
        self.prompt_rect = self.prompt_surface.get_rect(midright = (WIDTH - 10, HEIGTH - 10))

    def check_if_prompt_should_launch(self):
        if pygame.time.get_ticks() - self.created_time >= self.time_before_prompt:
            self.prompting = True

    def update_prompt_alpha(self):
        sin_value = sin(pygame.time.get_ticks()/250)
        if sin_value > 0:
            alpha = 255
        else:
            alpha = 0
        self.prompt_surface.set_alpha(alpha)

    def show(self):
        screen = pygame.display.get_surface()
        screen.blit(self.text_surface, self.text_rect)
        if not self.prompting:
            self.check_if_prompt_should_launch()
        if self.prompting:
            self.update_prompt_alpha()
            screen.blit(self.prompt_surface, self.prompt_rect)
        pygame.display.update()
