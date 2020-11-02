from Constants import *
from ColorDefinition import *
from SkillDefinition import *
from Utils import *


class ItemUnit:
    def __init__(self, name, shape, color, scale):
        self.name = name
        self.shape = shape
        self.color = color
        self.scale = scale


class SkillItemUnit(ItemUnit):
    def __init__(self, skill_data, scale=1.5):
        s = skill_data
        super().__init__(s.name, s.shape, s.color, scale)
        self.skill_data = deepcopy(skill_data)


skill_fire_ball_item_sample = SkillItemUnit(skill_fire_ball)

skill_ice_ball_item_sample = SkillItemUnit(skill_ice_ball)

skill_icy_blast_item_sample = SkillItemUnit(skill_icy_blast)

skill_nova_item_sample = SkillItemUnit(skill_nova)


def handle_item_pick_up(player_data, item_data, bind_skill_callback):
    if isinstance(item_data, SkillItemUnit):
        skill_data = item_data.skill_data
        print("skill_data.key = " + str(skill_data.key))
        print("player_data.skills = " + str(player_data.skills))
        if skill_data.name not in {s.name for _, s in player_data.skills.items()}:
            new_skill_key = str(len(player_data.skills)+1)
            player_data.skills[new_skill_key] = skill_data
            print("Acquired skill: {}, key = {}".format(str(skill_data.name), str(skill_data.key)))
            bind_skill_callback()