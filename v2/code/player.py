import pygame
from settings import *
from support import import_folder
from entity import Entity

# we're passing the Sprite class into the parentheses of Player() so that
# this Player class inherits everything from Sprite class
# in essence, a Player is also a sprite
class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_attack):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        self.image = pygame.image.load('graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) #creating a rectangle based on the image attribute, putting the position at the top left
        self.hitbox = self.rect.inflate(0,-26)

        # graphics setup
        self.import_player_assets()
        self.status = 'down'

        # direction attribute gets set to a vector so that we can multiply it be a speed variable
        # movement attributes
        self.direction = pygame.math.Vector2()

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

        # weapon
        self.create_attack = create_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.destroy_attack = destroy_attack
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        # stats
        self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'speed':7.5,'stamina':100, 'sprint_drain': 0.5, 'sprint_replenish':0.25}
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.exp = 123
        self.speed = self.stats['speed']

        self.stamina = self.stats['stamina']
        self.sprint_drain = self.stats['sprint_drain']
        self.sprint_replenish = self.stats['sprint_replenish']
        self.oversprinting_status = False
        self.oversprint_time = None
        self.oversprint_cooldown = 2500

        #damage timer
        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
        'up': [],'down': [],'left': [],'right': [],
        'right_idle': [],'left_idle': [],'up_idle': [],'down_idle': [],
        'right_attack': [],'left_attack': [],'up_attack': [],'down_attack': []
        }
        for animation in self.animations.keys():
            folder_path = character_path + animation
            self.animations[animation] = import_folder(folder_path)

    def input(self):
        if not self.attacking:
            # getting all the keys that are being pressed
            keys = pygame.key.get_pressed()

            # movement input
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]: 
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0
            
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT]: 
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # run input
            if keys[pygame.K_LSHIFT] and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]): # if shift is being held
                if self.stamina > 0: # if 
                    if not self.oversprinting_status:
                        self.speed = 10
                        self.animation_speed = 0.15*1.33
                        self.stamina -= self.sprint_drain
                    else:
                        self.speed = 4.5
                        self.animation_speed = 0.125
                        if self.stamina < self.stats['stamina']:
                            self.stamina += self.sprint_replenish
                        else:
                            self.stamina = self.stats['stamina']
                else:
                    self.oversprinting_status = True
                    self.oversprint_time = pygame.time.get_ticks()
                    self.speed = 4.5
                    self.animation_speed = 0.125

            else:
                if not self.oversprinting_status:
                    self.speed = 7.5
                    self.animation_speed = 0.15
                else:
                    self.speed = 4.5
                    self.animation_speed = 0.125
                if self.stamina < self.stats['stamina']:
                    self.stamina += self.sprint_replenish
                else:
                    self.stamina = self.stats['stamina']

            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # magic input
            if keys[pygame.K_LSUPER] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()
                if self.weapon_index < len(list(weapon_data.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0
                self.weapon = list(weapon_data.keys())[self.weapon_index]
    
    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status = self.status + '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    # overwrite idle
                    self.status = self.status.replace('_idle','_attack')
                else:
                    self.status = self.status + '_attack'
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
                self.destroy_attack()

    def move(self,speed):
        # we have to normalize the self.direction vector in order
        # to not make going diagonal be so much faster
        # the reason why we have this if statement is because if the vector
        # had a length of 0, the normalize would throw an error

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            # looping through every sprite in the obstacle sprite group
            # and checking to see if there is a collission
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # if moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # if moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # if moving down (remember increasing y is down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # if moving up
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
                self.attacking = False

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if self.oversprinting_status:
            if current_time - self.oversprint_time >= self.oversprint_cooldown:
                self.oversprinting_status = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self):
        animation = self.animations[self.status]
        # loop over the frame index 
        self.frame_index += self.animation_speed
        # resetting the frame index once you hit the length of the list
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        # flicker
        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self):
        base_damage = self.stats['attack']
        weapon_damage = weapon_data[self.weapon]['damage']
        return base_damage + weapon_damage

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)