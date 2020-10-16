def inv(v):
    return round(float(v) / 255, 2)


def normalize(r, g, b):
    return inv(r), inv(g), inv(b)


ORANGE = normalize(255, 69, 0)

RED = normalize(255, 0, 0)
PURPLE = normalize(148, 0, 211)
BLUE = normalize(0, 0, 255)
GREEN = normalize(0, 128, 0)

SILVER = normalize(216, 216, 216)
CHOCOLATE = normalize(210, 105, 30)
BROWN = normalize(165, 42, 42)

BLACK = normalize(0, 0, 0)