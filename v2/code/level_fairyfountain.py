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
from fairy import Fairy
from random import randint
from base_level_class import BaseLevel


class FairyFountain(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)

        # outside
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.background = (57,41,41)
        self.particle_sprites = pygame.sprite.Group()
        # attack sprites
        self.particles_playing = False
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        self.special_interaction_sprites = pygame.sprite.Group()
        self.player_level_code = 'fairyfountain'

        self.player_starting_pos = (471,932)

        # sprite setup
        self.create_map()

        # music
        self.main_sound = pygame.mixer.Sound('audio/fairyfountain.ogg')
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
        self.establish_boundaries()
        Fairy((480,437),[self.visible_sprites],self.player,self.obstacle_sprites,None)
        Fairy((334,437),[self.visible_sprites],self.player,self.obstacle_sprites,None,1)
        Fairy((579,358),[self.visible_sprites],self.player,self.obstacle_sprites,None,2)

    def establish_boundaries(self):
        # exit surface
        exit_surf = pygame.Surface((128,128))
        exit_surf.fill((57,41,41))
        Tile((420,1000),[self.visible_sprites,self.obstacle_sprites],sprite_type='exit',surface=exit_surf)
        #statue blockers
        fountain_block_surf = pygame.Surface((123,134))
        Tile((220,512),[self.obstacle_sprites],sprite_type='boundary',surface=fountain_block_surf)
        Tile((654,512),[self.obstacle_sprites],sprite_type='boundary',surface=fountain_block_surf)
        #wall blockers - vertical
        vert_wall_block_surf = pygame.Surface((20,1000))
        Tile((100,0),[self.obstacle_sprites],sprite_type='boundary',surface=vert_wall_block_surf)
        Tile((879,0),[self.obstacle_sprites],sprite_type='boundary',surface=vert_wall_block_surf)
        #wall blockers - horizontal
        horiz_wall_block_surf = pygame.Surface((1000,20))
        Tile((0,180),[self.obstacle_sprites],sprite_type='boundary',surface=horiz_wall_block_surf)
        #entrance wall blockers
        front_wall_surf = pygame.Surface((350,120))
        Tile((545,880),[self.obstacle_sprites],sprite_type='boundary',surface=front_wall_surf)
        Tile((112,880),[self.obstacle_sprites],sprite_type='boundary',surface=front_wall_surf)
        #corner blockers
        #bottom left
        corner_surf_0 = pygame.Surface((128,32))
        corner_surf_1 = pygame.Surface((96,32))
        corner_surf_2 = pygame.Surface((64,32))
        corner_surf_3 = pygame.Surface((32,32))
        Tile((120,760),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_3)
        Tile((120,792),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_2)
        Tile((120,824),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_1)
        Tile((120,856),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_0)
        Tile((881-32,760),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_3)
        Tile((881-64,792),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_2)
        Tile((881-96,824),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_1)
        Tile((881-128,856),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_0)
        Tile((120,205),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_0)
        Tile((120,205+32),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_1)
        Tile((120,205+64),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_2)
        Tile((120,205+96),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_3)
        Tile((750,205),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_0)
        Tile((750+32,205+32),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_1)
        Tile((750+64,205+64),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_2)
        Tile((750+96,205+96),[self.obstacle_sprites],sprite_type='boundary_no_hb',surface=corner_surf_3)
        # water interaction tiles
        water_surf_0 = pygame.Surface((360,72))
        water_surf_1 = pygame.Surface((514,50))
        water_surf_2 = pygame.Surface((222,50))
        Tile((316,343),[self.special_interaction_sprites],sprite_type='water',surface=water_surf_0)
        Tile((245,415),[self.special_interaction_sprites],sprite_type='water',surface=water_surf_1)
        Tile((391,487),[self.special_interaction_sprites],sprite_type='water',surface=water_surf_2)

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

    def check_for_fairy_interaction(self):
        if self.player.regenerating_health and not self.particles_playing:
            self.animation_player.create_heal_particles(self.player.rect.center,[self.visible_sprites])
            self.particles_playing = True

    def restart_particles_timer(self):
        if not self.particle_sprites:
            self.particles_playing = False

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
        self.display_surface.fill(self.background)
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
            self.check_for_fairy_interaction()
            self.restart_particles_timer()
            # debug(pygame.mouse.get_pos())
            # debug(self.fairy.direction)


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
        self.floor_surf = pygame.image.load('graphics/tilemap/fairyfountain/fairyfountain.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
        # self.night_surface = pygame.Surface((640,360),pygame.SRCALPHA)

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

        self.door_top_surf = pygame.image.load('graphics/tilemap/fairyfountain/fairyfountain_door.png').convert()
        self.door_top_rect = self.floor_surf.get_rect(topleft=(450,988))
        door_top_offset = self.door_top_rect.topleft - self.offset
        self.display_surface.blit(self.door_top_surf,door_top_offset)

        if hasattr(self,'night_surface'):
            self.night_surface.fill((19,24,98,100))
            self.display_surface.blit(self.night_surface, (0,0))

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
