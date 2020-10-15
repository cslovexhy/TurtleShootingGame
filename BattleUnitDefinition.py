from Constants import *
from AIDefinition import *
from SkillDefinition import *


class BattleUnit:
    def __init__(self, start_pos, health, attack, defense, speed=1.0, skills=None):
        if skills is None:
            skills = list()
        self.start_pos = start_pos
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.skills = {skill.key: skill for skill in skills}
        self.effects = dict()

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
    def __init__(self, start_pos=(-200, 0), health=STANDARD_HEALTH, attack=20, defense=3, speed=3.0, skills=None):
        if skills is None:
            skills = [skill_fire_ball]
        assert len(skills) >= 1
        super().__init__(start_pos, health, attack, defense, speed, skills)
        self.left_click_skill_key = skills[0].key
        if len(skills) == 1:
            self.right_click_skill_key = skills[0].key
        else:
            self.right_click_skill_key = skills[1].key


class EnemyUnit(BattleUnit):
    def __init__(self, start_pos, health, attack, defense, player, ai_mode=ENFORCER, speed=.5, skills=None):
        if skills is None:
            skills = get_skill_list_by_mode(ai_mode)
        assert len(skills) >= 1
        super().__init__(start_pos, health, attack, defense, speed, skills)
        self.left_click_skill_key = skills[0].key
        self.ai = AI(ai_mode, self, player)

