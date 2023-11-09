import sys
import pygame
from enemy import Enemy
from fruit import Fruit
from player import Player
from pygame.locals import *

pygame.init()

FPS = 60
framesPerSec = pygame.time.Clock()

pygame.font.init()                           
FONT = pygame.font.SysFont("Monospace", 28, True, True)             

BLACK = (0, 0, 0)
WHITE = (230, 240, 250)

WIDTH = 1200
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2000)

counter = 0

UPDATECOUNTER = pygame.USEREVENT + 2
pygame.time.set_timer(UPDATECOUNTER, 1000)

points = 0

ADDFRUIT = pygame.USEREVENT + 3
pygame.time.set_timer(ADDFRUIT, 5000)

PLAYER = Player(WIDTH, HEIGHT)

enemies = pygame.sprite.Group()
fruits = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(PLAYER)

img = pygame.image.load("images/background.png").convert_alpha()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))


def add_enemy():
    new_enemy = Enemy(WIDTH, HEIGHT)
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)


def add_fruit():
    new_fruit = Fruit(WIDTH, HEIGHT)
    fruits.add(new_fruit)
    all_sprites.add(new_fruit)


def write_in_screen(text, width, height):
    txt = FONT.render(text, False, WHITE) 
    DISPLAYSURF.blit(txt, (width, height))


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
            add_enemy()
            add_enemy()

        elif event.type == UPDATECOUNTER:
            if not lose:         
                counter += 1

        elif event.type == ADDFRUIT:
            add_fruit()

    DISPLAYSURF.blit(img, (0,0))

    write_in_screen(f"Tempo: {counter}s", 50, 50)
    write_in_screen(f"Pontuação: {points}", 50, 60)

    for entity in all_sprites:
        entity.draw(DISPLAYSURF)

    if pygame.sprite.spritecollideany(PLAYER, enemies):
        PLAYER.kill()
        lose = True

    for f in fruits:
        if pygame.sprite.spritecollideany(PLAYER, f):
            f.kill()
            points += 1;

    if lose:
        write_in_screen(f"Você perdeu! Pontuação: {points}", (WIDTH/2, HEIGHT/2))
        write_in_screen(f"Pressione [ESC] para sair", WIDTH/2 - 5, HEIGHT/2) 

    enemies.update()
    fruits.update()
    PLAYER.update()

    pygame.display.update()
    framesPerSec.tick(FPS)

pygame.exit()
sys.quit()
