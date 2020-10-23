def inv(v):
    return round(float(v) / 255, 2)


def normalize(r, g, b):
    return inv(r), inv(g), inv(b)


ORANGE = normalize(255, 69, 0)

RED = normalize(255, 0, 0)
PURPLE = normalize(148, 0, 211)
BLUE = normalize(0, 0, 255)
GREEN = normalize(0, 128, 0)
DARK_GREEN = normalize(0, 64, 0)

CHOCOLATE = normalize(210, 105, 30)
BROWN = normalize(165, 42, 42)

WHITE = normalize(255, 255, 255)
SILVER = normalize(216, 216, 216)
GRAY = normalize(128, 128, 128)
BLACK = normalize(0, 0, 0)