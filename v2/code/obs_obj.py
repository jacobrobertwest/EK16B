import pygame

class ObstacleObject(pygame.sprite.Sprite):
    OBJ_COUNT = 0
    def __init__(self, groups, data, surf=None):
        super().__init__(groups)
        ObstacleObject.OBJ_COUNT += 1
        self.id = ObstacleObject.OBJ_COUNT
        self.topleft = pygame.Vector2(data['topleft'][0], data['topleft'][1])
        self.bottomright = pygame.Vector2(data['bottomright'][0], data['bottomright'][1])
        self.color = data['color']
        self.size = (data['size'][0], data['size'][1])
        if surf:
            self.surface = surf
        else:
            self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

    def update(self, offset_pos, display_surf):
        self.rect = self.surface.get_rect(topleft=(pygame.Vector2(self.topleft) + pygame.Vector2(offset_pos)))
        display_surf.blit(self.surface,self.rect)

    