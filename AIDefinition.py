from Constants import *
from Utils import *
from SkillDefinition import *
from copy import deepcopy


class AI:
    def __init__(self, ai_mode, battle_unit, target_unit):
        self.ai_mode = ai_mode
        self.battle_unit = battle_unit
        self.target_unit = target_unit

    def decide(self, walls_cor_set):
        if self.ai_mode == ENFORCER:
            t = self.target_unit.ui
            tx, ty = t.xcor(), t.ycor()
            b = self.battle_unit.ui
            bx, by = b.xcor(), b.ycor()
            skill = self.battle_unit.skills['3']
            # this is not-so-hardcore version...
            if get_dist((bx, by), (tx, ty)) < skill.attack_range and skill.is_ready():
            # enabling this, enemy will take down brick walls
            # if skill.is_ready():
                return {"decision": AI_DECISION_ATTACK, "skill": skill, "target_cor": (tx, ty)}
            else:
                if hasattr(b, "way_point_ttl") and time.time() < b.way_point_ttl:
                    if b.way_points and (bx, by) == b.way_points[-1]:
                        # print("way point popped up")
                        b.way_points.pop()
                else:
                    # print("trying to get way point")
                    b.way_points = get_way_points((bx, by), (tx, ty), walls_cor_set)
                    # print("way point got: {}".format(str(b.way_points)))
                    if b.way_points:
                        b.way_point_ttl = time.time() + 2.0
                    else:
                        b.way_point_ttl = time.time() + 0.5
                b.orig_pos = (bx, by)
                if not b.way_points:
                    # print("no way point, b.target_pos = {}".format(str(b.target_pos)))
                    pass
                else:
                    # print("has way point, next one = {}".format(str(b.way_points[-1])))
                    b.target_pos = deepcopy(b.way_points[-1])
                max_step = min(BATTLE_UNIT_BASE_SPEED * self.battle_unit.get_speed(), get_dist(b.orig_pos, b.target_pos))
                next_stop = get_new_cors(b, max_step)
                # print("next stop = {}".format(str(next_stop)))

                return {"decision": AI_DECISION_MOVE, "next_stop": next_stop}
        else:
            raise Exception("ai_mode {} is not supported yet".format(self.ai_mode))


def get_skill_list_by_mode(ai_mode):
    if ai_mode is ENFORCER:
        return [deepcopy(skill_punch)]
    else:
        raise Exception("ai_mode is not defined")