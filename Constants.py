# numbers here needs to be 40*N, otherwise path-finding algorithm will not work
WINDOW_X, WINDOW_Y = 1400, 760

FRAME = 13
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


def get_battle_unit_base_speed():
    base_speed = BATTLE_UNIT_BASE_SPEED / FRAME
    # print("base speed = " + str(base_speed))
    return base_speed


def get_missile_base_speed():
    return MISSILE_BASE_SPEED / FRAME


def update_frame(value):
    global FRAME
    print("FRAME updated to: " + str(value))
    FRAME = value
