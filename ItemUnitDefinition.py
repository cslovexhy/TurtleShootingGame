from Constants import *
from ColorDefinition import *
from SkillDefinition import *
from BattleUnitDefinition import *
from ShapeDefinition import *
from Utils import *

CONSUMABLE_MINOR_HEALTH_POTION = "Minor Health Potion"


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


class ConsumableItemUnit(ItemUnit):
    def __init__(self, name, attribute, value, shape, scale=1.0):
        super().__init__(name, shape, BLACK, scale)
        # TODO: crappy assert here, need to do a set instead
        assert(hasattr(player_sample, attribute))
        self.attribute = attribute
        self.value = value


def handle_item_pick_up(player_data, item_data, bind_skill_callback):
    if isinstance(item_data, SkillItemUnit):
        skill_data = item_data.skill_data
        if skill_data.name not in {s.name for _, s in player_data.skills.items()}:
            new_skill_key = str(len(player_data.skills)+1)
            player_data.skills[new_skill_key] = skill_data
            print("Acquired skill: {}".format(str(skill_data.name)))
            print("player_data.skills = " + str(player_data.skills))
            bind_skill_callback()
        else:
            print("Already had this skill, skip")
    elif isinstance(item_data, ConsumableItemUnit):
        attr_key = item_data.attribute
        value = item_data.value
        old_val = getattr(player_data, attr_key)
        new_val = old_val + value
        if attr_key == "health":
            new_val = min(player_data.max_health, new_val)
        setattr(player_data, attr_key, new_val)
        print("player {} increased by {}".format(attr_key, str(new_val - old_val)))


skill_fire_ball_item_sample = SkillItemUnit(skill_fire_ball)

skill_ice_ball_item_sample = SkillItemUnit(skill_ice_ball)

skill_icy_blast_item_sample = SkillItemUnit(skill_icy_blast)

skill_nova_item_sample = SkillItemUnit(skill_nova)

consumable_item_minor_health_potion_sample = ConsumableItemUnit(CONSUMABLE_MINOR_HEALTH_POTION, "health", 20, SHAPE_HEALTH_POTION)