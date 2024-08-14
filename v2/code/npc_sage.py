import pygame
from settings import *
from support import import_folder
from dialog_box import DialogBox
from entity import Entity
from debug import debug
from math import sin
from random import randint
import re


class Sage(Entity):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.starting_pos = pos
        self.obstacle_sprites = obstacle_sprites
        self.animation_speed = 0.08
        # setting up surface
        # self.image = pygame.Surface((64, 80))
        # self.image.fill((137, 207, 240)) 
        self.image = pygame.image.load('graphics/sage/down_idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = self.starting_pos)
        self.hitbox = self.rect.inflate(0,-26)
        self.sprite_type = 'npc'

        self.speed = 1
        self.status = 'down_idle'
        self.is_moving = False
        self.direction = pygame.math.Vector2(0,0)
        self.current_y_direction = round(randint(-100,100)/100,2)

        self.begin_idle_timestamp = pygame.time.get_ticks()
        self.idle_duration = randint(10000,20000)

        self.begin_move_timestamp = None
        self.move_duration = randint(4000,7500)

        self.x_boundaries = [10,470]
        self.y_boundaries = [10,290]

        self.hit_boundary = False

        self.next_move_direction_is_left = True

        self.import_npc_assets()

        # Time reference for oscillation
        self.start_time = pygame.time.get_ticks()

    def import_npc_assets(self):
        character_path = 'graphics/sage/'
        self.animations = {
        'up': [],'down': [],'left': [],'right': [],
        'right_idle': [],'left_idle': [],'up_idle': [],'down_idle': [],
        'right_move': [],'left_move': [],'up_move': [],'down_move': [],
        }
        for animation in self.animations.keys():
            folder_path = character_path + animation
            self.animations[animation] = import_folder(folder_path)

    
    def animate(self):
        animation = self.animations[self.status]
        # # loop over the frame index 
        self.frame_index += self.animation_speed
        # # resetting the frame index once you hit the length of the list
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # # flicker
        alpha = min(self.wave_value_continuous() + 70,200)
        self.image.set_alpha(alpha)
        # if not self.vulnerable:
        #     alpha = self.wave_value()
        #     self.image.set_alpha(alpha)
        # else:
        #     self.image.set_alpha(255)

    def trigger_dialog(self):
        self.dialogue_box = DialogBox("\"MALON...\"",DESERET_FONT)
        self.dialogue_box.show()

    def get_status_direction(self):
        current_time = pygame.time.get_ticks()
        if not self.is_moving:
            self.direction = pygame.math.Vector2(0,0)
            if 'idle' not in self.status:
                self.status = re.sub(r'_\w*', '_idle', self.status)
            if current_time - self.begin_idle_timestamp >= self.idle_duration:
                self.is_moving = True
                self.begin_move_timestamp = current_time
        elif self.is_moving:
            if not self.hit_boundary:
                y_value = self.current_y_direction
                if self.next_move_direction_is_left:
                    self.direction = pygame.math.Vector2(-1,y_value)
                    self.status = 'left'
                else:
                    self.direction = pygame.math.Vector2(1,y_value)
                    self.status = 'right'
                self.status += '_move'
            else:
                if 'idle' not in self.status:
                    self.status = re.sub(r'_\w*', '_idle', self.status)
                self.direction = pygame.math.Vector2(0,0)
            if current_time - self.begin_move_timestamp >= self.move_duration:
                self.is_moving = False
                self.begin_idle_timestamp = current_time
                self.move_duration = randint(4000,7500)
                self.idle_duration = randint(10000,20000)
                self.next_move_direction_is_left = not self.next_move_direction_is_left
                if self.rect.top < 25:
                    range_btm = 20
                    range_top = 90
                elif self.rect.bottom > 275:
                    range_btm = -90
                    range_top = -20
                else:
                    range_btm = -100
                    range_top = 100
                self.current_y_direction = round(randint(range_btm,range_top)/100,2)
                self.hit_boundary = False

    def keep_within_boundaries(self):
        adjustments = 0
        if self.rect.left < self.x_boundaries[0]:
            self.rect.left = self.x_boundaries[0]
            adjustments += 1
        if self.rect.right > self.x_boundaries[1]:
            self.rect.right = self.x_boundaries[1]
            adjustments += 1
        if self.rect.top < self.y_boundaries[0]:
            self.rect.top = self.y_boundaries[0]
            adjustments += 1
        if self.rect.bottom > self.y_boundaries[1]:
            self.rect.bottom = self.y_boundaries[1]
            adjustments += 1
        self.hitbox.center = self.rect.center
        if adjustments > 0:
            self.hit_boundary = True
            
    def update(self):
        self.get_status_direction()
        self.animate()
        self.move(self.speed)
        self.keep_within_boundaries()
        # debug(self.status,x=10,y=300)