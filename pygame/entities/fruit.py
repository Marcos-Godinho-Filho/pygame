import random
import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (50, 50)

class Fruit(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, type: str):
        super().__init__()
        self.type: str = type
        src = ""
        if type == "hp":
            src = "images/strawberry.png"
        elif type == "explosion":
            src = "images/blueberry.png"
        elif type == "attack":
            src = "images/banana.png"
        self.img: pygame.Surface = pygame.image.load(src).convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect: pygame.Rect = self.img.get_rect()
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.up: bool = True
        self.c: int = 0
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


    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)
