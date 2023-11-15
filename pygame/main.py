import sys
import pygame
from game import Game
from pygame.locals import *

pygame.init()

FPS = 60
framesPerSec = pygame.time.Clock()

pygame.font.init()                        
SMALL_FONT = pygame.font.Font("fonts/SuperMario256.ttf", 28)
LARGE_FONT = pygame.font.Font("fonts/SuperMario256.ttf", 36)             

BLUE = (0, 125, 200)
RED = (250, 30, 30)
YELLOW = (240, 210, 5)
WHITE = (250, 250, 250)

WIDTH = 1000
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

img = pygame.image.load("images/background.png").convert_alpha()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))


#useful functions
def write_in_screen(text: str, width: float, height: float, color: tuple = WHITE, font: pygame.font.Font = SMALL_FONT):
    txt = font.render(text, False, color) 
    DISPLAYSURF.blit(txt, (width, height))


def update_screen():
    DISPLAYSURF.blit(img, (0,0))

    if not game.lose:
        write_in_screen(f"Time: {game.counter}s", 50, 50)
        write_in_screen(f"SCORE: {game.points}", 50, 100, YELLOW)
        write_in_screen(f"LIFE: {game.PLAYER.hp}", 50, 150, RED) 

    for entity in game.all_sprites:
        entity.draw(DISPLAYSURF)

    if game.attack:
        write_in_screen(f"ATTACK!", game.WIDTH/2 - 50, 50, color=BLUE, font=LARGE_FONT)

    if game.lose:
        if game.points > game.record:
            write_in_screen(f"NEW RECORD! Score: {game.points}", game.WIDTH/2 - 250, game.HEIGHT/2 - 50, color=YELLOW, font=LARGE_FONT)
        else:
            write_in_screen(f"GAME OVER! Score: {game.points}", game.WIDTH/2 - 250, game.HEIGHT/2 - 50, font=LARGE_FONT)
        write_in_screen(f"Press [Space] to restart", game.WIDTH/2 - 200, game.HEIGHT/2) 

    game.all_sprites.update()


#main
programIcon = pygame.image.load("images/mario.png").convert_alpha()
pygame.display.set_icon(programIcon)

game = Game(WIDTH, HEIGHT)

running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                game.save_record()
                game = Game(WIDTH, HEIGHT)

    game.handle_events(events)

    game.handle_collisions()

    update_screen()

    pygame.display.update()
    framesPerSec.tick(FPS)

game.save_record()

pygame.quit()
sys.exit()
