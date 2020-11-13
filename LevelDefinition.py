from BattleUnitDefinition import *
from SkillDefinition import *
from WallUnitDefinition import *
from MapDefinition import *

MIN_LEVEL = 1
MAX_LEVEL = 4
START_LEVEL = 3

MAX_GAME_TIME = 3600

assert(MIN_LEVEL <= START_LEVEL <= MAX_LEVEL)


def validate_level(level):
    assert(MIN_LEVEL <= level <= MAX_LEVEL, "Wrong level: {}".format(str(level)))


def get_units_by_level(level):
    validate_level(level)
    if level == 1:
        return get_units_from_layout(LEVEL_1_LAYOUT)
    elif level == 2:
        return get_units_from_layout(LEVEL_2_LAYOUT)
    elif level == 3:
        return get_units_from_layout(LEVEL_3_LAYOUT)
    elif level == 4:
        return get_units_from_layout(LEVEL_4_LAYOUT)
    else:
        raise Exception("level %s map is not defined.".format(str(level)))
