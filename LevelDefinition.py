from BattleUnitDefinition import *
from SkillDefinition import *
from WallUnitDefinition import *

MIN_LEVEL = 1
MAX_LEVEL = 3

MAX_GAME_TIME = 3600


def validate_level(level):
    assert(MIN_LEVEL <= level <= MAX_LEVEL, "Wrong level: {}".format(str(level)))


def get_player_by_level(level):
    validate_level(level)
    if level == 1:
        return PlayerUnit()
    elif level == 2:
        return PlayerUnit(skills=[skill_fire_ball, skill_ice_ball])
    elif level == 3:
        return PlayerUnit(skills=[skill_fire_ball, skill_ice_ball])
    else:
        raise "level %s player is not defined.".format(str(level))


def get_enemies_by_level(level, player):
    validate_level(level)
    if level == 1:
        return [
            EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=player),
        ]
    elif level == 2:
        return [
            EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=player),
            EnemyUnit(start_pos=(100, 0), health=30, attack=5, defense=3, player=player),
            EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=player),
        ]
    elif level == 3:
        return [
            EnemyUnit(start_pos=(100, 100), health=20, attack=5, defense=2, player=player, speed=.5),
            EnemyUnit(start_pos=(100, 0), health=30, attack=5, defense=3, player=player, speed=.55),
            EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=player, speed=.6),
            EnemyUnit(start_pos=(100, -200), health=50, attack=7, defense=2, player=player, speed=.65),
            EnemyUnit(start_pos=(100, -300), health=50, attack=7, defense=2, player=player, speed=.7),
            EnemyUnit(start_pos=(100, -400), health=50, attack=7, defense=2, player=player, speed=.75),
            EnemyUnit(start_pos=(100, -500), health=50, attack=7, defense=2, player=player, speed=.8),
        ]
    else:
        raise "level %s enemy list is not defined.".format(str(level))


def get_walls_by_level(level):
    validate_level(level)
    if level == 1:
        return get_walls_from_layout(WALL_LAY_OUT_LEVEL_1)
    elif level == 2:
        return get_walls_from_layout(WALL_LAY_OUT_LEVEL_1)
    elif level == 3:
        return get_walls_from_layout(WALL_LAY_OUT_LEVEL_1)
    else:
        raise "level %s wall list is not defined.".format(str(level))