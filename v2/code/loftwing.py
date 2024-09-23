import pygame
from settings import *

# we're passing the Sprite class into the parentheses of Tile() so that
# this Tile class inherits everything from Sprite class
# in essence, a Tile is a Sprite
class Loftwing(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        self.sprite_type = 'loftwing'
        self.image = pygame.Surface((160,96))
        self.rect = self.image.get_rect(center = pos)
        self.player = player
    
    def update(self):
        self.rect.center = self.player.rect.center
