# EK16B main.py
# Created by Jacob R. West
# Originally Created: 12/17/2023
# Last Updated: 12/17/2023

#module imports
import pygame
from random import randint
from sys import exit

# create functions
def display_score(end_time=None):
    if end_time is None:
        curtime = pygame.time.get_ticks() - start_time
    else:
        curtime = end_time - start_time
    current_time = curtime // 100
    score_surface = test_font.render(f'Score: {current_time}',False,(64,64,64))
    score_rect = score_surface.get_rect(midtop = (240,25))
    pygame.draw.rect(screen,'#C4A968',score_rect)
    screen.blit(score_surface,score_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 2
            if obstacle_rect.w == 11:
                screen.blit(bunny_surface,obstacle_rect)
            else:
                screen.blit(monk_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else: return []

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): 
                final_time = pygame.time.get_ticks()
                return False, final_time
    return True, 0
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

# creating background & npc surfaces & setting initial variables
bg_surface = pygame.image.load('graphics/bg_test.png').convert_alpha()
text_surface = test_font.render('Ellie Kemper: 16-Bit Edition', False, '#DE4E2A')
text_rect = text_surface.get_rect(midtop=(240, 25))

monk_surface = pygame.image.load('graphics/spr_monkey_l.png').convert_alpha()
bunny_surface = pygame.image.load('graphics/spr_bunny.png').convert_alpha()

obstacle_rect_list = []

# creating player surface
player_surface = pygame.image.load('graphics/spr_link.png').convert_alpha()
player_rect = player_surface.get_rect(topleft=(145,200))

# creating scaled player
player_scaled = pygame.transform.scale(player_surface,(64,64))
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
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    print('key down')
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    print('key up')
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                obstacle_rect_list.clear()
                player_rect = player_surface.get_rect(topleft=(145,200))
                start_time = pygame.time.get_ticks()
        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(monk_surface.get_rect(topleft=(randint(500,700),randint(100,300))))
            else:
                obstacle_rect_list.append(bunny_surface.get_rect(topleft=(randint(500,700),randint(100,300))))

    if game_active:
        # draw all our elements & update everything
        screen.blit(bg_surface,(0,0))

        # moving the player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] is True: player_rect.x -= 2
        if keys[pygame.K_RIGHT] is True: player_rect.x += 2
        if keys[pygame.K_UP] is True: player_rect.y -= 2
        if keys[pygame.K_DOWN] is True: player_rect.y += 2

        # creating boundaries for the map
        if player_rect.top < 0: player_rect.top = 0
        if player_rect.bottom >= 320: player_rect.bottom = 320
        if player_rect.left < 0: player_rect.left = 0
        if player_rect.right >= 480: player_rect.right = 480

        screen.blit(player_surface,player_rect)

        obstacle_rec_list = obstacle_movement(obstacle_rect_list)
    
        display_score()

        game_active, final_time = collisions(player_rect,obstacle_rect_list)

    else:
        screen.fill('#C4A968')
        screen.blit(player_scaled,player_scaled_rect)
        display_score(final_time)
        screen.blit(start_text_surface, start_text_rect)




    pygame.display.update()
    clock.tick(60) # setting maximum framerate to 60FPS