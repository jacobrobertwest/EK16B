import pygame
from random import randint

class Cloud(pygame.sprite.Sprite):  # Added Cloud class
    def __init__(self, groups):
        super().__init__(groups)
        self.randomized_cloud = randint(0,5)
        self.image = pygame.image.load(f'graphics/cloud/{self.randomized_cloud}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(-1000, randint(0, 1900)))
        self.speed = 1

    def update(self):
        self.rect.x += self.speed
        if self.rect.centerx > 4000:
            self.kill()