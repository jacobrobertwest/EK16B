import pygame
from settings import *

# we're passing the Sprite class into the parentheses of Player() so that
# this Player class inherits everything from Sprite class
# in essence, a Player is also a sprite
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) #creating a rectangle based on the image attribute, putting the position at the top left
        