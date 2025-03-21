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
from base_level_class import BaseLevel

class Level2(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        
        # sprite setup
        self.create_map()

        # music
        self.main_sound = pygame.mixer.Sound('audio/1b.ogg')
        self.main_sound.set_volume(0.3)
        self.top_sound = pygame.mixer.Sound('audio/1t.ogg')
        self.top_sound.set_volume(0.05)
        # self.main_sound.play(loops = -1)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks2.csv'),
            'grass': import_csv_layout('map/map_Grass2.csv'),
            'object': import_csv_layout('map/map_Objects2.csv'),
            'entities': import_csv_layout('map/map_Entities2.csv')
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
                            else:
                                Tile((x,y),[self.obstacle_sprites],'invisible')
                        if style == 'grass':
                            surf_grass = graphics['grass'][int(col)]
                            Tile((x,y),[self.visible_sprites],'grass',surf_grass)
                        if style == 'object':
                            if int(col) in (2,3):
                                sp_type = 'invisible_half'
                            elif int(col) == 4:
                                sp_type = 'invisible_half_bottom_left'
                            elif int(col) == 5:
                                sp_type = 'level_2_big_tree'
                            else:
                                sp_type = 'object'
                            surf = graphics['objects'][int(col)]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites, self.object_sprites],sp_type,surf)
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
                                    player_level=1,
                                    in_dev_mode=self.mode_at_start)
                            else:
                                if col == '401':
                                    monster_name = 'monkey'
                                    Enemy(
                                        monster_name,
                                        (x,y),
                                        [self.visible_sprites, self.attackable_sprites],
                                        self.obstacle_sprites,
                                        self.damage_player,
                                        self.trigger_death_particles)

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

    def update_in_screen(self):
        for obspr in self.object_sprites:
            if pygame.math.Vector2(self.player.rect.centerx, self.player.rect.centery).distance_to(obspr.rect.center) < 400:
                obspr.in_screen = True
            else:
                obspr.in_screen = False

    def level_complete_update(self):
        exit_sprites = [sprite for sprite in self.obstacle_sprites if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'exit']
        for exit_sprite in exit_sprites:
            if self.player.hitbox.colliderect(exit_sprite.hitbox):
                self.main_sound.stop()
                self.top_sound.stop()
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
            self.visible_sprites.custom_draw(self.player,self.top_sound)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.player_defense_logic()
            self.update_in_screen()
            self.level_complete_update()
            self.ui.display(self.player)
            self.toggle_end()

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
        self.floor_surf = pygame.image.load('graphics/tilemap/ground2.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

        self.fog_surface = pygame.Surface((640,360),pygame.SRCALPHA) 

    def calculate_alpha(self,distance):
        base_alpha = 250
        max_distance = 3400
        min_alpha = 0
        alpha = round(base_alpha * (1 - (distance / max_distance)) ** 2)
        return max(alpha, min_alpha)

    def calculate_volume(self,distance):
        base_volume = 0.26
        max_distance = 3400
        min_volume = 0.05
        volume = round(base_volume * (1 - (distance / max_distance)) ** 2,2)
        return max(volume, min_volume)

    def custom_draw(self,player,sound):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # all we are effectively doing here is sorting the sprites in order of their rectangles center y value
        # that way the sprites are drawn in from the top of the screen to the bottom
        filtered_sprites = [sprite for sprite in self.sprites() if ((hasattr(sprite,'in_screen') and sprite.in_screen) or (not hasattr(sprite,'in_screen')))]
        for sprite in sorted(filtered_sprites,key = lambda sprite: sprite.rect.centery):
            # in order to create an illusion of depth we can offset where the
            # image actually gets rastered so that its not directly inside the rectangle
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)

        player_vec = pygame.math.Vector2(player.rect.center)
        end_vec = pygame.math.Vector2(0, 0)
        distance = (player_vec - end_vec).magnitude()

        
        top_level_volume = self.calculate_volume(distance)
        sound.set_volume(top_level_volume)
        alpha = self.calculate_alpha(distance)
        self.fog_surface.fill((224,224,224,alpha))
        self.display_surface.blit(self.fog_surface, (0,0))

        self.night_surface = pygame.Surface((640,360),pygame.SRCALPHA)
        self.night_surface.fill((19,24,98,50))
        self.display_surface.blit(self.night_surface, (0,0))

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
