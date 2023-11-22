import sys
import pygame
from game import Game
from pygame.locals import *

pygame.init()

FPS = 60
framesPerSec = pygame.time.Clock()

# fontes usadas no jogo
pygame.font.init()                        
SMALL_FONT = pygame.font.Font("fonts/SuperMario256.ttf", 28)
LARGE_FONT = pygame.font.Font("fonts/SuperMario256.ttf", 36)             

# cores usadas no jogo
BLUE = (0, 125, 200)
RED = (250, 30, 30)
YELLOW = (240, 210, 5)
WHITE = (250, 250, 250)

# dimensões do mapa
WIDTH = 1000
HEIGHT = 600

# superfície a ser desenhada
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("GAME")

# plano de fundo do jogo
img = pygame.image.load("images/background.png").convert_alpha()
img = pygame.transform.scale(img, (WIDTH, HEIGHT))


# escreve texto na tela
def write_in_screen(text: str, width: float, height: float, color: tuple = WHITE, font: pygame.font.Font = SMALL_FONT):
    txt = font.render(text, False, color) 
    DISPLAYSURF.blit(txt, (width, height))


# cria retângulo na tela (barras de status do jogador)
def create_rect(coord: tuple, width: int, height: int, color: tuple):
    rect = pygame.Rect(coord[0], coord[1], width, height)
    pygame.draw.rect(DISPLAYSURF, color, rect)


# atualiza a tela (coloca as imagens, escreve os atributos do jogador e variáveis do jogo)
def update_screen():
    DISPLAYSURF.blit(img, (0,0))

    # se o jogo ainda não começou, espera o jogador pressionar enter to start
    if not game.started:
        write_in_screen(f"Welcome to MARIO SHOOTING!", game.WIDTH/2 - 200, game.HEIGHT/2 - 50) 
        write_in_screen(f"Press [Enter] to start!", game.WIDTH/2 - 200, game.HEIGHT/2)

    # se não perdeu, escreve na tela o tempo de jogo, sua pontuação,
    # a dificuldade atual, sua vida e sua munição, bem como atualiza as posições dos inimigos
    if not game.lose and game.started:
        write_in_screen(f"Time: {game.counter}s", 50, 50)
        write_in_screen(f"SCORE: {game.points}", 50, 100)
        write_in_screen(f"DIFFICULTY: {game.difficulty}", 50, HEIGHT - 50)
        write_in_screen(f"LIFE: ", WIDTH - 325, 50, RED) 
        write_in_screen(f"FIRE: ", WIDTH - 325, 100, YELLOW) 

        # barras de vida e munição
        create_rect((WIDTH - 250, 50), game.PLAYER.hp * 20, 20, RED)

        create_rect((WIDTH - 250, 100), game.PLAYER.munition * 20, 20, YELLOW)
        
        # atualiza as entidades
        game.PLAYER.update()
        game.PLAYER.draw(DISPLAYSURF)
        for enemy in game.enemies:
            # antes de atualizar as sprites inimigas, atualiza a posição do jogador em cada inimigo, para que eles saibam onde persegui-lo
            enemy.update_player_coord(game.PLAYER.rect.center)

        game.all_sprites.update()
        for entity in game.all_sprites:
            entity.draw(DISPLAYSURF)

        # se shield está ativo, isso é informado ao jogador
        if game.shield:
            write_in_screen(f"SHIELD ON!", game.WIDTH/2 - 100, 50, color=BLUE, font=LARGE_FONT)
            create_rect((game.WIDTH/2 - 100, 100), (game.MAX_SHIELD - game.shield_counter) * 250/game.MAX_SHIELD, 20, BLUE)

        # se double score está ativo, isso é informado ao jogador
        elif game.double:
            write_in_screen(f"2x SCORE!", game.WIDTH/2 - 100, 50, color=YELLOW, font=LARGE_FONT)
            create_rect((game.WIDTH/2 - 100, 100), (game.MAX_DOUBLE - game.double_counter) * 250/game.MAX_DOUBLE, 20, YELLOW)

    # se jogador perdeu, escreve na tela o recorde, a pontuação e uma mensagem de restart
    if game.lose:
        if game.points > game.record:
            write_in_screen(f"NEW RECORD! Score: {game.points}", game.WIDTH/2 - 225, game.HEIGHT/2 - 100, color=YELLOW, font=LARGE_FONT)
        else:
            write_in_screen(f"GAME OVER! Score: {game.points}", game.WIDTH/2 - 225, game.HEIGHT/2 - 100, color=YELLOW, font=LARGE_FONT)

        write_in_screen(f"Record: {game.record}", game.WIDTH/2 - 100, game.HEIGHT/2 - 50)
        write_in_screen(f"Press [Enter] to restart", game.WIDTH/2 - 200, game.HEIGHT/2) 

    pygame.display.update()


# ícone do jogo
programIcon = pygame.image.load("images/mario.png").convert_alpha()
pygame.display.set_icon(programIcon)

# inicia um novo jogo
game = Game(WIDTH, HEIGHT)

running = True

while running:
    events = pygame.event.get()
    for event in events:
        # X para sair do jogo
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # ESC para sair do jogo
            if event.key == pygame.K_ESCAPE:
                running = False
            # Enter para iniciar e reiniciar
            if event.key == pygame.K_RETURN:
                if game.lose:
                    game.save_record()
                    game = Game(WIDTH, HEIGHT)

                if not game.started:
                    game.started = True

    # se não perdeu, trata os eventos e colisões
    if not game.lose and game.started:
        game.handle_events(events)
        game.handle_collisions()

    # atualiza a tela
    update_screen()

    # define o FPS
    framesPerSec.tick(FPS)

# quando o jogo termina, salva o recorde
game.save_record()

# sai do jogo e para o programa
pygame.quit()
sys.exit()
