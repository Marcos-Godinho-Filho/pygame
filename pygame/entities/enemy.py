import random
import math
import pygame
from pygame.locals import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, difficulty: int, player_coord: tuple, img_array: list):
        super().__init__()
        
        self.img = img_array[random.randint(0, 4)]
        size = random.randint(25, 75)
        self.img = pygame.transform.scale(self.img, (size, size * self.img.get_height() / self.img.get_width()))
        self.rect: pygame.Rect = self.img.get_rect()

        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.player_coord: tuple = player_coord

        self.way: int = random.randint(0, 3)

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

        self.difficulty: int = difficulty


    def update(self):
        width = 0
        height = 0
        
        speed = 1 + random.randint(0, int(self.difficulty / 5))

        if self.player_coord != self.rect.center:
            dif: int = math.fabs(self.player_coord[0] - self.rect.center[0])
            is_enemy_left: bool = self.player_coord[0] > self.rect.center[0]
            if dif < speed:
                if is_enemy_left:
                    width = dif
                else:
                    width = -dif
            else:
                if is_enemy_left:
                    width = speed
                else:
                    width = -speed
            
            dif: int = math.fabs(self.player_coord[1] - self.rect.center[1])
            is_enemy_up: bool = self.player_coord[1] > self.rect.center[1]
            if dif < speed:
                if is_enemy_up:
                    height = dif
                else:
                    height = -dif
            else:
                if is_enemy_up:
                    height = speed
                else:
                    height = -speed

        self.rect.move_ip(width, height)

        if self.rect.left < 0 or self.rect.right > self.WIDTH or self.rect.top < 0 or self.rect.bottom > self.HEIGHT:
            self.kill()


    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

    
    def update_player_coord(self, player_coord: tuple):
        self.player_coord = player_coord
