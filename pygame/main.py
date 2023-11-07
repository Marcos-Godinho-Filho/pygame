import sys
import pygame
from player import Player
from pygame.locals import *

pygame.init()

FPS = 60
framesPerSec = pygame.time.Clock()

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

WIDTH = 600
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

PLAYER = Player(WIDTH, HEIGHT)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

    DISPLAYSURF.fill(WHITE)

    PLAYER.update()
    PLAYER.draw(DISPLAYSURF)

    pygame.display.update()
    framesPerSec.tick(FPS)

pygame.exit()
sys.quit()