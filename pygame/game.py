import pygame
from pygame.locals import *
from random import randint
from entities.player import Player
from entities.enemy import Enemy
from entities.fruit import Fruit

class Game():
    def __init__(self, width: int, height: int):
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.PLAYER: Player = Player(self.WIDTH, self.HEIGHT)
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.fruits: pygame.sprite.Group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.PLAYER)
        self.points: int = 0
        self.counter: int = 0
        self.difficulty: int = 1
        self.collide_time: int = 0
        self.FILE = open("record.dat", mode="wb+")
        self.record: int = 0
        if len(self.FILE.readlines()) != 0:
            self.FILE.seek(0)
            self.record = int.from_bytes(self.FILE.read(), "big") 
        self.lose: bool = False
        self.attack: bool = False
        self.shield: bool = False
        self.events: dict = {}
        self.event_counter: int = pygame.USEREVENT + 1
        self.add_events()


    def add_events(self):
        self.add_event("ADDENEMY")
        self.add_timer("ADDENEMY", 1000)

        self.add_event("ADDFRUIT")
        self.add_timer("ADDFRUIT", 5000)

        self.add_event("UPDATECOUNTER")
        self.add_timer("UPDATECOUNTER", 1000)

        self.add_event("UPDATEDIFFICULTY")
        self.add_timer("UPDATEDIFFICULTY", 15000)

        self.add_event("DISABLESHIELD")

        self.add_event("DISABLEATTACK")

        self.add_event("DISABLEDAMAGEICON")

    
    def add_event(self, eventName: str):
        self.events[eventName] = self.event_counter
        self.event_counter += 1


    def add_timer(self, eventName: str, millis: int):
        pygame.time.set_timer(self.events[eventName], millis)


    def add_enemy(self):
        new_enemy = Enemy(self.WIDTH, self.HEIGHT, self.difficulty)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)


    def add_fruit(self):
        x = randint(0, 3)
        new_fruit = 0
        if x == 0:
            new_fruit = Fruit(self.WIDTH, self.HEIGHT, "shield")
        elif x == 1:
            new_fruit = Fruit(self.WIDTH, self.HEIGHT, "attack")
        else:
            new_fruit = Fruit(self.WIDTH, self.HEIGHT, "hp")
        self.fruits.add(new_fruit)
        self.all_sprites.add(new_fruit)

    
    def handle_events(self, events):
        for event in events:
            if event.type == self.events["ADDENEMY"]:
                for i in range(0, int(1 + self.difficulty / 2)):
                    self.add_enemy()

            elif event.type == self.events["ADDFRUIT"]:
                self.add_fruit()

            elif event.type == self.events["UPDATECOUNTER"]:
                if not self.lose:         
                    self.counter += 1

            elif event.type == self.events["UPDATEDIFFICULTY"]:
                self.difficulty += 1

            elif event.type == self.events["DISABLESHIELD"]:
                self.shield = False

            elif event.type == self.events["DISABLEATTACK"]:
                self.attack = False


    def handle_collisions(self):
        if pygame.sprite.spritecollideany(self.PLAYER, self.enemies):
            if self.collide_time < 5:
                self.collide_time += 1
            else:
                if not self.shield:
                    if not self.attack:
                        self.PLAYER.hp -= 1
                    else:
                        for k in self.enemies:
                            if pygame.sprite.collide_rect(self.PLAYER, k):
                                self.points += 5
                                k.kill()
                self.collide_time = 0
            if self.PLAYER.hp == 0:
                self.PLAYER.kill()
                self.lose = True

        if pygame.sprite.spritecollideany(self.PLAYER, self.fruits):
            for k in self.fruits:
                if pygame.sprite.collide_rect(self.PLAYER, k):
                    if not self.lose:
                        if k.type == "hp":
                            self.PLAYER.hp += 1
                        elif k.type == "shield":
                            self.shield = True
                            self.add_timer("DISABLESHIELD", 1500)
                        elif k.type == "attack":
                            self.attack = True
                            self.add_timer("DISABLEATTACK", 1500)
                        k.kill()
                        self.points += 3


    def save_record(self):
        if self.points > self.record:
            self.record = self.points
            self.FILE.seek(0)
            a = bytearray([self.record])
            self.FILE.write(a)
            self.FILE.close()
