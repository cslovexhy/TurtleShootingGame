from Constants import *
from BattleUnitDefinition import *
from WallUnitDefinition import *
from ItemUnitDefinition import *

MAP_STONE_WALL = 's'
MAP_BRICK_WALL = 'b'

MAP_PLAYER = 'p'

MAP_ENEMY_BIKER = '0'
MAP_ENEMY_ENFORCER = '1'
MAP_ENEMY_FREEZER = '2'
MAP_ENEMY_FLAMETHROWER = '3'
MAP_ENEMY_SUICIDE_DRONE = '4'
MAP_ENEMY_UNDERBOSS = '5'

MAP_ITEM_SKILL_FIRE_BALL = 'F'
MAP_ITEM_SKILL_ICE_BALL = 'I'
MAP_ITEM_SKILL_ICY_BLAST = 'B'

MAP_EMPTY = '.'

MAP_UNIT_KEY_TO_SAMPLE_OBJ = {
    MAP_STONE_WALL: stone_sample,
    MAP_BRICK_WALL: brick_sample,
    MAP_PLAYER: player_sample,
    MAP_ENEMY_BIKER: enemy_biker_sample,
    MAP_ENEMY_ENFORCER: enemy_enforcer_sample,
    MAP_ENEMY_FREEZER: enemy_freezer_sample,
    MAP_ENEMY_FLAMETHROWER: enemy_flamethrower_sample,
    MAP_ENEMY_SUICIDE_DRONE: enemy_suicide_drone_sample,
    MAP_ENEMY_UNDERBOSS: enemy_underboss_sample,
    MAP_ITEM_SKILL_FIRE_BALL: skill_fire_ball_item_sample,
    MAP_ITEM_SKILL_ICE_BALL: skill_ice_ball_item_sample,
    MAP_ITEM_SKILL_ICY_BLAST: skill_icy_blast_item_sample,
}

MAP_WALL_UNIT_SET = {
    MAP_STONE_WALL,
    MAP_BRICK_WALL,
}

MAP_BATTLE_UNIT_SET = {
    MAP_PLAYER,
    MAP_ENEMY_BIKER,
    MAP_ENEMY_ENFORCER,
    MAP_ENEMY_FREEZER,
    MAP_ENEMY_FLAMETHROWER,
    MAP_ENEMY_SUICIDE_DRONE,
    MAP_ENEMY_UNDERBOSS,
}

MAP_ITEM_UNIT_SET = {
    MAP_ITEM_SKILL_FIRE_BALL,
    MAP_ITEM_SKILL_ICE_BALL,
    MAP_ITEM_SKILL_ICY_BLAST,
}


def to_map_cor(col_id, row_id):
    return int(col_id * 20 - WINDOW_X / 2 + 10), int(row_id * 20 - WINDOW_Y / 2 + 10)


def get_units_from_layout(layout):
    player = None
    enemies = []
    walls = []
    items = []
    rows = reversed([row for row in layout.split("\n") if row])
    for row_id, row in enumerate(rows):
        for col_id, v in enumerate(row.split(" ")):
            if v in MAP_UNIT_KEY_TO_SAMPLE_OBJ:
                x, y = to_map_cor(col_id, row_id)
                if v not in MAP_UNIT_KEY_TO_SAMPLE_OBJ:
                    raise Exception("unsupported map unit type 1")
                unit = deepcopy(MAP_UNIT_KEY_TO_SAMPLE_OBJ[v])
                if v in MAP_BATTLE_UNIT_SET:
                    unit.start_pos = (x, y)
                    if v == MAP_PLAYER:
                        player = unit
                    else:
                        enemies.append(unit)
                if v in MAP_WALL_UNIT_SET:
                    unit.pos = (x, y)
                    walls.append(unit)
                if v in MAP_ITEM_UNIT_SET:
                    unit.pos = (x, y)
                    items.append(unit)
            else:
                if v != MAP_EMPTY:
                    raise Exception("unexpected map item: {}".format(v))
    for e in enemies:
        e.set_player(player)
    return player, enemies, walls, items


LEVEL_1_LAYOUT = """
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . I . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . F . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . p . . . . . . . . . . . 1 . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . 1 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . B . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
"""

LEVEL_2_LAYOUT = """
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . 3 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . 2 . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . 1 . . . . . . . . . . . . . . . . . s
s . . . . . . . p . . . . . . . . . . . 3 . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . 1 . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1 . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 3 . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 3 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
"""

LEVEL_3_LAYOUT = """
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . 3 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . 4 . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . 2 . . . . . . . . . . . . . . . . . s
s . . . . . . . p . . . . . . . . . . . 4 . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . 2 . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 4 . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 3 . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 1 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 3 . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
"""

LEVEL_4_LAYOUT = """
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s s s s s s s s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . 4 . . 4 . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . 3 . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s s s s s s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . . . s . s
s . . . . . . . . . . . . . . . . . . . . 2 . . . . . . . . . . . . 3 . . s . s
s . . . . . . . . . . . . . . . . . . . 1 . 1 . . . . . . . . . . 1 . . . s . s
s . . . . . . . p . . . . . . . . . . . . 2 . . . . . . . . . . . . . 5 . s . s
s . . . . . . . . . . . . . . . . . . . 1 . 1 . . . . . . . . . . 1 . . . s . s
s . . . . . . . . . . . . . . . . . . . . 2 . . . . . . . . . . . . 3 . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4 . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s s s s s s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . 3 . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . 4 . . 4 . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s s s s s s s s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
"""

