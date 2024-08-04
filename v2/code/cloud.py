import pygame
from random import randint, choice

class Cloud(pygame.sprite.Sprite):  # Added Cloud class

    def __init__(self, groups,speed_type="static"):
        super().__init__(groups)
        self.randomized_cloud = randint(0,5)
        self.image = pygame.image.load(f'graphics/cloud/{self.randomized_cloud}.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(-1000, randint(0, 1900)))
        if speed_type == "static":
            self.speed = 1
        elif speed_type == "rand" or speed_type == "random":
            speed_choices = [1,1,1,1,1,1.25,1.25,1.5,1.5,2,3]
            self.speed = choice(speed_choices)

    def update(self):
        self.rect.x += self.speed
        if self.rect.centerx > 4000:
            self.kill()