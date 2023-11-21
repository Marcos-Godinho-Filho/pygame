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

    # se não perdeu, escreve na tela o tempo de jogo, sua pontuação,
    # a dificuldade atual, sua vida e sua munição, bem como atualiza as posições dos inimigos
    if not game.lose:
        write_in_screen(f"Time: {game.counter}s", WIDTH - 200, 50)
        write_in_screen(f"SCORE: {game.points}", WIDTH - 200, 100)
        write_in_screen(f"DIFFICULTY: {game.difficulty}", WIDTH - 250, HEIGHT - 50)
        write_in_screen(f"LIFE: ", 50, 50, RED) 
        write_in_screen(f"FIRE: ", 50, 100, YELLOW) 

        # barras de vida e munição
        create_rect((130, 50), game.PLAYER.hp * 20, 20, RED)

        create_rect((130, 100), game.PLAYER.munition * 20, 20, YELLOW)
        
        game.PLAYER.update()
        game.PLAYER.draw(DISPLAYSURF)
        for enemy in game.enemies:
            enemy.update_player_coord(game.PLAYER.rect.center)

    game.all_sprites.update()
    for entity in game.all_sprites:
        entity.draw(DISPLAYSURF)

    # se shield está ativo, isso é informado ao jogador
    if game.shield:
        write_in_screen(f"SHIELD ACTIVE!", game.WIDTH/2 - 100, 50, color=BLUE, font=LARGE_FONT)
        create_rect((game.WIDTH/2 - 100, 100), (game.MAX_SHIELD - game.shield_counter) * 300/game.MAX_SHIELD, 20, BLUE)

    # se double score está ativo, isso é informado ao jogador
    elif game.double:
        write_in_screen(f"2x SCORE!", game.WIDTH/2 - 100, 50, color=YELLOW, font=LARGE_FONT)
        create_rect((game.WIDTH/2 - 100, 100), (game.MAX_DOUBLE - game.double_counter) * 300/game.MAX_DOUBLE, 20, YELLOW)

    # se jogador perdeu, escreve na tela o recorde, a pontuação e uma mensagem de restart
    if game.lose:
        if game.points > game.record:
            write_in_screen(f"NEW RECORD! Score: {game.points}", game.WIDTH/2 - 225, game.HEIGHT/2 - 100, color=YELLOW, font=LARGE_FONT)
        else:
            write_in_screen(f"GAME OVER! Score: {game.points}", game.WIDTH/2 - 225, game.HEIGHT/2 - 100, color=YELLOW, font=LARGE_FONT)

        write_in_screen(f"Record: {game.record}", game.WIDTH/2 - 100, game.HEIGHT/2 - 50)
        write_in_screen(f"Press [Enter] to restart", game.WIDTH/2 - 200, game.HEIGHT/2) 


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
            # Enter para reiniciar
            if event.key == pygame.K_RETURN:
                if game.lose:
                    game.save_record()
                    game = Game(WIDTH, HEIGHT)

    # se não perdeu, trata os eventos e colisões
    if not game.lose:
        game.handle_events(events)
        game.handle_collisions()

    # atualiza a tela
    update_screen()

    # define o FPS
    pygame.display.update()
    framesPerSec.tick(FPS)

# quando o jogo termina, salva o recorde
game.save_record()

# sai do jogo
pygame.quit()
sys.exit()
