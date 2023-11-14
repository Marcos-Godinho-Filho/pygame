import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (75, 75)

class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.img: pygame.Surface = pygame.image.load("images/mario.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect: pygame.Rect = self.img.get_rect()
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.rect.center = (
            (self.WIDTH - self.img.get_width())/2,
            (self.HEIGHT - self.img.get_height())/2
        )
        self.hp: int = 10


    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.rect.move_ip(0, -7)
        if pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.rect.move_ip(0, 7) 
        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-7, 0)
        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(7, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.HEIGHT:
            self.rect.bottom = self.HEIGHT

    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

    
    def set_img(self, img: pygame.Surface, width: int, height: int):
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect = self.img.get_rect()
        self.rect.center = (
            (self.WIDTH - width)/2,
            (self.HEIGHT - height)/2
        )
