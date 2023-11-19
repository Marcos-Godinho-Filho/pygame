import pygame
import pickle
from pygame.locals import *
from random import randint
from entities.player import Player
from entities.enemy import Enemy
from entities.item import Item
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
        self.MAX_SHIELD: int = 5
        self.shield_counter: int = 0
        self.double: bool = False
        self.MAX_DOUBLE: int = 5
        self.double_counter: int = 0

        self.events: dict = {}
        self.event_counter: int = pygame.USEREVENT + 1

        self.explosion_array = []
        for i in range(8, 0, -1):
            img = pygame.image.load(f"images/explosions/{i}.png").convert_alpha()
            img = pygame.transform.scale(img, (50, 50))
            self.explosion_array.append(img)

        array = ["bowser.png", "super.png", "turtle.png", "magikoopa.png", "koopa_troopa.png"]
        self.enemies_array = []
        for k in array:
            img = pygame.image.load("images/enemies/" + k).convert_alpha()
            self.enemies_array.append(img)

        self.add_events()


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

    
    def add_event(self, eventName: str):
        self.events[eventName] = self.event_counter
        self.event_counter += 1


    def add_timer(self, eventName: str, millis: int):
        pygame.time.set_timer(self.events[eventName], millis)


    def add_enemy(self):
        new_enemy = Enemy(self.WIDTH, self.HEIGHT, self.difficulty, self.PLAYER.rect.center, self.enemies_array)
        self.enemies.add(new_enemy)
        self.all_sprites.add(new_enemy)


    def add_item(self):
        x = randint(0, 7)
        new_item = 0
        if x == 0:
            new_item = Item(self.WIDTH, self.HEIGHT, "explosion")
        elif x == 1 or x == 2:
            new_item = Item(self.WIDTH, self.HEIGHT, "shield")
        elif x == 3 or x == 4:
            new_item = Item(self.WIDTH, self.HEIGHT, "double")
        elif x == 5:
            new_item = Item(self.WIDTH, self.HEIGHT, "points")
        else:
            new_item = Item(self.WIDTH, self.HEIGHT, "hp")
        self.fruits.add(new_item)
        self.all_sprites.add(new_item)

    
    def add_explosion(self, coord):
        new_explosion = Explosion(coord[0], coord[1], self.explosion_array)
        self.all_sprites.add(new_explosion)


    def add_bullet(self):
        new_shot = Shot((self.PLAYER.rect.center), (self.WIDTH, self.HEIGHT), self.PLAYER.way)
        self.shots.add(new_shot)
        self.all_sprites.add(new_shot)


    def update_player_hp(self, plus: int):
        self.PLAYER.hp += plus
        if self.PLAYER.hp > self.PLAYER.MAX_HP:
            self.PLAYER.hp = self.PLAYER.MAX_HP


    def update_player_munition(self, plus: int):
        self.PLAYER.munition += plus
        if self.PLAYER.munition > self.PLAYER.MAX_MUNITION:
            self.PLAYER.munition = self.PLAYER.MAX_MUNITION

    
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

            elif event.type == self.events["ADDITEM"]:
                self.add_item()

            elif event.type == self.events["UPDATECOUNTER"]:
                if not self.lose:
                    self.counter += 1
                    if self.shield:
                        self.shield_counter += 1
                    if self.double:
                        self.double_counter += 1

            elif event.type == self.events["UPDATEDIFFICULTY"]:
                self.difficulty += 1

            elif event.type == self.events["HEAL"]:
                self.update_player_hp(1)

            elif event.type == self.events["RECHARGEMUNITION"]:
                self.update_player_munition(1)

            elif event.type == self.events["DISABLESHIELD"]:
                self.shield = False
                self.shield_counter = 0

            elif event.type == self.events["DISABLEDOUBLE"]:
                self.double = False
                self.double_counter = 0


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
                            self.update_player_hp(3)
                            self.update_player_munition(3)
                        elif k.type == "explosion":
                            for j in self.enemies:
                                if not self.double:
                                    self.points += 1
                                else:
                                    self.points += 2
                                self.add_explosion(j.rect.center)
                                j.kill()
                        elif k.type == "shield":
                            self.shield = True
                            self.add_timer("DISABLESHIELD", self.MAX_SHIELD * 1000)
                        elif k.type == "points":
                            if not self.double:
                                self.points += 50
                            else:
                                self.points += 100
                        elif k.type == "double":
                            self.double = True
                            self.add_timer("DISABLEDOUBLE", self.MAX_DOUBLE * 1000)
                        k.kill()
                        if not self.double:
                            self.points += 3
                        else:
                            self.points += 6

        for j in self.enemies:
            if pygame.sprite.spritecollideany(j, self.shots):
                for k in self.shots:
                    if pygame.sprite.collide_rect(j, k):
                        j.kill()
                        k.c += 1
                        self.add_explosion(j.rect.center)
                        if (randint(0, 4) == 4):
                            self.update_player_hp(2)
                        if (randint(0, 4) == 4):
                            self.update_player_munition(2)
                        if not self.double:
                            self.points += 2
                        else:
                            self.points += 4


    def save_record(self):
        self.file = open(self.URL, "wb")
        if self.points > self.record:
            pickle.dump(self.points, self.file)
        else:
            pickle.dump(self.record, self.file)
        self.file.close()
