import time
from copy import deepcopy
from ColorDefinition import *
from ShapeDefinition import *

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

    def is_ready(self):
        now = time.time()
        return now - self.last_used > self.cool_down


class SimpleRangedSkill(Skill):
    # conversion means how much % of attack goes into damage
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=0):
        super().__init__(
            name=name,
            key=key,
            cool_down=cool_down,
            effects=effects
        )
        self.flying_speed = flying_speed
        self.attack_range = attack_range
        self.conversion = conversion
        self.shape = shape
        self.color = color
        self.spin = spin


class SimpleRangedSkillWithSplash(SimpleRangedSkill):
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, shard_count=3, shard_data=None):
        super().__init__(
            name=name,
            key=key,
            attack_range=attack_range,
            flying_speed=flying_speed,
            conversion=conversion,
            cool_down=cool_down,
            shape=shape,
            color=color,
            effects=effects,
            spin=spin
        )
        self.shard_count = shard_count
        self.shard_data = shard_data


class SimpleRangedSkillWithHealthBurn(SimpleRangedSkill):
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, health_burn=999):
        super().__init__(
            name=name,
            key=key,
            attack_range=attack_range,
            flying_speed=flying_speed,
            conversion=conversion,
            cool_down=cool_down,
            shape=shape,
            color=color,
            effects=effects,
            spin=spin
        )
        self.health_burn = health_burn


class SimpleNovaSkill(SimpleRangedSkill):
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, shard_count=16):
        super().__init__(
            name=name,
            key=key,
            attack_range=attack_range,
            flying_speed=flying_speed,
            conversion=conversion,
            cool_down=cool_down,
            shape=shape,
            color=color,
            effects=effects,
            spin=spin,
        )
        self.shard_count = shard_count


def copy_effects_with_apply_time(effect):
    e = deepcopy(effect)
    e[EFFECT_KEY_APPLY_TIME] = time.time()
    return e


def reassign_skill_keys(skills):
    for i, s in enumerate(skills):
        s.key = str(i+1)


skill_fire_ball = SimpleRangedSkill(
    name="Fire Ball",
    key='1',
    attack_range=250,
    flying_speed=2.0,
    conversion=0.7,
    cool_down=1,
    shape=SHAPE_CIRCLE,
    color=RED,
)

skill_ice_ball = SimpleRangedSkill(
    name="Ice Ball",
    key='2',
    attack_range=350,
    flying_speed=1.2,
    conversion=0.5,
    cool_down=1,
    shape=SHAPE_CIRCLE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5}},
    color=BLUE,
)

skill_punch = SimpleRangedSkill(
    name="Punch",
    key='3',
    attack_range=150,
    flying_speed=1,
    conversion=1,
    cool_down=0.5,
    shape=SHAPE_TRIANGLE,
    color=PURPLE
)

skill_icy_blast_shard = SimpleRangedSkill(
    name="Icy Blast Shard",
    key=None,
    attack_range=50,
    flying_speed=1.5,
    conversion=0.45,
    cool_down=None,
    shape=SHAPE_TRIANGLE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5}},
    color=BLUE,
    spin=30
)

skill_icy_blast = SimpleRangedSkillWithSplash(
    name="Icy Blast",
    key='4',
    attack_range=300,
    flying_speed=1.5,
    conversion=0.8,
    cool_down=.5,
    shape=SHAPE_TRIANGLE,
    color=BLUE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5}},
    spin=30,
    shard_data=deepcopy(skill_icy_blast_shard)
)

skill_suicide_attack = SimpleRangedSkillWithHealthBurn(
    name="Suicide Attack",
    key='3',
    attack_range=10,
    flying_speed=5,
    conversion=1,
    cool_down=999,
    shape=SHAPE_TRIANGLE,
    color=WHITE,
    health_burn=999
)

skill_nova = SimpleNovaSkill(
    name="Nova",
    key='4',
    attack_range=200,
    flying_speed=2.0,
    conversion=0.6,
    cool_down=1,
    shape=SHAPE_ARROW,
    color=WHITE,
    spin=45
)

skill_poison_dart = SimpleRangedSkill(
    name="Poison Dart",
    key='3',
    attack_range=300,
    flying_speed=1,
    conversion=1,
    cool_down=1.5,
    shape=SHAPE_TRIANGLE,
    color=DARK_GREEN,
    spin=25
)

skill_fire_dart = SimpleRangedSkill(
    name="Fire Dart",
    key='3',
    attack_range=300,
    flying_speed=1,
    conversion=1,
    cool_down=1.5,
    shape=SHAPE_TRIANGLE,
    color=RED,
    spin=25
)