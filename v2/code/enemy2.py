import pygame
from settings import *
from entity import Entity
from support import *
from math import sqrt
from debug import debug

class Enemy2(Entity):
    def __init__(self,monster_name,pos,groups,obstacle_sprites,damage_player,trigger_death_particles):

        # general setup
        super().__init__(groups)
        self.sprite_type = 'enemy'

        # graphics setup
        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        # movement
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']

        # player interaction
        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown_time = 1000
        self.damage_player = damage_player
        self.trigger_death_particles = trigger_death_particles

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


        # invincibility timer
        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle':[], 'move':[], 'attack':[], 'roll':[], 'dizzy':[]}
        main_path = f'graphics/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()
        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()
        return (distance,direction)

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

    def avoid_collisions(self, other_enemies):
        for enemy in other_enemies:
            separation_strength = 0.1
            alignment_strength = 0.02
            cohesion_strength = 0.005

            separation_vector = pygame.math.Vector2(0,0)
            alignment_vector = pygame.math.Vector2(0,0)
            cohesion_vector = pygame.math.Vector2(0,0)

            if enemy != self:
                if self.hitbox.colliderect(enemy.hitbox):
                    separation_vector += pygame.math.Vector2(self.hitbox.center) - pygame.math.Vector2(enemy.hitbox.center)
                    alignment_vector += pygame.math.Vector2(enemy.direction)
                    cohesion_vector += pygame.math.Vector2(enemy.rect.center)

            if len(other_enemies) > 1:
                # Normalize vectors if they are not zero
                if separation_vector.length() > 0:
                    separation_vector.normalize_ip()
                    separation_vector *= separation_strength
                if alignment_vector.length() > 0:
                    alignment_vector.normalize_ip()
                    alignment_vector *= alignment_strength
                if cohesion_vector.length() > 0:
                    cohesion_vector.normalize_ip()
                    cohesion_vector *= cohesion_strength
                # Update direction based on combined vectors
                self.direction += separation_vector + alignment_vector + cohesion_vector
                try:
                    self.direction.normalize_ip()
                except:
                    pass

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
        
    def check_death(self):
        if self.health <= 0:
            self.kill()
            self.trigger_death_particles(self.rect.center,'spirit')

    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0
        self.image = animation[int(self.frame_index)]
        if self.direction.x > 0:
            self.image = pygame.transform.flip(self.image,True,False)
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_death()

    def enemy_update(self,player,enemy_sprites):
        self.get_status(player)
        self.actions(player,enemy_sprites)