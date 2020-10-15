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


def get_walls_from_layout(layout):
    walls = []
    rows = reversed([row for row in layout.split("\n") if row])
    for row_id, row in enumerate(rows):
        for col_id, v in enumerate(row.split(" ")):
            if v in ('s', 'b'):
                x = int(col_id * 20 - WINDOW_X / 2 + 10)
                y = int(row_id * 20 - WINDOW_Y / 2 + 10)
                if v == 's':
                    walls.append(StoneWallUnit((x, y)))
                else:
                    walls.append(BrickWallUnit((x, y)))
    return walls


WALL_LAY_OUT_LEVEL_1 = """
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . b b b b b b b b b b b b b b b b b b b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b b b b b b b b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b . . . . . . b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b . . . . . . b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b . . . . . . b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b . . . . . . b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b . . . . . . b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . b b b b b b b b . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b . . . . . . . . . . . . . . . . . b . . . . . . . . . . . . . . . . . . s
s . b b b b b b b b b b b b b b b b b b b . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . s
s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s s
"""