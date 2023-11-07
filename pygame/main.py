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
FONT = pygame.font.SysFont("Monospace", 15, True, True)             

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

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
            txt = FONT.render(f"Pontuação: {counter}", False, BLACK)  
            DISPLAYSURF.blit(txt, (50, 50)) 
            counter += 1

    DISPLAYSURF.fill(WHITE)

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