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
from random import randint


class BaseLevel:
    def __init__(self,health,in_dev_mode,bgcolor='black'):
        self.display_surface = pygame.display.get_surface()
        self.player_health = health
        self.mode_at_start = in_dev_mode

        # shield sprites
        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()

        #user interface
        self.ui = UI()
        self.background = bgcolor

        # particles
        self.animation_player = AnimationPlayer()

        #level status
        self.level_complete_status = False
        self.restart = Restart()
        self.game_over = False
    
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

    def damage_player(self,amount,attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            pos = self.player.rect.center
            self.animation_player.create_ghost_particles(pos,[self.visible_sprites])

    def toggle_end(self):
        if self.player.is_dead:
            self.main_sound.stop()
            if hasattr(self, 'top_sound') and self.top_sound:  # Check if top_sound exists and is not None
                self.top_sound.stop()
            self.game_over = True

    def trigger_death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.visible_sprites)

    def player_climbing_logic(self):
        if self.special_interaction_sprites:
            ladder_collision_sprites = pygame.sprite.spritecollide(self.player,self.special_interaction_sprites,False)
            if ladder_collision_sprites:
                for target_sprite in ladder_collision_sprites:
                    if target_sprite.sprite_type == 'ladder':
                        self.player.special_interactions_code = 1
            else:
                self.player.special_interactions_code = 0