from Constants import *
from ColorDefinition import *
from ShapeDefinition import *
from copy import deepcopy


class WallUnit:
    def __init__(self, health=5, defense=0, color=CHOCOLATE, shape=SHAPE_SQUARE):
        self.max_health = health
        self.health = health
        self.defense = defense
        self.color = color
        self.color_dim = to_dim_color(color)
        self.shape = shape


class BrickWallUnit(WallUnit):
    def __init__(self):
        super().__init__(shape=SHAPE_BRICK_WALL)


class StoneWallUnit(WallUnit):
    def __init__(self):
        super().__init__(health=99999, defense=99999, shape=SHAPE_STONE_WALL)


brick_sample = BrickWallUnit()

stone_sample = StoneWallUnit()