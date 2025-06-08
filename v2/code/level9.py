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
from enemy_shooting import ShootingEnemy, Projectile
from base_level_class import BaseLevel

class Level9(BaseLevel):
    def __init__(self,health,in_dev_mode,audio_manager):
        super().__init__(health,in_dev_mode,audio_manager)

        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.current_projectiles = pygame.sprite.Group()
        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        self.special_interaction_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # music
        # self.main_sound = pygame.mixer.Sound('audio/9.ogg')
        pygame.mixer.music.load('audio/9.ogg')
        # self.main_sound.set_volume(0.3)
        pygame.mixer.music.set_volume(0.3)

    def create_map(self):
        self.start_time = pygame.time.get_ticks()
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks9.csv'),
            'entities': import_csv_layout('map/map_Entities9.csv'),
            'ladder': import_csv_layout('map/map_Ladder9.csv')
        }

        # graphics = {
        #     'grass': import_folder('graphics/grass'),
        #     'objects': import_folder('graphics/objects')
        # }

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
                        if style == 'ladder':
                            if col == '1': #ladder
                                Tile((x,y),[self.special_interaction_sprites],sprite_type='ladder')
                        # if style == 'object':
                        #     if int(col) in (2,3,8):
                        #         sp_type = 'invisible_half'
                        #     elif int(col) == 4:
                        #         sp_type = 'invisible_half_bottom_left'
                        #     elif int(col) == 5:
                        #         sp_type = 'level_2_big_tree'
                        #     else:
                        #         sp_type = 'object'
                        #     surf = graphics['objects'][int(col)]
                        #     Tile((x,y),[self.visible_sprites, self.obstacle_sprites],sp_type,surf)
                        if style == 'entities':
                            if col == '394':
                                self.player = Player(
                                    (x,y),
                                    # (408,780),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.player_health,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_shield,
                                    self.destroy_shield,
                                    self.audio_manager,
                                    player_level=9,
                                    in_dev_mode = self.mode_at_start)
                            elif col == '601':
                                pando_surf = pygame.image.load('graphics/pando.png').convert_alpha()
                                self.pando = Tile((x,y),[self.visible_sprites,self.obstacle_sprites],sprite_type='pando',surface=pando_surf)
        Tile((192,235),[self.obstacle_sprites],sprite_type='exit')        

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

    def level_complete_update(self):
        exit_sprites = [sprite for sprite in self.obstacle_sprites if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'exit']
        for exit_sprite in exit_sprites:
            if self.player.hitbox.colliderect(exit_sprite.hitbox):
                pygame.mixer.music.stop()
                self.level_complete_status = True

    def restart_level(self):
        self.display_surface = pygame.display.get_surface()
        
        # sprite group setup
        # A level has 2 attributes for visibile sprites and obstacle sprites
        # both are sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites.empty()
        self.attackable_sprites.empty()

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
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.player_defense_logic()
            self.player_special_interactions_logic()
            self.level_complete_update()
            self.ui.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        # general setup of all the stuff we need
        # initialize parent class
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        self.level_start_time = pygame.time.get_ticks()

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground9.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

        self.night_surface = pygame.Surface((640,360),pygame.SRCALPHA)
        
    def custom_draw(self,player):
        # getting the offset
        player.hitbox.clamp_ip(self.floor_rect)
        player.rect.center = player.hitbox.center
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # all we are effectively doing here is sorting the sprites in order of their rectangles center y value
        # that way the sprites are drawn in from the top of the screen to the bottom
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        self.night_surface.fill((19,24,98,100))
        self.display_surface.blit(self.night_surface, (0,0))

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
