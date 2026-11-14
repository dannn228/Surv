"""Настройки, палитра и таблицы данных игры.

Только данные и чистые вычисления: ни pygame, ни состояния игры.
Модуль загружается первым, его имена попадают в `surv.runtime`.
"""
import struct


WIDTH, HEIGHT = 1280, 720
FPS = 60

# --- локальный мультиплеер ------------------------------------------------
MP_MAX_PLAYERS = 4
MP_WORLD_SYNC_INTERVAL = 0.25
MP_PLAYER_SYNC_INTERVAL = 0.05
MP_INPUT_INTERVAL = 1.0 / 30.0
# The host owns world simulation.  A client only has to announce its own
# local edits; a frequent full world scan is both unnecessary and a source
# of frame spikes on slower machines.
MP_CLIENT_WORLD_SYNC_INTERVAL = 0.6
MP_CODE_PREFIX = "SURV"  # старый формат, продолжаем принимать его при подключении
MP_CODE_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MP_PVP_DAMAGE = 8
MP_RESPAWN_DELAY = 3.0

# --- UDP-транспорт -------------------------------------------------------
# Поверх UDP работает маленький надёжный слой: порядок, подтверждения,
# фрагментация и сжатие.  Ввод и позиции идут без гарантий (их выгоднее
# потерять, чем задержать), а мир, команды и рукопожатие — надёжно.
MP_UDP_MAGIC = b"SU"
MP_UDP_HEADER = struct.Struct("!2sBIIIIIHH")
MP_UDP_FLAG_RELIABLE = 1
MP_UDP_FLAG_FRAGMENT = 2
MP_UDP_FLAG_COMPRESSED = 4
MP_UDP_FRAG_SIZE = 1200
MP_UDP_MAX_MESSAGE = 16 * 1024 * 1024
MP_UDP_RESEND_INTERVAL = 0.25
MP_UDP_MAX_RESENDS = 60
MP_UDP_FRAG_BURST = 48
MP_UDP_ACK_INTERVAL = 0.05
MP_UDP_IDLE_TIMEOUT = 20.0
MP_UDP_CONNECT_TIMEOUT = 12.0
MP_UDP_SOCKET_BUFFER = 1 << 20
# Если предыдущий дифф мира ещё не подтверждён, следующий не ставим в
# очередь: изменения накопятся и уйдут одним пакетом.  Иначе при подвисании
# канала надёжная очередь растёт быстрее, чем успевает разгружаться.
MP_UDP_WORLD_SYNC_BACKLOG = 1
MP_UDP_RELIABLE_TYPES = {
    'hello', 'welcome', 'world_diff', 'world_state', 'enter_world',
    'cmd', 'cmd_result', 'pvp_attack', 'player_damage', 'player_down',
    'player_respawn', 'throw', 'error', 'kicked', 'bye',
}

# --- предсказание действий ----------------------------------------------
MP_CMD_RATE_LIMIT = 30          # действий в секунду с одного клиента
MP_CMD_MAX_OBJECTS = 80         # объектов в одной команде
MP_CMD_REACH = 300.0            # максимальная дистанция правки мира
MP_CMD_FREE_LISTS = {'puffs'}         # косметика без проверки дистанции
MP_CMD_RESULT_TIMEOUT = 4.0     # сколько ждём подтверждения предсказания
MP_RESPAWN_REACH = 160.0        # насколько возрождение может отойти от спавна
MP_RECONCILE_ERROR = 18.0       # расхождение, после которого пересчитываем путь
MP_RECONCILE_REPLAY = 12        # максимум входов для повторного расчёта

BUTTON_COLOR    = (58, 72, 100)
BUTTON_HOVER    = (84, 106, 144)
BUTTON_DISABLED = (46, 52, 66)
TEXT_ON_BUTTON  = (248, 251, 255)
TEXT_DISABLED   = (146, 156, 176)
TITLE_COLOR     = (238, 244, 253)
LABEL_COLOR     = (214, 228, 246)
VALUE_COLOR     = (250, 206, 120)
HINT_COLOR      = (164, 182, 210)
ACCENT          = (242, 198, 108)
PANEL_BG        = (24, 31, 46)
PANEL_BG_LIGHT  = (52, 64, 90)

SKIN_COLOR       = (245, 205, 165)
SKIN_SHADOW      = (210, 170, 135)
SKIN_HIGHLIGHT   = (255, 225, 195)
SKIN_OUTLINE     = (170, 120, 80)
EYE_WHITE        = (255, 255, 255)
EYE_PUPIL        = (30, 25, 25)
HAIR_COLOR       = (95, 60, 35)
HAIR_DARK        = (60, 35, 20)
HAIR_HIGHLIGHT   = (135, 95, 60)
CHEEK_COLOR      = (245, 150, 140)
MOUTH_COLOR      = (140, 70, 60)
GRASS_SKIRT_1    = (85, 150, 60)
GRASS_SKIRT_2    = (60, 115, 45)
GRASS_SKIRT_BAND = (50, 95, 40)

TREE_TRUNK       = (90, 60, 35)
TREE_TRUNK_DARK  = (60, 40, 22)
TREE_TRUNK_LIGHT = (135, 95, 55)
TREE_LEAF_DARK   = (45, 95, 45)
TREE_LEAF_MID    = (60, 125, 55)
TREE_LEAF_LIGHT  = (85, 155, 70)
TREE_LEAF_HILITE = (110, 180, 90)

LAKE_SHORE     = (210, 192, 148)
LAKE_SHORE_DARK= (166, 146, 104)
LAKE_DEEP      = (12, 52, 74)
LAKE_SHALLOW   = (78, 164, 152)
LAKE_REFLECT   = (176, 224, 232)
LAKE_FOAM      = (226, 240, 232)


MUSHROOM_STEM      = (235, 220, 195)
MUSHROOM_STEM_DARK = (190, 175, 150)
MUSHROOM_CAP_DARK  = (150, 30, 30)
MUSHROOM_CAP       = (205, 55, 50)
MUSHROOM_CAP_LIGHT = (240, 95, 85)
MUSHROOM_SPOT      = (245, 235, 220)

STONE_DARK      = (70, 72, 80)
STONE_MAIN      = (130, 132, 140)
STONE_LIGHT     = (180, 182, 190)
STONE_HIGHLIGHT = (220, 222, 228)


TILLED_SOIL_MAIN    = (110, 75, 50)
TILLED_SOIL_DARK    = (70, 45, 25)
TILLED_SOIL_LIGHT   = (140, 100, 65)


BOARD_MAIN      = (170, 120, 70)
BOARD_DARK      = (100, 65, 30)
BOARD_LINE      = (140, 95, 55)

GRAVE_STONE       = (115, 115, 125)
GRAVE_STONE_DARK  = (70, 70, 80)
GRAVE_MOUND       = (85, 70, 55)
GRAVE_MOUND_DARK  = (55, 45, 35)
GRAVE_CROSS       = (60, 60, 70)

CAVE_ROCK_DARK   = (65, 65, 78)
CAVE_ROCK_MID    = (95, 95, 108)
CAVE_ROCK_LIGHT  = (130, 130, 145)
CAVE_ROCK_HILITE = (160, 160, 175)
CAVE_INNER       = (18, 18, 26)
CAVE_INNER_DEEP  = (8, 8, 14)

BRICK_OUTLINE   = (72, 70, 76)
BRICK_MORTAR    = (98, 96, 100)
BRICK_MAIN      = (152, 150, 154)
BRICK_DARK      = (118, 116, 122)
BRICK_LIGHT     = (182, 180, 186)
BRICK_HIGHLIGHT = (214, 212, 218)

WOOD_BLOCK_OUTLINE   = (68, 43, 24)
WOOD_BLOCK_DARK      = (112, 68, 36)
WOOD_BLOCK_MAIN      = (158, 102, 54)
WOOD_BLOCK_LIGHT     = (192, 136, 78)
WOOD_BLOCK_HIGHLIGHT = (222, 174, 112)

FURNACE_DARK     = (92, 88, 92)
FURNACE_LIGHT    = (176, 171, 174)
FURNACE_VOID     = (26, 20, 20)
FURNACE_EMBER    = (66, 30, 20)
FURNACE_FIRE_OUT = (232, 112, 34)
FURNACE_FIRE_MID = (248, 170, 52)
FURNACE_FIRE_IN  = (255, 232, 140)
FURNACE_CHIMNEY  = (118, 112, 116)

CHEST_WOOD_DARK    = (92, 56, 32)
CHEST_WOOD         = (132, 86, 48)
CHEST_WOOD_LIGHT   = (168, 114, 64)
CHEST_WOOD_HILITE  = (202, 150, 92)
CHEST_IRON         = (92, 96, 108)
CHEST_IRON_LIGHT   = (154, 160, 172)
CHEST_IRON_DARK    = (52, 56, 66)
CHEST_GOLD         = (214, 170, 74)
CHEST_GOLD_LIGHT   = (255, 224, 138)

ARMCHAIR_WOOD_DARK   = (57, 36, 20)
ARMCHAIR_WOOD        = (104, 68, 38)
ARMCHAIR_WOOD_LIGHT  = (156, 106, 58)
ARMCHAIR_GREEN_DARK  = (31, 83, 53)
ARMCHAIR_GREEN       = (52, 126, 76)
ARMCHAIR_GREEN_LIGHT = (82, 163, 101)
ARMCHAIR_GREEN_HILITE = (131, 204, 137)

TABLE_WOOD_DARK    = (62, 40, 22)
TABLE_WOOD         = (124, 82, 44)
TABLE_WOOD_LIGHT   = (174, 122, 68)
TABLE_WOOD_HILITE  = (214, 166, 104)

TEDDY_FUR_DARK   = (96, 62, 38)
TEDDY_FUR        = (150, 104, 66)
TEDDY_FUR_LIGHT  = (192, 146, 102)
TEDDY_MUZZLE     = (228, 200, 164)
TEDDY_EYE        = (44, 30, 22)
TEDDY_BOW        = (188, 62, 72)
TEDDY_BOW_DARK   = (132, 38, 50)

OVERHEAL_BADGE_BG     = (50, 130, 200, 235)
OVERHEAL_BADGE_BORDER = (150, 210, 240)
OVERHEAL_TEXT_COLOR   = (220, 245, 255)


NIGHT_SKY_TOP     = (10, 15, 40)
NIGHT_SKY_BOTTOM  = (35, 45, 85)

RUN_HUNGER_PER_SEC = 2.5
HUNGER_PASSIVE_PER_SEC = 1.0 / 15.0
HUNGER_LOW = 20.0
HUNGER_FULL_THRESHOLD = 0.5
PICKUP_RADIUS  = 130.0
SEED_LIFETIME  = 120.0
AUTO_PICKUP_RADIUS  = 130.0
AUTO_PICKUP_COLLECT = 24.0
SEED_FLY_SPEED      = 380.0
DROP_DEACTIVATE_DIST = 200.0
COOKING_DURATION = 5.0
FURNACE_COOK_TIME = 5.0

BRICK_WALL_SIZE = 64
BRICK_WALL_MIN_GAP = int(BRICK_WALL_SIZE * 0.85)

FURNACE_SIZE = 76
FURNACE_PLACE_RANGE = 130

CHEST_SIZE = 72
CHEST_PLACE_RANGE = 130

DESIGN_TABLE_SIZE = 80
DESIGN_TABLE_PLACE_RANGE = 130

ARMCHAIR_SIZE = 64
ARMCHAIR_PLACE_RANGE = 130
ARMCHAIR_SEAT_DY = -16.0
ARMCHAIR_COLLISION_RADIUS = 29

TABLE_SIZE = 76
TABLE_PLACE_RANGE = 130
TABLE_COLLISION_RADIUS = 31
TABLE_CAPACITY = 3

TEDDY_BEAR_SIZE = 56
TEDDY_BEAR_PLACE_RANGE = 130
TEDDY_BEAR_COLLISION_RADIUS = 24

ANVIL_SIZE = 76
ANVIL_PLACE_RANGE = 130

# Four build cells (4 * 40 px) with the same small end clearance as before.
GATE_LENGTH = 148.0
GATE_THICKNESS = 22.0
GATE_POST = 16.0
GATE_PLACE_RANGE = 130.0
GATE_OPEN_SPEED = 7.0
# У клиента ворота анимируются медленнее: сеть приходит всего 4 раза в секунду,
# и открытие успевает проскочить между снапшотами. Скорость чисто визуальная —
# коллизия определяется флагом is_open и не задерживается.
GATE_MP_CLIENT_OPEN_SPEED = 3.2

HOUR_REAL_SECONDS = 60
DAY_REAL_SECONDS = 24 * HOUR_REAL_SECONDS
START_GAME_HOUR = 8
NEXT_MORNING_INIT = 22 * HOUR_REAL_SECONDS

# Ночью дикие животные не появляются, зато регулярно выходит по одному зомби.
NIGHT_SPAWN_THRESHOLD = 0.5
# Сколько секунд существо и игрок остаются на земле после смерти.
ENTITY_DEATH_TIME = 0.9
PLAYER_DEATH_TIME = 1.5
NIGHT_ZOMBIE_SPAWN_INTERVAL = 6.0
NIGHT_ZOMBIE_SPAWN_MIN_DIST = 420.0
NIGHT_ZOMBIE_SPAWN_MAX_DIST = 620.0
NIGHT_ZOMBIE_NEARBY_RADIUS = 900.0
NIGHT_ZOMBIE_NEARBY_LIMIT = 12

# Паук: ночной ночной гость, реже и дальше от игрока, чем зомби.
NIGHT_SPIDER_SPAWN_INTERVAL = 20.0
NIGHT_SPIDER_SPAWN_MIN_DIST = 620.0
NIGHT_SPIDER_SPAWN_MAX_DIST = 900.0
NIGHT_SPIDER_NEARBY_RADIUS = 1200.0
NIGHT_SPIDER_NEARBY_LIMIT = 5

# Волки: редкие дневные стаи по 3-5 особей.  Интервал большой, а шанс
# не стопроцентный, поэтому за день игрок встречает одну-две стаи.
WOLF_PACK_INTERVAL = 150.0
WOLF_PACK_CHANCE = 0.40
WOLF_PACK_MIN = 3
WOLF_PACK_MAX = 5
WOLF_SPAWN_MIN_DIST = 430.0
WOLF_SPAWN_MAX_DIST = 680.0
WOLF_NEARBY_RADIUS = 1200.0
WOLF_NEARBY_LIMIT = 10
# Трусливый волк выглядит точно так же, но не нападает первым.
WOLF_COWARDLY_CHANCE = 0.22
WOLF_DAY_START_HOUR = 7.0
WOLF_DAY_END_HOUR = 19.0

# Проверка точки спавна: зомби не должен появиться внутри стены или
# в замкнутом со всех сторон загоне. Заливка идёт по габаритам стен:
# если свободные клетки кончились раньше границы, значит это загон.
NIGHT_SPAWN_FREE_CELL = 28.0
NIGHT_SPAWN_FREE_MARGIN = 2.0

# Чем игрок огораживается: кирпичные/деревянные стены и закрытые ворота.
_ENCLOSURE_OBSTACLE_ATTRS = ('brick_walls',)

# Размножение животных.
BABY_GROW_HOURS = 5
BREEDING_COOLDOWN_HOURS = 24
BABY_GROW_TIME = BABY_GROW_HOURS * HOUR_REAL_SECONDS
BREEDING_COOLDOWN_TIME = BREEDING_COOLDOWN_HOURS * HOUR_REAL_SECONDS
BREEDING_SEARCH_RADIUS = 700.0
BREEDING_APPROACH_TIMEOUT = 25.0
BREEDING_CIRCLE_TIME = 3.0

CELL_SIZE = 128

CHUNK_TILES_OVERWORLD = 8
CHUNK_TILES_CAVE = 4
CHUNK_RADIUS_OVERWORLD = 3
CHUNK_RADIUS_CAVE = 3

# Пещера конечная: 24 x 24 чанка (12 288 x 12 288 пикселей).
CAVE_CHUNKS_ACROSS = 24
CAVE_MIN_CHUNK = -(CAVE_CHUNKS_ACROSS // 2)
CAVE_MAX_CHUNK = CAVE_CHUNKS_ACROSS // 2 - 1
CAVE_CHUNK_BOUNDS = (CAVE_MIN_CHUNK, CAVE_MIN_CHUNK,
                     CAVE_MAX_CHUNK, CAVE_MAX_CHUNK)
CAVE_MIN_COL = CAVE_MIN_CHUNK * CHUNK_TILES_CAVE
CAVE_MAX_COL = (CAVE_MAX_CHUNK + 1) * CHUNK_TILES_CAVE
CAVE_MIN_PX = CAVE_MIN_COL * CELL_SIZE
CAVE_MAX_PX = CAVE_MAX_COL * CELL_SIZE
CAVE_BOUNDARY_EDGE = 24

WORLD_MIN_X = 0
WORLD_MIN_Y = 0
WORLD_W = 1280
WORLD_H = 720
WORLD_COLS = 0
WORLD_ROWS = 0

MAX_STACK = 10
STACK_LIMITS = {
    'log': 3, 'carrot': 5, 'potato': 10, 'tomato': 10, 'wheat': 10,
    'stick': 3, 'stone': 10, 'flour': 10, 'sawdust': 10, 'board': 3,
    'raw_beef': 10, 'steak': 10, 'raw_pork': 10, 'cooked_pork': 10,
    'raw_chicken': 10, 'cooked_chicken': 10, 'egg': 10,
    'raw_mutton': 10, 'cooked_mutton': 10,
    'brick_block': 10, 'wood_block': 10, 'bread': 10,
    'meat_pirozhok': 10, 'potato_pirozhok': 10,
    'wool': 10, 'teddy_bear': 3, 'leather': 10,
}

STACKABLE_TYPES = {'seed', 'raspberry', 'blueberry', 'mushroom', 'acorn',
                   'coal', 'iron', 'ingot', 'leaf', 'log', 'apple',
                   'copper', 'copper_ingot', 'gold', 'gold_ingot',
                   'emerald', 'ruby',
                   'carrot', 'potato', 'tomato', 'wheat',
                   'stick', 'stone', 'flour', 'sawdust', 'board',
                   'raw_beef', 'steak', 'raw_pork', 'cooked_pork',
                   'raw_chicken', 'cooked_chicken', 'egg', 'brick_block',
                   'raw_mutton', 'cooked_mutton',
                   'wood_block', 'bread', 'meat_pirozhok', 'potato_pirozhok',
                   'cabbage_rolls', 'wool', 'teddy_bear', 'leather'}
NON_STACKABLE_TYPES = {'axe', 'pickaxe', 'campfire', 'cauldron', 'bucket',
                       'bucket_water', 'bucket_milk', 'berry_jam', 'mushroom_soup',
                       'pumpkin_soup',
                       'rake', 'tea', 'pumpkin', 'cabbage', 'thresher', 'sawmill',
                       'sword', 'furnace', 'chest', 'berry_pie', 'gate',
                       'pumpkin_pie', 'apple_pie', 'key', 'design_table', 'armchair',
                       'table', 'iron_axe', 'iron_pickaxe', 'iron_rake',
                       'iron_sword', 'shears', 'anvil',
                       'test_helmet', 'test_chestplate', 'test_leggings',
                       'test_boots', 'iron_helmet', 'iron_chestplate',
                       'iron_leggings', 'iron_boots', 'backpack', 'torch'}
# Броня: четыре предмета под четыре слота. Каждая деталь снижает
# входящий урон и отбрасывание; тестовый набор слабее, железный —
# прочнее. Тестовый набор даётся отладкой, железный куётся на наковальне.
ARMOR_ITEM_KINDS = {
    'test_helmet': 'head',
    'test_chestplate': 'body',
    'test_leggings': 'legs',
    'test_boots': 'feet',
    'iron_helmet': 'head',
    'iron_chestplate': 'body',
    'iron_leggings': 'legs',
    'iron_boots': 'feet',
    'backpack': 'body',
}
# Доля снижения урона каждой деталью. Полный тестовый набор — 20%,
# полный железный — 40%.
ARMOR_DEFENSE = {
    'test_helmet': 0.04,
    'test_chestplate': 0.08,
    'test_leggings': 0.05,
    'test_boots': 0.03,
    'iron_helmet': 0.08,
    'iron_chestplate': 0.16,
    'iron_leggings': 0.10,
    'iron_boots': 0.06,
}
MAX_ARMOR_DEFENSE = 0.55
# Доля от процента брони, которая гасит ещё и отбрасывание.
ARMOR_KNOCKBACK_FACTOR = 0.75
TEST_ARMOR_ACCENT = {
    'test_helmet': (96, 206, 226),
    'test_chestplate': (236, 156, 72),
    'test_leggings': (138, 208, 118),
    'test_boots': (188, 142, 232),
}
IRON_ARMOR_ACCENT = {
    'iron_helmet': (196, 214, 236),
    'iron_chestplate': (216, 224, 236),
    'iron_leggings': (176, 198, 222),
    'iron_boots': (202, 214, 232),
}
RAW_MEAT_TYPES = ('raw_beef', 'raw_pork', 'raw_chicken', 'raw_mutton')
BUILDING_TYPES = {'campfire', 'thresher', 'sawmill', 'furnace', 'chest',
                  'design_table', 'armchair', 'table', 'teddy_bear', 'anvil'}
PLACEABLE_TYPES = BUILDING_TYPES | {'brick_block', 'wood_block', 'gate'}
BUILD_CELL_SIZE = 40
BUILD_FOOTPRINTS = {t: (2, 2) for t in PLACEABLE_TYPES}
BUILD_FOOTPRINTS['gate'] = (1, 4)
BUILD_FREE_COLOR = (24, 82, 255, 102)
BUILD_BLOCKED_COLOR = (255, 18, 42, 118)
BUILD_OCCUPIED_COLOR = (255, 130, 20, 124)
BUILD_GRID_LINE = (240, 248, 255, 72)
BUILD_GHOST_OK = (92, 232, 132)
BUILD_GHOST_BAD = (240, 82, 72)
BUILD_SUCCESS_TEXT = {
    'campfire': "Костёр построен",
    'thresher': "Молотилка построена",
    'sawmill': "Лесопилка построена",
    'furnace': "Печь установлена",
    'chest': "Сундук установлен",
    'design_table': "Стол конструктора установлен",
    'armchair': "Кресло установлено",
    'table': "Стол установлен",
    'teddy_bear': "Мишка установлен",
    'anvil': "Наковальня установлена",
    'brick_block': "Стена построена",
    'wood_block': "Деревянная стена построена",
    'gate': "Ворота установлены",
}
STONE_TOOL_TYPES = {'axe', 'pickaxe', 'rake', 'sword'}
IRON_TOOL_TYPES = {'iron_axe', 'iron_pickaxe', 'iron_rake', 'iron_sword'}
SHEARS_TOOL_TYPES = {'shears'}
TOOL_TYPES = STONE_TOOL_TYPES | IRON_TOOL_TYPES | SHEARS_TOOL_TYPES
TOOL_MAX_DURABILITY = 8
IRON_TOOL_MAX_DURABILITY = 20
SHEARS_MAX_DURABILITY = 10
TOOL_DURABILITY = {
    'axe': TOOL_MAX_DURABILITY, 'pickaxe': TOOL_MAX_DURABILITY,
    'rake': TOOL_MAX_DURABILITY, 'sword': TOOL_MAX_DURABILITY,
    'iron_axe': IRON_TOOL_MAX_DURABILITY,
    'iron_pickaxe': IRON_TOOL_MAX_DURABILITY,
    'iron_rake': IRON_TOOL_MAX_DURABILITY,
    'iron_sword': IRON_TOOL_MAX_DURABILITY,
    'shears': SHEARS_MAX_DURABILITY,
}
TOOL_FAMILIES = {
    'axe': {'axe', 'iron_axe'},
    'pickaxe': {'pickaxe', 'iron_pickaxe'},
    'rake': {'rake', 'iron_rake'},
    'sword': {'sword', 'iron_sword'},
}
WEAPON_DAMAGE = {'sword': 1, 'iron_sword': 1}
THROWN_DAMAGE = 1
ATTACK_COOLDOWN = 0.45
SWING_RANGE = 110.0
COW_GROUP_CHANCE = 0.30
PIG_GROUP_CHANCE = 0.28
CHICKEN_GROUP_CHANCE = 0.26
SHEEP_GROUP_CHANCE = 0.22
BULL_GROUP_CHANCE = 0.06
BOAR_GROUP_CHANCE = 0.07
ROOSTER_GROUP_CHANCE = 0.05
RAM_GROUP_CHANCE = 0.06
GRILL_RESULTS = {'raw_beef': 'steak', 'raw_pork': 'cooked_pork',
                 'raw_chicken': 'cooked_chicken',
                 'raw_mutton': 'cooked_mutton'}
# Обломки руды плавятся на костре в слитки. Изумруд и рубин выпадают
# готовыми кристаллами, поэтому в плавке не участвуют.
SMELT_RESULTS = {'iron': 'ingot', 'copper': 'copper_ingot',
                 'gold': 'gold_ingot'}
# Всё, что можно перетащить на костёр: топливо, руда, котёл, вода и мясо.
CAMPFIRE_DROP_TYPES = ({'coal', 'cauldron', 'bucket_water'} |
                       set(SMELT_RESULTS) | set(GRILL_RESULTS))

# Руды в пещерах: тип и вес появления. Уголь и железо остаются самыми
# частыми, золото — реже, изумруд и рубин — редкая находка.
ORE_SPAWN_TYPES = ['coal', 'iron', 'copper', 'gold', 'emerald', 'ruby']
ORE_SPAWN_WEIGHTS = [30, 24, 20, 12, 8, 6]
# Эти руды не поддаются каменной кирке — нужна железная.
IRON_PICKAXE_ORES = {'gold', 'emerald'}
# Цвет всплывающей подсказки после добычи.
ORE_TOAST_COLORS = {
    'coal': (156, 164, 182),
    'iron': (210, 158, 120),
    'copper': (230, 150, 100),
    'gold': (245, 215, 120),
    'emerald': (120, 220, 150),
    'ruby': (240, 110, 120),
}

CROP_TYPES = ['pumpkin', 'carrot', 'cabbage', 'potato', 'tomato', 'wheat']

THRESH_LEVER_THRESHOLD = 400.0




ITEM_NAMES = {
    'seed': 'Семечко', 'stick': 'Палка', 'leaf': 'Листок',
    'raspberry': 'Малина', 'blueberry': 'Черника', 'mushroom': 'Гриб',
    'stone': 'Камушек', 'axe': 'Топор', 'pickaxe': 'Кирка', 'rake': 'Грабли',
    'iron_axe': 'Железный топор', 'iron_pickaxe': 'Железная кирка',
    'iron_rake': 'Железные грабли', 'iron_sword': 'Железный меч',
    'shears': 'Ножницы', 'wool': 'Комок шерсти',
    'acorn': 'Желудь', 'log': 'Бревно', 'coal': 'Уголь',
    'iron': 'Железный обломок', 'ingot': 'Железный слиток',
    'copper': 'Медный обломок', 'copper_ingot': 'Медный слиток',
    'gold': 'Золотой обломок', 'gold_ingot': 'Золотой слиток',
    'emerald': 'Кристалл изумруда', 'ruby': 'Кристалл рубина',
    'campfire': 'Костёр', 'cauldron': 'Котёл', 'bucket': 'Ведро',
    'bucket_water': 'Ведро с водой', 'berry_jam': 'Ягодное варенье',
    'mushroom_soup': 'Грибной суп', 'pumpkin_soup': 'Тыквенный суп', 'tea': 'Чай',
    'pumpkin': 'Тыква', 'carrot': 'Морковь', 'cabbage': 'Капуста',
    'potato': 'Картошка', 'tomato': 'Помидор', 'wheat': 'Пшеница',
    'flour': 'Мука', 'sawdust': 'Опилки', 'board': 'Доска',
    'brick_block': 'Кирпичный блок', 'wood_block': 'Деревянный блок',
    'furnace': 'Печь', 'chest': 'Сундук',
    'design_table': 'Стол конструктора',
    'armchair': 'Кресло',
    'table': 'Стол',
    'teddy_bear': 'Плюшевый мишка',
    'gate': 'Ворота', 'key': 'Ключ',
    'thresher': 'Молотилка', 'sawmill': 'Лесопилка',
    'anvil': 'Наковальня',
    'test_helmet': 'Тестовый шлем',
    'test_chestplate': 'Тестовая кираса',
    'test_leggings': 'Тестовые поножи',
    'test_boots': 'Тестовые сапоги',
    'iron_helmet': 'Железный шлем',
    'iron_chestplate': 'Железная кираса',
    'iron_leggings': 'Железные поножи',
    'iron_boots': 'Железные сапоги',
    'leather': 'Кожа',
    'backpack': 'Рюкзак',
    'apple': 'Яблоко', 'sword': 'Каменный меч',
    'bucket_milk': 'Ведро с молоком',
    'raw_beef': 'Сырая говядина', 'steak': 'Стейк',
    'raw_pork': 'Сырая свинина', 'cooked_pork': 'Жареная свинина',
    'raw_chicken': 'Курятина', 'cooked_chicken': 'Жареная курица',
    'raw_mutton': 'Сырая баранина', 'cooked_mutton': 'Жареная баранина',
    'egg': 'Яйцо', 'bread': 'Хлеб', 'berry_pie': 'Ягодный пирог',
    'pumpkin_pie': 'Тыквенный пирог',
    'apple_pie': 'Яблочный пирог',
    'meat_pirozhok': 'Пирожок с мясом',
    'potato_pirozhok': 'Пирожок с картошкой',
    'cabbage_rolls': 'Голубцы',
    'torch': 'Факел',
}

FOOD_VALUES = {
    'raspberry': 1, 'blueberry': 1, 'berry_jam': 14,
    'mushroom_soup': 16, 'pumpkin_soup': 7, 'tea': 6, 'carrot': 2, 'tomato': 2,
    'apple': 3, 'bucket_milk': 2, 'steak': 10, 'cooked_pork': 10,
    'cooked_chicken': 8, 'cooked_mutton': 10, 'bread': 6, 'berry_pie': 13,
    'pumpkin_pie': 18, 'apple_pie': 10, 'meat_pirozhok': 4, 'potato_pirozhok': 4,
    'cabbage_rolls': 6,
}

OVERHEAL_VALUES = {'berry_jam': 10, 'mushroom_soup': 15, 'pumpkin_soup': 5,
                   'tea': 12,
                   'steak': 5, 'cooked_pork': 5, 'cooked_chicken': 4,
                   'cooked_mutton': 5,
                   'bread': 2, 'berry_pie': 7, 'pumpkin_pie': 15,
                   'apple_pie': 8,
                   'meat_pirozhok': 1, 'potato_pirozhok': 1,
                   'cabbage_rolls': 4}

# Порядок рецептов соответствует темпу прохождения:
# стартовый камень → первый уголь → костёр и печь → слитки → поздние постройки.
RECIPES = [
    {'name': 'Топор', 'desc': 'Инструмент для рубки деревьев (8 использований)',
     'ingredients': [{'type': 'stick', 'count': 1}, {'type': 'stone', 'count': 2}],
     'result': {'type': 'axe', 'count': 1}},
    {'name': 'Кирка', 'desc': 'Инструмент для добычи руды (8 использований)',
     'ingredients': [{'type': 'stick', 'count': 1}, {'type': 'stone', 'count': 3}],
     'result': {'type': 'pickaxe', 'count': 1}},
    {'name': 'Грабли', 'desc': 'Инструмент для вскапывания земли (8 использований)',
     'ingredients': [{'type': 'stick', 'count': 2}, {'type': 'stone', 'count': 1}],
     'result': {'type': 'rake', 'count': 1}},
    {'name': 'Меч', 'desc': 'Каменный клинок для защиты (8 ударов)',
     'ingredients': [{'type': 'stick', 'count': 2}, {'type': 'stone', 'count': 2}],
     'result': {'type': 'sword', 'count': 1}},
    {'name': 'Кирпичный блок', 'desc': 'Стена из серых кирпичей. Ставится кликом по земле',
     'ingredients': [{'type': 'stone', 'count': 4}],
     'result': {'type': 'brick_block', 'count': 1}},
    {'name': 'Деревянный блок',
     'desc': 'Стена из деревянных досок. Ставится кликом по земле',
     'ingredients': [{'type': 'board', 'count': 4}],
     'result': {'type': 'wood_block', 'count': 1}},
    {'name': 'Костёр', 'desc': 'Тёплое место для отдыха',
     'ingredients': [{'type': 'log', 'count': 2}, {'type': 'stick', 'count': 1},
                     {'type': 'coal', 'count': 2}, {'type': 'stone', 'count': 2}],
     'result': {'type': 'campfire', 'count': 1}},
    {'name': 'Печь', 'desc': 'Плавильная печь. Ставится кликом по земле рядом с игроком',
     'ingredients': [{'type': 'brick_block', 'count': 3}, {'type': 'coal', 'count': 2}],
     'result': {'type': 'furnace', 'count': 1}},
    {'name': 'Ведро', 'desc': 'Металлическое ведро для воды',
     'ingredients': [{'type': 'ingot', 'count': 2}],
     'result': {'type': 'bucket', 'count': 1}},
    {'name': 'Ножницы',
     'desc': 'Обычные ножницы для стрижки овец и баранов (10 использований)',
     'ingredients': [{'type': 'ingot', 'count': 2}],
     'result': {'type': 'shears', 'count': 1}},
    {'name': 'Молотилка', 'desc': 'Мелет пшеницу в муку',
     'ingredients': [{'type': 'ingot', 'count': 2}, {'type': 'stone', 'count': 3},
                     {'type': 'stick', 'count': 1}],
     'result': {'type': 'thresher', 'count': 1}},
    {'name': 'Лесопилка', 'desc': 'Пилит брёвна на доски и опилки',
     'ingredients': [{'type': 'ingot', 'count': 3}, {'type': 'stone', 'count': 5},
                     {'type': 'log', 'count': 3}],
     'result': {'type': 'sawmill', 'count': 1}},
    {'name': 'Котёл', 'desc': 'Металлический котёл для костра',
     'ingredients': [{'type': 'ingot', 'count': 4}],
     'result': {'type': 'cauldron', 'count': 1}},
    {'name': 'Сундук', 'desc': 'Хранилище на 32 ячейки. Ставится кликом по земле, можно запереть ключом',
     'ingredients': [{'type': 'board', 'count': 4}, {'type': 'ingot', 'count': 1}],
     'result': {'type': 'chest', 'count': 1}},
    {'name': 'Ворота', 'desc': 'Деревянные ворота. Ставятся кликом по земле, открываются и закрываются кликом',
     'ingredients': [{'type': 'board', 'count': 6}],
     'result': {'type': 'gate', 'count': 1}},
    {'name': 'Ключ',
     'desc': 'Железный ключ. Перетащите его на ворота или сундук, чтобы привязать и запереть их',
     'ingredients': [{'type': 'ingot', 'count': 1}],
     'result': {'type': 'key', 'count': 1}},
    {'name': 'Стол конструктора',
     'desc': 'Рабочий стол для чертежей. Ставится кликом по земле и открывает меню чертежей',
     'ingredients': [{'type': 'ingot', 'count': 2}, {'type': 'board', 'count': 2},
                     {'type': 'log', 'count': 1}, {'type': 'stick', 'count': 1},
                     {'type': 'stone', 'count': 2}],
     'result': {'type': 'design_table', 'count': 1}},
    {'name': 'Наковальня',
     'desc': 'Тяжёлая кузнечная наковальня. Ставится кликом по земле '
             'и открывает своё меню',
     'ingredients': [{'type': 'ingot', 'count': 12}],
     'result': {'type': 'anvil', 'count': 1}},
    {'name': 'Рюкзак',
     'desc': 'Добавляет 6 дополнительных слотов инвентаря. '
             'Надевается в слот груди.',
     'ingredients': [{'type': 'leather', 'count': 4}, {'type': 'ingot', 'count': 1}],
     'result': {'type': 'backpack', 'count': 1}},
]

COOKING_RECIPES = [
    {'name': 'Ягодное варенье', 'desc': 'Восстанавливает 14 голода. Оверхил +10. Требуется вода.',
     'ingredients': [{'type': 'raspberry', 'count': 3}, {'type': 'blueberry', 'count': 3},
                     {'type': 'leaf', 'count': 1}],
     'result': {'type': 'berry_jam', 'count': 1}},
    {'name': 'Грибной суп', 'desc': 'Восстанавливает 16 голода. Оверхил +15. Требуется вода.',
     'ingredients': [{'type': 'mushroom', 'count': 6}, {'type': 'acorn', 'count': 2}],
     'result': {'type': 'mushroom_soup', 'count': 1}},
    {'name': 'Тыквенный суп',
     'desc': 'Восстанавливает 7 голода. Оверхил +5. Требуется вода.',
     'ingredients': [{'type': 'pumpkin', 'count': 1},
                     {'type': 'leaf', 'count': 1},
                     {'type': 'carrot', 'count': 2}],
     'result': {'type': 'pumpkin_soup', 'count': 1}},
    {'name': 'Чай', 'desc': 'Восстанавливает 6 голода. Оверхил +12. Требуется вода.',
     'ingredients': [{'type': 'leaf', 'count': 5}],
     'result': {'type': 'tea', 'count': 1}},
]

FURNACE_RECIPES = [
    {'name': 'Хлеб',
     'desc': 'Румяный хлеб. Восстанавливает 6 голода и даёт 2 оверхилла.',
     'ingredients': [{'type': 'wheat', 'count': 2},
                     {'type': 'bucket_milk', 'count': 1},
                     {'type': 'egg', 'count': 1}],
     'result': {'type': 'bread', 'count': 1},
     'time': FURNACE_COOK_TIME},
    {'name': 'Ягодный пирог',
     'desc': 'Пирог с малиной и черникой. Восстанавливает 13 голода и даёт 7 оверхилла.',
     'ingredients': [{'type': 'raspberry', 'count': 4},
                     {'type': 'blueberry', 'count': 2},
                     {'type': 'flour', 'count': 2},
                     {'type': 'bucket_milk', 'count': 1}],
     'result': {'type': 'berry_pie', 'count': 1},
     'time': FURNACE_COOK_TIME},
    {'name': 'Тыквенный пирог',
     'desc': 'Пирог с тыквой и молоком. Восстанавливает 18 голода и даёт 15 оверхилла.',
     'ingredients': [{'type': 'flour', 'count': 3},
                     {'type': 'bucket_milk', 'count': 1},
                     {'type': 'pumpkin', 'count': 1}],
     'result': {'type': 'pumpkin_pie', 'count': 1},
     'time': 8.0},
    {'name': 'Пирожок с мясом',
     'desc': 'Румяный пирожок с мясом. Восстанавливает 4 голода и даёт 1 оверхилл.',
     'ingredients': [{'type': 'flour', 'count': 1},
                     {'type': 'bucket_milk', 'count': 1},
                     {'types': RAW_MEAT_TYPES, 'count': 2,
                      'label': 'Любое сырое мясо', 'icon': 'raw_beef'}],
     'result': {'type': 'meat_pirozhok', 'count': 1},
     'time': 2.0},
    {'name': 'Пирожок с картошкой',
     'desc': 'Румяный пирожок с картошкой. Восстанавливает 4 голода и даёт 1 оверхилл.',
     'ingredients': [{'type': 'flour', 'count': 1},
                     {'type': 'bucket_milk', 'count': 1},
                     {'type': 'potato', 'count': 2}],
     'result': {'type': 'potato_pirozhok', 'count': 1},
     'time': 2.0},
    {'name': 'Голубцы',
     'desc': 'Капустные рулетики с мясом. Восстанавливает 6 голода и даёт 4 оверхилла.',
     'ingredients': [{'type': 'cabbage', 'count': 1},
                     {'types': RAW_MEAT_TYPES, 'count': 2,
                      'label': 'Любое сырое мясо', 'icon': 'raw_beef'}],
     'result': {'type': 'cabbage_rolls', 'count': 1},
     'time': 3.0},
    {'name': 'Яблочный пирог',
     'desc': 'Пирог с яблоками и молоком. Восстанавливает 10 голода и даёт 8 оверхилла.',
     'ingredients': [{'type': 'wheat', 'count': 2},
                     {'type': 'bucket_milk', 'count': 1},
                     {'type': 'apple', 'count': 4}],
     'result': {'type': 'apple_pie', 'count': 1},
     'time': FURNACE_COOK_TIME},
]

SAW_RECIPES = [
    {'name': 'Опилки', 'desc': '1 бревно → 3 опилки',
     'logs': 1, 'result': {'type': 'sawdust', 'count': 3}},
    {'name': 'Палка', 'desc': '1 бревно → 4 палки',
     'logs': 1, 'result': {'type': 'stick', 'count': 4}},
    {'name': 'Доска', 'desc': '1 бревно → 2 доски',
     'logs': 1, 'result': {'type': 'board', 'count': 2}},
]

# Чертежи, доступные только через стол конструктора.
DESIGN_TABLE_RECIPES = [
    {'name': 'Кресло',
     'desc': 'Мягкое зелёное кресло. Ставится кликом по земле; '
             'щёлкните по нему, чтобы сесть.',
     'ingredients': [{'type': 'wool', 'count': 6},
                     {'type': 'stick', 'count': 2}],
     'result': {'type': 'armchair', 'count': 1}},
    {'name': 'Стол',
     'desc': 'Деревянный стол для трёх предметов. Поставьте его и '
             'перетащите предметы из инвентаря; щёлкните по столу, '
             'чтобы забрать вещь.',
     'ingredients': [{'type': 'board', 'count': 3},
                     {'type': 'stick', 'count': 2}],
     'result': {'type': 'table', 'count': 1}},
    {'name': 'Плюшевый мишка',
     'desc': 'Мягкий мишка из опилок и шерсти. Чистое украшение: '
             'ставится кликом по земле, ничего не делает.',
     'ingredients': [{'type': 'sawdust', 'count': 3},
                     {'type': 'wool', 'count': 4}],
     'result': {'type': 'teddy_bear', 'count': 1}},
]

# Кузнечные рецепты: железный набор брони и улучшенные инструменты.
# Броня, как и тестовая, ничего не меняет в характеристиках — только внешний вид.
ANVIL_RECIPES = [
    {'name': 'Железный шлем',
     'desc': 'Кованый шлем из трёх слитков. Надевается в слот головы.',
     'ingredients': [{'type': 'ingot', 'count': 3}],
     'result': {'type': 'iron_helmet', 'count': 1}},
    {'name': 'Железная кираса',
     'desc': 'Тяжёлая кираса из шести слитков. Надевается в слот тела.',
     'ingredients': [{'type': 'ingot', 'count': 6}],
     'result': {'type': 'iron_chestplate', 'count': 1}},
    {'name': 'Железные поножи',
     'desc': 'Пластины на ноги из четырёх слитков. Надеваются в слот ног.',
     'ingredients': [{'type': 'ingot', 'count': 4}],
     'result': {'type': 'iron_leggings', 'count': 1}},
    {'name': 'Железные сапоги',
     'desc': 'Кованые сапоги из трёх слитков. Надеваются в слот ступней.',
     'ingredients': [{'type': 'ingot', 'count': 3}],
     'result': {'type': 'iron_boots', 'count': 1}},
    {'name': 'Железные грабли',
     'desc': 'Улучшенные грабли для вскапывания земли (20 использований)',
     'ingredients': [{'type': 'stick', 'count': 2},
                     {'type': 'ingot', 'count': 1}],
     'result': {'type': 'iron_rake', 'count': 1}},
    {'name': 'Железный топор',
     'desc': 'Улучшенный топор для рубки деревьев (20 использований)',
     'ingredients': [{'type': 'stick', 'count': 1},
                     {'type': 'ingot', 'count': 2}],
     'result': {'type': 'iron_axe', 'count': 1}},
    {'name': 'Железный меч',
     'desc': 'Улучшенный клинок для защиты (20 ударов)',
     'ingredients': [{'type': 'stick', 'count': 2},
                     {'type': 'ingot', 'count': 2}],
     'result': {'type': 'iron_sword', 'count': 1}},
    {'name': 'Железная кирка',
     'desc': 'Улучшенная кирка для добычи руды (20 использований)',
     'ingredients': [{'type': 'stick', 'count': 1},
                     {'type': 'ingot', 'count': 3}],
     'result': {'type': 'iron_pickaxe', 'count': 1}},
]

# Базовые ячейки расширенного инвентаря. Рюкзак добавляет к ним ещё 6,
# поэтому массив всегда выделяется под MAX_EXT_SLOT_COUNT, а игроку
# показываются только доступные сейчас ячейки.
EXT_SLOT_COUNT = 18
BACKPACK_EXTRA_SLOTS = 6
MAX_EXT_SLOT_COUNT = EXT_SLOT_COUNT + BACKPACK_EXTRA_SLOTS

# Рюкзак добавляет 6 дополнительных слотов в инвентарь
# Крафтится из 4 кожи и 1 слитка железа
BACKPACK_CRAFT_RECIPES = [
    {'name': 'Рюкзак',
     'desc': 'Добавляет 6 дополнительных слотов инвентаря. '
             'Надевается в слот груди.',
     'ingredients': [{'type': 'leather', 'count': 4}, {'type': 'ingot', 'count': 1}],
     'result': {'type': 'backpack', 'count': 1}},
]
