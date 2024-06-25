import pygame
from settings import *
from enemy import Enemy
from support import *
from math import sqrt
from debug import debug

class SnailEnemy(Enemy):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles):
        super().__init__(monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles)
        self.roll_time = None
        self.roll_startup = 120
        self.roll_length = 2000
        self.rolling = False

        self.is_dizzy = False
        self.dizzy_time = None
        self.dizzy_length = 3000

        self.charging = False
        self.charge_time = None
        self.charge_cooldown = 500
        self.charge = 0
        self.roll_threshold = 120
        self.roll_direction = None

    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[], 'roll':[], 'dizzy':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if self.is_dizzy:
            self.status = 'dizzy'
        elif distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius and self.charge < self.roll_threshold:
            self.status = 'move'
            if not self.charging:
                self.charge_time = pygame.time.get_ticks()
            self.charging = True
            self.speed = 0
            self.charge += 1
        elif self.charge >= self.roll_threshold:
            if not self.rolling:
                self.roll_time = pygame.time.get_ticks()
                self.roll_direction = self.get_player_distance_direction(player)[1]
                self.rolling = True
            self.status = 'roll'
            self.rolling = True
            self.speed = 6
        else: 
            self.status = 'idle'
            self.charge -= 5
            if self.charge < 0:
                self.charge = 0

    def actions(self,player,other_enemies):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage,self.attack_type)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
            self.avoid_collisions(other_enemies)
        elif self.status == 'roll':
            if self.colliding and pygame.time.get_ticks() - self.roll_time >= self.roll_startup:
                self.dizzy_time = pygame.time.get_ticks()
                self.status = 'dizzy'
                self.is_dizzy = True
                self.rolling = False
                self.direction = pygame.math.Vector2()
                self.speed = 0
        elif self.status == 'dizzy':
            self.direction = pygame.math.Vector2()
            self.speed = 0
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown_time:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

        if self.rolling:
            if current_time - self.roll_time >= self.roll_length:
                self.rolling = False
                self.status = 'idle'
                self.charge = 0

        if self.is_dizzy:
            if current_time - self.dizzy_time >= self.dizzy_length:
                self.is_dizzy = False
                self.status = 'idle'
                self.charge = 0

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon' and self.status == 'dizzy':
                self.health -= player.get_full_weapon_damage()
            elif attack_type == 'shield':
                self.status = 'dizzy'
                self.rolling = False
                self.is_dizzy = True
                self.dizzy_time = pygame.time.get_ticks()
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
        

