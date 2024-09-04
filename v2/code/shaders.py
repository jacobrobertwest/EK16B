import pygame
from settings import *
from support import import_folder
from random import choice, randint

class Shaders(pygame.sprite.Sprite):
    def __init__(self,pos,groups,shader_type,speed=0.1,randomize=False,fade=False,full_alpha_duration=1000):
        super().__init__(groups)
        self.frames = import_folder(f'graphics/particles/{shader_type}')
        self.frame_index = 0
        self.animation_speed = speed
        self.image = self.frames[self.frame_index]
        self.alpha = 255
        self.rect = self.image.get_rect(center = pos)
        self.fade = False
        if randomize:
            self.reflect = choice([True,False])
            self.rotate = choice([0,90,180,270])
        else:
            self.reflect = False
            self.rotate = 0

        if fade:
            self.fade = True
            self.is_fading_in = True
            self.is_full_alpha = False
            self.is_fading_out = False
            self.full_alpha_duration = full_alpha_duration
            self.full_alpha_start_time = None
            self.alpha = 0
            if randomize:
                self.random_adder = randint(0,750)
                self.random_multiplier = round(1 / randint(1, 6),3)
            else:
                self.random_adder = 0
                self.random_multiplier = 1


    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        if self.reflect:
            self.image = pygame.transform.flip(self.image,True,False)
        elif self.rotate:
            self.image = pygame.transform.rotate(self.image,self.rotate)

    def update(self):
        self.animate()
        if self.fade:
            if self.is_fading_in:
                if self.alpha < 255:
                    self.alpha += (0.5 * self.random_multiplier)
                    self.image.set_alpha(int(self.alpha))
                if self.alpha == 255:
                    self.is_fading_in = False
                    self.is_full_alpha = True
                    self.full_alpha_start_time = pygame.time.get_ticks()
            elif self.is_full_alpha:
                self.alpha = 255
                if pygame.time.get_ticks() - self.full_alpha_start_time > (self.full_alpha_duration + self.random_adder):
                    self.is_full_alpha = False
                    self.is_fading_out = True
            elif self.is_fading_out:
                if self.alpha > 0:
                    self.alpha -= (0.5 * self.random_multiplier)
                    self.image.set_alpha(int(self.alpha))
                else:
                    # print('despawned')
                    self.kill()
