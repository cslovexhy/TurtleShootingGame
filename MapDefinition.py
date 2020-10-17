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
MAP_ENEMY_UNDERBOSS = '4'

MAP_EMPTY = '.'

MAP_UNIT_SET = {
    MAP_STONE_WALL,
    MAP_BRICK_WALL,
    MAP_PLAYER,
    MAP_ENEMY_BIKER,
    MAP_ENEMY_ENFORCER,
    MAP_ENEMY_FREEZER,
    MAP_ENEMY_FLAMETHROWER,
    MAP_ENEMY_UNDERBOSS
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
    MAP_ENEMY_UNDERBOSS
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
            if v in MAP_UNIT_SET:
                unit = None
                x, y = to_map_cor(col_id, row_id)
                if v == MAP_STONE_WALL:
                    unit = deepcopy(stone_sample)
                elif v == MAP_BRICK_WALL:
                    unit = deepcopy(brick_sample)
                elif v == MAP_PLAYER:
                    unit = deepcopy(player_sample)
                elif v == MAP_ENEMY_BIKER:
                    unit = deepcopy(enemy_biker_sample)
                elif v == MAP_ENEMY_ENFORCER:
                    unit = deepcopy(enemy_enforcer_sample)
                elif v == MAP_ENEMY_FREEZER:
                    unit = deepcopy(enemy_freezer_sample)
                elif v == MAP_ENEMY_FLAMETHROWER:
                    unit = deepcopy(enemy_flamethrower_sample)
                elif v == MAP_ENEMY_UNDERBOSS:
                    unit = deepcopy(enemy_underboss_sample)
                else:
                    raise Exception("unsupported map unit type 1")
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
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s s s s s s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0 . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0 . . . s . s
s . . . . . . . p . . . . . . . . . . . . . . . . . . . . . . . . . . 2 . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0 . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 1 . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 0 . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s s s s s s . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
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

