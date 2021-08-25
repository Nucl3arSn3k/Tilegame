import pygame
import pickle
from sprites import *
from main import *

def write_data(self):
        self.data = ''
        self.data += 'P,' + str((int)(self.player.pos.x)) + ',' + str((int)(self.player.pos.y)) + ',' + str((int)(self.player.rot)) + ',' + str((int)(self.player.health)) + ',' + str(self.player.weapon) + ',' + str(self.player.clip) + ',' + str(len(self.player.weapon_inventory)) + ',' + str(self.player.weapon_inventory) + ',\n'

        with open(self.map_save, 'wb') as savefile: 
            
            for sprite in self.mobs:
                if isinstance(sprite, Mob):
                    self.data += 'Z,' + str(sprite.id) + ',' + str((int)(sprite.pos.x)) + ',' + str((int)(sprite.pos.y)) + ',' + str((int)(sprite.rot)) + ',' + str((int)(sprite.health)) + ',\n'
            for sprite in self.items:   
                if isinstance(sprite, Item):
                    self.data += 'I,' + str(sprite.id) + ',\n'
            for sprite in self.chests:   
                if isinstance(sprite, Chest):
                    self.data += 'C,' + str(sprite.id) +  ',' + str(sprite.open) +',\n'
            pickle.dump(self.data, savefile)

def load_game(self):
        self.info = ''
        self.temp = ''
        load_inventory_num = False
        weapon_count = 0
        player = False
        zombie = False
        item = False
        chest = False
        with open(self.map_save, 'rb') as savefile:
            self.info = pickle.load(savefile)
        count = 0
        for element in range(0, len(self.info)):
            if player:
                if self.info[element] != ',':
                    if self.info[element] != '[' and self.info[element] != ']' and self.info[element] != "'" and self.info[element] != " ":
                        self.temp += self.info[element]
                else:
                    count += 1
                    if count == 2:
                        x = self.temp
                        self.temp = ''
                    if count == 3:
                        y = self.temp
                        self.temp = ''
                        self.player.pos = ((int)(x), (int)(y))
                    if count == 4:
                        self.player.rot = ((int)(self.temp))
                        self.temp = ''
                    if count == 5:
                        self.player.health = ((int)(self.temp))
                        self.temp = ''  
                    if count == 6:
                        self.player.weapon = self.temp 
                        # if self.temp != 'pistol':
                        #     self.player.weapon_inventory.append(self.temp)
                        self.temp = ''
                    if count == 7:
                        self.player.clip = ((int)(self.temp))
                        self.temp = ''
                    if count == 8:
                        if load_inventory_num == False:
                            weapon_num = ((int)(self.temp))
                            load_inventory_num = True
                            count = 7
                            self.temp = ''
                        else:
                            weapon_count += 1
                            count = 7
                            if self.temp != 'pistol':
                                self.player.weapon_inventory.append(self.temp) 
                            self.temp = ''
                            if weapon_count >= weapon_num:
                                self.temp = ''
                                count = 0
                                player = False   
            if self.info[element] == 'P':
                player = True
            if zombie:
                if self.info[element] != ',':
                    if self.info[element] != '[' and self.info[element] != ']' and self.info[element] != "'" and self.info[element] != " " and self.info[element] != "\n" and self.info[element] != "Z":
                        self.temp += self.info[element]
                else:
                    count += 1
                    if count == 2:
                        id = ((int)(self.temp))
                        print(id)
                        self.temp = ''
                    if count == 3:
                        x = self.temp
                        self.temp = ''
                    if count == 4:
                        y = self.temp
                        pos = vec((int)(x), (int)(y))
                        print(pos)
                        self.temp = ''
                    if count == 5:
                        print(self.temp)
                        rot = ((int)(self.temp))
                        self.temp = ''
                    if count == 6:
                        health = (int)(self.temp)
                        for sprite in self.all_sprites:
                            if isinstance(sprite, Mob) and sprite.id == id:
                                    sprite.pos = pos
                                    sprite.rot = rot
                                    sprite.health = health
                        self.temp = ''
                        count = 0
                        zombie = False
            if self.info[element] == 'Z':
                zombie = True
            
            if self.info[element] == 'I':
                item = True
            if self.info[element] == 'C':
                chest = True