import pygame
from settings import *
from enemy import Enemy
from support import *
from math import sqrt

class ShootingEnemy(Enemy):
    def __init__(self,pos,groups,obstacle_sprites,damage_player,trigger_death_particles,monster_name='okto'):
        super().__init__(monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles)
        self.attack_duration = 1000
        self.attack_cooldown_time = 4000
        self.is_shooting = False

    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[], 'charging':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.is_shooting = True
                self.can_attack = False
                self.attack_time = pygame.time.get_ticks()
                self.frame_index = 0
                self.shoot()
            self.status = 'attack'
        elif self.is_shooting:
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status = 'idle'

    def shoot(self):
        pass

    def actions(self,player,other_enemies):
        if self.status == 'attack':
            self.direction = pygame.Vector2()
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
            self.avoid_collisions(other_enemies)
        else:
            self.direction = pygame.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown_time:
                self.can_attack = True
        if self.is_shooting:
            if current_time - self.attack_time >= self.attack_duration:
                self.is_shooting = False
                self.status = 'idle'
        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player,attack_type):
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                self.health -= player.get_full_weapon_damage()
            elif attack_type == 'shield':
                pass
            else:
                pass
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False