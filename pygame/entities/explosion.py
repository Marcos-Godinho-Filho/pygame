import random
import pygame
from pygame.locals import *

# recebe as dimensões da tela do jogo e a array de imagens 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, img_array: list):
        super().__init__()
        self.type: str = type
        self.current_img = 9
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.img_array = img_array

        # atualiza a imagem
        self.c: int = 0
        self.update_img()
        
    
    # usa a variável c como um contador (ou delay)
    def update(self):
        self.c += 1
        if (self.c == 5):
            self.c = 0
            self.update_img()


    # desenha na surface
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

    
    # atualiza a imagem com base na array 
    def update_img(self):
        if self.current_img == 1:
            self.current_img = 9
            self.kill()
        self.current_img -= 1
        self.img: pygame.Surface = self.img_array[self.current_img-1]
        self.rect: pygame.Rect = self.img.get_rect()
        self.rect.center = (self.WIDTH, self.HEIGHT)
