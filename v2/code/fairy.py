import pygame
from settings import *
from entity import Entity
from support import *
from math import sqrt, sin, cos, pi, tan
from debug import debug
from particles import AnimationPlayer

class Fairy(Entity):
    def __init__(self, pos, groups, player, obstacle_sprites, heal_player, loop_pattern = 0):
        super().__init__(groups)
        self.obstacle_sprites = obstacle_sprites
        self.heal_player = heal_player
        self.sprite_type = 'fairy'
        self.surface = pygame.Surface((16,16))
        self.surface.fill((255,0,0))
        self.speed = 2
        self.player = player
        self.rect = self.surface.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.status = 'move'
        self.import_graphics()
        self.image = self.animations[self.status][self.frame_index]

        self.loop_pattern_code = loop_pattern
        self.loop_time = 0
        if self.loop_pattern_code == 0:
            self.loop_speed = 0.01
        if self.loop_pattern_code == 1:
            self.loop_speed = 0.0085
        if self.loop_pattern_code == 2:
            self.loop_speed = 0.014

        # Original position (center of the loops)
        self.origin_pos = pygame.math.Vector2(self.rect.center)

    def adjust_flight_direction(self):
        # Increment loop time
        self.loop_time += self.loop_speed
        if self.loop_pattern_code == 0:
            self.direction.x = sin(self.loop_time * 2 * pi) 
            self.direction.y = sin(self.loop_time * 4 * pi) * cos(self.loop_time * 2 * pi) 
        if self.loop_pattern_code == 1:
            self.direction.y = -sin(self.loop_time * 2 * pi) 
            self.direction.x = sin(self.loop_time * 4 * pi) * cos(self.loop_time * 2 * pi) 
        if self.loop_pattern_code == 2:
            self.direction.x = cos(self.loop_time * pi)
            self.direction.y = sin(self.loop_time * pi)

        # Normalize the direction to ensure consistent speed
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def import_graphics(self):
        self.animations = {'move':[], 'disappear':[]}
        main_path = f'graphics/fairy/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self):
        self.status = 'move'

    def check_interaction(self):
        if self.rect.colliderect(self.player.hitbox):
            self.player.fairy_health_regen()
            self.kill()

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        if self.direction.x > 0:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.adjust_flight_direction()
        self.get_status()
        self.move(self.speed)
        self.animate()
        self.check_interaction()
