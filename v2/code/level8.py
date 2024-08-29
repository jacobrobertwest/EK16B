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
from random import randint
from base_level_class import BaseLevel


class Level8(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)

        # outside
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        self.special_interaction_sprites = pygame.sprite.Group()
        self.player_level_code = 8

        self.player_starting_pos = (5,948)

        # sprite setup
        self.create_map()

        # music
        self.main_sound = pygame.mixer.Sound('audio/7.ogg')
        self.main_sound.set_volume(0.2)

    def create_map(self):
        self.player = Player(
            self.player_starting_pos,
            [self.visible_sprites],
            self.obstacle_sprites,
            self.player_health,
            self.create_attack,
            self.destroy_attack,
            self.create_shield,
            self.destroy_shield,
            player_level=self.player_level_code,
            in_dev_mode = self.mode_at_start
        )
        block_surf = pygame.Surface((1200,700))
        block_surf.fill((139, 69, 19))
        Tile((0,180),[self.visible_sprites,self.obstacle_sprites],sprite_type='block',surface=block_surf)
        exit_surf = pygame.Surface((128,64))
        exit_surf.fill((0,255,0))
        Tile((200,-64),[self.visible_sprites,self.obstacle_sprites],sprite_type='exit',surface=exit_surf)

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite,self.attackable_sprites,False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'enemy':
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
                self.main_sound.stop()
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
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.special_interaction_sprites.empty()

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
            self.player_climbing_logic()
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
        self.floor_surf = pygame.Surface((1536, 1024))
        self.floor_surf.fill((92, 162, 74)) 
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
        self.night_surface = pygame.Surface((640,360),pygame.SRCALPHA)

    def custom_draw(self,player):
        # getting the offset
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

        if hasattr(self,'night_surface'):
            self.night_surface.fill((19,24,98,100))
            self.display_surface.blit(self.night_surface, (0,0))

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
