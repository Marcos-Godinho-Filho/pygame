import random
import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (100, 100)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.img = pygame.image.load("bowser.png")
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE).convert_alpha()
        self.rect = self.img.get_rect()
        self.rect.center = (
            random.randint(0, width - 100),
            random.randint(0, height - 100)
        )
        self.speed = random.randint(-20, 20)
        self.WIDTH = width
        self.HEIGHT = height


    def update(self):
        self.rect.move_ip(self.speed, 0)
        self.rect.move_ip(0, self.speed)

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