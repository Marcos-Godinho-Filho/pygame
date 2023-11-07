import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (100, 100)

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.img = pygame.image.load("mario.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect = self.img.get_rect()
        self.rect.center = (
            (width-self.img.get_width())/2,
            (height-self.img.get_height())/2
        )
        self.WIDTH = width
        self.HEIGHT = height


    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.HEIGHT:
            self.rect.bottom = self.HEIGHT

    
    def draw(self, surface):
        surface.blit(self.img, self.rect)