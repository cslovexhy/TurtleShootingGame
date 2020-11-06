from Constants import *
from ColorDefinition import *
from ShapeDefinition import *
from copy import deepcopy


class WallUnit:
    def __init__(self, health=5, defense=0, color=CHOCOLATE):
        self.max_health = health
        self.health = health
        self.defense = defense
        self.color = color
        self.color_dim = to_dim_color(color)
        self.shape = SHAPE_SQUARE


class BrickWallUnit(WallUnit):
    def __init__(self):
        super().__init__()


class StoneWallUnit(WallUnit):
    def __init__(self):
        super().__init__(99999, 99999, SILVER)


brick_sample = BrickWallUnit()

stone_sample = StoneWallUnit()