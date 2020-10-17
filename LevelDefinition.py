from BattleUnitDefinition import *
from SkillDefinition import *
from WallUnitDefinition import *

MIN_LEVEL = 1
MAX_LEVEL = 3
START_LEVEL = 3

MAX_GAME_TIME = 3600

assert(MIN_LEVEL <= START_LEVEL <= MAX_LEVEL)


def validate_level(level):
    assert(MIN_LEVEL <= level <= MAX_LEVEL, "Wrong level: {}".format(str(level)))


def get_player_by_level(level):
    validate_level(level)
    if level == 1:
        return PlayerUnit()
    elif level == 2:
        return PlayerUnit()
    elif level == 3:
        return PlayerUnit()
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
            EnemyUnit(start_pos=(100, 100), health=50, attack=5, defense=2, player=player, speed=1.2),
            EnemyUnit(start_pos=(100, 0), health=50, attack=5, defense=3, player=player, speed=1.0, skills=[deepcopy(skill_ice_ball)], color=BLUE),
            EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=player, speed=1.2),
        ]
    elif level == 3:
        return [
            EnemyUnit(start_pos=(100, 100), health=50, attack=5, defense=2, player=player, speed=1.2),
            EnemyUnit(start_pos=(100, 0), health=50, attack=5, defense=3, player=player, speed=1.0, skills=[deepcopy(skill_ice_ball)], color=BLUE),
            EnemyUnit(start_pos=(100, -100), health=50, attack=7, defense=2, player=player, speed=1.2),
            EnemyUnit(start_pos=(200, 0), health=200, attack=15, defense=5, player=player, speed=1.5, skills=[deepcopy(skill_fire_ball)], color=PURPLE),
            EnemyUnit(start_pos=(300, 100), health=50, attack=5, defense=2, player=player, speed=1.2),
            EnemyUnit(start_pos=(300, 0), health=50, attack=5, defense=3, player=player, speed=1.0, skills=[deepcopy(skill_ice_ball)], color=BLUE),
            EnemyUnit(start_pos=(300, -100), health=50, attack=7, defense=2, player=player, speed=1.2),
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