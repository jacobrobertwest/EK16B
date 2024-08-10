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


class BaseLevel:
    def __init__(self,health,in_dev_mode):
        self.display_surface = pygame.display.get_surface()
        self.player_health = health
        self.mode_at_start = in_dev_mode