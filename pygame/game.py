import pygame
import pickle
from pygame.locals import *
from random import randint
from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item
from entities.explosion import Explosion
from entities.shot import Shot

# classe onde fica a lógica do jogo
class Game():
    def __init__(self, width: int, height: int):
        # dimensões do jogo
        self.WIDTH: int = width
        self.HEIGHT: int = height

        # sprites do jogo (player, inimigos, itens e tiros)
        self.PLAYER: Player = Player(self.WIDTH, self.HEIGHT)
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.items: pygame.sprite.Group = pygame.sprite.Group()
        self.shots: pygame.sprite.Group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        # atributos do jogo 
        self.points: int = 0
        self.counter: int = 0
        self.difficulty: int = 1
        self.collide_time: int = 0

        # arquivo binário de recorde
        self.URL: str = "record.dat"
        self.file = open(self.URL, mode="rb")
        self.record: int = 0
        try:
            self.record = pickle.load(self.file)
        except:
            self.record = 0
        self.file.close()

        # mais atributos do jogo
        self.lose: bool = False
        self.shield: bool = False
        self.MAX_SHIELD: int = 5
        self.shield_counter: int = 0
        self.double: bool = False
        self.MAX_DOUBLE: int = 5
        self.double_counter: int = 0

        # dicionário de eventos (com as keys sendo os nomes, e os valores os ids)
        self.events: dict = {}
        self.event_counter: int = pygame.USEREVENT + 1

        # array imagens de explosões
        self.explosion_array = []
        for i in range(8, 0, -1):
            img = pygame.image.load(f"images/explosions/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (50, 50))
            self.explosion_array.append(img)

        # array de imagens de inimigos
        array = ["super.png", "turtle.png", "magikoopa.png"]
        self.enemies_array = []
        for k in array:
            img = pygame.image.load("images/enemies/" + k).convert_alpha()
            self.enemies_array.append(img)

        # imagem de tiro
        self.shot_img: pygame.Surface = pygame.image.load("images/shot.png").convert_alpha()

        self.add_events()


    # função que adiciona os eventos do jogo e os timers para cada um
    def add_events(self):
        self.add_event("ADDENEMY")
        self.add_timer("ADDENEMY", 1000)

        self.add_event("ADDITEM")
        self.add_timer("ADDITEM", 5000)

        self.add_event("UPDATECOUNTER")
        self.add_timer("UPDATECOUNTER", 1000)

        self.add_event("UPDATEDIFFICULTY")
        self.add_timer("UPDATEDIFFICULTY", 15000)

        self.add_event("RECHARGEMUNITION")
        self.add_timer("RECHARGEMUNITION", 2000)

        self.add_event("HEAL")
        self.add_timer("HEAL", 7000)

        self.add_event("DISABLESHIELD")

        self.add_event("DISABLEDOUBLE")

    
    # função para adicionar o evento no dicionário 
    def add_event(self, eventName: str):
        self.events[eventName] = self.event_counter
        # atualizamos o id (como se fosse autoincremento)
        self.event_counter += 1


    # função para adicionar timer ao evento (de quanto em quanto tempo ele vai acontecer)
    def add_timer(self, eventName: str, millis: int):
        pygame.time.set_timer(self.events[eventName], millis)


    # função para adicionar inimigo 
    def add_enemy(self):
        new_enemy = Enemy(self.WIDTH, self.HEIGHT, self.difficulty, self.PLAYER.rect.center, self.enemies_array)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)


    # função para adiconar item (de forma aleatória, de diferentes tipos)
    def add_item(self):
        x = randint(0, 7)
        new_item = 0
        type: str = "explosion"
        
        if x == 1 or x == 2:
           type = "shield"
        elif x == 3 or x == 4:
           type = "double"
        elif x == 5:
            type = "points"
        else:
            type = "hp"

        new_item = Item(self.WIDTH, self.HEIGHT, type)
        self.items.add(new_item)
        self.all_sprites.add(new_item)

    
    # função para adicionar explosão (no local passado por parâmetro, que é onde o inimigo morreu)
    def add_explosion(self, coord):
        new_explosion = Explosion(coord[0], coord[1], self.explosion_array)
        self.all_sprites.add(new_explosion)


    # adiciona bala conforme a direção e posição do jogador no mapa
    def add_bullet(self):
        new_shot = Shot((self.PLAYER.rect.center), (self.WIDTH, self.HEIGHT), self.PLAYER.way, self.shot_img)
        self.shots.add(new_shot)
        self.all_sprites.add(new_shot)

    
    # função para lidar com os eventos (diferentes tipos)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                # espaço para atirar
                if event.key == pygame.K_SPACE:
                    # se a munição for maior que zero, o player atira
                    if self.PLAYER.munition > 0:
                        self.PLAYER.munition -= 1
                        self.add_bullet()

            # adiciona inimigos (quanto maior a dificuldade, mais inimigos são adicionados)
            if event.type == self.events["ADDENEMY"]:
                for i in range(0, int(1 + self.difficulty / 3)):
                    self.add_enemy()

            # adiciona um novo item
            elif event.type == self.events["ADDITEM"]:
                self.add_item()

            # atualiza os contadores de tempo de jogo, duração de escudo e duração e duplicador de pontos
            elif event.type == self.events["UPDATECOUNTER"]:
                if not self.lose:
                    self.counter += 1
                    if self.shield:
                        self.shield_counter += 1
                    if self.double:
                        self.double_counter += 1

            # atualiza a dificuldade do jogo
            elif event.type == self.events["UPDATEDIFFICULTY"]:
                self.difficulty += 1

            # cura o personagem
            elif event.type == self.events["HEAL"]:
                self.PLAYER.update_hp(1)

            # recarrega a munição do personagem
            elif event.type == self.events["RECHARGEMUNITION"]:
                self.PLAYER.update_munition(1)

            # desabilita o escudo
            elif event.type == self.events["DISABLESHIELD"]:
                self.shield = False
                self.shield_counter = 0

            # desabilita o duplicador de pontos
            elif event.type == self.events["DISABLEDOUBLE"]:
                self.double = False
                self.double_counter = 0

   
    # lida com colisões
    def handle_collisions(self):
        # colisões entre jogador e inimigo
        if pygame.sprite.spritecollideany(self.PLAYER, self.enemies):
            # delay para que o jogador não perca toda a vida de uma vez ao entrar em contato com um inimigo
            if self.collide_time < 10:
                self.collide_time += 1
            else:
                # se o jogador não está com escudo ativo, então ele leva dano
                if not self.shield:
                    self.PLAYER.hp -= 1
                    self.collide_time = 0
            # se vida do jogador zera, ele perde
            if self.PLAYER.hp == 0:
                self.PLAYER.kill()
                self.lose = True

        # colisões entre jogador e item
        if pygame.sprite.spritecollideany(self.PLAYER, self.items):
            for k in self.items:
                # se o jogador colidiu com aquele item
                if pygame.sprite.collide_rect(self.PLAYER, k):
                    if not self.lose:
                        # de acordo com o tipo de item, é feita uma ação diferente 
                        if k.type_img == "hp": # recupera vida e munição
                            self.PLAYER.update_hp(3)
                            self.PLAYER.update_munition(3)
                        elif k.type_img == "explosion": # mata todos os inimigos
                            for j in self.enemies:
                                if not self.double:
                                    self.points += 1
                                else:
                                    self.points += 2
                                self.add_explosion(j.rect.center)
                                j.kill()
                        elif k.type_img == "shield": # habilita escudo
                            self.shield = True
                            self.add_timer("DISABLESHIELD", self.MAX_SHIELD * 1000)
                        elif k.type_img == "points": # ganha pontos
                            if not self.double:
                                self.points += 50
                            else:
                                self.points += 100
                        elif k.type_img == "double": # habilita duplicador de pontos
                            self.double = True
                            self.add_timer("DISABLEDOUBLE", self.MAX_DOUBLE * 1000)
                        k.kill()
                        # toda vez que o player pega uma fruta, ele ganha pontos
                        if not self.double:
                            self.points += 3
                        else:
                            self.points += 6

        # colisões entre inimigos e tiros
        for j in self.enemies:
            if pygame.sprite.spritecollideany(j, self.shots):
                for k in self.shots:
                    if pygame.sprite.collide_rect(j, k):
                        j.kill()
                        k.c += 1
                        # exibe uma explosão depois de matar o inimigo que foi atingido pela bala
                        self.add_explosion(j.rect.center)
                        # há uma pequena chance de recuperar vida e munição depois de atingir um inimigo
                        if (randint(0, 4) == 4):
                            self.PLAYER.update_hp(2)
                        if (randint(0, 4) == 4):
                            self.PLAYER.update_munition(2)
                        if not self.double:
                            self.points += 2
                        else:
                            self.points += 4


    # salva o novo recorde (se há um novo) no arquivo
    def save_record(self):
        self.file = open(self.URL, "wb")
        if self.points > self.record:
            pickle.dump(self.points, self.file)
        else:
            pickle.dump(self.record, self.file)
        self.file.close()
