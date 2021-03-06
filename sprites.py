import pygame as pg
import pytweening as tween
import time
import pickle
from itertools import chain
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2
dead_data = ''
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2.0
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2.0
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2.0
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2.0
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def check_vicinity(sprite, group):
    return pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)

def get_dead_data():
    return dead_data

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.last_damage = 0
        self.health = PLAYER_HEALTH
        self.player_hud_step = 0
        self.player_hud_dir = 1
        self.idx = 0
        self.weapon = 'pistol'
        self.weapon_inventory = []
        self.weapon_inventory.append(self.weapon)
        self.clip =  WEAPONS[self.weapon]['bullet_mag']
        self.reload_time = 0
        self.reload = False
        self.tween = tween.easeInOutSine
        self.damaged = False
        self.equipped = False

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        if keys[pg.K_SPACE] and not self.reload:
            self.shoot()
        
        if keys[pg.K_TAB]:
            if not self.equipped:
                self.weapon = self.weapon_inventory[self.idx]
                self.clip = WEAPONS[self.weapon]['bullet_mag']
                self.idx = (self.idx + 1) % len(self.weapon_inventory)
                print(self.weapon)
            self.equipped = True
        else:
            self.equipped = False

    def shoot(self):
        now = pg.time.get_ticks()
        if self.clip <= 1:
            self.start = time.time()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.clip -= 1
            print(self.clip)
            self.last_shot = now
            dir = vec(1,0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def add_health(self, amt):
        self.health += amt
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def screen_flash(self, hurt_rect):
        fill = SCREEN_FLASH_RANGE * (self.tween(self.player_hud_step / SCREEN_FLASH_RANGE) - 0.5)
        self.player_hud_step += FLASH_SPEED
        if self.player_hud_step > SCREEN_FLASH_RANGE:
                self.player_hud_step = 0
                self.player_hud_dir *= -1
        return hurt_rect.fill((155, 0, 0, abs(fill)))

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def update(self):
        self.get_keys()
        if self.clip <= 0:
            self.reload = True
            print((time.time() - self.start))
            if time.time() - self.start > WEAPONS[self.weapon]['reload']:
                self.clip = WEAPONS[self.weapon]['bullet_mag']
                self.reload = False
            
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try: 
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags = pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False

            
        self.rect = self.image.get_rect()
        self.rect.center = self.pos 
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        
        collide_with_walls(self, self.game.walls, 'x')
        collide_with_walls(self, self.game.chests, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        collide_with_walls(self, self.game.chests, 'y')
        self.rect.center = self.hit_rect.center

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y, id):
        self.id = id
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.zombie_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) 
        self.hit_rect = ZOMBIE_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = ZOMBIE_HEALTH
        self.speed = choice(ZOMBIE_SPEED)
        self.target = game.player


    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def update(self):
        target_dist = self.target.pos - self.pos
        if self.health == 100:
            detect = DETECT_RADIUS
        else:
            detect = DETECT_RADIUS * 1.5
        if target_dist.length_squared() < detect**2:
            if random() < 0.0018:
                choice(self.game.zombie_moan_sounds).play()
            self.rot = target_dist.angle_to(vec(1,0))
            self.image = pg.transform.rotate(self.game.zombie_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            global dead_data
            dead_data += 'D,' + str(self.id) + ',False,\n' 
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            self.kill()

        

    def draw_health(self):
        if self.health > (int)(ZOMBIE_HEALTH * 6/10):
            col = GREEN
        elif self.health > (int)(ZOMBIE_HEALTH * 3/10):
            col = YELLOW
        else: 
            col = RED
        width = int(self.rect.width * self.health / ZOMBIE_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < ZOMBIE_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.rect.center = pos
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.8, 1.2)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage
    
    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATOIN:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type, id):
        self._layer = ITEMS_LAYER
        self.id = id
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        self.spawn_time = pg.time.get_ticks()
        self.pickup = False
    
    def update(self):
        # Bobbing motion
        if pg.time.get_ticks() - self.spawn_time > ITEM_PICKUP_DELAY:
            self.pickup = True
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
    
class Chest(pg.sprite.Sprite):
    def __init__(self, game, pos, type, id):
        self.groups = game.all_sprites, game.chests
        self.id = id
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = type
        self.game = game
        self.image = self.game.chest_images[0].copy()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.hit_rect = CHEST_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.chest_open = False
        

    def update(self):
        self.open_chest()
        if self.chest_open:
            self.image = self.game.chest_images[1]
        else:
            self.image = self.game.chest_images[0]
    
    def open_chest(self):
        hits = pg.sprite.spritecollide(self, self.game.player_group, False)
        if self.game.open:
            for hit in hits:
                if hit and not self.chest_open:
                    self.game.effects_sounds['chest_open'].play()
                    if self.type == None:
                        self.type = choice(ITEM_NAMES)
                    self.drop = Item(self.game, vec(self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), self.type, randint(1000,999999))
                    self.chest_open = True
        
class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.door_images[0]
        self.rect = self.image.get_rect().copy()
        self.rect.topright = (x+w,y)
        self.hit_rect = self.rect.copy()
        self.old_rect = self.hit_rect
        self.spawn_time = pg.time.get_ticks()
        self.open = False
    
    
    def update(self):
        if self.game.open:
            self.open_door()
            self.spawn_time = pg.time.get_ticks()
        if pg.time.get_ticks() - self.spawn_time > DOOR_CLOSE_DELAY:
            self.open = False
            self.rect = self.old_rect
            self.hit_rect = self.old_rect            
        
    def open_door(self):
        hits = pg.sprite.spritecollide(self, self.game.player_group, False)
        if hits and not self.open:
                self.rect = pg.Rect(0,0,0,0)
                self.hit_rect = pg.Rect(0,0,0,0)
                self.open = True
                

             
#OLD Wall
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.dungeon_wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE