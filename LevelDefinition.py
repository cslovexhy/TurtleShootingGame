from BattleUnitDefinition import *
from SkillDefinition import *
from WallUnitDefinition import *
from MapDefinition import *

MIN_LEVEL = 1
MAX_LEVEL = 9
START_LEVEL = 9

MAX_GAME_TIME = 3600

assert(MIN_LEVEL <= START_LEVEL <= MAX_LEVEL)


def validate_level(level):
    assert(MIN_LEVEL <= level <= MAX_LEVEL, "Wrong level: {}".format(str(level)))


def get_units_by_level(level):
    validate_level(level)
    if level not in all_levels:
        raise Exception("level %s map is not defined.".format(str(level)))
    level_map = all_levels[level]
    return get_units_from_layout(level_map)
