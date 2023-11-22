import random
import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (50, 50)

# recebe as dimensões da tela do jogo e o tipo de item 
class Item(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int, type_img: str):
        super().__init__()
        src = "images/items/"
        self.type_img = type_img

        # com base no tipo de item, muda a imagem
        if type_img == "hp": # item que recupera vida e munição
            src += "strawberry.png"
        elif type_img == "explosion": # item que explode inimigos
            src += "blueberry.png"
        elif type_img == "shield": # item que te deixa imune por um tempo
            src += "banana.png"
        elif type_img == "double": # item que duplica os pontso por um tempo
            src += "star.png"
        elif type_img == "points": # item que te dá pontos
            src += "coin.png"

        self.img: pygame.Surface = pygame.image.load(src).convert_alpha()
        self.img = pygame.transform.scale(self.img, DEFAULT_IMG_SIZE)
        self.rect: pygame.Rect = self.img.get_rect()

        self.WIDTH: int = width
        self.HEIGHT: int = height
        # variável up define se o item é para ir para cima ou para baixo
        self.up: bool = True
        # c: contador (ou delay)
        self.c: int = 0

        # o local onde o item vai surgir é definido aleatoriamente
        self.rect.center = (
            random.randint(5, self.WIDTH - self.img.get_width()), 
            random.randint(5, self.HEIGHT - self.img.get_height())
        )
        
    
    # atualiza a posição do item (de modo que ele fica indo para cima e para baixo)
    def update(self):
        self.c += 1
        if (self.up):
            self.rect.move_ip(0, -1)
        else:
            self.rect.move_ip(0, 1)
        if (self.c == 5):
            if (self.up):
                self.up = False
            else:
                self.up = True
            self.c = 0


    # desenha o item na surface
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)
