SHAPE_TURTLE = "turtle"
SHAPE_TRIANGLE = "triangle"
SHAPE_CIRCLE = "circle"
SHAPE_SQUARE = "square"
SHAPE_ARROW = "arrow"

SHAPE_SHARK = "assets/baby_shark.gif"
SHAPE_HEALTH_POTION = "assets/health_potion.gif"
SHAPE_ATTACK_PACK = "assets/attack.gif"
SHAPE_DEFENSE_PACK = "assets/defense.gif"
SHAPE_BRICK_WALL = "assets/brick.gif"
SHAPE_STONE_WALL = "assets/stone.gif"
SHAPE_SNOWFLAKE = "assets/snowflake.gif"

all_customized_shapes = {
    SHAPE_SHARK,
    SHAPE_HEALTH_POTION,
    SHAPE_ATTACK_PACK,
    SHAPE_DEFENSE_PACK,
    SHAPE_BRICK_WALL,
    SHAPE_STONE_WALL,
    SHAPE_SNOWFLAKE,
}


def register_all_shapes(screen):
    for shape in all_customized_shapes:
        screen.register_shape(shape)