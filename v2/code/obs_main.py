import pygame
from obs_obj import ObstacleObject
import sys
from debug import debug
import os
import json

class Obstickle:
    def __init__(self):
        pygame.init()
        self.level_editing = 7
        self.level_floor_fp = 'graphics/tilemap/ground7-new.png'

        self.screen_size = (1400,800)
        self.screen = pygame.display.set_mode(self.screen_size,pygame.DOUBLEBUF)
        self.display_surface = pygame.display.get_surface()
        pygame.display.set_caption('EK16B - Obstickle')
        pygame.display.set_icon(pygame.image.load('graphics/logo_ek16b.png'))
        self.clock = pygame.time.Clock()
        self.level_floor_surf = pygame.image.load(self.level_floor_fp).convert()
        self.level_floor_rect = self.level_floor_surf.get_rect(topleft=(0,0))
        self.level_floor_size = self.level_floor_rect.bottomright
        self.frame_offset_bottomright = pygame.Vector2(self.screen_size)
        self.offset_pos = pygame.Vector2()
        
        self.mouse_edge_border = 25
        self.mouse_drag_speed = 10

        self.selecting = False
        self.saving = False
        self.hovering_over = False
        self.deleting = False
        self.has_selection = False
        self.selection_topleft = None
        self.selection_bottomright = None
        self.selection_surf = None
        self.selection_rect = None
        self.persist = []
        self.obstacle_group = pygame.sprite.Group()
        self.load_persist()

    def load_persist(self):
        fp = f'lvl{self.level_editing}_obstacles.json'
        if os.path.exists(fp):
            try:
                print('Found existing level obstacle file. Attempting to read...')
                with open(fp) as f:
                    self.persist = json.loads(f.read())['data']
                print('Loaded successfully.')
            except Exception as e:
                print(f'ERROR: {e}')
                pass
        else:
            print('Did not find existing level obstacle file. Proceeding...')
        for obj in self.persist:
            ObstacleObject([self.obstacle_group],obj)

    def handle_offset(self):
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[0] < self.mouse_edge_border:
            self.frame_offset_bottomright[0] = max(self.screen_size[0]-100,self.frame_offset_bottomright[0] - self.mouse_drag_speed)
        elif mouse_pos[0] > self.screen_size[0] - self.mouse_edge_border:
            self.frame_offset_bottomright[0] = min(self.level_floor_size[0]+100,self.frame_offset_bottomright[0] + self.mouse_drag_speed)
        elif mouse_pos[1] < self.mouse_edge_border:
            self.frame_offset_bottomright[1] = max(self.screen_size[1]-100,self.frame_offset_bottomright[1] - self.mouse_drag_speed)
        elif mouse_pos[1] > self.screen_size[1] - self.mouse_edge_border:
            self.frame_offset_bottomright[1] = min(self.level_floor_size[1]+100,self.frame_offset_bottomright[1] + self.mouse_drag_speed)
        
        self.offset_pos = self.screen_size - self.frame_offset_bottomright
    
    def show_selections(self):
        if self.selecting:
            self.selection_surf = pygame.Surface((abs(pygame.mouse.get_pos()[0] - (self.selection_topleft[0] + self.offset_pos[0])),abs(pygame.mouse.get_pos()[1] - (self.selection_topleft[1] + self.offset_pos[1]))))
            self.selection_surf.fill('gold')
            self.selection_rect = self.selection_surf.get_rect(topleft=(pygame.Vector2(self.selection_topleft) + pygame.Vector2(self.offset_pos)))
            self.display_surface.blit(self.selection_surf,self.selection_rect)
        else:
            if self.selection_bottomright:
                self.selection_surf = pygame.Surface(pygame.Vector2(self.selection_bottomright) - pygame.Vector2(self.selection_topleft))
                self.selection_surf.fill('gold')
                self.selection_rect = self.selection_surf.get_rect(topleft=(pygame.Vector2(self.selection_topleft) + pygame.Vector2(self.offset_pos)))
                self.display_surface.blit(self.selection_surf,self.selection_rect)

    
    def lock_selection(self):
        data = {
            "topleft": [int(self.selection_topleft.x), int(self.selection_topleft.y)],
            "bottomright": [int(self.selection_bottomright.x), int(self.selection_bottomright.y)],
            "size": [int(self.selection_bottomright.x)-int(self.selection_topleft.x), int(self.selection_bottomright.y)-int(self.selection_topleft.y)],
            "type": "standard",
            "color": "red"
        }
        obj = ObstacleObject([self.obstacle_group],data,self.selection_surf)
        data["id"] = obj.id
        self.persist.append(data)
        self.has_selection = False
        self.selection_topleft = None
        self.selection_bottomright = None

    def enforce_persist(self):
        self.obstacle_group.update(self.offset_pos, self.display_surface)

    def save_selections(self):
       with open(f'lvl{self.level_editing}_obstacles.json', 'w') as f:
           final_data = {"data":self.persist}
           json.dump(final_data, f, indent=4)

    def handle_hover(self):
        self.hovering_over = False
        self.hovered_over = []
        mouse_pos = pygame.mouse.get_pos()
        for obj in self.obstacle_group:
            if obj.rect.collidepoint(mouse_pos):
                self.hovering_over = True
                self.hovered_over.append(obj.id)


    def delete_obs(self):
        for obj in self.obstacle_group:
            if obj.id in self.hovered_over:
                obj.kill()
        self.persist = [d for d in self.persist if d['id'] not in self.hovered_over]

    def update_timers(self):
        if self.saving:
            if pygame.time.get_ticks() - self.save_start > 500:
                self.saving = False
        if self.deleting:
            if pygame.time.get_ticks() - self.delete_start > 500:
                self.deleting = False

    def run(self):
        while True: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        self.selecting = not self.selecting
                        if self.selecting:
                            self.has_selection = False
                            self.selection_bottomright = None
                            self.selection_topleft = pygame.Vector2(mouse_pos) - pygame.Vector2(self.offset_pos)
                        else:
                            self.selection_bottomright = pygame.Vector2(mouse_pos) - pygame.Vector2(self.offset_pos)
                            self.has_selection = True
                if event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_RETURN] and self.has_selection:
                        self.lock_selection()
                    if keys_pressed[pygame.K_ESCAPE] and not self.saving:
                        self.save_selections()
                        self.saving = True
                        self.save_start = pygame.time.get_ticks()
                    if keys_pressed[pygame.K_d] and self.hovering_over and not self.deleting:
                        self.deleting = True
                        self.delete_start = pygame.time.get_ticks()
                        self.delete_obs()

            self.screen.fill('black')
            self.handle_offset()
            self.display_surface.blit(self.level_floor_surf,self.offset_pos)
            self.show_selections()
            self.enforce_persist()
            self.handle_hover()
            self.update_timers()
            self.clock.tick(60)
            debug(pygame.mouse.get_pos())
            debug(self.selecting,mult=2)
            debug(self.selection_topleft,mult=3)
            debug(self.selection_bottomright,mult=4)
            debug(self.has_selection,mult=6)
            # debug(self.frame_offset_bottomright,10,40)
            debug(self.offset_pos,mult=5)
            debug(self.saving, mult=8)
            debug(self.hovering_over, mult = 10)
            debug(self.hovered_over, mult = 12)
            pygame.display.update()

if __name__ == '__main__':
    Obstickle().run()
        
    