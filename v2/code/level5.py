import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder
from random import choice
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from restart import Restart
from shield import Shield
from cloud import Cloud
from random import randint
from enemy2 import SnailEnemy

class Level5:
    def __init__(self,health):
        # this function gets the display surface from any part of the code
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        # A level has 2 attributes for visible sprites and obstacle sprites
        # both are sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_health = health
        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        self.special_interaction_sprites = pygame.sprite.Group()

        self.cloud_sprites = pygame.sprite.Group()
        self.last_cloud_time = None
        self.cloud_cooldown = 500
        self.cloud_modifier = randint(0,4000)

        # sprite setup
        self.create_map()

        #user interface
        self.ui = UI()
        self.background = 'black'
        # particles
        self.animation_player = AnimationPlayer()

        #level status
        self.level_complete_status = False
        self.restart = Restart()
        self.game_over = False

        # music
        self.main_sound = pygame.mixer.Sound('audio/4.ogg')
        self.main_sound.set_volume(0.3)
        # self.main_sound.play(loops = -1)

        self.spawn_cloud()

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks5.csv'),
            'grass': import_csv_layout('map/map_Grass5.csv'),
            'object': import_csv_layout('map/map_Objects5.csv'),
            'entities': import_csv_layout('map/map_Entities5.csv')
        }

        graphics = {
            'grass': import_folder('graphics/grass'),
            'objects': import_folder('graphics/objects')
        }

        for style,layout in layouts.items():
            for row_index, row in enumerate(layout): # enumerate seems to unpack both the index of the element & the row itself
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            if col == '222':
                                Tile((x,y),[self.obstacle_sprites],sprite_type='invisible_half')
                            elif col == '666':
                                Tile((x,y),[self.obstacle_sprites],sprite_type='exit')
                            elif col == '88': #ladder
                                Tile((x,y),[self.special_interaction_sprites],sprite_type='ladder')
                            else:
                                Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'grass':
                            surf_grass = graphics['grass'][int(col)]
                            Tile((x,y),[self.visible_sprites],'grass',surf_grass)
                        if style == 'object':
                            if int(col) in (2,3,8):
                                sp_type = 'invisible_half'
                            elif int(col) == 4:
                                sp_type = 'invisible_half_bottom_left'
                            elif int(col) == 5:
                                sp_type = 'level_2_big_tree'
                            else:
                                sp_type = 'object'
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites],sp_type,surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.player_health,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_shield,
                                    self.destroy_shield,
                                    player_level=4)
                            else:
                                monster_name = 'snail'
                                SnailEnemy(
                                    monster_name,
                                    (x,y),
                                    [self.visible_sprites, self.attackable_sprites],
                                    self.obstacle_sprites,
                                    self.damage_player,
                                    self.trigger_death_particles)

    def create_attack(self):
        self.current_attack = Weapon(self.player,[self.visible_sprites,self.attack_sprites])

    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def create_shield(self):
        self.current_shield = Shield(self.player,[self.visible_sprites,self.shield_sprites])

    def destroy_shield(self):
        if self.current_shield:
            self.current_shield.kill()
        self.current_shield = None

    def spawn_cloud(self):
        Cloud([self.visible_sprites, self.cloud_sprites])
        self.last_cloud_time = pygame.time.get_ticks()
        self.cloud_modifier = randint(0,4000)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy' and target_sprite.status == 'dizzy':
                            pos = target_sprite.rect.center
                            self.animation_player.create_slash_particles(pos,[self.visible_sprites])
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def player_defense_logic(self):
        if self.shield_sprites:
            for shield_sprite in self.shield_sprites:
                collision_sprites = pygame.sprite.spritecollide(shield_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, shield_sprite.sprite_type)

    def player_climbing_logic(self):
        if self.special_interaction_sprites:
            ladder_collision_sprites = pygame.sprite.spritecollide(self.player,self.special_interaction_sprites,False)
            if ladder_collision_sprites:
                self.player.special_interactions_code = 1 # climbing
            else:
                self.player.special_interactions_code = 0

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            pos = self.player.rect.center
            self.animation_player.create_ghost_particles(pos,[self.visible_sprites])

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def level_complete_update(self):
        exit_sprites = [sprite for sprite in self.obstacle_sprites if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'exit']
        for exit_sprite in exit_sprites:
            # if self.player.hitbox.left == exit_sprite.hitbox.right and self.player.hitbox.top == exit_sprite.hitbox.top:
            if self.player.hitbox.colliderect(exit_sprite.hitbox):
                self.main_sound.stop()
                self.level_complete_status = True
    
    def toggle_end(self):
        if self.player.is_dead:
            self.main_sound.stop()
            self.game_over = True

    def continuous_cloud_spawn(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_cloud_time >= self.cloud_cooldown + self.cloud_modifier:
            self.spawn_cloud()

    def restart_level(self):
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        # A level has 2 attributes for visibile sprites and obstacle sprites
        # both are sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        #user interface
        self.ui = UI()
        self.restart = Restart()
        self.game_over = False

        # particles
        self.animation_player = AnimationPlayer()
       
    def run(self):
        self.toggle_end()
        if self.game_over:
            self.restart.display()
        else:
            self.visible_sprites.custom_draw(self.player,self.main_sound)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.player_defense_logic()
            self.player_climbing_logic()
            self.level_complete_update()
            self.ui.display(self.player)
            self.continuous_cloud_spawn()
            self.cloud_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup of all the stuff we need
        # initialize parent class
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground5.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

    def custom_draw(self,player,sound):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # all we are effectively doing here is sorting the sprites in order of their rectangles center y value
        # that way the sprites are drawn in from the top of the screen to the bottom
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if not isinstance(sprite, Cloud):  # Exclude cloud sprites
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # Draw cloud sprites last to ensure they are on top
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if isinstance(sprite, Cloud): 
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
