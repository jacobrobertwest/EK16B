import pygame
from settings import *

# we're passing the Sprite class into the parentheses of Tile() so that
# this Tile class inherits everything from Sprite class
# in essence, a Tile is a Sprite
class GroundTile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,tile_id,surface = pygame.Surface((768,512))):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        self.tile_id = tile_id
        self.image = surface
        self.origin = pos
        self.rect = self.image.get_rect(topleft = pos) #creating a rectangle based on the image attribute, putting the position at the top left