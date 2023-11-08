import sys
import pygame
from pygame import font
from enemy import Enemy
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

PLAYER = Player(WIDTH, HEIGHT)

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(PLAYER)

img = pygame.image.load("images/background.png").convert_alpha()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))


def add_enemy():
    new_enemy = Enemy(WIDTH, HEIGHT)
    enemies.add(new_enemy)
    all_sprites.add(new_enemy)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

        if event.type == ADDENEMY:
            add_enemy()
            add_enemy()

        if event.type == UPDATECOUNTER:         
            counter += 1

    DISPLAYSURF.blit(img, (0,0))

    txt = FONT.render(f"Pontuação: {counter}", False, WHITE)  
    DISPLAYSURF.blit(txt, (50, 50)) 

    for entity in all_sprites:
        entity.draw(DISPLAYSURF)

    if pygame.sprite.spritecollideany(PLAYER, enemies):
        PLAYER.kill()
        running = False

    enemies.update()
    PLAYER.update()

    pygame.display.update()
    framesPerSec.tick(FPS)

pygame.exit()
sys.quit()