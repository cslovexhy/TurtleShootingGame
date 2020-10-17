from Constants import *
from ColorDefinition import *


class WallUnit:
    def __init__(self, health=5, defense=0, color=CHOCOLATE):
        self.max_health = health
        self.health = health
        self.defense = defense
        self.color = color
        self.shape = "square"


class BrickWallUnit(WallUnit):
    def __init__(self):
        super().__init__()


class StoneWallUnit(WallUnit):
    def __init__(self):
        super().__init__(99999, 99999, SILVER)


brick_sample = BrickWallUnit()

stone_sample = StoneWallUnit()