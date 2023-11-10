import sys
import pygame
from random import randint
from entities.enemy import Enemy
from entities.fruit import Fruit
from entities.player import Player
from pygame.locals import *

pygame.init()

FPS = 60
framesPerSec = pygame.time.Clock()

pygame.font.init()                           
FONT = pygame.font.SysFont("Monospace", 28, True, False)             

BLACK = (0, 0, 0)
BLUE = (30, 30, 250)
RED = (250, 30, 30)
WHITE = (230, 240, 250)

WIDTH = 1000
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

#events

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

points = 0

ADDFRUIT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDFRUIT, 5000)

counter = 0

UPDATECOUNTER = pygame.USEREVENT + 3
pygame.time.set_timer(UPDATECOUNTER, 1000)

difficulty = 1

UPDATEDIFICULTY = pygame.USEREVENT + 4
pygame.time.set_timer(UPDATEDIFICULTY, 15000)

DISABLESHIELD = pygame.USEREVENT + 5

#sprites

PLAYER = Player(WIDTH, HEIGHT)

c = 0

enemies = pygame.sprite.Group()
fruits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(PLAYER)

img = pygame.image.load("images/background.png").convert_alpha()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))

#useful functions

def add_enemy():
    new_enemy = Enemy(WIDTH, HEIGHT)
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)


def add_fruit():
    x = randint(0, 3)
    new_fruit = 0
    if x == 0:
        new_fruit = Fruit(WIDTH, HEIGHT, "shield")
    else:
        new_fruit = Fruit(WIDTH, HEIGHT, "point")
    fruits.add(new_fruit)
    all_sprites.add(new_fruit)


def write_in_screen(text, width, height, color = WHITE):
    txt = FONT.render(text, False, color) 
    DISPLAYSURF.blit(txt, (width, height))


shield = False
def change_shield():
    global shield
    shield = False


#main

running = True
lose = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        elif event.type == pygame.QUIT:
            running = False

        elif event.type == ADDENEMY:
            for i in range(0, difficulty):
                add_enemy()

        elif event.type == ADDFRUIT:
            add_fruit()

        elif event.type == UPDATECOUNTER:
            if not lose:         
                counter += 1

        elif event.type == UPDATEDIFICULTY:
            difficulty += 1

        elif event.type == DISABLESHIELD:
            shield = False

    DISPLAYSURF.blit(img, (0,0))

    if not lose:
        write_in_screen(f"Tempo: {counter}s", 50, 50)
        write_in_screen(f"Pontuação: {points}", 50, 75, BLUE)
        write_in_screen(f"Vida: {PLAYER.hp}", 50, 100, RED)

    for entity in all_sprites:
        entity.draw(DISPLAYSURF)

    if pygame.sprite.spritecollideany(PLAYER, enemies):
        if c < 5:
            c += 1
        else:
            if not shield:
                PLAYER.hp -= 1
            c = 0
        if PLAYER.hp == 0:
            PLAYER.kill()
            lose = True

    if pygame.sprite.spritecollideany(PLAYER, fruits):
        for k in fruits:
            if pygame.sprite.collide_rect(PLAYER, k):
                if not lose:
                    if k.type == "point":
                        points += 3
                    elif k.type == "shield":
                        points += 1
                        shield = True
                        pygame.time.set_timer(DISABLESHIELD, 1500)
                    k.kill()

    if shield:
        write_in_screen(f"Escudo ativo!", WIDTH/2 - 100, 20)

    if lose:
        write_in_screen(f"Você perdeu! Pontuação: {points}", WIDTH/2 - 200, HEIGHT/2 - 25)
        write_in_screen(f"Pressione [ESC] para sair", WIDTH/2 - 200, HEIGHT/2) 

    enemies.update()
    fruits.update()
    PLAYER.update()

    pygame.display.update()
    framesPerSec.tick(FPS)

pygame.exit()
sys.quit()
