# EK16B main.py
# Created by Jacob R. West
# Originally Created: 12/17/2023
# Last Updated: 12/17/2023

#module imports
import pygame
from random import randint, choice
from sys import exit

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_surface_w1 = pygame.image.load('graphics/spr_link.png').convert_alpha()
        player_surface_w2 = pygame.image.load('graphics/spr_link_2.png').convert_alpha()
        self.player_walk = [player_surface_w1, player_surface_w2]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.rect.x = 100
        self.rect.y = 200

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] is True: self.rect.x -= 2
        if keys[pygame.K_RIGHT] is True: self.rect.x += 2
        if keys[pygame.K_UP] is True: self.rect.y -= 2
        if keys[pygame.K_DOWN] is True: self.rect.y += 2
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom >= 320: self.rect.bottom = 320
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right >= 480: self.rect.right = 480

    def animation_state(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] is True or keys[pygame.K_RIGHT] is True or keys[pygame.K_DOWN] is True or keys[pygame.K_UP] is True:
            self.player_index += 0.05
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'monkey':
            self.frame_1 = pygame.image.load('graphics/spr_monkey_l.png').convert_alpha()
            self.frame_2 = pygame.image.load('graphics/spr_monkey_r.png').convert_alpha()
        elif type == 'bunny':
            self.frame_1 = pygame.image.load('graphics/spr_bunny.png').convert_alpha()
            self.frame_2 = pygame.image.load('graphics/spr_bunny_2.png').convert_alpha()
        self.frames = [self.frame_1, self.frame_2]
        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft=(randint(500,700),randint(100,300)))

    def animation_state(self):
        self.animation_index += 0.075
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 2
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

# create functions
def display_score():
    curtime = pygame.time.get_ticks() - start_time
    current_time = curtime // 100
    score_surface = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(midtop = (240,25))
    pygame.draw.rect(screen,'#C4A968',score_rect)
    screen.blit(score_surface,score_rect)
    return current_time

    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                final_time = pygame.time.get_ticks()
                return False, final_time
    return True, 0

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else: return True

# initializing pygame & setting up the screen
pygame.init()
screen_width = 480
screen_height = 320
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('ELLIE KEMPER: 16-Bit Edition')
pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/AncientModernTales.ttf',30)
game_active = True
start_time = 0

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# creating background & npc surfaces & setting initial variables
bg_surface = pygame.image.load('graphics/bg_test.png').convert_alpha()
text_surface = test_font.render('Ellie Kemper: 16-Bit Edition', False, '#DE4E2A')
text_rect = text_surface.get_rect(midtop=(240, 25))

# creating player surface
player_surface_w1 = pygame.image.load('graphics/spr_link.png').convert_alpha()

# creating scaled player
player_scaled = pygame.transform.scale(player_surface_w1,(64,64))
player_scaled_rect = player_scaled.get_rect(center=(240,160))

# creating press_start_text
start_text_surface = test_font.render('Ellie Kemper: 16-Bit Edition', False, '#DE4E2A')
start_text_rect = start_text_surface.get_rect(center=(240, 280))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

# the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['monkey', 'bunny', 'monkey', 'monkey'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.empty()
                game_active = True
                player = pygame.sprite.GroupSingle()
                player.add(Player())
                start_time = pygame.time.get_ticks()

    if game_active:
        # draw all our elements & update everything
        screen.blit(bg_surface,(0,0))

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()
    
        score = display_score()

    else:
        screen.fill('#C4A968')
        screen.blit(player_scaled,player_scaled_rect)
        screen.blit(start_text_surface, start_text_rect)
        final_score_surface = test_font.render(f'Final Score: {score}', False, (64,64,64))
        final_score_rect = final_score_surface.get_rect(midtop=(240,25))
        screen.blit(final_score_surface, final_score_rect)

    pygame.display.update()
    clock.tick(60) # setting maximum framerate to 60FPS