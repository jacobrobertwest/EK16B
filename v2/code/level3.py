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

class Level3(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)
        
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_health = health
        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()

        self.mode_at_start = in_dev_mode
        # sprite setup
        self.create_map()

        #user interface
        self.ui = UI()
        self.background = 'white'

        # particles
        self.animation_player = AnimationPlayer()

        #level status
        self.level_complete_status = False
        self.restart = Restart()
        self.game_over = False

        # music
        self.main_sound = pygame.mixer.Sound('audio/2.ogg')
        self.main_sound.set_volume(0.3)
        # self.main_sound.play(loops = -1)

    def create_map(self):
        layouts = {
            'boundary': import_csv_layout('map/map_FloorBlocks3.csv'),
            'grass': import_csv_layout('map/map_Grass3.csv'),
            'object': import_csv_layout('map/map_Objects3.csv'),
            'entities': import_csv_layout('map/map_Entities3.csv')
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
                                    player_level=2,
                                    in_dev_mode = self.mode_at_start)
                            else:
                                monster_name = 'them'
                                Enemy(
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

        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground3.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))
        self.fog_surface = pygame.Surface((640,360),pygame.SRCALPHA)
        self.fractal_surface_0 = pygame.image.load('graphics/fractal/level3_fractal/0.png').convert_alpha()
        self.fractal_surface_1 = pygame.image.load('graphics/fractal/level3_fractal/1.png').convert_alpha()
        self.fractal_surface_2 = pygame.image.load('graphics/fractal/level3_fractal/2.png').convert_alpha()
        self.fractal_surface_3 = pygame.image.load('graphics/fractal/level3_fractal/3.png').convert_alpha()
        self.fractal_surface_4 = pygame.image.load('graphics/fractal/level3_fractal/4.png').convert_alpha()
        self.fractal_surface_5 = pygame.image.load('graphics/fractal/level3_fractal/5.png').convert_alpha()

    def calculate_alpha(self,distance):
        base_alpha = 255
        max_distance = 3400
        min_alpha = 150
        alpha = base_alpha * (1 - (distance / max_distance))
        return max(alpha, min_alpha)
    
    def calculate_fractal_alphas(self,x):
        if x > 3072:
            return [0,0,0,0,0,0]
        if x <= 3072 and x > 2560:
            return [int((1-((x-2560)/512))*255),0,0,0,0,0]
        elif x <= 2560 and x > 2048:
            return [255,int((1-((x-2048)/512))*255),0,0,0,0]
        elif x <= 2048 and x > 1536:
            return [255,255,int((1-((x-1536)/512))*255),0,0,0]
        elif x <= 1536 and x > 1024:
            return [255,255,255,int((1-((x-1024)/512))*255),0,0]
        elif x <= 1024 and x > 512:
            return [255,255,255,255,int((1-((x-512)/512))*255),0]
        elif x <= 512 and x > 0:
            return [255,255,255,255,255,int((1-((x-0)/512))*255)]
        elif x <= 0:
            return [255,255,255,255,255,255]

    def custom_draw(self,player):
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf,floor_offset_pos)

        # all we are effectively doing here is sorting the sprites in order of their rectangles center y value
        # that way the sprites are drawn in from the top of the screen to the bottom
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            # in order to create an illusion of depth we can offset where the
            # image actually gets rastered so that its not directly inside the rectangle
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image,offset_pos)
        mask_offset_pos = player.rect.topleft - self.offset
        self.display_surface.blit(player.mask_image,mask_offset_pos)

        player_vec = pygame.math.Vector2(player.rect.center)
        end_vec = pygame.math.Vector2(0, 0)
        distance = (player_vec - end_vec).magnitude()
        alpha = self.calculate_alpha(distance)
        self.fog_surface.fill((224,224,224,alpha))

        # getting fractal alphas
        fractal_alphas = self.calculate_fractal_alphas(player.rect.x)

        self.fractal_surface_0.set_alpha(fractal_alphas[0])
        self.fractal_surface_1.set_alpha(fractal_alphas[1])
        self.fractal_surface_2.set_alpha(fractal_alphas[2])
        self.fractal_surface_3.set_alpha(fractal_alphas[3])
        self.fractal_surface_4.set_alpha(fractal_alphas[4])
        self.fractal_surface_5.set_alpha(fractal_alphas[5])

        self.display_surface.blit(self.fractal_surface_0,(0,0))
        self.display_surface.blit(self.fractal_surface_1,(0,0))
        self.display_surface.blit(self.fractal_surface_2,(0,0))
        self.display_surface.blit(self.fractal_surface_3,(0,0))
        self.display_surface.blit(self.fractal_surface_4,(0,0))
        self.display_surface.blit(self.fractal_surface_5,(0,0))
        self.display_surface.blit(self.fog_surface, (0,0))
        
    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
