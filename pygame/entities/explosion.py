import random
import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (50, 50)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.type: str = type
        self.current_img = 9
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.up: bool = True
        self.c: int = 0
        self.update_img()
        
    
    def update(self):
        self.c += 1
        if (self.c == 5):
            self.c = 0
            self.update_img()


    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

    
    def update_img(self):
        if self.current_img == 1:
            self.current_img = 9
            self.kill()
        self.current_img -= 1
        self.img: pygame.Surface = pygame.image.load(f"images/{self.current_img}.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect: pygame.Rect = self.img.get_rect()
        self.rect.center = (self.WIDTH, self.HEIGHT)
