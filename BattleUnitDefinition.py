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


class PlayerUnit(BattleUnit):
    def __init__(self, start_pos, health, attack, defense, speed=1.2, skills=None):
        assert len(skills) >= 2
        super().__init__(start_pos, health, attack, defense, speed, skills)
        self.left_click_skill_key = skills[0].key
        self.right_click_skill_key = skills[1].key


class EnemyUnit(BattleUnit):
    def __init__(self, start_pos, health, attack, defense, player, ai_mode=ENFORCER, speed=.5, skills=None):
        if skills is None:
            skills = get_skill_list_by_mode(ai_mode)
        assert len(skills) >= 1
        super().__init__(start_pos, health, attack, defense, speed, skills)
        self.left_click_skill_key = skills[0].key
        self.ai = AI(ai_mode, self, player)

