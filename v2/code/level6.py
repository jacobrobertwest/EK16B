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
from base_level_class import BaseLevel

class Level6(BaseLevel):
    def __init__(self,health,in_dev_mode):
        super().__init__(health,in_dev_mode)
        
        # sprite group setup
         #blood moon
        self.blood_moon_x = randint(3000,7000)
        self.blood_moon_y = randint(1300,1700)*(-1)
        self.blood_moon_pos = (self.blood_moon_x, self.blood_moon_y)
        # A level has 2 attributes for visible sprites and obstacle sprites
        # both are sprite groups
        self.visible_sprites = YSortCameraGroup(self.blood_moon_pos)
        self.obstacle_sprites = pygame.sprite.Group()
        self.mode_at_start = in_dev_mode
        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.player_health = health
        self.current_shield = None
        self.shield_sprites = pygame.sprite.Group()
        self.special_interaction_sprites = pygame.sprite.Group()

        self.ground_tiles = pygame.sprite.Group()
        self.tiles = {}

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
        self.main_sound = pygame.mixer.Sound('audio/6.ogg')
        self.main_sound.set_volume(0.1)

    def create_map(self):
        graphics = {
            'objects': import_folder('graphics/objects')
        }
        self.ground_tile_width = 750
        self.ground_tile_height = 500
        self.ground_images = [pygame.image.load(f'graphics/tilemap/ground6/{i}.png').convert() for i in range(1, 7)]
        player_start_pos = (WIDTH // 2, HEIGTH // 2)
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
            in_dev_mode = self.mode_at_start
        )
        surf = graphics['objects'][10]
        scaled_surf = pygame.transform.scale(surf, (320, 320))
        Tile(self.blood_moon_pos,[self.visible_sprites],'bloodmoon',scaled_surf)
        self.generate_tiles_around_player()

    def generate_tiles_around_player(self):
        player_x, player_y = self.player.rect.centerx, self.player.rect.centery
        player_tile_x, player_tile_y = player_x // self.ground_tile_width, player_y // self.ground_tile_height
        radius = 2  # Number of tiles around the player to generate

        for x in range(player_tile_x - radius, player_tile_x + radius + 1):
            for y in range(player_tile_y - radius, player_tile_y + radius + 1):
                if (x, y) not in self.tiles:
                    chosen_surf = choice(self.ground_images)
                    self.tiles[(x,y)] = GroundTile((x*self.ground_tile_width,y*self.ground_tile_height),[self.visible_sprites,self.ground_tiles],(x,y),chosen_surf)

    def remove_distant_tiles(self):
        player_tile_x = self.player.rect.centerx // self.ground_tile_width
        player_tile_y = self.player.rect.centery // self.ground_tile_height

        keys_to_remove = []
        for (x, y) in self.tiles.keys():
            if abs(player_tile_x - x) > 2 or abs(player_tile_y - y) > 2:
                keys_to_remove.append((x, y))

        for ground_tile in self.ground_tiles:
            if ground_tile.tile_id in keys_to_remove:
                ground_tile.kill()

        for key in keys_to_remove:
            del self.tiles[key]

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
        # exit_sprites = [sprite for sprite in self.obstacle_sprites if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'exit']
        # for exit_sprite in exit_sprites:
        #     # if self.player.hitbox.left == exit_sprite.hitbox.right and self.player.hitbox.top == exit_sprite.hitbox.top:
        #     if self.player.hitbox.colliderect(exit_sprite.hitbox):
        #         self.main_sound.stop()
        #         self.level_complete_status = True
        if (self.blood_moon_pos[0] - 32) <= self.player.rect.center[0] <= (self.blood_moon_pos[0] + 32) and (self.blood_moon_pos[1] - 32) <= self.player.rect.center[1] <= (self.blood_moon_pos[1] + 32):
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
            self.remove_distant_tiles()
            self.generate_tiles_around_player()
            self.visible_sprites.custom_draw(self.player)
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.player_defense_logic()
            self.player_climbing_logic()
            self.level_complete_update()
            self.ui.display(self.player)
            # debug(f"({self.player.rect.x},{self.player.rect.y}) | BMP: ({self.blood_moon_x},{self.blood_moon_y})" )

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self,bmp):
        # general setup of all the stuff we need
        # initialize parent class
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.blood_moon_pos = bmp
        # creating the floor
        self.floor_surf = pygame.image.load('graphics/tilemap/ground6/1.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0,0))

        self.fog_surface = pygame.Surface((640,360),pygame.SRCALPHA) 

    def calculate_alpha(self,distance):
        base_alpha = 230
        max_distance = 5000
        min_alpha = 0
        
        if distance >= max_distance:
            return 0
        
        alpha = round(base_alpha * (1 - (distance / max_distance)) ** 4)
        return min(max(alpha, min_alpha), base_alpha)

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
            if isinstance(sprite, GroundTile): 
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)

        # Draw cloud sprites last to ensure they are on top
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if not isinstance(sprite, GroundTile): 
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
        mask_offset_pos = player.rect.topleft - self.offset
        mask_image = player.mask.to_surface(setcolor=(36,45,67,200),unsetcolor=None)
        mask_image = mask_image.convert_alpha()
        self.display_surface.blit(mask_image,mask_offset_pos)

        player_vec = pygame.math.Vector2(player.rect.center)
        end_vec = pygame.math.Vector2(self.blood_moon_pos)
        distance = (player_vec - end_vec).magnitude()

        alpha = self.calculate_alpha(distance)
        self.fog_surface.fill((255,0,0,alpha))
        self.display_surface.blit(self.fog_surface, (0,0))
        # debug(f'A: {alpha} | Dist: {round(distance)}',x = 10, y = 320)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player, enemy_sprites)
