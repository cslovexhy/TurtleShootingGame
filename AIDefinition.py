from Constants import *
from Utils import *
from SkillDefinition import *
from copy import deepcopy


class AI:
    def __init__(self, ai_mode, battle_unit, target_unit):
        self.ai_mode = ai_mode
        self.battle_unit = battle_unit
        self.target_unit = target_unit

    def decide(self):
        if self.ai_mode == ENFORCER:
            t = self.target_unit.ui
            tx, ty = t.xcor(), t.ycor()
            b = self.battle_unit.ui
            bx, by = b.xcor(), b.ycor()
            dist = get_dist((tx, ty), (bx, by))
            max_step = BATTLE_UNIT_BASE_SPEED * self.battle_unit.get_speed()
            skill = self.battle_unit.skills['3']
            # print("e_id = {}, dist = {}, range = {}".format(str(b.id), str(dist), str(skill.attack_range)))
            if dist < skill.attack_range and skill.is_ready():
                return {"decision": AI_DECISION_ATTACK, "skill": skill, "target_cor": (tx, ty)}
            else:
                b.orig_pos = (bx, by)
                b.target_pos = (tx, ty)
                return {"decision": AI_DECISION_MOVE, "next_stop": get_new_cors(b, max_step)}
        else:
            raise Exception("ai_mode {} is not supported yet".format(self.ai_mode))


def get_skill_list_by_mode(ai_mode):
    if ai_mode is ENFORCER:
        return [deepcopy(skill_punch)]
    else:
        raise Exception("ai_mode is not defined")