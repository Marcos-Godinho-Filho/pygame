import random
import math
import pygame
from pygame.locals import *

# recebe a width e height do jogo, a dificuldade atual, as coordenadas do jogador e a array de imagens de inimigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, difficulty: int, player_coord: tuple, img_array: list):
        super().__init__()
        
        self.img = img_array[random.randint(0, 2)]
        size = random.randint(25, 75)
        self.img = pygame.transform.scale(self.img, (size, size * self.img.get_height() / self.img.get_width()))
        self.rect: pygame.Rect = self.img.get_rect()

        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.player_coord: tuple = player_coord

        # define onde o inimigo vai nascer (topo, embaixo, esquerda e direita)
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
        
        # inimigos ficam mais rápidos conforme a dificuldade
        speed = 1 + random.randint(0, int(self.difficulty / 5))

        # inimigo se move em direção ao jogador
        if self.player_coord != self.rect.center:
            # distância entre o inimigo e o jogador na width
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
            
            # distância entre o inimigo e o jogador na height
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


    # desenha o inimigo na surface
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

    
    # atualiza as coordenadas do jogador para que o inimigo sempre ande em direção a ele
    def update_player_coord(self, player_coord: tuple):
        self.player_coord = player_coord
