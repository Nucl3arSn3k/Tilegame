import pygame as pg
import sys
import pickle
from os import path
from sprites import *
from settings import *
from tilemap import *
from gui import *
from save import *

# HUD functions
def draw_hud(self, surf, x, y, pct):
    hurt_rect = pg.Surface(self.screen.get_size()).convert_alpha()
    hurt_rect.fill((155, 0, 0, 20))
    self.tween = tween.easeInOutSine
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    # draws health bar
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
        self.screen.blit(hurt_rect, (0, 0))
    else:
        col = RED
        self.player.screen_flash(hurt_rect)
        self.screen.blit(hurt_rect, (0, 0))
    # draws gun
    xoffset = WIDTH - 100
    yoffset = 30
    bullet_size = "lg"
    if self.player.weapon == "shotgun":
        draw_weapon = pg.transform.scale(self.item_images[self.player.weapon], (80, 40))
        self.screen.blit(draw_weapon, (xoffset - 10, 60))
    elif self.player.weapon == "uzi":
        draw_weapon = pg.transform.scale(
            self.item_images[self.player.weapon], (100, 80)
        )
        self.screen.blit(draw_weapon, (xoffset - 10, 45))
    else:
        draw_weapon = pg.transform.scale(
            self.item_images[self.player.weapon], (100, 100)
        )
        self.screen.blit(draw_weapon, (xoffset - 20, 45))
    # draws bullets
    for x in range(0, self.player.clip):
        if yoffset >= 230:
            yoffset = 30
            xoffset -= 25
        self.screen.blit(self.bullet_images[bullet_size], (xoffset + 50, 100 + yoffset))
        yoffset += 25
    self.draw_text(
        "Zombies: {}".format(len(self.mobs)),
        self.hud_font,
        30,
        WHITE,
        WIDTH - 10,
        10,
        align="ne",
    )
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = getattr(sys, "_MEIPASS", path.abspath(path.dirname(__file__)))
        # game_folder = path.dirname('C:\\Users\\shado\\Documents\\Tutoring\\TileGame\\Tilegame\\')
        res_folder = path.abspath(path.join(game_folder, "res"))
        items_folder = path.abspath(path.join(res_folder, "items"))
        entity_folder = path.abspath(path.join(res_folder, "entities"))
        weapon_folder = path.abspath(path.join(res_folder, "weapons"))
        music_folder = path.abspath(path.join(res_folder, "music"))
        snd_folder = path.abspath(path.join(res_folder, "snd"))
        effects_folder = path.abspath(path.join(res_folder, "effects"))
        fonts_folder = path.abspath(path.join(res_folder, "fonts"))
        self.map_folder = path.abspath(path.join(res_folder, "maps"))
        self.map_save = path.abspath(path.join(self.map_folder, "save.pickle"))
        self.map_save_dead = path.abspath(path.join(self.map_folder, "dead.pickle"))
        self.title_font = path.abspath(path.join(fonts_folder, ZOMBIE_FONT))
        self.hud_font = path.abspath(path.join(fonts_folder, IMPACTED_FONT))
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_img = pg.image.load(
            path.abspath(path.join(entity_folder, PLAYER_IMG))
        ).convert_alpha()
        self.bullet_images = {}
        self.bullet_images["lg"] = pg.image.load(
            path.abspath(path.join(weapon_folder, BULLET_IMG))
        ).convert_alpha()
        self.bullet_images["sm"] = pg.transform.scale(
            self.bullet_images["lg"], (10, 10)
        )
        self.bullet_images["tn"] = pg.transform.scale(self.bullet_images["lg"], (7, 7))
        self.zombie_img = pg.image.load(
            path.abspath(path.join(entity_folder, ZOMBIE_IMAGE))
        ).convert_alpha()
        self.splat = pg.image.load(
            path.abspath(path.join(effects_folder, SPLAT))
        ).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.gun_flashes = []
        for img in MUZZEL_FLASHES:
            self.gun_flashes.append(
                pg.image.load(
                    path.abspath(path.join(effects_folder, img))
                ).convert_alpha()
            )
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(
                path.abspath(path.join(items_folder, ITEM_IMAGES[item]))
            ).convert_alpha()
            try:
                if self.item_images[item] == self.item_images["uzi"]:
                    self.item_images[item] = pg.transform.scale(
                        self.item_images[item], (54, 48)
                    )
            except:
                pass
        self.chest_images = []
        for img in CHEST_IMAGES:
            self.chest_images.append(
                pg.image.load(
                    path.abspath(path.join(entity_folder, img))
                ).convert_alpha()
            )
        self.chest_images[0] = pg.transform.scale(self.chest_images[0], (40, 40))
        self.chest_images[1] = pg.transform.scale(self.chest_images[1], (40, 40))
        self.door_images = []
        for img in DOOR_IMG:
            self.door_images.append(
                pg.image.load(
                    path.abspath(path.join(entity_folder, img))
                ).convert_alpha()
            )
        # Lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(
            path.abspath(path.join(effects_folder, LIGHT_MASK))
        ).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(
                path.abspath(path.join(snd_folder, EFFECTS_SOUNDS[type]))
            )
            self.effects_sounds[type].set_volume(0.05)
        self.effects_sounds["chest_open"].set_volume(1)
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.abspath(path.join(snd_folder, snd)))
                s.set_volume(0.05)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.abspath(path.join(snd_folder, snd)))
            s.set_volume(0.06)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.abspath(path.join(snd_folder, snd)))
            s.set_volume(0.2)
            self.player_hit_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.abspath(path.join(snd_folder, snd)))
            s.set_volume(0.2)
            self.zombie_hit_sounds.append(s)
        pg.mixer.music.load(path.abspath(path.join(music_folder, BG_MUSIC)))
        pg.mixer.music.set_volume(0.3)

    def new(self):
        # initialize all variables and do all the setup for the game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player_group = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.chests = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.map = TiledMap(path.abspath(path.join(self.map_folder, TILED_MAP_1)))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.item_pickup_data = ""

        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(
                tile_object.x + tile_object.width / 2,
                tile_object.y + tile_object.height / 2,
            )
            if tile_object.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == "zombie":
                Mob(self, obj_center.x, obj_center.y, tile_object.id)
            if tile_object.name == "wall":
                Obstacle(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )
            if tile_object.name in ["health", "shotgun", "uzi"]:
                Item(self, obj_center, tile_object.name, tile_object.id)
            if tile_object.name == "chest":
                Chest(self, obj_center, tile_object.drop, tile_object.id)
            if tile_object.name == "door":
                Door(
                    self,
                    tile_object.x,
                    tile_object.y,
                    tile_object.width,
                    tile_object.height,
                )

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.open = False
        self.effects_sounds["level_start"].set_volume(0.1)
        self.effects_sounds["level_start"].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def get_item_pickup_data(self):
        return self.item_pickup_data

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # define game over?
        if len(self.mobs) == 0:
            self.playing = False
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.pickup:
                self.item_pickup_data += "D," + str(hit.id) + ",False,\n"
                if hit.type == "health" and self.player.health < PLAYER_HEALTH:
                    if hit.add:
                        hit.kill()
                    self.effects_sounds["health_up"].play()
                    self.player.add_health(HEALTH_PACK_AMOUNT)
                for weapons in WEAPONS:
                    if hit.type == weapons:
                        hit.kill()
                        self.effects_sounds["gun_pickup"].play()
                        self.player.weapon = weapons
                        self.player.weapon_inventory.append(self.player.weapon)
                        self.player.clip = WEAPONS[self.player.weapon]["bullet_mag"]
                        self.player.weapon_inventory = list(
                            set(self.player.weapon_inventory)
                        )
        # mob hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.health -= ZOMBIE_DAMAGE
            hit.vel = vec(ZOMBIE_KNOCKBACK, 0).rotate(-hits[0].rot)
            if self.player.health <= 0:
                self.playing = False
                self.player.health = PLAYER_HEALTH
                self.player.pos = 836, 442

        if hits:
            self.player.hit()
            self.player.pos += vec(ZOMBIE_KNOCKBACK, 0).rotate(-hits[0].rot)

        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # Draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BG_COLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                try:
                    pg.draw.rect(
                        self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1
                    )
                except:
                    pass
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)

        if self.night:
            self.render_fog()

        # HUD functions
        draw_hud(self, self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if check_vicinity(self.player, self.chests):
            self.draw_text(
                "Press E to open",
                self.hud_font,
                30,
                WHITE,
                WIDTH / 2,
                HEIGHT / 2 + 50,
                align="center",
            )
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text(
                "Paused",
                self.title_font,
                105,
                RED,
                WIDTH / 2,
                HEIGHT / 2,
                align="center",
            )
        pg.display.flip()

    def events(self):
        # catch all events here
        self.open = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
            if event.type == pg.KEYUP:
                if event.key == pg.K_e and not self.open:
                    self.open = True
                if event.key == pg.K_m:
                    write_data(self, Game)
                    write_load_data(self, Game)
                    print("data is saved")

    def show_start_screen(self):
        start = True
        self.load_dead = False
        start_button = Button(
            self, "START", self.hud_font, 72, 200, 100, WIDTH / 2, HEIGHT / 2
        )
        load_button = Button(
            self, "LOAD", self.hud_font, 40, 80, 50, WIDTH / 2, HEIGHT / 2 + 100
        )
        quit_button = Button(
            self, "QUIT", self.hud_font, 40, 80, 50, WIDTH / 2, HEIGHT / 2 + 200
        )
        while start:
            self.clock.tick(FPS)
            start_button.update()
            quit_button.update()
            load_button.update()
            for event in pg.event.get():
                if event.type == pg.QUIT or (
                    event.type == pg.MOUSEBUTTONUP and quit_button.hovering
                ):
                    self.quit()
                if event.type == pg.MOUSEBUTTONUP and start_button.hovering:
                    start = False
                if event.type == pg.MOUSEBUTTONUP and load_button.hovering:
                    start = False
                    self.load_dead = True
                    load_game(self, Game)

            pg.display.flip()

    def load_game_bool(self):
        return self.load_dead

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text(
            "GAME OVER", self.title_font, 80, RED, WIDTH / 2, HEIGHT / 2, align="center"
        )
        self.draw_text(
            "PRESS R TO START",
            self.title_font,
            75,
            WHITE,
            WIDTH / 2,
            HEIGHT * 3 / 4,
            align="center",
        )
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):

        pg.event.wait()
        waiting = True
        keys = pg.key.get_pressed()
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False


def main():
    # create the game object
    g = Game()
    g.new()
    g.show_start_screen()
    while True:
        g.run()
        g.show_go_screen()


if __name__ == "__main__":
    main()
