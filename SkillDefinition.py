import time

class Skill:
    def __init__(self, name, key, cool_down):
        self.name = name
        self.key = key
        self.cool_down = cool_down
        self.last_used = 0


class SimpleRangedSkill(Skill):
    # conversion means how much % of attack goes into damage
    def __init__(self, name, key, attack_range, flying_speed, conversion, cool_down, shape, color):
        super().__init__(name, key, cool_down)
        self.flying_speed = flying_speed
        self.attack_range = attack_range
        self.conversion = conversion
        self.shape = shape
        self.color = color

    def is_ready(self):
        now = time.time()
        return now - self.last_used > self.cool_down

skill_fire_ball = SimpleRangedSkill(
    name="Fire Ball",
    key='1',
    attack_range=200,
    flying_speed=1,
    conversion=0.7,
    cool_down=0.3,
    shape="circle",
    color="red"
)

skill_ice_ball = SimpleRangedSkill(
    name="Ice Ball",
    key='2',
    attack_range=300,
    flying_speed=0.8,
    conversion=0.5,
    cool_down=1,
    shape="circle",
    color="blue"
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