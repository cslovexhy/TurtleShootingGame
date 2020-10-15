import time
from copy import deepcopy

EFFECT_SLOW_MOVEMENT = "EFFECT_SLOW_MOVEMENT"
EFFECT_SLOW_ATTACK = "EFFECT_SLOW_ATTACK"
EFFECT_BURN = "EFFECT_BURN"

EFFECT_KEY_PERCENT = "percent"
EFFECT_KEY_DURATION = "duration"
EFFECT_KEY_DAMAGE = "damage"
EFFECT_KEY_INTERVAL = "interval"
EFFECT_KEY_COUNT = "count"
EFFECT_KEY_APPLY_TIME = "apply_time"

EFFECT_KEY_MAP = {
    EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT, EFFECT_KEY_DURATION},
    EFFECT_SLOW_ATTACK: {EFFECT_KEY_PERCENT, EFFECT_KEY_DURATION},
    EFFECT_BURN: {EFFECT_KEY_DAMAGE, EFFECT_KEY_INTERVAL, EFFECT_KEY_COUNT}
}


class Skill:
    def __init__(self, name, key, cool_down, effects=None):
        self.name = name
        self.key = key
        self.cool_down = cool_down
        self.last_used = 0
        self.effects = effects if effects is not None else dict()


class SimpleRangedSkill(Skill):
    # conversion means how much % of attack goes into damage
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30):
        super().__init__(name, key, cool_down, effects)
        self.flying_speed = flying_speed
        self.attack_range = attack_range
        self.conversion = conversion
        self.shape = shape
        self.color = color
        self.spin = spin

    def is_ready(self):
        now = time.time()
        return now - self.last_used > self.cool_down


def copy_effects_with_apply_time(effect):
    e = deepcopy(effect)
    e[EFFECT_KEY_APPLY_TIME] = time.time()
    return e


skill_fire_ball = SimpleRangedSkill(
    name="Fire Ball",
    key='1',
    attack_range=250,
    flying_speed=2.0,
    conversion=0.7,
    cool_down=1,
    shape="circle",
    color="red",
    spin=0
)

skill_ice_ball = SimpleRangedSkill(
    name="Ice Ball",
    key='2',
    attack_range=350,
    flying_speed=1.2,
    conversion=0.5,
    cool_down=2,
    shape="square",
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 5}},
    color="blue",
    spin=20
)

skill_punch = SimpleRangedSkill(
    name="Punch",
    key='3',
    attack_range=150,
    flying_speed=1,
    conversion=1,
    cool_down=3,
    shape="triangle",
    color="black"
)