import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder
from random import choice
from GroundTile import GroundTile
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from restart import Restart
from shield import Shield
from loftwing import Loftwing
from random import randint
from base_level_class import BaseLevel

class Level10(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)
        
        # A level has 2 attributes for visible sprites and obstacle sprites
        # both are sprite groups
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        self.special_interaction_sprites = pygame.sprite.Group()

        # sprite setup
        self.create_map()

        # music
        self.main_sound = pygame.mixer.Sound('audio/6.ogg')
        self.main_sound.set_volume(0.1)

    def create_map(self):
        player_start_pos = (WIDTH // 2, HEIGTH - 64)
        self.player = Player(
            player_start_pos,
            [self.visible_sprites],
            self.obstacle_sprites,
            self.player_health,
            self.create_attack,
            self.destroy_attack,
            self.create_shield,
            self.destroy_shield,
            player_level=6,
            in_flying_mode=True,
            in_dev_mode = self.mode_at_start
        )
        self.loftwing = Loftwing(self.player.rect.center, [self.visible_sprites], self.player)

    def player_attack_logic(self):
        pass

    def player_defense_logic(self):
        pass

    def level_complete_update(self):
        if self.visible_sprites.counter > 20:
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
            # debug(self.loftwing.status)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.ground_tile_width = 640
        self.ground_tile_height = 360
        self.ground_images = [pygame.image.load(f'graphics/tilemap/ground10/{i}.png').convert() for i in range(0, 4)]
        self.tile_index=0
        self.on_deck_tile_index=1
        self.counter = 0

        self.floor_surf = self.ground_images[self.tile_index]
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
        self.boundary_rect = self.floor_rect.copy()
        self.next_floor_surf = self.ground_images[self.on_deck_tile_index]
        self.next_floor_rect = self.next_floor_surf.get_rect(topleft=(0,-self.ground_tile_height))

    def move_floor(self):
        self.floor_movement_speed = 5
        self.floor_rect.move_ip(0,self.floor_movement_speed)
        self.next_floor_rect.move_ip(0,self.floor_movement_speed)
        if self.floor_rect.y >= self.ground_tile_height:
            self.counter+=1
            self.floor_rect.y = 0
            self.next_floor_rect.y = -self.ground_tile_height
            self.tile_index = self.on_deck_tile_index
            self.on_deck_tile_index = (self.on_deck_tile_index + 1) % len(self.ground_images)
            self.floor_surf = self.ground_images[self.tile_index]
            self.next_floor_surf = self.ground_images[self.on_deck_tile_index]

    def custom_draw(self,player):
        # # drawing the floor
        player.hitbox.clamp_ip(self.boundary_rect)
        self.display_surface.blit(self.floor_surf,self.floor_rect)
        self.display_surface.blit(self.next_floor_surf,self.next_floor_rect)
        self.move_floor()
        self.loftwing_sprites = [sprite for sprite in self.sprites() if isinstance(sprite, Loftwing)]
        if self.loftwing_sprites:
            self.loftwing_sprite = self.loftwing_sprites[0]
        
        # that way the sprites are drawn in from the top of the screen to the bottom
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if not isinstance(sprite, Loftwing):
                if isinstance(sprite, Player):
                    if self.loftwing_sprites:
                        self.display_surface.blit(self.loftwing_sprite.image,self.loftwing_sprite.rect.topleft)
                    self.display_surface.blit(sprite.image, sprite.rect.topleft)
                else:
                    self.display_surface.blit(sprite.image, sprite.rect.topleft)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
