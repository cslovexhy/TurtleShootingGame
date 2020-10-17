from Constants import *
from AIDefinition import *
from SkillDefinition import *
from ColorDefinition import *


class BattleUnit:
    def __init__(self, health, attack, defense, speed=1.0, color=GREEN, skills=None):
        if skills is None:
            skills = list()
        self.start_pos = None
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.skills = {skill.key: skill for skill in skills}
        self.color = color
        self.effects = dict()

    def set_start_pos(self, pos):
        """
        This has to be set from after init
        :param pos:
        :return:
        """
        self.start_pos = pos

    def get_shape_size(self):
        max_possible = MIN_SHAPE_PCT + (self.max_health / (STANDARD_HEALTH * MAX_SHAPE_PCT))
        pct = MIN_SHAPE_PCT + (max_possible - MIN_SHAPE_PCT) * (self.health / self.max_health)
        return pct


    def add_effects(self, effects):
        for effect_type, effect in effects.items():
            effect_with_apply_time = copy_effects_with_apply_time(effects[EFFECT_SLOW_MOVEMENT])
            self.effects[effect_type] = effect_with_apply_time
            print("effect {} added ".format(str(effect_type)))

    def get_speed(self):
        if EFFECT_SLOW_MOVEMENT not in self.effects:
            return self.speed

        # handle effect expiring case
        now = time.time()
        e = self.effects[EFFECT_SLOW_MOVEMENT]
        if now - e[EFFECT_KEY_APPLY_TIME] > e[EFFECT_KEY_DURATION]:
            del self.effects[EFFECT_SLOW_MOVEMENT]
            return self.speed

        # handle effect active case
        return self.speed * e[EFFECT_KEY_PERCENT]


class PlayerUnit(BattleUnit):
    def __init__(self, health=STANDARD_HEALTH, attack=20, defense=3, speed=2.0, color=ORANGE, skills=None):
        if skills is None:
            skills = [deepcopy(skill_fire_ball), deepcopy(skill_ice_ball), deepcopy(skill_punch)]
        assert len(skills) >= 1
        super().__init__(
            health=health,
            attack=attack,
            defense=defense,
            speed=speed,
            color=color,
            skills=skills
        )
        self.left_click_skill_key = skills[0].key
        if len(skills) == 1:
            self.right_click_skill_key = skills[0].key
        else:
            self.right_click_skill_key = skills[1].key


class EnemyUnit(BattleUnit):
    def __init__(self, health, attack, defense, ai_mode=ENFORCER, speed=1.0, color=GREEN, skills=None, aggro_range=AGGRO_RANGE_FOR_PULLING):
        if skills is None:
            skills = get_skill_list_by_mode(ai_mode)
        assert len(skills) >= 1
        super().__init__(
            health=health,
            attack=attack,
            defense=defense,
            speed=speed,
            color=color,
            skills=skills,
        )
        self.aggro_range = aggro_range
        self.left_click_skill_key = skills[0].key
        self.ai = AI(ai_mode, self)

    def set_player(self, player):
        self.ai.set_target_unit(player)


player_sample = PlayerUnit()
enemy_biker_sample = EnemyUnit(health=20, attack=5, defense=2, speed=1.5, color=GREEN)
enemy_enforcer_sample = EnemyUnit(health=40, attack=10, defense=3, color=DARK_GREEN)
enemy_freezer_sample = EnemyUnit(health=40, attack=10, defense=2, color=BLUE, skills=deepcopy([skill_ice_ball]))
enemy_flamethrower_sample = EnemyUnit(health=60, attack=10, defense=4, color=RED, skills=deepcopy([skill_fire_ball]))
enemy_underboss_sample = EnemyUnit(health=150, attack=20, defense=10, color=PURPLE, speed=1.3, skills=deepcopy([skill_fire_ball, skill_ice_ball]))
