from Constants import *


class WallUnit:
    def __init__(self, pos, health, defense, color):
        self.pos = pos
        self.max_health = health
        self.health = health
        self.defense = defense
        self.color = color
        self.shape = "square"


class BrickWallUnit(WallUnit):
    def __init__(self, pos):
        super().__init__(pos, 5, 0, 'brown')


class StoneWallUnit(WallUnit):
    def __init__(self, pos):
        super().__init__(pos, 99999, 99999, 'black')

