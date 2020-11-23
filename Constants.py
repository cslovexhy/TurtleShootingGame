import os

FRAME_KEY = "FRAME"

# numbers here needs to be 40*N, otherwise path-finding algorithm will not work
WINDOW_X, WINDOW_Y = 1400, 760

MAX_SHAPE_PCT = 2.0
MIN_SHAPE_PCT = .4
STANDARD_HEALTH = 100
SLEEP_INTERVAL = 0
UP, DOWN, RIGHT, LEFT, STOP = "up", "down", "right", "left", "stop"
BATTLE_UNIT_BASE_SPEED = 30.0      # 50 pixel per second
MISSILE_BASE_SPEED = 100.0    # 200 pixel per second
ENFORCER = "ENFORCER"
SNIPER = "SNIPER"

AI_DECISION_MOVE = "AI_DECISION_MOVE"
AI_DECISION_ATTACK = "AI_DECISION_ATTACK"

ENABLE_CANVAS_MOVING = False
ENABLE_WAR_MIST = False


def get_frame():
    if FRAME_KEY not in os.environ:
        os.environ[FRAME_KEY] = str(13.0)
    return float(os.environ[FRAME_KEY])


def update_frame(value):
    os.environ[FRAME_KEY] = str(value)


def get_battle_unit_base_speed():
    base_speed = BATTLE_UNIT_BASE_SPEED / get_frame()
    # print("base speed = " + str(base_speed))
    return base_speed


def get_missile_base_speed():
    return MISSILE_BASE_SPEED / get_frame()
