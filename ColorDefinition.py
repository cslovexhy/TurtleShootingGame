def inv(v):
    return round(float(v) / 255, 2)


def normalize_color(r, g, b):
    return inv(r), inv(g), inv(b)


def to_dim_color(color):
    r, g, b = color
    x = .8
    return x * r, x * g, x * b


ORANGE = normalize_color(255, 69, 0)

RED = normalize_color(255, 0, 0)
PURPLE = normalize_color(148, 0, 211)
BLUE = normalize_color(0, 0, 255)
GREEN = normalize_color(0, 128, 0)
DARK_GREEN = normalize_color(0, 64, 0)

CHOCOLATE = normalize_color(210, 105, 30)
BROWN = normalize_color(165, 42, 42)

WHITE = normalize_color(255, 255, 255)
SILVER = normalize_color(216, 216, 216)
GRAY = normalize_color(128, 128, 128)
BLACK = normalize_color(0, 0, 0)