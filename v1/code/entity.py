import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self,speed):
        # we have to normalize the self.direction vector in order
        # to not make going diagonal be so much faster
        # the reason why we have this if statement is because if the vector
        # had a length of 0, the normalize would throw an error

        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == 'horizontal':
            # looping through every sprite in the obstacle sprite group
            # and checking to see if there is a collission
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # if moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # if moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # if moving down (remember increasing y is down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # if moving up
                        self.hitbox.top = sprite.hitbox.bottom