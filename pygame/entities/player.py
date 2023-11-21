import pygame
from pygame.locals import *

DEFAULT_IMG_SIZE = (75, 75)

# recebe as dimensões da tela do jogo
class Player(pygame.sprite.Sprite):
    def __init__(self, width: int, height: int):
        super().__init__()

        # array de imagens do player
        array = ["down_1", "down_2", "horizontal_1", "horizontal_2", "stopped", "up_1", "up_2"]
        self.imgs: list = []
        for k in array:
            img = pygame.image.load(f"images/mario/{k}.png").convert_alpha()
            img = pygame.transform.scale(img, DEFAULT_IMG_SIZE)
            self.imgs.append(img)

        self.WIDTH: int = width
        self.HEIGHT: int = height

        self.img: pygame.Surface
        self.rect: pygame.Rect = pygame.Rect(self.WIDTH/2, self.HEIGHT/2, DEFAULT_IMG_SIZE[0], DEFAULT_IMG_SIZE[1])
        # jogador inicia o jogo parado
        self.set_img(self.imgs[4])

        # munição e hp do jogador
        self.MAX_MUNITION = 10
        self.MAX_HP = 10

        self.hp: int = self.MAX_HP
        self.munition: int = self.MAX_MUNITION
        self.way = 0

        self.c = 0


    # atualiza a posição do jogador com base nas teclas pressionadas
    def update(self):
        speed: int = 7
        pressed_keys = pygame.key.get_pressed()

        self.c += 1
        if self.c == 5:
            self.c = 0

        if pressed_keys[K_UP] or pressed_keys[K_w]:
            self.way = 0
            self.set_img(self.imgs[5])
            self.rect.move_ip(0, -speed)

        elif pressed_keys[K_DOWN] or pressed_keys[K_s]:
            self.way = 2
            self.set_img(self.imgs[0])
            self.rect.move_ip(0, speed) 

        elif pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.way = 3
            self.set_img(self.imgs[2], flip=True)
            self.rect.move_ip(-speed, 0)

        elif pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.way = 1
            self.set_img(self.imgs[2])
            self.rect.move_ip(speed, 0)

        # se o jogador chegou nas bordas do mapa, ele morre
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.HEIGHT:
            self.rect.bottom = self.HEIGHT


    # desenha o player    
    def draw(self, surface: pygame.Surface):
        surface.blit(self.img, self.rect)

    
    # muda a imagem do player
    def set_img(self, img: pygame.Surface, flip=False):
        center = self.rect.center
        self.img = img
        if flip:
            self.img = pygame.transform.flip(self.img, True, False)
        self.rect = self.img.get_rect()
        self.rect.center = center


    # incrementa a vida do jogador (até o máximo de hp)
    def update_hp(self, plus: int):
        self.hp += plus
        if self.hp > self.MAX_HP:
            self.hp = self.MAX_HP


    # incrementa a munição do jogador (até o máximo de munição)
    def update_munition(self, plus: int):
        self.munition += plus
        if self.munition > self.MAX_MUNITION:
            self.munition = self.MAX_MUNITION
