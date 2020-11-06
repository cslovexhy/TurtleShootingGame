SHAPE_TURTLE = "turtle"
SHAPE_TRIANGLE = "triangle"
SHAPE_CIRCLE = "circle"
SHAPE_SQUARE = "square"
SHAPE_ARROW = "arrow"

SHAPE_SHARK = "assets/baby_shark.gif"
SHAPE_HEALTH_POTION = "assets/health_potion.gif"

all_customized_shapes = {
    SHAPE_SHARK,
    SHAPE_HEALTH_POTION,
}


def register_all_shapes(screen):
    for shape in all_customized_shapes:
        screen.register_shape(shape)