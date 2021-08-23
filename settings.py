import pygame as pg
vec = pg.math.Vector2
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
DARK_GREEN = (0, 100, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (105, 55, 5)
BLUE = (0, 0, 255)

# game settings
WIDTH = 1024 # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768 # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tile RPG"
BG_COLOR = DARK_GREY

TILE_SIZE = 64
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 300.0
PLAYER_ROT_SPEED = 250.0
PLAYER_IMG = 'manBlue_gun.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
BARREL_OFFSET = vec(30, 10)
INVINCIBLE_TIMER = 2000

# Zombie settings
ZOMBIE_SPEED = [250, 175, 150, 150, 150, 125, 100, 50]
ZOMBIE_IMAGE = 'zoimbie1_hold.png'
ZOMBIE_HIT_RECT = pg.Rect(0, 0, 30, 30)
ZOMBIE_HEALTH = 100
ZOMBIE_DAMAGE = 10
ZOMBIE_KNOCKBACK = 25
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Misc png
DOOR_IMG = ['door_closed.png', 'door_opened.png']
DOOR_ROT_SPEED = 250
DOOR_CLOSE_DELAY = 2000

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 500, 
                     'bullet_lifetime': 1000,
                     'rate': 250, 
                     'reload': 1.8,
                     'damage': 13,
                     'kickback': 200, 
                     'spread': 5,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'bullet_mag': 16}
WEAPONS['shotgun'] = {'bullet_speed': 350, 
                     'bullet_lifetime': 500,
                     'rate': 900,
                     'reload': 2.5, 
                     'damage': 8,
                     'kickback': 300, 
                     'spread': 20,
                     'bullet_size': 'sm',
                     'bullet_count': 14,
                     'bullet_mag': 8}
WEAPONS['uzi'] = {'bullet_speed': 850, 
                     'bullet_lifetime': 600,
                     'rate': 80, 
                     'reload': 1,
                     'damage': 8,
                     'kickback': 100, 
                     'spread': 8,
                     'bullet_size': 'tn',
                     'bullet_count': 1,
                     'bullet_mag': 40}

# Items
ITEM_IMAGES = {'health': 'health_pack.png', 'shotgun': 'obj_shotgun.png', 'uzi': 'obj_uzi.png', 'pistol': 'obj_pistol.png'}
ITEM_NAMES = ['health', 'shotgun', 'uzi']
ITEM_PICKUP_DELAY = 2000
BOB_RANGE = 15
BOB_SPEED = 0.4
HEALTH_PACK_AMOUNT = 20

# Chests
CHEST_IMAGES = ['chest_closed.png', 'chest_opened.png']
CHEST_HIT_RECT = pg.Rect(0, 0, 40, 40)

# Effects
MUZZEL_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png', 'whitePuff18.png']
FLASH_DURATOIN = 40
DAMAGE_ALPHA = [i for i in range(0, 255, 35)]
SPLAT = 'splat green.png'
SCREEN_FLASH_RANGE = 155
FLASH_SPEED = 2
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_med.png"


#Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'uzi': ['pistol.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'chest_open': 'chest_open.wav'}
# Layers
UI_LAYER = 1
WALL_LAYER = 2
ITEMS_LAYER = 2
PLAYER_LAYER = 3
MOB_LAYER = 3
BULLET_LAYER = 4
EFFECTS_LAYER = 5


# Map List
TILED_MAP_1 = 'tilemap.tmx'
MAP_1 = 'map.txt'
MAP_2 = 'map2.txt'

# Font List
ZOMBIE_FONT = 'ZOMBIE.TTF'
IMPACTED_FONT = 'Impacted2.0.ttf'