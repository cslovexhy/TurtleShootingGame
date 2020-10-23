from Constants import *
from BattleUnitDefinition import *
from WallUnitDefinition import *

MAP_STONE_WALL = 's'
MAP_BRICK_WALL = 'b'

MAP_PLAYER = 'p'

MAP_ENEMY_BIKER = '0'
MAP_ENEMY_ENFORCER = '1'
MAP_ENEMY_FREEZER = '2'
MAP_ENEMY_FLAMETHROWER = '3'
MAP_ENEMY_SUICIDE_DRONE = '4'
MAP_ENEMY_UNDERBOSS = '5'

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


def to_map_cor(col_id, row_id):
    return int(col_id * 20 - WINDOW_X / 2 + 10), int(row_id * 20 - WINDOW_Y / 2 + 10)


def get_units_from_layout(layout):
    player = None
    enemies = []
    walls = []
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
            else:
                if v != MAP_EMPTY:
                    raise Exception("unexpected map item: {}".format(v))
    for e in enemies:
        e.set_player(player)
    return player, enemies, walls


LEVEL_1_LAYOUT = """
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s s s s s s s s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . 0 . . 0 . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . 3 . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s s s s s s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . . . s . s
s . . . . . . . . . . . . . . . . . . . . 4 . . . . . . . . . . . . 3 . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . . s . s
s . . . . . . . p . . . . . . . . . . . . 4 . . . . . . . . . . . . . 5 . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . . s . s
s . . . . . . . . . . . . . . . . . . . . 4 . . . . . . . . . . . . 3 . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s s s s s s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . 2 . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . 0 . . 0 . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s . . . . . . s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . s s s s s s s s . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
"""

