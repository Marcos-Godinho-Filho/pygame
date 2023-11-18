import pygame
import pickle
from pygame.locals import *
from random import randint
from entities.player import Player
from entities.enemy import Enemy
from entities.fruit import Fruit
from entities.explosion import Explosion
from entities.shot import Shot

class Game():
    def __init__(self, width: int, height: int):
        self.WIDTH: int = width
        self.HEIGHT: int = height

        self.PLAYER: Player = Player(self.WIDTH, self.HEIGHT)
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.fruits: pygame.sprite.Group = pygame.sprite.Group()
        self.shots: pygame.sprite.Group = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.points: int = 0
        self.counter: int = 0
        self.difficulty: int = 1
        self.collide_time: int = 0
        self.URL: str = "record.dat"
        self.file = open(self.URL, mode="rb")
        self.record: int = 0
        try:
            self.record = pickle.load(self.file)
        except:
            self.record = 0
        self.file.close()
        self.lose: bool = False
        self.shield: bool = False
        self.events: dict = {}
        self.event_counter: int = pygame.USEREVENT + 1

        self.img_array = []
        for i in range(8, 0, -1):
            img = pygame.image.load(f"images/{i}.png").convert_alpha()
            self.img_array.append(img)

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

        self.add_event("RECHARGEMUNITION")
        self.add_timer("RECHARGEMUNITION", 7500)

        self.add_event("DISABLESHIELD")

        self.add_event("DISABLEDAMAGEICON")

    
    def add_event(self, eventName: str):
        self.events[eventName] = self.event_counter
        self.event_counter += 1


    def add_timer(self, eventName: str, millis: int):
        pygame.time.set_timer(self.events[eventName], millis)


    def add_enemy(self):
        new_enemy = Enemy(self.WIDTH, self.HEIGHT, self.difficulty, self.PLAYER.rect.center)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)


    def add_fruit(self):
        x = randint(0, 4)
        new_fruit = 0
        if x == 0:
            new_fruit = Fruit(self.WIDTH, self.HEIGHT, "explosion")
        elif x == 1 or x == 2:
            new_fruit = Fruit(self.WIDTH, self.HEIGHT, "shield")
        else:
            new_fruit = Fruit(self.WIDTH, self.HEIGHT, "hp")
        self.fruits.add(new_fruit)
        self.all_sprites.add(new_fruit)

    
    def add_explosion(self, coord):
        new_explosion = Explosion(coord[0], coord[1], self.img_array)
        self.all_sprites.add(new_explosion)


    def add_bullet(self):
        new_shot = Shot((self.PLAYER.rect.center), (self.WIDTH, self.HEIGHT), self.PLAYER.way)
        self.shots.add(new_shot)
        self.all_sprites.add(new_shot)

    
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.PLAYER.munition > 0:
                        self.PLAYER.munition -= 1
                        self.add_bullet()

            if event.type == self.events["ADDENEMY"]:
                for i in range(0, int(1 + self.difficulty / 3)):
                    self.add_enemy()

            elif event.type == self.events["ADDFRUIT"]:
                self.add_fruit()

            elif event.type == self.events["UPDATECOUNTER"]:
                if not self.lose:         
                    self.counter += 1

            elif event.type == self.events["UPDATEDIFFICULTY"]:
                self.difficulty += 1

            elif event.type == self.events["RECHARGEMUNITION"]:
                self.PLAYER.munition += 10 - self.PLAYER.munition

            elif event.type == self.events["DISABLESHIELD"]:
                self.shield = False


    def handle_collisions(self):
        if pygame.sprite.spritecollideany(self.PLAYER, self.enemies):
            if self.collide_time < 10:
                self.collide_time += 1
            else:
                if not self.shield:
                    self.PLAYER.hp -= 1
                    self.collide_time = 0
            if self.PLAYER.hp == 0:
                self.PLAYER.kill()
                self.lose = True

        if pygame.sprite.spritecollideany(self.PLAYER, self.fruits):
            for k in self.fruits:
                if pygame.sprite.collide_rect(self.PLAYER, k):
                    if not self.lose:
                        if k.type == "hp":
                            self.PLAYER.hp += 3
                            if self.PLAYER.hp > 10:
                                self.PLAYER.hp = 10 
                        elif k.type == "explosion":
                            for j in self.enemies:
                                self.points += 1
                                self.PLAYER.munition = 10
                                self.add_explosion(j.rect.center)
                                j.kill()
                        elif k.type == "shield":
                            self.shield = True
                            self.add_timer("DISABLESHIELD", 3000)
                        k.kill()
                        self.points += 3

        for j in self.enemies:
            if pygame.sprite.spritecollideany(j, self.shots):
                for k in self.shots:
                    if pygame.sprite.collide_rect(j, k):
                        j.kill()
                        k.c += 1
                        self.add_explosion(j.rect.center)
                        self.points += 1


    def save_record(self):
        self.file = open(self.URL, "wb")
        if self.points > self.record:
            pickle.dump(self.points, self.file)
        else:
            pickle.dump(self.record, self.file)
        self.file.close()
