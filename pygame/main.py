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
        write_in_screen(f"Time: {game.counter}s", WIDTH - 200, 50)
        write_in_screen(f"SCORE: {game.points}", WIDTH - 200, 100)
        write_in_screen(f"DIFFICULTY: {game.difficulty}", WIDTH - 250, HEIGHT - 50)
        write_in_screen(f"LIFE: ", 50, 50, RED) 
        write_in_screen(f"FIRE: ", 50, 100, YELLOW) 

        rect = pygame.Rect(130, 50, game.PLAYER.hp * 20, 20)
        pygame.draw.rect(DISPLAYSURF, RED, rect)

        rect = pygame.Rect(130, 100, game.PLAYER.munition * 20, 20)
        pygame.draw.rect(DISPLAYSURF, YELLOW, rect)
       
        game.PLAYER.update()
        game.PLAYER.draw(DISPLAYSURF)
        for enemy in game.enemies:
            enemy.update_player_coord(game.PLAYER.rect.center)

    game.all_sprites.update()
    for entity in game.all_sprites:
        entity.draw(DISPLAYSURF)

    if game.shield:
        write_in_screen(f"SHIELD ACTIVE!", game.WIDTH/2 - 100, 50, color=BLUE, font=LARGE_FONT)
        rect = pygame.Rect(game.WIDTH/2 - 100, 100, (game.MAX_SHIELD - game.shield_counter) * 60, 20)
        pygame.draw.rect(DISPLAYSURF, BLUE, rect)

    elif game.double:
        write_in_screen(f"2x SCORE!", game.WIDTH/2 - 100, 50, color=YELLOW, font=LARGE_FONT)
        rect = pygame.Rect(game.WIDTH/2 - 100, 100, (game.MAX_DOUBLE - game.double_counter) * 60, 20)
        pygame.draw.rect(DISPLAYSURF, YELLOW, rect)

    if game.lose:
        if game.points > game.record:
            write_in_screen(f"NEW RECORD! Score: {game.points}", game.WIDTH/2 - 225, game.HEIGHT/2 - 100, color=YELLOW, font=LARGE_FONT)
        else:
            write_in_screen(f"GAME OVER! Score: {game.points}", game.WIDTH/2 - 225, game.HEIGHT/2 - 100, color=YELLOW, font=LARGE_FONT)

        write_in_screen(f"Record: {game.record}", game.WIDTH/2 - 100, game.HEIGHT/2 - 50)
        write_in_screen(f"Press [Enter] to restart", game.WIDTH/2 - 200, game.HEIGHT/2) 

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
            if event.key == pygame.K_RETURN:
                if game.lose:
                    game.save_record()
                    game = Game(WIDTH, HEIGHT)

    if not game.lose:
        game.handle_events(events)
        game.handle_collisions()

    update_screen()

    pygame.display.update()
    framesPerSec.tick(FPS)

game.save_record()

pygame.quit()
sys.exit()
