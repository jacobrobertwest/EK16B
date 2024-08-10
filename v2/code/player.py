import pygame
from settings import *
from support import import_folder
from entity import Entity
from debug import debug

# we're passing the Sprite class into the parentheses of Player() so that
# this Player class inherits everything from Sprite class
# in essence, a Player is also a sprite
class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites,player_health,create_attack,destroy_attack,create_shield,destroy_shield,player_level=0,in_dev_mode=False):
        super().__init__(groups) # we gotta use this to initialize our base/parent class!
        if player_level == 0:
            self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'down'
        elif player_level == 1:
            self.image = pygame.image.load('graphics/player/up_idle/idle_up.png').convert_alpha()
            rect_offset = pygame.math.Vector2(-38,130)
            self.status = 'up'
        elif player_level == 2:
            self.image = pygame.image.load('graphics/player/left_idle/idle_left.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'left'
            self.mask = pygame.mask.from_surface(self.image,threshold=1)
            self.mask_image = self.mask.to_surface(setcolor=(200,200,200,255),unsetcolor=(0,0,0,0))
            # colliding_bits_image = colliding_bits.to_surface(setcolor=(0, 255, 0, 255), unsetcolor=(0, 0, 0, 0))
            # self.mask_image.fill((100, 100, 100, 255))  # Dark grey color with 50% transparency
        elif player_level == 4:
            self.image = pygame.image.load('graphics/player/left_idle/idle_left.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'left'
        elif player_level == 6:
            self.image = pygame.image.load('graphics/player/up_idle/idle_up.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'up'
            self.mask = pygame.mask.from_surface(self.image)
        elif player_level == 7 or player_level == '7a':
            self.image = pygame.image.load('graphics/player/up_idle/idle_up.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'up'
            self.mask = pygame.mask.from_surface(self.image)
        elif player_level == '7o':
            self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'down'
        else:
            self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()
            rect_offset = pygame.math.Vector2(0,0)
            self.status = 'down'
        self.rect = self.image.get_rect(topleft = pos + rect_offset) #creating a rectangle based on the image attribute, putting the position at the top left
        self.hitbox = self.rect.inflate(0,-26)
        self.sprite_type = 'player'
        # graphics setup
        self.import_player_assets()

        # direction attribute gets set to a vector so that we can multiply it be a speed variable
        # movement attributes
        self.direction = pygame.math.Vector2()

        self.is_climbing = False

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

        self.defending = False
        self.defend_cooldown = 400
        self.defend_time = None
        self.create_shield = create_shield
        self.destroy_shield = destroy_shield
        self.special_interactions_code = 0

        # stats
        self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'stamina':100, 'sprint_drain': 0.5, 'sprint_replenish':0.25}
        self.health = player_health
        self.max_health = self.stats['health']
        self.energy = self.stats['energy']

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

        self.in_dev_mode = in_dev_mode
        self.mode_change_time = 0
        self.mode_change_duration = 500

        #is dead
        self.is_dead = False

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
        'up': [],'down': [],'left': [],'right': [],
        'right_idle': [],'left_idle': [],'up_idle': [],'down_idle': [],
        'right_attack': [],'left_attack': [],'up_attack': [],'down_attack': [],
        'right_defend': [],'left_defend': [],'up_defend': [],'down_defend': [],
        'right_climbing': [],'left_climbing': [],'up_climbing': [],'down_climbing': []
        }
        for animation in self.animations.keys():
            folder_path = character_path + animation
            self.animations[animation] = import_folder(folder_path)
    
    def enforce_player_dev_mode(self):
        if self.in_dev_mode:
            if self.health < self.max_health:
                self.health += 1
            debug("DEV",x=10,y=335)

    def input(self):
        if not self.attacking and not self.defending:
            self.direction.x = 0
            self.direction.y = 0
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

            if keys[pygame.K_q] and not self.in_dev_mode and pygame.time.get_ticks() - self.mode_change_time >= self.mode_change_duration:
                self.in_dev_mode = True
                self.mode_change_time = pygame.time.get_ticks()

            if keys[pygame.K_q] and self.in_dev_mode and pygame.time.get_ticks() - self.mode_change_time >= self.mode_change_duration:
                self.in_dev_mode = False
                self.mode_change_time = pygame.time.get_ticks()
            
            # BASE SPEED LEVELS
            self.base_speed = 4
            self.sprint_buff = 0.5
            self.sprint_speed = self.base_speed * (1 + self.sprint_buff)
            self.tired_speed = self.base_speed * (1 - self.sprint_buff)

            self.base_animation_speed = 0.15
            self.sprint_animation_buff = 0.33
            self.sprint_animation_speed = self.base_animation_speed * (1 + self.sprint_animation_buff)
            self.tired_animation_speed = self.base_animation_speed * (1 - self.sprint_animation_buff)

            if self.in_dev_mode:
                self.base_speed *= 3
                self.sprint_buff *= 3
                self.base_animation_speed *= 3
                self.sprint_animation_buff *= 3
            # run input
            if keys[pygame.K_LSHIFT] and (keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]): # if shift is being held
                if self.stamina > 0: 
                    if not self.oversprinting_status:
                        self.speed = self.sprint_speed
                        self.animation_speed = self.sprint_animation_speed
                        self.stamina -= self.sprint_drain
                    else:
                        self.speed = self.tired_speed
                        self.animation_speed = self.tired_animation_speed
                        if self.stamina < self.stats['stamina']:
                            self.stamina += self.sprint_replenish
                        else:
                            self.stamina = self.stats['stamina']
                else:
                    self.oversprinting_status = True
                    self.oversprint_time = pygame.time.get_ticks()
                    self.speed = self.tired_speed
                    self.animation_speed = self.tired_animation_speed

            else:
                if not self.oversprinting_status:
                    self.speed = self.base_speed
                    self.animation_speed = self.base_animation_speed
                else:
                    self.speed = self.tired_speed
                    self.animation_speed = self.tired_animation_speed
                if self.stamina < self.stats['stamina']:
                    self.stamina += self.sprint_replenish
                else:
                    self.stamina = self.stats['stamina']

            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()

            # shield input
            if keys[pygame.K_c] and not self.defending and not self.attacking:
                self.defending = True
                self.defend_time = pygame.time.get_ticks()
                self.create_shield()
        else:
            self.direction.x = 0
            self.direction.y = 0
    
    def get_status(self):
        if self.is_climbing:
            if self.direction.x == 0 and self.direction.y == 0:
                self.status = 'up_idle'
            elif '_idle' in self.status:
                self.status = self.status.replace('_idle','_climbing')
            elif not '_climbing' in self.status:
                self.status = self.status + '_climbing'
        else:
            if self.direction.x == 0 and self.direction.y == 0:
                if not 'idle' in self.status and not 'attack' in self.status and not 'defend' in self.status:
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
            elif self.defending:
                self.direction.x = 0
                self.direction.y = 0
                if not 'defend' in self.status:
                    if 'idle' in self.status:
                        # overwrite idle
                        self.status = self.status.replace('_idle','_defend')
                    elif 'attack' in self.status:
                        # overwrite attack
                        self.status = self.status.replace('_attack','_defend')
                    else:
                        self.status = self.status + '_defend'
            else:
                if 'attack' in self.status:
                    self.status = self.status.replace('_attack', '')
                    self.destroy_attack()
                    self.destroy_shield()
                    self.direction.x = 0
                    self.direction.y = 0
                if 'defend' in self.status:
                    self.status = self.status.replace('_defend', '')
                    self.destroy_shield()
                    self.direction.x = 0
                    self.direction.y = 0

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
                if sprite.sprite_type == 'exit':
                    pass
                else:
                    if sprite.hitbox.colliderect(self.hitbox):
                        if self.direction.x > 0: # if moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: # if moving left
                            self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
                for sprite in self.obstacle_sprites:
                    if sprite.sprite_type == 'exit':
                        pass
                    else:
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

        if self.defending:
            if current_time - self.defend_time >= self.defend_cooldown:
                self.defending = False

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if self.oversprinting_status:
            if current_time - self.oversprint_time >= self.oversprint_cooldown:
                self.oversprinting_status = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def check_death(self):
        if self.health <= 0:
            self.is_dead = True

    def check_special_interactions(self):
        if self.special_interactions_code == 1: # climbing special interaction
            self.is_climbing = True
            self.speed = 2
            self.animation_speed = 0.1
        else:
            self.is_climbing = False

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

    def update_mask(self):
        if hasattr(self,'mask'):
            self.mask = pygame.mask.from_surface(self.image,threshold=1)
            self.mask_image = self.mask.to_surface().convert_alpha()
            self.mask_image = self.mask.to_surface(setcolor=(200,200,200,255),unsetcolor=(0,0,0,0))
            # self.mask_image.fill((100, 100, 100, 255))  # Dark grey color with 50% transparency

    def update(self):
        self.enforce_player_dev_mode()
        self.check_death()
        self.input()
        self.cooldowns()
        self.check_special_interactions()
        self.get_status()
        self.animate()
        self.move(self.speed)
        self.update_mask()
