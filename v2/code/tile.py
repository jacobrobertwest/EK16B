import pygame
from settings import *

# we're passing the Sprite class into the parentheses of Tile() so that
# this Tile class inherits everything from Sprite class
# in essence, a Tile is a Sprite
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,sprite_type,surface = pygame.Surface((TILESIZE,TILESIZE))):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        self.pos = pos
        self.sprite_type = sprite_type
        self.image = surface
        self.in_screen = None
        if self.sprite_type == 'invisible_half_bottom_left':
            self.rect = self.image.get_rect(midleft = pos + pygame.math.Vector2(0,-30))
        elif self.sprite_type == 'level_2_big_tree':
            self.rect = self.image.get_rect(midleft = pos)
        elif self.sprite_type == 'bloodmoon':
            self.rect = self.image.get_rect(center=pos)
        else:
            self.rect = self.image.get_rect(topleft = pos) #creating a rectangle based on the image attribute, putting the position at the top left
        if self.sprite_type in ('invisible_half','level_2_big_tree'):
            self.hitbox = self.rect.inflate(-65,-30)
        elif self.sprite_type == 'invisible_willow':
            self.hitbox = self.rect.inflate(-100,-100)
        elif self.sprite_type == 'invisible_half_bottom_left':
            self.hitbox = self.rect.inflate(-100,-150)
        elif self.sprite_type == 'door':
            self.hitbox = self.rect.inflate(-30,-30)
        elif self.sprite_type == 'boundary_no_hb':
            self.hitbox = self.rect
        elif self.sprite_type == 'pando':
            self.hitbox = self.rect.inflate(-1000,-500)
        else:
            self.hitbox = self.rect.inflate(-10,-10)