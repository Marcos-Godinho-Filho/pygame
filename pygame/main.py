import sys
import pygame
from game import Game
from pygame.locals import *

pygame.init()

FPS = 60
framesPerSec = pygame.time.Clock()

pygame.font.init()                        
FONT = pygame.font.SysFont("Monospace", 28, True, False)             

BLUE = (100, 100, 250)
RED = (250, 30, 30)
WHITE = (230, 240, 250)

WIDTH = 1000
HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

img = pygame.image.load("images/background.png").convert_alpha()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))


#useful functions
def write_in_screen(text, width, height, color = WHITE):
    txt = FONT.render(text, False, color) 
    DISPLAYSURF.blit(txt, (width, height))


def update_screen():
    DISPLAYSURF.blit(img, (0,0))

    if not game.lose:
        write_in_screen(f"Tempo: {game.counter}s", 50, 50)
        write_in_screen(f"Pontuação: {game.points}", 50, 75, BLUE)
        write_in_screen(f"Vida: {game.PLAYER.hp}", 50, 100, RED)

    for entity in game.all_sprites:
        entity.draw(DISPLAYSURF)

    if game.shield:
        write_in_screen(f"Escudo ativo!", game.WIDTH/2 - 100, 20)

    if game.attack:
        write_in_screen(f"Ataque ativo!", game.WIDTH/2 - 100, 20)

    if game.lose:
        if game.points > game.record:
            write_in_screen(f"Novo recorde! Pontuação: {game.points}!", game.WIDTH/2 - 250, game.HEIGHT/2 - 25)
        else:
            write_in_screen(f"Fim de jogo! Pontuação: {game.points}", game.WIDTH/2 - 250, game.HEIGHT/2 - 25)
        write_in_screen(f"Pressione [Espaço] para reiniciar", game.WIDTH/2 - 250, game.HEIGHT/2) 

    game.enemies.update()
    game.fruits.update()
    game.PLAYER.update()


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
