import random
import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (50, 50)

class Fruit(pygame.sprite.Sprite):
    def __init__(self, width, height, type):
        super().__init__()
        self.type = type
        src = ""
        if type == "hp":
            src = "images/strawberry.png"
        elif type == "shield":
            src = "images/blueberry.png"
        self.img = pygame.image.load(src).convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect = self.img.get_rect()
        self.WIDTH = width
        self.HEIGHT = height
        self.up = True
        self.c = 0
        self.rect.center = (
                random.randint(5, self.WIDTH - self.img.get_width()), 
                random.randint(5, self.HEIGHT - self.img.get_height())
            )
        
    
    def update(self):
        self.c += 1
        if (self.up):
            self.rect.move_ip(0, -1)
        else:
            self.rect.move_ip(0, 1)
        if (self.c == 5):
            if (self.up):
                self.up = False
            else:
                self.up = True
            self.c = 0


    def draw(self, surface):
        surface.blit(self.img, self.rect)
