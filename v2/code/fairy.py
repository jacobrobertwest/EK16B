import pygame
from settings import *
from entity import Entity
from support import *
from math import sqrt, sin, cos, pi, tan
from debug import debug
from particles import AnimationPlayer
import csv

class Fairy(Entity):
    def __init__(self, pos, groups, player, obstacle_sprites, heal_player, fairynum):
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
        self.fairynum = fairynum
        self.status = 'move'
        self.import_graphics()
        self.image = self.animations[self.status][self.frame_index]

        self.pos_index = 0
        self.pos_pattern_list = self.import_pos_pattern()
        self.pos_pattern_len = len(self.pos_pattern_list)
        
        self.origin_pos = self.pos_pattern_list[self.pos_index]

    def import_graphics(self):
        self.animations = {'move':[], 'disappear':[]}
        main_path = f'graphics/fairy/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def string_to_vector2(self,vector_string1,vector_string2):
        vector_string1 = vector_string1.replace("\ufeff", "")
        x = int(vector_string1)
        vector_string2 = vector_string2.replace("\ufeff", "")
        y = int(vector_string2)
        return pygame.Vector2(x, y)

    def import_pos_pattern(self):
        pattern_fp = f'data/fairy/fairy{self.fairynum}_mvmt.csv'
        vectors = []
        with open(pattern_fp, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                vector = self.string_to_vector2(row[0],row[1])
                vectors.append(vector)
        return vectors

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
        self.correct_image_flip()
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def correct_image_flip(self):
        current_pos = self.hitbox.center
        if self.pos_index + 1 < self.pos_pattern_len:
            next_pos = self.pos_pattern_list[self.pos_index + 1]
        else:
            next_pos = self.pos_pattern_list[0]
        self.direction_vector = next_pos - current_pos  # Subtract the positions to get the direction
        if self.direction_vector.length() > 0:
            self.direction_vector = self.direction_vector.normalize()
        else:
            self.direction_vector = pygame.Vector2(0, 0)
        if self.direction_vector.x >= 0:
            self.image = pygame.transform.flip(self.image,True,False)
        
    def move(self):
        self.pos_index += 1
        if self.pos_index >= self.pos_pattern_len:
            self.pos_index = 0
        self.hitbox.center = self.pos_pattern_list[self.pos_index]
        self.rect.center = self.hitbox.center

    def update(self):
        self.get_status()
        self.move()
        self.animate()
        self.check_interaction()
