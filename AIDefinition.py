from Constants import *
from Utils import *
from BattleUnitDefinition import *
from SkillDefinition import *
from copy import deepcopy


class AI:
    def __init__(self, ai_mode, battle_unit, target_unit=None):
        self.ai_mode = ai_mode
        self.battle_unit = battle_unit
        self.target_unit = target_unit

    def set_target_unit(self, target_unit):
        self.target_unit = target_unit

    def decide(self, walls_cor_set):
        if self.ai_mode == ENFORCER:
            t = self.target_unit.ui
            tx, ty = t.xcor(), t.ycor()
            b = self.battle_unit.ui
            bx, by = b.xcor(), b.ycor()

            # set a random skill for enemy
            skill_items = [(key, skill) for key, skill in self.battle_unit.skills.items()]
            skill_count = len(skill_items)
            skill_idx = random.randint(0, skill_count-1)
            key, skill = skill_items[skill_idx]
            b.battle_unit_data.left_click_skill_key = key
            # print("skill key {} selected".format(key))

            def move_to_dest(dest_pos):
                if hasattr(b, "way_point_ttl") and time.time() < b.way_point_ttl:
                    if b.way_points and (bx, by) == b.way_points[-1]:
                        # print("way point popped up")
                        b.way_points.pop()
                        # don't make ai standing there waiting for ttl when it reaches destination before it
                        if not b.way_points:
                            b.way_point_ttl = 0
                else:
                    # print("trying to get way point")
                    b.way_points = get_way_points((bx, by), dest_pos, walls_cor_set)
                    print("way point got: {}".format(str(b.way_points)))
                    if b.way_points:
                        # space out the path finding here for enemies
                        # so calculation can be smoother across frames.
                        b.way_point_ttl = time.time() + rand_f(2, 4)
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

            if b.last_aggro == 0:
                x, y = b.battle_unit_data.start_pos
                return {"decision": AI_DECISION_MOVE, "next_stop": (x, y, 90)}
            elif time.time() - b.last_aggro > 5:
                # if already went back home, treat it as never moved
                if (bx, by) == b.battle_unit_data.start_pos:
                    b.last_aggro = 0
                    return {"decision": AI_DECISION_MOVE, "next_stop": (bx, by, 90)}
                else:
                    dest_pos = b.battle_unit_data.start_pos
                    return move_to_dest(dest_pos)
            elif get_dist((bx, by), (tx, ty)) < skill.attack_range and skill.is_ready():
                return {"decision": AI_DECISION_ATTACK, "skill": skill, "target_cor": (tx, ty)}
            else:
                dest_pos = (tx, ty)
                return move_to_dest(dest_pos)
        else:
            raise Exception("ai_mode {} is not supported yet".format(self.ai_mode))


def get_skill_list_by_mode(ai_mode):
    if ai_mode is ENFORCER:
        return [deepcopy(skill_punch)]
    else:
        raise Exception("ai_mode is not defined")