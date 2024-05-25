import pygame
import sys
from settings import *

class TitleScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.title_image = pygame.image.load('graphics/title.png')  # Path to your title screen image

    def display(self):
        self.screen.blit(self.title_image, (0, 0))
        pygame.display.update()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    running = False  # Exit the title screen loop on any key press
            self.display()
            self.clock.tick(FPS)  # Control the frame rate for the title screen
