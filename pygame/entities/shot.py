import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (75, 75)

class Shot(pygame.sprite.Sprite):
    def __init__(self, player_coord: tuple, game_coord: tuple, way: int):
        super().__init__()
        self.img: pygame.Surface = pygame.image.load("images/shot.png").convert_alpha()

        self.WAY: int = way
        if self.WAY == 0:
            self.img = pygame.transform.rotate(self.img, 90)
        if self.WAY == 2:
            self.img = pygame.transform.rotate(self.img, -90)
        if self.WAY == 3:
            self.img = pygame.transform.rotate(self.img, 180)

        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect: pygame.Rect = self.img.get_rect()

        self.GAME_WIDTH: int = game_coord[0]
        self.GAME_HEIGHT: int = game_coord[1]
        self.rect.center = player_coord

        self.c = 0


    def update(self):
        if self.c == 3:
            self.kill()

        speed: int = 10

        if self.WAY == 0:
            self.rect.move_ip(0, -speed)
        elif self.WAY == 1:
            self.rect.move_ip(speed, 0)
        elif self.WAY == 2:
            self.rect.move_ip(0, speed)
        elif self.WAY == 3:
            self.rect.move_ip(-speed, 0)

        if self.rect.left < 0 or self.rect.right > self.GAME_WIDTH or self.rect.top < 0 or self.rect.bottom > self.GAME_HEIGHT:
            self.kill()

    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)
