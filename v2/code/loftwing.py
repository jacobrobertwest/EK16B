import pygame
from entity import Entity
from support import import_folder
from settings import *

class Loftwing(Entity):
    def __init__(self,pos,groups,player):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        self.sprite_type = 'loftwing'
        self.player = player
        self.status = 'idle_flying'
        self.import_loftwing_assets()
        self.image = self.animations[self.status][0]
        self.rect = self.image.get_rect(center = self.player.rect.center - pygame.Vector2(0,-15))
        self.hitbox = self.rect
        self.animation_speed = 0.1
        self.frame_index = 0
        self.vulnerable = True

    def import_loftwing_assets(self):
        loftwing_path = 'graphics/loftwing/'
        self.animations = {
        'up_flying': [], 'down_flying': [],'left_flying': [],'right_flying': [], 'idle_flying': []
        }
        for animation in self.animations.keys():
            folder_path = loftwing_path + animation
            self.animations[animation] = import_folder(folder_path)
    
    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)
    
    def update(self):
        self.hitbox.center = self.player.rect.center - pygame.Vector2(0,-15)
        self.rect.center = self.hitbox.center
        self.status = self.player.status
        self.animate()
