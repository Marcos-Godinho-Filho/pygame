import random
import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width, height, difficulty):
        super().__init__()

        array = ["images/bowser.png", "images/super.png", "images/turtle.png", "images/magikoopa.png", "images/koopa_troopa.png"]
        self.img = pygame.image.load(array[random.randint(0, 4)]).convert_alpha()
        self.img = pygame.transform.scale(self.img, (50, 50 * self.img.get_height() / self.img.get_width()))
        
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

        self.difficulty = difficulty
    
        if self.way == 0 or self.way == 2:
            self.speed = random.randint(1, 3) * (1 + self.difficulty / 4)
        elif self.way == 1 or self.way == 3:
            self.speed = random.randint(-3, -1) * (1 + self.difficulty / 4)


    def update(self):
        if (self.way == 0 or self.way == 1):
            self.rect.move_ip(self.speed, 0)
        else:
            self.rect.move_ip(0, self.speed)

        if self.rect.left < 0 or self.rect.right > self.WIDTH:
            self.kill()


    def draw(self, surface):
        surface.blit(self.img, self.rect)
