import time, random
from copy import deepcopy
from ColorDefinition import *
from ShapeDefinition import *
from WallUnitDefinition import *

EFFECT_SLOW_MOVEMENT = "EFFECT_SLOW_MOVEMENT"
EFFECT_SLOW_ATTACK = "EFFECT_SLOW_ATTACK"
EFFECT_BURN = "EFFECT_BURN"
EFFECT_POISON = "EFFECT_POISON"

EFFECT_KEY_PERCENT = "percent"
EFFECT_KEY_DURATION = "duration"
EFFECT_KEY_DAMAGE = "damage"
EFFECT_KEY_INTERVAL = "interval"
EFFECT_KEY_COUNT = "count"
EFFECT_KEY_APPLY_TIME = "apply_time"
EFFECT_KEY_LAST_PROC_TIME = "last_proc_time"

EFFECT_KEY_MAP = {
    EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT, EFFECT_KEY_DURATION},
    EFFECT_SLOW_ATTACK: {EFFECT_KEY_PERCENT, EFFECT_KEY_DURATION},  # TODO: slow attack
    EFFECT_BURN: {EFFECT_KEY_DAMAGE, EFFECT_KEY_INTERVAL, EFFECT_KEY_COUNT},
    EFFECT_POISON: {EFFECT_KEY_PERCENT, EFFECT_KEY_INTERVAL, EFFECT_KEY_COUNT},
}


class Skill:
    def __init__(self, name, cool_down, effects=None):
        self.name = name
        self.cool_down = cool_down
        self.last_used = 0
        self.effects = effects if effects is not None else dict()

    def is_ready(self):
        now = time.time()
        return now - self.last_used > self.cool_down


class SimpleRangedSkill(Skill):
    # conversion means how much % of attack goes into damage
    def __init__(self, name, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=0):
        super().__init__(
            name=name,
            cool_down=cool_down,
            effects=effects
        )
        self.flying_speed = flying_speed
        self.attack_range = attack_range
        self.conversion = conversion
        self.shape = shape
        self.color = color
        self.spin = spin
        self.visited = set()

    def should_penetrate(self, obj_hit):
        is_wall = "wall_" in obj_hit.id and isinstance(obj_hit.wall_unit_data, WallUnit)
        if is_wall:
            return False
        value = random.randint(0, 99)
        if self.shape == SHAPE_ARROW:
            return value < 50
        elif self.shape == SHAPE_TRIANGLE:
            return value < 35
        elif self.shape == SHAPE_SQUARE:
            return value < 20
        elif self.shape == SHAPE_CIRCLE:
            return value < 10
        else:
            return False

    def is_visited(self, obj_hit):
        id = obj_hit.id
        is_stone_wall = "wall_" in id and isinstance(obj_hit.wall_unit_data, StoneWallUnit)
        if is_stone_wall:
            # print("is stone wall")
            return False
        else:
            pass
            # print("not stone wall: " + str(vars(obj_hit)))
            # print("is not stone wall")
        result = id in self.visited
        self.visited.add(id)
        # print("obj_id = {}, visited = {}".format(str(self.visited), result))
        return result

    def increase_power(self):
        self.conversion += 0.1


class SimpleSummonSkill(Skill):
    def __init__(self, name, cool_down, battle_unit, attack_range=250, count=1):
        super().__init__(
            name=name,
            cool_down=cool_down,
        )
        self.attack_range = attack_range
        self.battle_unit = battle_unit
        self.shape = battle_unit.shape
        self.color = battle_unit.color
        self.count = count

    def increase_power(self):
        self.count += 1


class SimpleRangedSkillWithSplash(SimpleRangedSkill):
    def __init__(self, name, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, shard_count=3, shard_data=None):
        super().__init__(
            name=name,
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

    def increase_power(self):
        self.conversion += 0.1
        self.shard_count += 1


class SimpleRangedSkillWithHealthBurn(SimpleRangedSkill):
    def __init__(self, name, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, health_burn=999):
        super().__init__(
            name=name,
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

    def increase_power(self):
        self.conversion += 0.1


class SimpleNovaSkill(SimpleRangedSkill):
    def __init__(self, name, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, shard_count=16):
        super().__init__(
            name=name,
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

    def increase_power(self):
        self.conversion += 0.1
        self.shard_count += 1


class SimpleMultiShotSkill(SimpleRangedSkill):
    def __init__(self, name, attack_range, flying_speed, conversion, cool_down, shape, color, effects=None, spin=30, shard_count=16):
        super().__init__(
            name=name,
            attack_range=attack_range,
            flying_speed=flying_speed,
            conversion=conversion,
            cool_down=cool_down,
            shape=shape,
            color=color,
            effects=effects,
            spin=spin,
        )
        assert(shard_count >= 2)
        self.shard_count = shard_count

    def increase_power(self):
        self.conversion += 0.1
        self.shard_count += 1


def copy_effects_with_apply_time(effect):
    e = deepcopy(effect)
    e[EFFECT_KEY_APPLY_TIME] = time.time()
    return e


skill_fire_ball = SimpleRangedSkill(
    name="Fire Ball",
    attack_range=300,
    flying_speed=2.0,
    conversion=1.0,
    cool_down=1,
    shape=SHAPE_CIRCLE,
    effects={EFFECT_BURN: {EFFECT_KEY_DAMAGE: 3, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3}},
    color=RED,
)

skill_ice_ball = SimpleRangedSkill(
    name="Ice Ball",
    attack_range=350,
    flying_speed=1.2,
    conversion=1.0,
    cool_down=1,
    shape=SHAPE_CIRCLE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5}},
    color=BLUE,
)

skill_punch = SimpleRangedSkill(
    name="Punch",
    attack_range=100,
    flying_speed=2,
    conversion=1.0,
    cool_down=0.5,
    shape=SHAPE_TRIANGLE,
    color=PURPLE
)

skill_icy_blast_shard = SimpleRangedSkill(
    name="Icy Blast Shard",
    attack_range=50,
    flying_speed=1.5,
    conversion=0.5,
    cool_down=None,
    shape=SHAPE_TRIANGLE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5}},
    color=BLUE,
    spin=30
)

skill_icy_blast = SimpleRangedSkillWithSplash(
    name="Icy Blast",
    attack_range=300,
    flying_speed=1.5,
    conversion=1.0,
    cool_down=.5,
    shape=SHAPE_TRIANGLE,
    color=BLUE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5}},
    spin=30,
    shard_data=deepcopy(skill_icy_blast_shard)
)

skill_suicide_attack = SimpleRangedSkillWithHealthBurn(
    name="Suicide Attack",
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
    attack_range=200,
    flying_speed=2.0,
    conversion=0.6,
    cool_down=1,
    shape=SHAPE_ARROW,
    color=WHITE,
    spin=45,
    shard_count=3
)


skill_frost_nova = SimpleNovaSkill(
    name="Frost Nova",
    attack_range=250,
    flying_speed=2.0,
    conversion=0.6,
    cool_down=1,
    shape=SHAPE_ARROW,
    color=BLUE,
    effects={EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .5, EFFECT_KEY_DURATION: 1.5},
             EFFECT_BURN: {EFFECT_KEY_DAMAGE: 10, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3}},
    spin=45,
    shard_count=3
)


skill_fire_ring = SimpleNovaSkill(
    name="Fire Ring",
    attack_range=700,
    flying_speed=2.5,
    conversion=0.6,
    cool_down=5,
    shape=SHAPE_CIRCLE,
    color=RED,
    effects={EFFECT_BURN: {EFFECT_KEY_DAMAGE: 3, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3}},
    shard_count=12,
    spin=0
)


skill_poison_nova = SimpleNovaSkill(
    name="Poison Nova",
    attack_range=500,
    flying_speed=1,
    conversion=0.3,
    cool_down=1,
    shape=SHAPE_CIRCLE,
    color=DARK_GREEN,
    effects={EFFECT_POISON: {EFFECT_KEY_PERCENT: 3, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3},
             EFFECT_BURN: {EFFECT_KEY_DAMAGE: 10, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3},
             EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .2, EFFECT_KEY_DURATION: 6}},
    shard_count=20,
    spin=25
)


skill_poison_dart = SimpleRangedSkill(
    name="Poison Dart",
    attack_range=300,
    flying_speed=1,
    conversion=1,
    cool_down=1.5,
    shape=SHAPE_TRIANGLE,
    color=DARK_GREEN,
    effects={EFFECT_POISON: {EFFECT_KEY_PERCENT: 3, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3},
             EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .2, EFFECT_KEY_DURATION: 6}},
    spin=25
)

skill_fire_dart = SimpleRangedSkill(
    name="Fire Dart",
    attack_range=300,
    flying_speed=1,
    conversion=1,
    cool_down=1.5,
    shape=SHAPE_TRIANGLE,
    color=RED,
    effects={EFFECT_BURN: {EFFECT_KEY_DAMAGE: 2, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 2}},
    spin=25,
)

skill_multi_shot = SimpleMultiShotSkill(
    name="Multi Shot",
    attack_range=400,
    flying_speed=3.5,
    conversion=0.8,
    cool_down=2,
    shape=SHAPE_TRIANGLE,
    color=PURPLE,
    shard_count=3,
    spin=45
)

skill_poison_barrage = SimpleMultiShotSkill(
    name="Poison Barrage",
    attack_range=400,
    flying_speed=3.5,
    conversion=0.5,
    cool_down=0.3,
    shape=SHAPE_TRIANGLE,
    color=DARK_GREEN,
    shard_count=3,
    effects={EFFECT_POISON: {EFFECT_KEY_PERCENT: 3, EFFECT_KEY_INTERVAL: 2, EFFECT_KEY_COUNT: 3},
             EFFECT_SLOW_MOVEMENT: {EFFECT_KEY_PERCENT: .2, EFFECT_KEY_DURATION: 6}},
    spin=45
)

# cannot circle back from BattleUnitDefinition's samples and create skills here, would cause some bad loop.
def create_summon_skill(name, cool_down, battle_unit, count):
    return SimpleSummonSkill(
        name=name,
        cool_down=cool_down,
        battle_unit=battle_unit,
        count=count,
    )
