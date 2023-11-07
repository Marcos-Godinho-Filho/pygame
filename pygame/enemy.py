import random
import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (75, 75)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.img = pygame.image.load("bowser.png")
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE).convert_alpha()
        self.rect = self.img.get_rect()
        self.WIDTH = width
        self.HEIGHT = height
        self.way = random.randint(0, 3)

        if (self.way == 0 or self.way == 1):
            self.rect.center = (
                self.img.get_width() + self.way * (self.WIDTH - 2 * self.img.get_width()), 
                random.randint(0, self.HEIGHT)
            )
        elif (self.way == 2 or self.way == 3):
            self.rect.center = (
                random.randint(0, self.WIDTH),
                self.img.get_height() + (self.way - 2) * (self.HEIGHT - 2 * self.img.get_height())
            )
    
        if self.way == 0 or self.way == 2:
            self.speed = random.randint(1, 5)
        elif self.way == 1 or self.way == 3:
            self.speed = random.randint(-5, -1)


    def update(self):
        if (self.way == 0 or self.way == 1):
            self.rect.move_ip(self.speed, 0)
        else:
            self.rect.move_ip(0, self.speed)

        if self.rect.left < 0 or self.rect.right > self.WIDTH:
            self.kill()


    def draw(self, surface):
        surface.blit(self.img, self.rect)