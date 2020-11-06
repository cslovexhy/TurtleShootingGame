SHAPE_TURTLE = "turtle"
SHAPE_TRIANGLE = "triangle"
SHAPE_CIRCLE = "circle"
SHAPE_SQUARE = "square"
SHAPE_ARROW = "arrow"

SHAPE_HEALTH_POTION = "assets/health_potion.gif"  # 128x128

all_customized_shapes = {
    SHAPE_HEALTH_POTION,
}


def register_all_shapes(screen):
    for shape in all_customized_shapes:
        screen.register_shape(shape)